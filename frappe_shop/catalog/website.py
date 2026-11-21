"""Website context hooks (specs/001-book-catalog, FR-011)."""

import frappe

COD_GATEWAY = "Cash on Delivery"
ORDER_DOCTYPES = ("Sales Order", "Sales Invoice")


def is_cash_on_delivery_store() -> bool:
	gateway_account = frappe.db.get_single_value("Webshop Settings", "payment_gateway_account")
	if not gateway_account:
		return False
	return frappe.db.get_value("Payment Gateway Account", gateway_account, "payment_gateway") == COD_GATEWAY


def hide_online_payment(context):
	"""update_website_context: hide the online "Pay" button on order pages when the store is COD-only.

	Frappe calls this hook after the page's own get_context, so it can override `enabled_checkout`
	that webshop's order page sets.
	"""
	doc = context.get("doc")
	if not doc or getattr(doc, "doctype", None) not in ORDER_DOCTYPES:
		return None
	if not context.get("enabled_checkout"):
		return None
	if is_cash_on_delivery_store():
		return {"enabled_checkout": False}
	return None


def add_storefront_navigation(context):
	"""update_website_context: the empty orders message (FR-006).

	No Admin link: the avatar dropdown already offers "Switch to Desk" to System Users.
	"""
	values = {}
	if context.get("doctype") == "Sales Order" and not context.get("no_result_message"):
		from frappe_shop.setup.store import ORDERS_EMPTY_MESSAGE

		values["no_result_message"] = frappe._(ORDERS_EMPTY_MESSAGE)
	return values or None
