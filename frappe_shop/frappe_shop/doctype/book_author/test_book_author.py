# Copyright (c) 2026, Mahdi Anwer and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase

EXTRA_TEST_RECORD_DEPENDENCIES = []
IGNORE_TEST_RECORD_DEPENDENCIES = []


class IntegrationTestBookAuthor(IntegrationTestCase):
	def test_author_is_named_by_author_name(self):
		author = frappe.get_doc({"doctype": "Book Author", "author_name": "_Test Named Author"}).insert()
		self.assertEqual(author.name, "_Test Named Author")

	def test_author_name_is_unique(self):
		"""FR-002: one entry per author in the maintained list."""
		frappe.get_doc({"doctype": "Book Author", "author_name": "_Test Unique Author"}).insert()
		with self.assertRaises(frappe.DuplicateEntryError):
			frappe.get_doc({"doctype": "Book Author", "author_name": "_Test Unique Author"}).insert()
