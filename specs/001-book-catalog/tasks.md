# Tasks: Book Catalog

**Input**: Design documents from `specs/001-book-catalog/`

**Prerequisites**: [plan.md](plan.md), [spec.md](spec.md), [research.md](research.md),
[data-model.md](data-model.md), [contracts/server-interfaces.md](contracts/server-interfaces.md)

**Tests**: Requested by the maintainer and by Constitution Principle III. Server-side tests are written
for every requirement that can be tested on the server.

**Format**: `[ID] [P?] [Story] Description`. `[P]` means the task can run in parallel (different file,
no open dependency).

## Phase 1: Setup

- [X] T001 Declare `required_apps = ["erpnext", "webshop"]` in frappe_shop/hooks.py
- [X] T002 [P] Create package folders frappe_shop/catalog/, frappe_shop/setup/, frappe_shop/demo/, frappe_shop/tests/ with `__init__.py`

## Phase 2: Foundational (blocks all stories)

- [X] T003 Create DocType `Book Author` (data-model.md `Book Author.author_name`) in frappe_shop/frappe_shop/doctype/book_author/
- [X] T004 Create Custom Fields on Item (data-model.md `Item.book_author`, `Item.book_isbn`, `Item.book_publisher`, `Item.book_pages`, `Item.book_language`) and on Website Item (data-model.md `Website Item.book_author`) with module `Frappe Shop`; add `fixtures` in frappe_shop/hooks.py and export to frappe_shop/fixtures/custom_field.json
- [X] T005 Add a `before_tests` hook in frappe_shop/setup/testing.py (setup wizard only when no Company exists, no password) and register it in frappe_shop/hooks.py
- [X] T006 Run `bench --site development.localhost migrate` and check that the DocType and fields exist

## Phase 3: User Story 1 — View book details (P1) 🎯 MVP

**Goal**: Book details are required, valid, and shown on the book page.
**Independent Test**: Publish one book and open its page. All five details are shown.

- [X] T007 [P] [US1] Tests for fields, required details, ISBN uniqueness, and pages > 0 in frappe_shop/tests/test_book_fields.py
- [X] T008 [US1] Implement `validate_book_item` (data-model.md `Item.book_*` validation) in frappe_shop/catalog/books.py
- [X] T009 [US1] Implement `set_book_details_on_website_item` and `sync_website_item` (data-model.md `Website Item.book_author`, specifications) in frappe_shop/catalog/books.py
- [X] T010 [US1] Register the `doc_events` for Item and Website Item in frappe_shop/hooks.py

## Phase 4: User Story 2 — Find books by author (P2)

**Goal**: The author filter and author search work on `/all-products`.
**Independent Test**: Filter by and search for one author. Only that author's books are shown.

- [X] T011 [US2] Property Setter `Website Item.search_fields` (adds `book_author`) with module `Frappe Shop`; export to frappe_shop/fixtures/property_setter.json
- [X] T012 [US2] Configure the Webshop field filter `book_author` in `setup_store` in frappe_shop/setup/store.py
- [X] T013 [P] [US2] Test that the search fields include `book_author` and that store setup sets the filter, in frappe_shop/tests/test_store_setup.py

## Phase 5: User Story 3 — Order with Cash on Delivery (P3)

**Goal**: Place Order creates a Sales Order with Cash on Delivery terms. No "Pay" button.
**Independent Test**: Place an order. The Sales Order has COD terms, and the order page has no "Pay".

- [X] T014 [US3] Extend `setup_store` with the Cash on Delivery gateway, gateway account, payment term and template, customer group terms, and Webshop checkout in frappe_shop/setup/store.py
- [X] T015 [US3] Implement `hide_online_payment` in frappe_shop/catalog/website.py and register `update_website_context` in frappe_shop/hooks.py
- [X] T016 [P] [US3] Tests for the COD configuration and the hidden "Pay" context in frappe_shop/tests/test_store_setup.py

## Phase 6: User Story 4 — Demo catalog (P4)

**Goal**: 10 sample books with price and stock, created idempotently.
**Independent Test**: Run the function twice. The second run creates nothing.

- [X] T017 [US4] Implement `create_sample_books` in frappe_shop/demo/sample_books.py
- [X] T018 [P] [US4] Idempotency test in frappe_shop/tests/test_sample_books.py
- [X] T019 [US4] Run `bench --site development.localhost execute frappe_shop.demo.sample_books.create_sample_books` twice and check the storefront

## Phase 7: User Story 5 — Store display name (P5)

**Goal**: The navbar shows "Frappe Books", and the owner can change it.
**Independent Test**: Read Website Settings after setup, change it, and re-run setup. The change is kept.

- [X] T020 [US5] Set `brand_html` and `app_name` only when empty or default, in frappe_shop/setup/store.py
- [X] T021 [P] [US5] Test the display name default and that a custom name is kept, in frappe_shop/tests/test_store_setup.py

## Phase 8: Polish & Cross-Cutting

- [X] T022 Update .github/workflows/ci.yml: pin `frappe-bench`, `--frappe-branch version-16`, and get and install payments, erpnext, webshop (`version-16`)
- [X] T023 Run `bench --site development.localhost run-tests --app frappe_shop`
- [X] T024 Run `pre-commit run --all-files`
- [X] T025 Walk through the scenarios in specs/001-book-catalog/quickstart.md on development.localhost

## Dependencies

- Phase 1 → Phase 2 → US1 → (US2, US3, US5 in any order) → US4, which uses all of the configuration → Polish.
- US4 depends on `setup_store` (US2, US3, US5) and on the book validation (US1).

## Parallel Examples

- T007 can be written alongside T008 and T009.
- T013, T016, and T021 share one test file, so they run in order with each other but in parallel with implementation.

## Implementation Strategy

MVP = Phases 1–3 (book details). Then add the stories one at a time, validating each one before the next.
