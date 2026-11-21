import frappe

from frappe_shop.catalog.books import BOOK_ITEM_GROUP
from frappe_shop.setup.store import ensure_item_group

TEST_AUTHOR = "_Test Book Author"
TEST_UOM = "Nos"


def ensure_book_prerequisites() -> None:
	ensure_item_group()
	if not frappe.db.exists("Book Author", TEST_AUTHOR):
		frappe.get_doc({"doctype": "Book Author", "author_name": TEST_AUTHOR}).insert(ignore_permissions=True)
	if not frappe.db.exists("UOM", TEST_UOM):
		frappe.get_doc({"doctype": "UOM", "uom_name": TEST_UOM}).insert(ignore_permissions=True)


def make_book(insert: bool = True, **overrides):
	"""Build (and by default insert) a book Item with all five details filled."""
	code = overrides.pop("item_code", None) or f"_TEST-BOOK-{frappe.generate_hash(length=8)}"
	doc = frappe.get_doc(
		{
			"doctype": "Item",
			"item_code": code,
			"item_name": code,
			"item_group": BOOK_ITEM_GROUP,
			"stock_uom": TEST_UOM,
			"is_stock_item": 0,
			"book_author": TEST_AUTHOR,
			"book_isbn": f"_TEST-ISBN-{frappe.generate_hash(length=10)}",
			"book_publisher": "_Test Publisher",
			"book_pages": 100,
			"book_language": "English",
			**overrides,
		}
	)
	if insert:
		doc.insert(ignore_permissions=True)
	return doc
