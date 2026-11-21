"""User Stories 2, 3, 5: author filter and search, Cash on Delivery, store display name."""

import frappe
from frappe.tests import IntegrationTestCase

from frappe_shop.catalog.website import COD_GATEWAY, hide_online_payment
from frappe_shop.setup.store import COD_TERM, STORE_DISPLAY_NAME, setup_store


class TestStoreSetup(IntegrationTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		cls.result = setup_store()

	def test_setup_is_idempotent(self):
		self.assertEqual(setup_store(), self.result)
		self.assertEqual(frappe.db.count("Payment Gateway", {"name": COD_GATEWAY}), 1)
		self.assertEqual(
			frappe.db.count(
				"Payment Gateway Account", {"payment_gateway": COD_GATEWAY, "company": self.result["company"]}
			),
			1,
		)
		settings = frappe.get_single("Webshop Settings")
		self.assertEqual([row.fieldname for row in settings.filter_fields].count("book_author"), 1)

	def test_author_filter_is_configured(self):
		"""FR-007: Webshop's standard field filter on Website Item.book_author."""
		settings = frappe.get_single("Webshop Settings")
		self.assertTrue(settings.enabled)
		self.assertTrue(settings.enable_field_filters)
		self.assertIn("book_author", [row.fieldname for row in settings.filter_fields])

	def test_author_is_searchable(self):
		"""FR-008: product listing search includes the author."""
		self.assertIn("book_author", frappe.get_meta("Website Item").get_search_fields())

	def test_cash_on_delivery_only(self):
		"""FR-010, FR-011: checkout creates orders with COD terms and a placeholder gateway."""
		settings = frappe.get_single("Webshop Settings")
		self.assertTrue(settings.enable_checkout)
		self.assertEqual(
			frappe.db.get_value(
				"Payment Gateway Account", settings.payment_gateway_account, "payment_gateway"
			),
			COD_GATEWAY,
		)
		gateway = frappe.get_doc("Payment Gateway", COD_GATEWAY)
		self.assertFalse(gateway.gateway_controller, "placeholder gateway must not process payments")

		self.assertEqual(
			frappe.db.get_value("Customer Group", settings.default_customer_group, "payment_terms"), COD_TERM
		)
		terms = frappe.get_doc("Payment Terms Template", COD_TERM).terms
		self.assertEqual(len(terms), 1)
		self.assertEqual(terms[0].invoice_portion, 100)

	def test_pay_button_hidden_on_order_pages(self):
		"""FR-011: the order page context hides the online Pay button."""
		order = frappe._dict(doctype="Sales Order", name="SO-TEST")
		self.assertEqual(
			hide_online_payment(frappe._dict(doc=order, enabled_checkout=1)), {"enabled_checkout": False}
		)
		self.assertIsNone(hide_online_payment(frappe._dict(doc=frappe._dict(doctype="Item"))))
		self.assertIsNone(hide_online_payment(frappe._dict()))

	def test_display_name_default_and_kept_when_changed(self):
		"""FR-012: defaults to "Frappe Books", and a name set by the owner is not overwritten."""
		settings = frappe.get_single("Website Settings")
		if settings.brand_html in (None, "", "Frappe", STORE_DISPLAY_NAME):
			self.assertEqual(settings.brand_html, STORE_DISPLAY_NAME)

		original = settings.brand_html
		self.addCleanup(frappe.db.set_single_value, "Website Settings", "brand_html", original)
		frappe.db.set_single_value("Website Settings", "brand_html", "_Test Store Name")
		setup_store()
		self.assertEqual(frappe.db.get_single_value("Website Settings", "brand_html"), "_Test Store Name")
