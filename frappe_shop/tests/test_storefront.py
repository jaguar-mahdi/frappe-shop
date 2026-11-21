"""Storefront polish (specs/002-storefront-polish)."""

import frappe
from frappe.tests import IntegrationTestCase

from frappe_shop.catalog.covers import COVER_PALETTE, author_colour, make_cover_svg
from frappe_shop.catalog.website import add_storefront_navigation
from frappe_shop.demo.sample_books import (
	SAMPLE_AUTHORS,
	SAMPLE_UOM,
	create_sample_books,
	ensure_cover,
	get_sample_books,
)
from frappe_shop.setup.store import (
	HOME_PAGE,
	NAVBAR_ITEMS,
	ORDERS_EMPTY_MESSAGE,
	STOREFRONT_TEXTS,
	THEME_FONT,
	THEME_NAME,
	THEME_PRIMARY_COLOUR,
	ensure_price_format,
	setup_store,
)
from frappe_shop.templates.pages.order import show_order_confirmation
from frappe_shop.www.home import LATEST_BOOKS, get_latest_books


class TestStorefrontSetup(IntegrationTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		setup_store()

	def test_theme_colour_and_font(self):
		"""FR-005."""
		theme = frappe.get_doc("Website Theme", THEME_NAME)
		self.assertEqual((theme.google_font, theme.primary_color), (THEME_FONT, THEME_PRIMARY_COLOUR))
		self.assertIn("--btn-primary", theme.custom_scss)  # v16 buttons use this variable
		self.assertEqual(frappe.db.get_single_value("Website Settings", "website_theme"), THEME_NAME)

	def test_theme_chosen_by_owner_is_kept(self):
		"""FR-007."""
		self.addCleanup(frappe.db.set_single_value, "Website Settings", "website_theme", THEME_NAME)
		if not frappe.db.exists("Website Theme", "_Test Owner Theme"):
			frappe.get_doc({"doctype": "Website Theme", "theme": "_Test Owner Theme", "custom": 1}).insert()
		frappe.db.set_single_value("Website Settings", "website_theme", "_Test Owner Theme")
		setup_store()
		self.assertEqual(frappe.db.get_single_value("Website Settings", "website_theme"), "_Test Owner Theme")

	def test_navbar_footer_home_page_without_duplicates(self):
		"""FR-001 to FR-003, idempotent."""
		setup_store()
		settings = frappe.get_single("Website Settings")
		urls = [row.url for row in settings.top_bar_items]
		for label, url in NAVBAR_ITEMS:
			self.assertEqual(urls.count(url), 1, url)
			self.assertIn(label, [row.label for row in settings.top_bar_items])
		self.assertEqual(settings.home_page, HOME_PAGE)
		self.assertTrue(settings.copyright)

	def test_empty_state_texts(self):
		"""FR-006: webshop texts reworded through English translations."""
		frappe.clear_cache()
		for source, text in STOREFRONT_TEXTS.items():
			self.assertEqual(frappe._(source, lang="en"), text)


class TestStorefrontPages(IntegrationTestCase):
	def test_no_admin_or_cart_text_link_in_navbar(self):
		"""Fix: no Admin link (Desk is in the avatar menu) and no "Cart" text link (cart icon stays)."""
		context = frappe._dict(top_bar_items=[frappe._dict(label="Books", url="/all-products")])
		self.assertIsNone(add_storefront_navigation(context))

		setup_store()
		items = [(row.label, row.url) for row in frappe.get_single("Website Settings").top_bar_items]
		self.assertNotIn(("Cart", "/cart"), items)
		self.assertNotIn("/app", [url for _label, url in items])

	def test_orders_empty_message(self):
		values = add_storefront_navigation(frappe._dict(doctype="Sales Order"))
		self.assertEqual(values["no_result_message"], frappe._(ORDERS_EMPTY_MESSAGE))

	def test_order_confirmation_only_for_placed_cart_orders(self):
		"""US5: confirmation for a submitted cart order, not for drafts, cancelled, or other orders."""
		placed = frappe._dict(
			doctype="Sales Order", order_type="Shopping Cart", docstatus=1, status="To Deliver and Bill"
		)
		self.assertTrue(show_order_confirmation(placed))
		self.assertFalse(show_order_confirmation(frappe._dict(placed, docstatus=0)))
		self.assertFalse(show_order_confirmation(frappe._dict(placed, status="Cancelled")))
		self.assertFalse(show_order_confirmation(frappe._dict(placed, order_type="Sales")))
		self.assertFalse(show_order_confirmation(None))


class TestPriceFormat(IntegrationTestCase):
	def test_iqd_prices_have_no_decimals(self):
		"""Fix: 15,000 not 15,000.000 when the store sells in IQD."""
		from frappe.utils import fmt_money

		price_list = frappe.db.get_single_value("Webshop Settings", "price_list")
		original = frappe.db.get_value("Price List", price_list, "currency")
		self.addCleanup(frappe.db.set_value, "Price List", price_list, "currency", original)
		frappe.db.set_value("Price List", price_list, "currency", "IQD")
		if frappe.db.get_default("currency_precision") not in (None, "", "0"):
			self.skipTest("the owner has chosen a currency precision")

		self.assertEqual(ensure_price_format(), "0")
		formatted = fmt_money(15000, currency="IQD")
		self.assertIn("15,000", formatted)
		self.assertNotIn("15,000.", formatted)


class TestCovers(IntegrationTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		create_sample_books()

	def test_author_colour_is_stable_and_from_palette(self):
		self.assertIn(author_colour("Jane Austen"), COVER_PALETTE)
		self.assertEqual(author_colour("Jane Austen"), author_colour(" jane austen "))

	def test_sample_authors_get_distinct_colours(self):
		"""Each sample author is recognisable by colour (7 authors, 7 palette colours)."""
		colours = [author_colour(author, SAMPLE_AUTHORS) for author in SAMPLE_AUTHORS]
		self.assertEqual(len(set(colours)), len(SAMPLE_AUTHORS))

	def test_cover_svg_has_title_author_and_escapes_text(self):
		svg = make_cover_svg("Cats & <Dogs>", "A. Writer")
		self.assertTrue(svg.startswith("<svg"))
		self.assertIn("Cats &amp; &lt;Dogs&gt;", svg)
		self.assertIn("A. Writer", svg)
		self.assertIn(author_colour("A. Writer"), svg)
		self.assertNotIn("<Dogs>", svg)

	def test_every_sample_book_has_a_cover_and_no_duplicates(self):
		"""FR-004, SC-001."""
		codes = [book["item_code"] for book in get_sample_books()]
		files = {"attached_to_doctype": "Item", "attached_to_name": ["in", codes]}
		before = frappe.db.count("File", files)

		create_sample_books()
		for book in get_sample_books():
			ensure_cover(book["item_code"], book["item_name"], book["book_author"])

		self.assertEqual(frappe.db.count("File", files), before)
		for code in codes:
			image = frappe.db.get_value("Item", code, "image")
			self.assertTrue(image and image.endswith(".svg"), code)
			self.assertEqual(frappe.db.get_value("Website Item", {"item_code": code}, "website_image"), image)

	def test_sample_books_use_the_book_unit(self):
		"""Fix: the book page shows "/ Book"; existing books are moved to the unit too."""
		for book in get_sample_books():
			code = book["item_code"]
			if frappe.db.get_value("Item", code, "stock_uom") == SAMPLE_UOM:
				continue
			# a book may stay on its old unit only when real orders or stock movements exist for it
			reserved = frappe.db.exists("Bin", {"item_code": code, "reserved_qty": [">", 0]})
			other = frappe.db.exists(
				"Stock Ledger Entry",
				{"item_code": code, "is_cancelled": 0, "voucher_type": ["!=", "Stock Entry"]},
			)
			self.assertTrue(reserved or other, f"{code} should have moved to {SAMPLE_UOM}")
		self.assertTrue(frappe.db.get_value("UOM", SAMPLE_UOM, "must_be_whole_number"))

	def test_home_page_latest_books(self):
		"""FR-001."""
		books = get_latest_books()
		self.assertEqual(len(books), LATEST_BOOKS)
		self.assertTrue(all(book.website_image and book.route for book in books))
