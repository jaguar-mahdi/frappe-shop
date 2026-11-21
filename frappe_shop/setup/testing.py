"""Test environment preparation (specs/001-book-catalog, research R11)."""

import frappe
from frappe.utils import now_datetime


def before_tests():
	"""Complete the setup wizard on a fresh site (CI) so ERPNext has a Company.

	Does nothing on a site that already has a Company, such as a developer site.
	No user password is set.
	"""
	frappe.clear_cache()
	if frappe.db.a_row_exists("Company"):
		return

	from frappe.desk.page.setup_wizard.setup_wizard import setup_complete

	year = now_datetime().year
	setup_complete(
		{
			"language": "English",
			"country": "United States",
			"timezone": "America/New_York",
			"currency": "USD",
			"company_name": "Frappe Books Test",
			"company_abbr": "FBT",
			"chart_of_accounts": "Standard",
			"fy_start_date": f"{year}-01-01",
			"fy_end_date": f"{year}-12-31",
			"setup_demo": 0,
		}
	)
	# No explicit commit here: setup_complete() commits in its last stage (run_post_setup_complete),
	# so the Company survives the per-class rollback of IntegrationTestCase.
