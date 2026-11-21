"""Idempotent store configuration (specs/001-book-catalog, data-model.md "Store configuration").

Run: bench --site <site> execute frappe_shop.setup.store.setup_store

Uses only standard ERPNext / Webshop settings and records. Running it again changes nothing that is
already correct, and it never deletes anything.
"""

import erpnext
import frappe
from frappe import _

from frappe_shop.catalog.books import BOOK_ITEM_GROUP
from frappe_shop.catalog.website import COD_GATEWAY

STORE_DISPLAY_NAME = "Frappe Books"
DEFAULT_BRAND_VALUES = (None, "", "Frappe")
COD_TERM = "Cash on Delivery"
CASH_MODE_OF_PAYMENT = "Cash"
AUTHOR_FILTER_FIELD = "book_author"
FALLBACK_CUSTOMER_GROUP = "Individual"
FALLBACK_PRICE_LIST = "Standard Selling"
CUSTOMER_ROLE = "Customer"


def setup_store(company: str | None = None) -> dict:
	company = resolve_company(company)
	return {
		"company": company,
		"item_group": ensure_item_group(),
		"payment_terms_template": ensure_cod_payment_terms(),
		"payment_gateway_account": ensure_cod_gateway_account(company),
		"customer_group": configure_webshop(company),
		"brand": ensure_store_display_name(),
		"signup_role": ensure_signup_role(),
	}


def resolve_company(company: str | None = None) -> str:
	company = (
		company
		or frappe.db.get_single_value("Webshop Settings", "company")
		or erpnext.get_default_company()
		or frappe.db.get_value("Company", {}, "name")
	)
	if not company:
		frappe.throw(_("No Company found. Complete the ERPNext setup wizard first."))
	return company


def ensure_item_group() -> str:
	if not frappe.db.exists("Item Group", BOOK_ITEM_GROUP):
		frappe.get_doc(
			{
				"doctype": "Item Group",
				"item_group_name": BOOK_ITEM_GROUP,
				"parent_item_group": frappe.db.get_value(
					"Item Group", {"is_group": 1, "parent_item_group": ""}
				)
				or "All Item Groups",
			}
		).insert(ignore_permissions=True)
	return BOOK_ITEM_GROUP


def ensure_cod_payment_terms() -> str:
	if not frappe.db.exists("Payment Term", COD_TERM):
		frappe.get_doc(
			{
				"doctype": "Payment Term",
				"payment_term_name": COD_TERM,
				"invoice_portion": 100,
				"mode_of_payment": CASH_MODE_OF_PAYMENT
				if frappe.db.exists("Mode of Payment", CASH_MODE_OF_PAYMENT)
				else None,
				"due_date_based_on": "Day(s) after invoice date",
				"credit_days": 0,
				"description": "Pay in cash when the order is delivered.",
			}
		).insert(ignore_permissions=True)

	if not frappe.db.exists("Payment Terms Template", COD_TERM):
		frappe.get_doc(
			{
				"doctype": "Payment Terms Template",
				"template_name": COD_TERM,
				"terms": [
					{
						"payment_term": COD_TERM,
						"invoice_portion": 100,
						"due_date_based_on": "Day(s) after invoice date",
						"credit_days": 0,
					}
				],
			}
		).insert(ignore_permissions=True)
	return COD_TERM


def ensure_cod_gateway_account(company: str) -> str:
	"""A placeholder gateway (no controller, cannot take online payments) so Webshop allows Place Order."""
	if not frappe.db.exists("Payment Gateway", COD_GATEWAY):
		frappe.get_doc({"doctype": "Payment Gateway", "gateway": COD_GATEWAY}).insert(ignore_permissions=True)

	existing = frappe.db.get_value(
		"Payment Gateway Account", {"payment_gateway": COD_GATEWAY, "company": company}
	)
	if existing:
		return existing

	cash_account = frappe.get_cached_value("Company", company, "default_cash_account")
	if not cash_account:
		frappe.throw(_("Company {0} has no Default Cash Account").format(company))

	doc = frappe.get_doc(
		{
			"doctype": "Payment Gateway Account",
			"payment_gateway": COD_GATEWAY,
			"company": company,
			"payment_account": cash_account,
			"currency": frappe.get_cached_value("Account", cash_account, "account_currency"),
		}
	).insert(ignore_permissions=True)
	return doc.name


def configure_webshop(company: str) -> str:
	settings = frappe.get_single("Webshop Settings")

	settings.enabled = 1
	settings.company = settings.company or company
	settings.price_list = (
		settings.price_list
		or frappe.db.get_single_value("Selling Settings", "selling_price_list")
		or FALLBACK_PRICE_LIST
	)
	settings.default_customer_group = (
		settings.default_customer_group
		or frappe.db.get_single_value("Selling Settings", "customer_group")
		or get_fallback_customer_group()
	)
	if not settings.quotation_series:
		settings.quotation_series = frappe.get_meta("Quotation").get_options("naming_series").split("\n")[0]
	settings.show_price = 1
	settings.show_stock_availability = 1

	# author filter (FR-007), standard Webshop field filter on Website Item.book_author
	settings.enable_field_filters = 1
	if AUTHOR_FILTER_FIELD not in [row.fieldname for row in settings.filter_fields]:
		settings.append("filter_fields", {"fieldname": AUTHOR_FILTER_FIELD})

	# direct order with Cash on Delivery (FR-010, FR-011)
	settings.enable_checkout = 1
	settings.payment_gateway_account = ensure_cod_gateway_account(settings.company)

	settings.flags.ignore_permissions = True
	settings.save()

	frappe.db.set_value("Customer Group", settings.default_customer_group, "payment_terms", COD_TERM)
	return settings.default_customer_group


def get_fallback_customer_group() -> str:
	if frappe.db.exists("Customer Group", FALLBACK_CUSTOMER_GROUP):
		return FALLBACK_CUSTOMER_GROUP
	return frappe.db.get_value("Customer Group", {"is_group": 0}, "name")


def ensure_store_display_name() -> str:
	"""FR-012: default to "Frappe Books" but never overwrite a name the owner has set."""
	settings = frappe.get_single("Website Settings")
	changed = False
	if settings.brand_html in DEFAULT_BRAND_VALUES:
		settings.brand_html = STORE_DISPLAY_NAME
		changed = True
	if settings.app_name in DEFAULT_BRAND_VALUES:
		settings.app_name = STORE_DISPLAY_NAME
		changed = True
	if changed:
		settings.flags.ignore_permissions = True
		settings.save()
	return settings.brand_html


def ensure_signup_role() -> str:
	"""Website users who sign up get the Customer role (fix: checkout and order page for new customers).

	Without a Portal Settings default role, new website users have no Customer role: ERPNext does not
	create a Customer for them at login, and the order confirmation page answers 403 after Place Order.
	A default role chosen by the owner is never overwritten.
	"""
	settings = frappe.get_single("Portal Settings")
	if not settings.default_role:
		settings.default_role = CUSTOMER_ROLE
		settings.flags.ignore_permissions = True
		settings.save()
	return settings.default_role
