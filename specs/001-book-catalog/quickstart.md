# Quickstart: validate the Book Catalog

## Prerequisites

- Bench with `frappe`, `erpnext`, `payments`, `webshop` (`version-16`) and `frappe_shop`.
- Site with the ERPNext setup wizard completed (a Company exists). `bench start` running.

## Setup

```bash
bench --site development.localhost migrate          # syncs Book Author DocType and fixtures
bench --site development.localhost execute frappe_shop.demo.sample_books.create_sample_books
bench --site development.localhost execute frappe_shop.demo.sample_books.create_sample_books  # 2nd run: all "existing"
```

## Automated checks

```bash
bench --site development.localhost set-config allow_tests true   # once per site, local only
bench --site development.localhost run-tests --app frappe_shop
```

## Manual scenarios (spec user stories)

| Story | Steps | Expected |
| --- | --- | --- |
| US1 | Open `/all-products`, open "Pride and Prejudice". | Specifications show Author, ISBN, Publisher, Number of Pages, Language. |
| US1 | In Desk, create an Item in group Books without ISBN. | Save fails, and the error lists the missing details. |
| US2 | On `/all-products`, tick author "Charles Dickens" in the filter. | Only the 2 Dickens books are listed. |
| US2 | On `/all-products`, search "dickens". | The Dickens books are listed. |
| US3 | Log in as a website customer with an address, add a book to the cart, Place Order. | A Sales Order is created with the Cash on Delivery payment terms, and the order page has no "Pay" button. |
| US4 | Count books on `/all-products`. | 10 books, each with a price and "In stock". |
| US5 | Look at the navbar. Change Website Settings → Brand HTML. | Shows "Frappe Books", then the new name. |
