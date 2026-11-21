# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Entries are built from the Conventional Commits on `main` (see [docs/releasing.md](docs/releasing.md)).

## [Unreleased]

## [0.2.1] - 2026-11-21

### Fixed

- Navbar: removed the "Admin" link (Switch to Desk is in the avatar menu) and the "Cart" text link (the
  cart icon with its count stays). ([#21])
- IQD prices show without decimals (`15,000`) on the product list, book page, cart, and order, through
  currency precision settings. ([#21])
- Sample books use the unit "Book" ("/ Book"). Existing sample books move to it when it is safe. ([#21])

## [0.2.0] - 2026-11-21

Storefront polish (`specs/002-storefront-polish`).

### Added

- Home page at `/` with the store name, tagline, a "Browse books" button, and the 4 latest books. ([#19])
- Website Theme "Frappe Books": burgundy `#7A2E3A` primary colour and the Inter font. ([#19])
- Navbar with Books, Cart, and My Orders, plus an "Admin" link for staff only. Footer with the store
  name. ([#19])
- Generated SVG covers for the sample books, one colour per author. ([#19])
- Clear empty states with a "Browse books" button, and an order confirmation after Place Order. ([#19])
- CodeQL code scanning (default setup).

### Fixed

- Checkout: new website users now get the `Customer` role (Portal Settings default role), so the
  order confirmation page no longer returns 403 after Place Order. ([#18])

### Security

- CI workflow `GITHUB_TOKEN` limited to `contents: read` (CodeQL alert #1). ([#17])

### Changed

- pre-commit now also checks files in `.github/`. ([#16])

## [0.1.0] - 2026-11-21

First release of the store: the Book catalog (`specs/001-book-catalog`).

### Added

- Book catalog: books are Items in the `Books` group with author, ISBN (unique), publisher,
  number of pages (> 0), and language. The details show on the product page. ([#11])
- `Book Author` list. Customers can filter and search books by author in the store. ([#11])
- Checkout with Cash on Delivery only. No online payment and no "Pay" button. ([#11])
- Store display name "Frappe Books", which can be changed in Website Settings. ([#11])
- Idempotent store setup (`frappe_shop.setup.store.setup_store`) and 10 demo books
  (`frappe_shop.demo.sample_books.create_sample_books`). ([#11])
- Server tests for the book catalog. ([#11])
- Project constitution and spec-driven development workflow (GitHub Spec Kit). ([#9], [#10])
- `CLAUDE.md` working rules and the learning log. ([#9])
- Dependabot configuration for GitHub Actions and pip. ([#2])
- Initial Frappe app scaffold. (`7d1da10`)

### Changed

- CI installs `payments`, `erpnext` and `webshop` (`version-16`) and pins `frappe-bench`. ([#11])
- Contribution workflow: Claude Code may open PRs and squash merge them after all required checks
  pass. The constitution is now 1.1.0. ([#12])

### Fixed

- CI branch name in the README. ([#1])

[Unreleased]: https://github.com/jaguar-mahdi/frappe-shop/compare/v0.2.1...HEAD
[0.2.1]: https://github.com/jaguar-mahdi/frappe-shop/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/jaguar-mahdi/frappe-shop/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/jaguar-mahdi/frappe-shop/releases/tag/v0.1.0
[#1]: https://github.com/jaguar-mahdi/frappe-shop/pull/1
[#2]: https://github.com/jaguar-mahdi/frappe-shop/pull/2
[#9]: https://github.com/jaguar-mahdi/frappe-shop/pull/9
[#10]: https://github.com/jaguar-mahdi/frappe-shop/pull/10
[#11]: https://github.com/jaguar-mahdi/frappe-shop/pull/11
[#12]: https://github.com/jaguar-mahdi/frappe-shop/pull/12
[#16]: https://github.com/jaguar-mahdi/frappe-shop/pull/16
[#17]: https://github.com/jaguar-mahdi/frappe-shop/pull/17
[#18]: https://github.com/jaguar-mahdi/frappe-shop/pull/18
[#19]: https://github.com/jaguar-mahdi/frappe-shop/pull/19
[#21]: https://github.com/jaguar-mahdi/frappe-shop/pull/21
