"""Order page: webshop's page plus a confirmation block (specs/002-storefront-polish, US5).

The template in this app extends webshop's template; the context comes from webshop unchanged.
"""

from webshop.templates.pages.order import get_context as webshop_get_context

no_cache = 1


def show_order_confirmation(doc) -> bool:
	return (
		getattr(doc, "doctype", None) == "Sales Order"
		and getattr(doc, "order_type", None) == "Shopping Cart"
		and getattr(doc, "docstatus", 0) == 1
		and getattr(doc, "status", "") not in ("Cancelled", "Closed", "Completed")
	)


def get_context(context):
	webshop_get_context(context)
	context.show_order_confirmation = show_order_confirmation(context.get("doc"))
	return context
