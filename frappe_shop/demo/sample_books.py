"""Demo catalog: 10 public-domain classics (specs/001-book-catalog, User Story 4, research R10).

Run: bench --site <site> execute frappe_shop.demo.sample_books.create_sample_books

Idempotent: every record is looked up by a natural key before it is created, and opening stock is
added only for items that have no stock ledger entries yet. Values approved by the maintainer on
2026-11-21. ISBNs and the publisher are clearly demo values, not real editions.
"""

import frappe
from frappe import _

from frappe_shop.catalog.books import BOOK_ITEM_GROUP
from frappe_shop.catalog.covers import make_cover_svg
from frappe_shop.setup.store import resolve_company, setup_store

SAMPLE_PRICE = 15000
SAMPLE_STOCK_QTY = 20
SAMPLE_PUBLISHER = "Frappe Books Demo Press"
SAMPLE_LANGUAGE = "English"
SAMPLE_UOM = "Book"

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
SAMPLE_AUTHORS = tuple(dict.fromkeys(author for _title, author, _pages in SAMPLE_BOOKS))


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
		ensure_sample_uom(book["item_code"])
		ensure_opening_stock(book["item_code"], settings.company, warehouse)
		ensure_cover(book["item_code"], book["item_name"], book["book_author"])
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
	ensure_uom()
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


def ensure_cover(item_code: str, title: str, author: str) -> str:
	"""Attach a generated SVG cover (specs/002-storefront-polish, FR-004) unless the book has an image."""
	image = frappe.db.get_value("Item", item_code, "image")
	if not image:
		file_doc = frappe.get_doc(
			{
				"doctype": "File",
				"file_name": f"{item_code.lower()}-cover.svg",
				"content": make_cover_svg(title, author, SAMPLE_AUTHORS),
				"is_private": 0,
				"attached_to_doctype": "Item",
				"attached_to_name": item_code,
				"attached_to_field": "image",
			}
		).insert(ignore_permissions=True)
		image = file_doc.file_url
		frappe.db.set_value("Item", item_code, "image", image)

	website_item = frappe.db.get_value(
		"Website Item", {"item_code": item_code}, ["name", "website_image"], as_dict=True
	)
	if website_item and not website_item.website_image:
		# PIL cannot thumbnail SVG, so the cover itself is the thumbnail
		frappe.db.set_value("Website Item", website_item.name, {"website_image": image, "thumbnail": image})
	return image


def ensure_uom() -> None:
	if not frappe.db.exists("UOM", SAMPLE_UOM):
		frappe.get_doc({"doctype": "UOM", "uom_name": SAMPLE_UOM, "must_be_whole_number": 1}).insert(
			ignore_permissions=True
		)


def ensure_sample_uom(item_code: str) -> bool:
	"""Move an existing sample book to the "Book" unit. Return True if it changed.

	ERPNext forbids changing the stock UOM once stock exists ("cancel the linked documents or create a new
	Item"). So this only proceeds when the book's only stock movements are its own sample opening receipts
	and nothing is reserved or ordered: those receipts are cancelled, the unit changes, and the caller
	re-creates the opening stock in the new unit. Anything else is left untouched.
	"""
	if frappe.db.get_value("Item", item_code, "stock_uom") == SAMPLE_UOM:
		return False

	vouchers = frappe.get_all(
		"Stock Ledger Entry",
		filters={"item_code": item_code, "is_cancelled": 0},
		fields=["voucher_type", "voucher_no"],
		distinct=True,
	)
	sample_codes = {book["item_code"] for book in get_sample_books()}
	for voucher in vouchers:
		if voucher.voucher_type != "Stock Entry":
			return False
		entry = frappe.get_doc("Stock Entry", voucher.voucher_no)
		if entry.stock_entry_type != "Material Receipt" or {d.item_code for d in entry.items} - sample_codes:
			return False
	if frappe.db.exists("Bin", {"item_code": item_code, "reserved_qty": [">", 0]}):
		return False

	for voucher in vouchers:
		entry = frappe.get_doc("Stock Entry", voucher.voucher_no)
		entry.flags.ignore_permissions = True
		entry.cancel()

	ensure_uom()
	item = frappe.get_doc("Item", item_code)
	old_uom = item.stock_uom
	item.stock_uom = SAMPLE_UOM
	item.flags.ignore_permissions = True
	item.save()
	for price in frappe.get_all("Item Price", filters={"item_code": item_code, "uom": old_uom}, pluck="name"):
		frappe.db.set_value("Item Price", price, "uom", SAMPLE_UOM)
	return True
