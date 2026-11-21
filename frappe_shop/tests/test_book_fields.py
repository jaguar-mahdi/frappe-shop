"""User Story 1: book details (spec FR-001 to FR-006)."""

import frappe
from frappe.tests import IntegrationTestCase

from frappe_shop.catalog.books import BOOK_FIELDS
from frappe_shop.tests.utils import TEST_AUTHOR, TEST_UOM, ensure_book_prerequisites, make_book


class TestBookFields(IntegrationTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		ensure_book_prerequisites()

	def test_custom_fields_exist(self):
		"""FR-001: the five details exist on Item with the planned types."""
		expected = {
			"book_author": ("Link", "Book Author"),
			"book_isbn": ("Data", None),
			"book_publisher": ("Data", None),
			"book_pages": ("Int", None),
			"book_language": ("Data", None),
		}
		meta = frappe.get_meta("Item")
		for fieldname, (fieldtype, options) in expected.items():
			df = meta.get_field(fieldname)
			self.assertIsNotNone(df, fieldname)
			self.assertEqual(df.fieldtype, fieldtype, fieldname)
			if options:
				self.assertEqual(df.options, options, fieldname)
		self.assertTrue(meta.get_field("book_isbn").unique)

		web_df = frappe.get_meta("Website Item").get_field("book_author")
		self.assertEqual((web_df.fieldtype, web_df.options), ("Link", "Book Author"))

	def test_valid_book_is_saved(self):
		book = make_book()
		self.assertTrue(frappe.db.exists("Item", book.name))

	def test_each_detail_is_required_for_books(self):
		"""FR-003: a book cannot be saved (so cannot be published) with a missing detail."""
		for fieldname, label in BOOK_FIELDS:
			with self.subTest(fieldname=fieldname):
				book = make_book(insert=False, **{fieldname: None})
				with self.assertRaises(frappe.MandatoryError) as ctx:
					book.insert(ignore_permissions=True)
				self.assertIn(label, str(ctx.exception))

	def test_non_book_items_need_no_book_details(self):
		item = frappe.get_doc(
			{
				"doctype": "Item",
				"item_code": f"_TEST-NONBOOK-{frappe.generate_hash(length=8)}",
				"item_group": frappe.db.get_value("Item Group", {"is_group": 0, "name": ["!=", "Books"]}),
				"stock_uom": TEST_UOM,
				"is_stock_item": 0,
			}
		).insert(ignore_permissions=True)
		self.assertTrue(frappe.db.exists("Item", item.name))

	def test_isbn_must_be_unique(self):
		"""FR-004: a second book with the same ISBN is rejected."""
		first = make_book()
		with self.assertRaises(frappe.UniqueValidationError):
			make_book(book_isbn=first.book_isbn)

	def test_isbn_format_is_not_checked(self):
		"""FR-004: any text is accepted as ISBN."""
		book = make_book(book_isbn=f"not-an-isbn {frappe.generate_hash(length=6)}")
		self.assertTrue(frappe.db.exists("Item", book.name))

	def test_pages_must_be_positive(self):
		"""FR-005: number of pages must be a positive whole number."""
		for pages in (0, -5):
			with self.subTest(pages=pages):
				with self.assertRaises(frappe.ValidationError):
					make_book(book_pages=pages)

	def test_website_item_shows_book_details(self):
		"""FR-006: the product page specifications carry the five details and follow Item edits."""
		from webshop.webshop.doctype.website_item.website_item import make_website_item

		book = make_book()
		name, _ = make_website_item(book.as_dict(), save=True)
		web_item = frappe.get_doc("Website Item", name)

		self.assertEqual(web_item.book_author, TEST_AUTHOR)
		specs = {row.label: row.description for row in web_item.website_specifications}
		self.assertEqual(
			specs,
			{
				"Author": TEST_AUTHOR,
				"ISBN": book.book_isbn,
				"Publisher": "_Test Publisher",
				"Number of Pages": "100",
				"Language": "English",
			},
		)

		book.reload()
		book.book_publisher = "_Test Publisher Two"
		book.save(ignore_permissions=True)
		web_item.reload()
		specs = {row.label: row.description for row in web_item.website_specifications}
		self.assertEqual(specs["Publisher"], "_Test Publisher Two")
