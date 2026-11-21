# Tasks: Storefront Polish

**Input**: [spec.md](spec.md), [plan.md](plan.md)

## Phase 1: Foundational

- [X] T001 Theme "Frappe Books" (Inter, `#7A2E3A`) in `ensure_website_theme` in frappe_shop/setup/store.py
- [X] T002 Navbar items, footer copyright, and `home_page` in `configure_website` in frappe_shop/setup/store.py
- [X] T003 English `Translation` records for the empty-state texts in frappe_shop/setup/store.py

## Phase 2: US1 Home page (P1)

- [X] T004 [US1] Landing page in frappe_shop/www/home.html and frappe_shop/www/home.py

## Phase 3: US2 Navigation (P1)

- [X] T005 [US2] Admin link for System Users and the orders empty message in frappe_shop/catalog/website.py; register them in frappe_shop/hooks.py

## Phase 4: US3 Covers (P2)

- [X] T006 [US3] SVG cover generator in frappe_shop/catalog/covers.py
- [X] T007 [US3] Attach covers idempotently in frappe_shop/demo/sample_books.py

## Phase 5: US5 Empty states and confirmation (P1)

- [X] T008 [US5] "Browse books" buttons in frappe_shop/public/js/storefront.js via `web_include_js` in frappe_shop/hooks.py
- [X] T009 [US5] Confirmation block in frappe_shop/templates/pages/order.html and order.py

## Phase 6: Tests and polish

- [X] T010 [P] Server tests in frappe_shop/tests/test_storefront.py
- [X] T011 Run setup and the sample function on development.localhost, migrate, and run the tests
- [X] T012 Screenshots in docs/screenshots/ (home, product list, book page, order confirmation)
- [X] T013 pre-commit, commit, and open the PR
