"""User Story 4: demo catalog (spec FR-013, FR-014, SC-006)."""

import frappe
from frappe.tests import IntegrationTestCase

from frappe_shop.catalog.books import BOOK_FIELDS
from frappe_shop.demo.sample_books import (
	SAMPLE_PRICE,
	SAMPLE_STOCK_QTY,
	create_sample_books,
	get_sample_books,
)


class TestSampleBooks(IntegrationTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		cls.codes = [book["item_code"] for book in get_sample_books()]
		cls.first_run = create_sample_books()

	def counts(self) -> dict:
		codes = ["in", self.codes]
		return {
			"items": frappe.db.count("Item", {"item_code": codes}),
			"prices": frappe.db.count("Item Price", {"item_code": codes}),
			"website_items": frappe.db.count("Website Item", {"item_code": codes}),
			"stock_entries": frappe.db.count("Stock Ledger Entry", {"item_code": codes, "is_cancelled": 0}),
			"authors": frappe.db.count(
				"Book Author", {"name": ["in", {b["book_author"] for b in get_sample_books()}]}
			),
		}

	def test_running_twice_creates_nothing_new(self):
		"""The function is idempotent: a second run reports everything as existing."""
		before = self.counts()
		second_run = create_sample_books()
		self.assertEqual(second_run["created"], [])
		self.assertEqual(sorted(second_run["existing"]), sorted(self.codes))
		self.assertEqual(self.counts(), before)

	def test_ten_complete_published_books(self):
		"""FR-013: 10 books, all five details, price, published, stock."""
		counts = self.counts()
		self.assertEqual(counts["items"], 10)
		self.assertEqual(counts["prices"], 10)
		self.assertEqual(counts["website_items"], 10)
		self.assertEqual(counts["authors"], 7)
		self.assertGreaterEqual(counts["stock_entries"], 10)

		for code in self.codes:
			item = frappe.db.get_value(
				"Item", code, [fieldname for fieldname, _label in BOOK_FIELDS], as_dict=True
			)
			self.assertTrue(all(item.values()), code)
			self.assertEqual(
				frappe.db.get_value("Item Price", {"item_code": code}, "price_list_rate"), SAMPLE_PRICE
			)
			self.assertTrue(frappe.db.get_value("Website Item", {"item_code": code}, "published"))

		for code in self.first_run["created"]:
			stock = sum(frappe.get_all("Bin", filters={"item_code": code}, pluck="actual_qty"))
			self.assertEqual(stock, SAMPLE_STOCK_QTY, code)

	def test_sample_isbns_are_demo_values(self):
		"""Demo ISBNs are clearly fake and unique."""
		isbns = [book["book_isbn"] for book in get_sample_books()]
		self.assertEqual(len(set(isbns)), 10)
		self.assertTrue(all(isbn.startswith("DEMO-") for isbn in isbns))
