# Implementation Plan: Book Catalog

**Branch**: `feat/001-book-catalog` | **Date**: 2026-11-21 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/001-book-catalog/spec.md`

## Summary

Sell books in the existing Webshop. Books are ERPNext Items in the `Books` group, with five Custom
Fields (author as a Link to a new `Book Author` DocType, ISBN unique, publisher, pages > 0, language).
The fields are shown on the product page through Website Item specifications. Customers filter by
author with Webshop's standard field filter and search by author through `Website Item.search_fields`.
Checkout creates a Sales Order with Cash on Delivery payment terms. A placeholder gateway record
enables "Place Order", and a context hook hides the online "Pay" button. An idempotent function
creates 10 demo books. All research is in [research.md](research.md).

## Technical Context

**Language/Version**: Python 3.14 (Frappe v16). JSON fixtures.

**Primary Dependencies**: `frappe` v16.60.1, `erpnext` v16.60.0, `payments` v16.0.1, `webshop`
`version-16` (`5ba1656`). All are `version-16` branches.

**Storage**: MariaDB through the Frappe ORM. No schema change outside Custom Fields and the new
DocType.

**Testing**: `bench --site <site> run-tests --app frappe_shop` (`frappe.tests.IntegrationTestCase`).
The same command runs in CI.

**Target Platform**: Frappe bench (Linux). Dev site `development.localhost`. CI site `test_site`.

**Project Type**: Frappe custom app that extends ERPNext and Webshop.

**Performance Goals**: Storefront pages behave as standard Webshop pages. The catalog is tiny (about
10 books).

**Constraints**: No edits to `frappe`, `erpnext`, `payments`, or `webshop` source. No real payment
gateway. No secrets.

**Scale/Scope**: About 10 demo books, 7 authors, one company.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-checked after Phase 1 design.* Constitution v1.0.0.

| Principle | Check | Result |
| --- | --- | --- |
| I. Extend, never modify | All changes live in `frappe_shop`: a DocType, Custom Fields and a Property Setter (fixtures), `doc_events`, and `update_website_context`. No upstream file is edited. | ✅ Pass |
| II. PR, green CI, Conventional Commits, SemVer | Work is on `feat/001-book-catalog`, delivered by PR. CI installs the dependencies so `Server` can pass. Commits are typed. The version is not bumped here; the release is a separate step. | ✅ Pass |
| III. Every feature ships with a test | Server tests cover the fields, ISBN uniqueness, pages > 0, required details, website sync, store setup, and sample-data idempotency. | ✅ Pass |
| IV. Security | No credentials in code. The CI setup wizard runs without a password. The scans are unchanged and still required. | ✅ Pass |
| V. Simplicity, no real gateway | Webshop's own filter, search, and checkout are reused. The `Cash on Delivery` gateway is a placeholder record with no controller. There is one small hook to hide "Pay". | ✅ Pass. See Complexity Tracking for the placeholder gateway. |

**Post-design re-check**: ✅ Pass. No new violations after data-model and contracts.

## Project Structure

### Documentation (this feature)

```text
specs/001-book-catalog/
├── spec.md
├── plan.md                         # this file
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/server-interfaces.md
├── checklists/requirements.md
└── tasks.md                        # /speckit-tasks
```

### Source Code (repository root)

```text
frappe_shop/
├── hooks.py                        # required_apps, fixtures, doc_events, update_website_context, before_tests
├── fixtures/
│   ├── custom_field.json           # Item.book_* and Website Item.book_author
│   └── property_setter.json        # Website Item.search_fields
├── catalog/
│   ├── books.py                    # Item validation and Website Item sync
│   └── website.py                  # hide "Pay" for Cash on Delivery
├── setup/
│   ├── store.py                    # setup_store(): idempotent store configuration
│   └── testing.py                  # before_tests(): setup wizard on fresh CI sites
├── demo/
│   └── sample_books.py             # create_sample_books(): idempotent demo data
├── frappe_shop/doctype/book_author/  # new DocType (module Frappe Shop)
└── tests/
    ├── test_book_fields.py
    ├── test_store_setup.py
    └── test_sample_books.py
.github/workflows/ci.yml            # installs payments, erpnext, webshop (version-16)
```

**Structure Decision**: This is a single Frappe app. Business logic lives in small modules under
`frappe_shop/`. Tests live under `frappe_shop/tests/`, where `run-tests --app` discovers them.

## Complexity Tracking

| Item | Why Needed | Simpler Alternative Rejected Because |
| --- | --- | --- |
| Placeholder `Cash on Delivery` Payment Gateway record and a hook to hide "Pay" | Webshop allows "Place Order" (a real Sales Order) only when a gateway account is set. The maintainer chose a direct order over a quotation request. | The quotation-request flow needs no code, but the customer would not get an order confirmation (spec US3). The maintainer rejected it on 2026-11-21. |
