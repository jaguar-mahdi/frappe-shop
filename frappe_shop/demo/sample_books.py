"""Demo catalog: 10 public-domain classics (specs/001-book-catalog, User Story 4, research R10).

Run: bench --site <site> execute frappe_shop.demo.sample_books.create_sample_books

Idempotent: every record is looked up by a natural key before it is created, and opening stock is
added only for items that have no stock ledger entries yet. Values approved by the maintainer on
2026-11-21. ISBNs and the publisher are clearly demo values, not real editions.
"""

import frappe
from frappe import _

from frappe_shop.catalog.books import BOOK_ITEM_GROUP
from frappe_shop.setup.store import resolve_company, setup_store

SAMPLE_PRICE = 15000
SAMPLE_STOCK_QTY = 20
SAMPLE_PUBLISHER = "Frappe Books Demo Press"
SAMPLE_LANGUAGE = "English"
SAMPLE_UOM = "Nos"

# (title, author, approximate number of pages)
SAMPLE_BOOKS = (
	("Pride and Prejudice", "Jane Austen", 432),
	("Emma", "Jane Austen", 474),
	("Great Expectations", "Charles Dickens", 505),
	("A Tale of Two Cities", "Charles Dickens", 448),
	("The Time Machine", "H. G. Wells", 118),
	("The War of the Worlds", "H. G. Wells", 192),
	("Moby-Dick", "Herman Melville", 635),
	("Frankenstein", "Mary Shelley", 280),
	("Dracula", "Bram Stoker", 418),
	("The Adventures of Sherlock Holmes", "Arthur Conan Doyle", 307),
)


def get_sample_books() -> list[dict]:
	return [
		{
			"item_code": f"BOOK-DEMO-{n:04d}",
			"item_name": title,
			"book_author": author,
			"book_isbn": f"DEMO-{n:04d}",
			"book_publisher": SAMPLE_PUBLISHER,
			"book_pages": pages,
			"book_language": SAMPLE_LANGUAGE,
		}
		for n, (title, author, pages) in enumerate(SAMPLE_BOOKS, start=1)
	]


def create_sample_books(company: str | None = None) -> dict:
	company = resolve_company(company)
	setup_store(company)

	settings = frappe.get_single("Webshop Settings")
	warehouse = get_store_warehouse(settings.company)
	result = {"created": [], "existing": []}

	for book in get_sample_books():
		ensure_author(book["book_author"])
		created = ensure_item(book)
		ensure_price(book["item_code"], settings.price_list)
		ensure_website_item(book["item_code"], warehouse)
		ensure_opening_stock(book["item_code"], settings.company, warehouse)
		result["created" if created else "existing"].append(book["item_code"])

	return result


def get_store_warehouse(company: str) -> str:
	abbr = frappe.get_cached_value("Company", company, "abbr")
	warehouse = frappe.db.exists("Warehouse", f"Stores - {abbr}") or frappe.db.get_value(
		"Warehouse", {"company": company, "is_group": 0}, "name"
	)
	if not warehouse:
		frappe.throw(_("Company {0} has no warehouse").format(company))
	return warehouse


def ensure_author(author_name: str) -> None:
	if not frappe.db.exists("Book Author", author_name):
		frappe.get_doc({"doctype": "Book Author", "author_name": author_name}).insert(ignore_permissions=True)


def ensure_item(book: dict) -> bool:
	"""Return True if the Item was created now."""
	if frappe.db.exists("Item", book["item_code"]) or frappe.db.exists(
		"Item", {"book_isbn": book["book_isbn"]}
	):
		return False
	if not frappe.db.exists("UOM", SAMPLE_UOM):
		frappe.get_doc({"doctype": "UOM", "uom_name": SAMPLE_UOM, "must_be_whole_number": 1}).insert(
			ignore_permissions=True
		)
	frappe.get_doc(
		{
			"doctype": "Item",
			**book,
			"item_group": BOOK_ITEM_GROUP,
			"stock_uom": SAMPLE_UOM,
			"is_stock_item": 1,
			"include_item_in_manufacturing": 0,
			"description": f"{book['item_name']} by {book['book_author']} (demo book).",
		}
	).insert(ignore_permissions=True)
	return True


def ensure_price(item_code: str, price_list: str) -> None:
	if frappe.db.exists("Item Price", {"item_code": item_code, "price_list": price_list}):
		return
	frappe.get_doc(
		{
			"doctype": "Item Price",
			"item_code": item_code,
			"price_list": price_list,
			"price_list_rate": SAMPLE_PRICE,
		}
	).insert(ignore_permissions=True)


def ensure_website_item(item_code: str, warehouse: str) -> None:
	if frappe.db.exists("Website Item", {"item_code": item_code}):
		return
	from webshop.webshop.doctype.website_item.website_item import make_website_item

	name, _web_item_name = make_website_item(frappe.get_doc("Item", item_code).as_dict(), save=True)
	web_item = frappe.get_doc("Website Item", name)
	web_item.published = 1
	web_item.website_warehouse = warehouse
	web_item.flags.ignore_permissions = True
	web_item.save()


def ensure_opening_stock(item_code: str, company: str, warehouse: str) -> None:
	if frappe.db.exists("Stock Ledger Entry", {"item_code": item_code, "is_cancelled": 0}):
		return
	entry = frappe.get_doc(
		{
			"doctype": "Stock Entry",
			"stock_entry_type": "Material Receipt",
			"company": company,
			"items": [
				{
					"item_code": item_code,
					"qty": SAMPLE_STOCK_QTY,
					"t_warehouse": warehouse,
					"uom": SAMPLE_UOM,
					"conversion_factor": 1,
					"allow_zero_valuation_rate": 1,
				}
			],
		}
	)
	entry.flags.ignore_permissions = True
	entry.insert()
	entry.submit()
