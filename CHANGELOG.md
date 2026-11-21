# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Entries are built from the Conventional Commits on `main` (see [docs/releasing.md](docs/releasing.md)).

## [Unreleased]

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

[Unreleased]: https://github.com/jaguar-mahdi/frappe-shop/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/jaguar-mahdi/frappe-shop/releases/tag/v0.1.0
[#1]: https://github.com/jaguar-mahdi/frappe-shop/pull/1
[#2]: https://github.com/jaguar-mahdi/frappe-shop/pull/2
[#9]: https://github.com/jaguar-mahdi/frappe-shop/pull/9
[#10]: https://github.com/jaguar-mahdi/frappe-shop/pull/10
[#11]: https://github.com/jaguar-mahdi/frappe-shop/pull/11
[#12]: https://github.com/jaguar-mahdi/frappe-shop/pull/12
