# Research: Book Catalog

Phase 0 output of `/speckit-plan`. Every finding below was checked against the installed source:
`frappe` v16.60.1, `erpnext` v16.60.0, `payments` v16.0.1, `webshop` `version-16` @ `5ba1656`.

## R1. Where the book details live

- **Decision**: Custom Fields on `Item` (`book_author`, `book_isbn`, `book_publisher`, `book_pages`,
  `book_language`), exported as fixtures from `frappe_shop`.
- **Rationale**: Constitution Principle I (extend, never modify). The spec defines a book as an existing
  product with extra details.
- **Alternatives considered**: A new "Book" DocType (rejected: it duplicates Item, price, and stock).
  Editing `erpnext` JSON (rejected: Principle I).

## R2. Which Items are books

- **Decision**: An Item is a book when its Item Group is `Books`. The maintainer approved this group
  name on 2026-11-21.
- **Rationale**: This needs no extra "is book" field. Book rules must not apply to non-book Items,
  because ERPNext and test setups create many other Items.
- **Alternatives considered**: A new `is_book` check field (rejected: it adds a product data field
  that is not in the spec).

## R3. Required details are enforced on the server

- **Finding**: Frappe enforces only `reqd` on the server. `mandatory_depends_on` is client-side only
  (`frappe/model/document.py::_get_missing_mandatory_fields` reads only `reqd`).
- **Decision**: `mandatory_depends_on: eval:doc.item_group=='Books'` gives a helpful UI. A `doc_events`
  `Item.validate` hook in `frappe_shop` enforces FR-003 and FR-005 on the server: all five details
  required, and `book_pages > 0`.
- **Alternatives considered**: `reqd: 1` (rejected: it would apply to every Item).

## R4. ISBN uniqueness

- **Decision**: Set `unique: 1` on the `book_isbn` Custom Field. Frappe stores empty unique values as
  NULL, so non-book Items without an ISBN do not collide. Do not check the format (spec FR-004).

## R5. Author filter on the storefront

- **Finding**: Webshop field filters (`Webshop Settings.filter_fields`) accept only `Website Item`
  fields of type `Link` or `Table MultiSelect`
  (`webshop_settings.py::validate_field_filters`). Filters read `Website Item` columns, not `Item`.
- **Decision** (approved by the maintainer on 2026-11-21): Author becomes a `Link` to a new DocType
  `Book Author` in `frappe_shop`, named by the author's name. A read-only `book_author` Custom Field
  on `Website Item` is copied from the Item. `Webshop Settings` gets `enable_field_filters = 1` with a
  filter row for `book_author`. This is configuration only, with no Webshop patch.
- **Alternatives considered**: Free text plus a custom filter page (rejected by the maintainer: more
  code). Search only (rejected by the maintainer: drops the filter).

## R6. Author search

- **Finding**: The product listing search (`product_data_engine/query.py::build_search_filters`)
  searches `Website Item` default fields plus `meta.get_search_fields()`.
- **Decision**: Add a Property Setter that sets `Website Item.search_fields` to
  `web_item_name, item_code, item_group, book_author`, exported as a fixture. `Book Author` is named
  by the author's name, so a `LIKE` search on the link value matches author names, partially and
  without case sensitivity.
- **Note**: The navbar quick search (`/search` without Redisearch) searches only item name, brand,
  and description. Author search is provided on the product listing page.

## R7. Book details on the book page

- **Finding**: The product page shows the `Website Item.website_specifications` table
  (`templates/generators/item/item.html`).
- **Decision**: A `doc_events` `Website Item.validate` hook copies the five details into
  `website_specifications` rows labelled Author, ISBN, Publisher, Number of Pages, and Language. It
  also copies `book_author`. An `Item.on_update` hook re-saves the linked Website Item, so edits to an
  Item reach the storefront. Specification rows that are not book rows are kept.
- **Alternatives considered**: Overriding the Webshop product template (rejected: it is heavier and
  breaks on Webshop upgrades).

## R8. Cash on Delivery checkout

- **Finding**: `Webshop Settings.enable_checkout` (the "Place Order" button that creates a Sales
  Order) is switched off unless `payment_gateway_account` is set (`validate_checkout`). With checkout
  enabled, the order page shows a "Pay" button (`templates/pages/order.html`, `enabled_checkout`).
- **Decision** (approved by the maintainer on 2026-11-21): direct order with a small override.
  - A placeholder `Payment Gateway` named `Cash on Delivery`, with no controller and no online
    processing, plus a `Payment Gateway Account` that posts to the company's default cash account.
    `Webshop Settings.enable_checkout = 1`.
  - A `Payment Terms Template` named `Cash on Delivery` (100%, Mode of Payment `Cash`, 0 days) is set
    on the Webshop default Customer Group. Sales Orders get a Cash on Delivery payment schedule, which
    records FR-011.
  - An `update_website_context` hook sets `enabled_checkout = False` on order pages when the
    configured gateway is `Cash on Delivery`, which hides "Pay". Frappe runs this hook after the
    page's `get_context` (`base_template_page.py::post_process_context`).
- **Constitution**: Principle V forbids a real gateway. The placeholder has no controller, so it
  cannot process payments.

## R9. Store display name

- **Finding**: The navbar shows `Website Settings.brand_html` (`templates/includes/navbar/navbar.html`).
- **Decision**: Store setup sets `brand_html` and `app_name` to `Frappe Books` only when they are empty
  or still the defaults. The owner can then change them in Website Settings (FR-012).

## R10. Sample books

- **Decision**: `frappe_shop.demo.sample_books.create_sample_books(company=None)` runs through
  `bench execute`. It is idempotent: every record is looked up by a natural key before it is created,
  and opening stock is added only when the item has no stock ledger entries. It first calls
  `frappe_shop.setup.store.setup_store()`. The data are 10 public-domain classics with demo ISBNs
  (`DEMO-0001`…), publisher `Frappe Books Demo Press`, approximate page counts, language English,
  price 15,000 in the selling price list's currency, and 20 in stock. All of these values were
  approved by the maintainer on 2026-11-21.
- **Stock**: Material Receipt with `allow_zero_valuation_rate`, so no cost price has to be invented.
- **Not fixtures**: sample data are demo content, not app configuration.

## R11. Tests in CI

- **Finding**: `bench run-tests --app frappe_shop` runs only `frappe_shop`'s `before_tests` hooks.
  ERPNext v16 has no `before_tests` hook. Importing `erpnext.tests.utils` creates a large `_Test`
  data set on import, so we do not use it, to keep developer sites clean.
- **Decision**: Add a `frappe_shop` `before_tests` hook that runs the setup wizard only when no Company
  exists (a fresh CI site), with no user password. On `development.localhost` it does nothing.
  Tests use `frappe.tests.IntegrationTestCase` and roll back.

## R12. CI bench

- **Decision**: Pin `frappe-bench==5.31.1` and `bench init --frappe-branch version-16`. Run
  `bench get-app --branch version-16` for `payments`, `erpnext`, and `webshop` before `frappe_shop`.
  Install them in dependency order. `frappe_shop` declares `required_apps = ["erpnext", "webshop"]`.
