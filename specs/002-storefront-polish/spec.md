# Feature Specification: Storefront Polish

**Feature Branch**: `feat/002-storefront-polish`

**Created**: 2026-11-21

**Status**: Draft

**Release**: Store version 0.2.0

**Input**: Maintainer decisions (2026-11-21): a home page at `/` with the store name, a one-line tagline,
a "Browse books" button and the latest books. A top navbar with Books, Cart, My Orders, and an "Admin"
link (System Users only). A footer with the store name. A generated cover per book (a simple SVG with
a solid colour, the title and the author; no copyrighted images). One calm primary colour and a clean
readable font. Clear empty states and a visible order confirmation after Place Order.

## Clarifications

### Session 2026-11-21

- Q: Primary colour? → A: Burgundy `#7A2E3A`.
- Q: Font? → A: Inter.
- Q: Tagline? → A: "Classic books, delivered to your door."
- Q: How many latest books, and which cover colours? → A: The 4 newest books. Each author gets one fixed
  colour from a muted warm palette (burgundy `#7A2E3A`, slate `#4A5568`, olive `#5F6B3A`, teal
  `#2F6F73`, plum `#5B3A5E`, brown `#7A5230`, navy `#2C3E64`), with white text.
- Q: Empty-state and confirmation texts? → A:
  - Empty catalog or search: "No books found. Try another author or clear the filters."
  - Empty cart: "Your cart is empty." plus a "Browse books" button.
  - No orders: "You have no orders yet." plus a "Browse books" button.
  - Confirmation: "Thank you! Your order {number} is placed. You will pay in cash on delivery."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Welcoming home page (Priority: P1)

A visitor opening the store sees the store name, the tagline, a "Browse books" button, and the 4
newest books with their covers.

**Independent Test**: Open `/`. The name, tagline, button, and 4 book cards are visible.

**Acceptance Scenarios**:

1. **Given** published books, **When** a visitor opens `/`, **Then** "Frappe Books", the tagline, a
   "Browse books" button to the book list, and the 4 newest books are shown.
2. **Given** no published books, **When** a visitor opens `/`, **Then** "No books found…" is shown
   instead of an empty grid.

### User Story 2 - Clear navigation (Priority: P1)

Every page has a navbar with Books, Cart, My Orders, and, for staff only, Admin. Every page has a
footer with the store name.

**Acceptance Scenarios**:

1. **Given** any visitor, **When** a page loads, **Then** the navbar shows Books, Cart, and My Orders,
   and the footer shows the store name.
2. **Given** a System User, **When** a page loads, **Then** an "Admin" link to the desk is shown.
   **Given** a customer or a guest, **Then** it is not shown.

### User Story 3 - Book covers (Priority: P2)

Every sample book shows a generated cover with its title and author on a solid colour. Books by the
same author share a colour.

**Acceptance Scenarios**:

1. **Given** the sample books, **When** the catalog or a book page is shown, **Then** each book has its
   cover image.
2. **Given** the sample function runs twice, **Then** no duplicate cover files are created.

### User Story 4 - Consistent look (Priority: P2)

The site uses one calm primary colour (burgundy) and the Inter font.

**Acceptance Scenarios**:

1. **Given** the store is set up, **When** any page loads, **Then** buttons and links use the primary
   colour and the text uses Inter.

### User Story 5 - Clear empty states and confirmation (Priority: P1)

Empty lists explain themselves and offer a way forward. After Place Order, the customer sees a clear
confirmation.

**Acceptance Scenarios**:

1. **Given** a filter or search with no results, **Then** "No books found. Try another author or clear
   the filters." is shown.
2. **Given** an empty cart, **Then** "Your cart is empty." and a "Browse books" button are shown.
3. **Given** a customer with no orders, **Then** "You have no orders yet." and a "Browse books" button
   are shown.
4. **Given** a customer has just placed an order, **When** the order page opens, **Then** "Thank you!
   Your order {number} is placed. You will pay in cash on delivery." is shown.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `/` MUST show the store name, the tagline, a "Browse books" button to the book list, and
  the 4 newest published books, each with cover, title, and author.
- **FR-002**: The navbar MUST contain Books, Cart, and My Orders. "Admin" MUST be shown only to System
  Users.
- **FR-003**: The footer MUST show the store name.
- **FR-004**: Each sample book MUST have a generated SVG cover (solid author colour, title, author) as
  its product image. Re-running the sample function MUST NOT create duplicates.
- **FR-005**: The site MUST use primary colour `#7A2E3A` and the Inter font.
- **FR-006**: The empty states and the confirmation MUST use the texts in Clarifications.
- **FR-007**: Store name, colour, font, and texts MUST stay configurable by the owner. Setup MUST NOT
  overwrite values the owner has changed.

### Key Entities

- **Cover**: An image file attached to a book. It is generated from the title, the author, and the
  author's colour.

## Success Criteria *(mandatory)*

- **SC-001**: 100% of sample books show a cover in the catalog and on their page.
- **SC-002**: A visitor reaches the book list from `/` in 1 click.
- **SC-003**: 0 empty-looking pages: every empty list shows its message and a way forward.
- **SC-004**: After Place Order, 100% of customers see the confirmation text on the next page.

## Assumptions

- Covers are generated only for the sample books. Covers for other books are added by staff.
- "Latest" means most recently created published books.
- Text changes use standard translations for English, so the owner can edit them later.

## Out of Scope

- Changes to webshop templates other than extending the order page with a confirmation block.
- Logos and real cover images.
