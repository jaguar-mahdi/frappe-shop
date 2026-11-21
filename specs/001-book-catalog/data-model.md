# Data Model: Book Catalog

Phase 1 output of `/speckit-plan`. Canonical source for field constraints.

## Book Author (new DocType, module `Frappe Shop`)

| Field | Type | Constraints |
| --- | --- | --- |
| `author_name` | Data | Required, unique. Used as the document name (`autoname: field:author_name`). |

- Read permission for all users and guests is not needed. Webshop builds filter values from
  `Website Item` with its own queries.
- Write access: `System Manager`, `Item Manager`, `Stock Manager`.

## Item (existing, Custom Fields)

The fields sit in a section "Book Details" that is shown when `item_group == "Books"`.

| Field | Type | Constraints |
| --- | --- | --- |
| `Item.book_author` | Link → Book Author | Required for books (FR-002, FR-003). |
| `Item.book_isbn` | Data | Required for books. Unique across all Items (FR-004). No format check. |
| `Item.book_publisher` | Data | Required for books. Free text (FR-005). |
| `Item.book_pages` | Int | Required for books. Must be > 0 (FR-005). |
| `Item.book_language` | Data | Required for books. Free text (FR-005). |

Validation (server, `Item.validate` hook): when `item_group == "Books"`, all five fields are required
(the error lists the missing labels) and `book_pages > 0`.

## Website Item (existing, Custom Field)

| Field | Type | Constraints |
| --- | --- | --- |
| `Website Item.book_author` | Link → Book Author | Read-only. Copied from `Item.book_author` on validate. Used by the author filter and search. |

- `website_specifications`: rows labelled `Author`, `ISBN`, `Publisher`, `Number of Pages`, and
  `Language` are kept in sync with the Item on validate. Other rows are kept.
- Property Setter: `search_fields = web_item_name, item_code, item_group, book_author`.

## Store configuration (site data, created by `setup_store`)

| Record | Key | Values |
| --- | --- | --- |
| Item Group | `Books` | Parent `All Item Groups`. |
| Payment Gateway | `Cash on Delivery` | No settings, no controller. |
| Payment Gateway Account | gateway `Cash on Delivery` + company | `payment_account` = company default cash account. |
| Payment Term | `Cash on Delivery` | 100%, Mode of Payment `Cash`, 0 days after invoice date. |
| Payment Terms Template | `Cash on Delivery` | One row: the term above. |
| Customer Group (Webshop default) | from settings | `payment_terms = Cash on Delivery`. |
| Webshop Settings | single | `enabled`, `company`, `price_list`, `default_customer_group`, `show_price`, `show_stock_availability`, `enable_field_filters` + filter `book_author`, `enable_checkout`, `payment_gateway_account`. |
| Website Settings | single | `brand_html` and `app_name` = `Frappe Books` if empty or default. |

## Order (existing)

Sales Order from Webshop checkout: `payment_terms_template = Cash on Delivery`. There is no Payment
Request and no online payment.
