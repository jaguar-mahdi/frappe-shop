# Implementation Plan: Storefront Polish

**Branch**: `feat/002-storefront-polish` | **Date**: 2026-11-21 | **Spec**: [spec.md](spec.md)

## Summary

Polish the storefront by extension only. A Website Theme sets the colour and font. Website Settings
set the navbar, footer, and home page. A `home` page in `frappe_shop` provides the landing page. An
`update_website_context` hook adds the staff-only Admin link. English `Translation` records reword the
empty states. A small storefront script adds "Browse books" buttons. A `frappe_shop` order page extends
webshop's template with a confirmation block. The sample-books function generates and attaches SVG
covers.

## Technical Context

**Language/Version**: Python 3.14, Jinja, a small JS file, SCSS (Website Theme). Frappe v16.
**Dependencies**: `frappe` (Website Theme, Website Settings, Translation, File), `webshop` (Website Item,
cart, order page).
**Testing**: `bench run-tests --app frappe_shop`. Screenshots taken with Playwright if available.
**Constraints**: No edits to webshop or erpnext. No copyrighted images.

## Research (Phase 0)

| Topic | Finding (source checked) | Decision |
| --- | --- | --- |
| Colour and font | `Website Theme` has `google_font` and `primary_color` (Link → `Color`). Validate compiles SCSS with `node generate_bootstrap_theme.js` (`website_theme.py`). | A custom theme "Frappe Books" (`Inter`, a `Color` record `#7A2E3A`). It is set as the site theme only if the site still uses the default theme. |
| Navbar and footer | Website Settings `top_bar_items` and `copyright`. The navbar renders `top_bar_items`. | Add Books `/all-products`, Cart `/cart`, My Orders `/orders` if missing. Set copyright to the store name if empty. |
| Admin link for staff only | Top Bar Items have no role condition. `update_website_context` runs after page context (feature 001, research R8). | The hook appends Admin → `/app` when `frappe.session.data.user_type == "System User"`. |
| Home page | `get_home_page` falls back to Website Settings and hooks. No app has a `home` route. | `frappe_shop/www/home.{html,py}`. Setup sets `home_page = "home"` if empty. |
| Empty-state texts | webshop uses `_()`/`__()` (`"No products found"`, `"Your cart is Empty"`). English user `Translation` records apply in both Python and JS (checked on the site, then rolled back). | `Translation` records for `en`, created only if missing. |
| "Browse books" buttons | Cart empty state has a "See past orders" button only. The orders list uses `no_result_message`. | `web_include_js` → `/assets/frappe_shop/js/storefront.js` adds the button. `update_website_context` sets the orders `no_result_message`. |
| Order confirmation | Jinja `ChoiceLoader` includes a `PrefixLoader` per app (`frappe/utils/jinja.py`). Page lookup checks the most recently installed app first (`template_page.py`). | `frappe_shop/templates/pages/order.html` extends `webshop/templates/pages/order.html` and adds a block. `order.py` re-exports webshop's `get_context`. |
| Covers | Website Item `make_thumbnail` uses PIL, which cannot read SVG. | Attach the SVG as `Item.image` and `Website Item.website_image`, and set `thumbnail` to the same URL. |

## Constitution Check (v1.1.0)

| Principle | Result |
| --- | --- |
| I. Extend, never modify | ✅ Theme, settings, translations, hooks, and pages live in `frappe_shop`. The order page is extended, not copied. |
| II. PR, green CI, Conventional Commits, SemVer | ✅ Delivered by PR. Release 0.2.0 is a separate PR. |
| III. Tests | ✅ Server tests for setup, covers, the home context, the Admin link, and the confirmation. |
| IV. Security | ✅ No secrets. Covers are escaped SVG text. No external images. |
| V. Simplicity | ✅ Configuration first. One small JS file and one extended template. |

## Structure

```text
frappe_shop/
├── hooks.py                      # web_include_js, extra update_website_context
├── setup/store.py                # theme, navbar, footer, home page, translations
├── catalog/website.py            # Admin link, orders empty message
├── catalog/covers.py             # SVG cover generation
├── demo/sample_books.py          # attach covers (idempotent)
├── www/home.html, home.py        # landing page
├── templates/pages/order.html    # extends webshop order page (confirmation)
├── templates/pages/order.py      # re-exports webshop get_context
├── public/js/storefront.js       # "Browse books" buttons in empty states
└── tests/test_storefront.py
docs/screenshots/
```
