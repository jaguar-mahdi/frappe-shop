# Contracts: server interfaces

Interfaces that `frappe_shop` exposes to operators and to the framework.

## Bench-executable functions

### `frappe_shop.setup.store.setup_store(company: str | None = None) -> dict`

- Run: `bench --site <site> execute frappe_shop.setup.store.setup_store`
- `company`: defaults to `Webshop Settings.company`, then to the ERPNext default company. If no
  Company exists, it raises a clear error.
- Idempotent: running it again changes nothing that is already correct. It never deletes records.
- Returns a summary dict: the names of the configured records.
- Does not commit. `bench execute` commits after the call.

### `frappe_shop.demo.sample_books.create_sample_books(company: str | None = None) -> dict`

- Run: `bench --site <site> execute frappe_shop.demo.sample_books.create_sample_books`
- Calls `setup_store(company)` first.
- Ensures that the 10 sample Book Authors, Items, Item Prices (15,000), Website Items (published),
  and opening stock (20 each) exist.
- Idempotent: records are matched by natural key (author name, item code `BOOK-DEMO-NNNN`, ISBN).
  Stock is added only for items without stock ledger entries.
- Returns `{"created": [...], "existing": [...]}`, listing item codes.

## Framework hooks (`frappe_shop/hooks.py`)

| Hook | Target | Purpose |
| --- | --- | --- |
| `required_apps` | `["erpnext", "webshop"]` | Install-time dependency. |
| `fixtures` | Custom Field and Property Setter with `module = "Frappe Shop"` | Book fields and search fields. |
| `doc_events["Item"]["validate"]` | `frappe_shop.catalog.books.validate_book_item` | FR-003, FR-005. |
| `doc_events["Item"]["on_update"]` | `frappe_shop.catalog.books.sync_website_item` | Re-sync the storefront after an Item edit. |
| `doc_events["Website Item"]["validate"]` | `frappe_shop.catalog.books.set_book_details_on_website_item` | FR-006 and the filter field. |
| `update_website_context` | `frappe_shop.catalog.website.hide_online_payment` | FR-011: no "Pay" button. |
| `before_tests` | `frappe_shop.setup.testing.before_tests` | Fresh CI sites get a company. |
