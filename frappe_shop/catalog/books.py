"""Book rules for Items in the "Books" item group (specs/001-book-catalog).

Constraints come from specs/001-book-catalog/data-model.md.
"""

import frappe
from frappe import _

BOOK_ITEM_GROUP = "Books"

# (Item fieldname, label shown to staff and on the product page)
BOOK_FIELDS = (
	("book_author", "Author"),
	("book_isbn", "ISBN"),
	("book_publisher", "Publisher"),
	("book_pages", "Number of Pages"),
	("book_language", "Language"),
)
BOOK_SPEC_LABELS = {label for _fieldname, label in BOOK_FIELDS}


def is_book(item) -> bool:
	return item.get("item_group") == BOOK_ITEM_GROUP


def validate_book_item(doc, method=None):
	"""Item.validate: all five details are required for books, and pages must be > 0 (FR-003, FR-005)."""
	if not is_book(doc):
		return

	missing = [_(label) for fieldname, label in BOOK_FIELDS if not doc.get(fieldname)]
	if missing:
		frappe.throw(
			_("Book details missing: {0}").format(", ".join(missing)),
			frappe.MandatoryError,
			title=_("Missing Book Details"),
		)

	if frappe.utils.cint(doc.book_pages) <= 0:
		frappe.throw(_("Number of Pages must be greater than 0"), title=_("Invalid Book Details"))


def set_book_details_on_website_item(doc, method=None):
	"""Website Item.validate: copy author and the five details from the Item (FR-006, FR-007)."""
	if not doc.item_code:
		return

	item = frappe.db.get_value(
		"Item",
		doc.item_code,
		["item_group", *(fieldname for fieldname, _label in BOOK_FIELDS)],
		as_dict=True,
	)
	if not item:
		return

	# keep rows that are not book details (added by staff or copied from the item group)
	other_rows = [row for row in doc.get("website_specifications") or [] if row.label not in BOOK_SPEC_LABELS]
	doc.set("website_specifications", [])

	if is_book(item):
		doc.book_author = item.book_author
		for fieldname, label in BOOK_FIELDS:
			doc.append("website_specifications", {"label": label, "description": str(item.get(fieldname))})
	else:
		doc.book_author = None

	for row in other_rows:
		doc.append("website_specifications", {"label": row.label, "description": row.description})


def sync_website_item(doc, method=None):
	"""Item.on_update: re-save the linked Website Item so storefront details follow the Item."""
	website_item = frappe.db.get_value("Website Item", {"item_code": doc.name})
	if not website_item:
		return

	web_doc = frappe.get_doc("Website Item", website_item)
	web_doc.flags.ignore_permissions = True
	web_doc.save()
