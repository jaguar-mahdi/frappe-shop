"""Store home page (specs/002-storefront-polish, US1)."""

import frappe

from frappe_shop.setup.store import STORE_DISPLAY_NAME, STORE_TAGLINE

LATEST_BOOKS = 4
no_cache = 1


def get_latest_books(limit: int = LATEST_BOOKS) -> list[dict]:
	return frappe.get_all(
		"Website Item",
		filters={"published": 1, "item_group": "Books"},
		fields=["web_item_name", "route", "website_image", "book_author"],
		order_by="creation desc",
		limit=limit,
	)


def get_context(context):
	context.no_breadcrumbs = True
	context.show_sidebar = False
	context.store_name = frappe.db.get_single_value("Website Settings", "app_name") or STORE_DISPLAY_NAME
	context.title = context.store_name
	context.tagline = STORE_TAGLINE
	context.books = get_latest_books()
	return context
