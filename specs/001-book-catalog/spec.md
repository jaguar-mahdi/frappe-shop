# Feature Specification: Book Catalog

**Feature Branch**: `docs/001-book-catalog-spec`

**Created**: 2026-11-21

**Status**: Draft

**Release**: Store version 0.1.0

**Input**: User description: "Book catalog (version 0.1.0 of the store). Store display name: 'Frappe Books'
(placeholder, configurable). A book is an ERPNext Item with extra fields: author, ISBN, publisher, number of
pages, language. Customers browse books on the Webshop and see these fields on the book page. Customers can
search or filter books by author. Cart and order use the standard Webshop flow; payment method is Cash on
Delivery only (no online payment). About 10 sample books are available for demo."

## Clarifications

### Session 2026-11-21

- Q: How do customers find books by author? → A: Both. Customers can pick an author from a filter and
  can type an author name into a search.
- Q: Can a book have more than one author? → A: No. Each book has exactly one author value.
- Q: Which book details are required? → A: All five (author, ISBN, publisher, number of pages, language)
  are required before a book can be shown in the store.
- Q: What rules apply to the ISBN? → A: It must be unique across books. Its format is not checked.
- Q: How is the language entered? → A: As free text.
- Q: What are the demo sample books? → A: Public-domain classics, each with a price and available stock.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - View book details (Priority: P1)

A customer browses the online store and opens a book. The book page shows the book's author, ISBN,
publisher, number of pages, and language next to the usual product information.

**Why this priority**: Book details are what make this a bookstore rather than a generic shop. Every
other story depends on books and their details existing.

**Independent Test**: Publish one book with all five details and open its page as a customer. The page
shows all five values.

**Acceptance Scenarios**:

1. **Given** a published book with all five details filled, **When** a customer opens the book page,
   **Then** the page shows the author, ISBN, publisher, number of pages, and language.
2. **Given** a catalog manager is adding a book, **When** any of the five details is missing,
   **Then** the book cannot be published in the store, and the manager is told which details are missing.
3. **Given** a book with ISBN "X" already exists, **When** a catalog manager saves another book with
   ISBN "X", **Then** the save is rejected with a message saying the ISBN is already in use.

---

### User Story 2 - Find books by author (Priority: P2)

A customer wants books by a specific author. They either pick the author from an author filter on the
catalog, or type the author's name into a search, and see only that author's books.

**Why this priority**: Author is the main way readers look for books. It needs the details from Story 1.

**Independent Test**: With books by at least two authors published, choose one author in the filter,
then search that author's name. Both show only that author's books.

**Acceptance Scenarios**:

1. **Given** published books by authors A and B, **When** a customer picks author A in the author filter,
   **Then** only author A's books are listed.
2. **Given** published books by authors A and B, **When** a customer searches for author A's name,
   **Then** author A's books are listed and author B's books are not.
3. **Given** no published book matches the searched author name, **When** the customer searches,
   **Then** the store shows a clear "no books found" message instead of an empty page.
4. **Given** the author filter, **When** a customer opens it, **Then** it lists only authors who have at
   least one published book.

---

### User Story 3 - Order a book with Cash on Delivery (Priority: P3)

A customer adds a book to the cart and places an order with the store's standard checkout. Cash on
Delivery is the only payment method offered.

**Why this priority**: It completes the shopping journey, but it reuses the store's existing cart and
checkout rather than adding a new flow.

**Independent Test**: Add an in-stock book to the cart, check out, and confirm the order is created with
Cash on Delivery as its payment method and no online payment step.

**Acceptance Scenarios**:

1. **Given** an in-stock book, **When** a customer adds it to the cart and checks out,
   **Then** an order is created and the customer sees an order confirmation.
2. **Given** a customer at checkout, **When** payment options are shown,
   **Then** Cash on Delivery is the only option, and no online payment is requested.

---

### User Story 4 - Demo catalog ready to show (Priority: P4)

The store owner sets up a demo store and gets about 10 sample books, so the catalog, author
filter, and checkout can be shown at once.

**Why this priority**: It supports demos and testing, but customers can use the store without it.

**Independent Test**: Set up a fresh demo store, load the sample books, and browse. All sample books are
visible with complete details, a price, and stock.

**Acceptance Scenarios**:

1. **Given** a fresh demo store, **When** the sample books are loaded,
   **Then** about 10 books appear in the catalog, each with all five details, a price, and available stock.
2. **Given** the sample books are loaded, **When** a customer opens the author filter,
   **Then** it lists the authors of the sample books.
3. **Given** the sample books, **When** their titles and authors are reviewed,
   **Then** each one is a public-domain work.

---

### User Story 5 - Store display name (Priority: P5)

The store shows the display name "Frappe Books". This name is a placeholder that the store owner can
change without changing code.

**Why this priority**: The name is visible branding, but it is a placeholder and does not block other stories.

**Independent Test**: Open the storefront and see "Frappe Books". Change the name in settings, reload,
and see the new name.

**Acceptance Scenarios**:

1. **Given** a newly set up store, **When** a customer opens the storefront,
   **Then** the store name shown is "Frappe Books".
2. **Given** the store owner changes the display name in settings, **When** a customer reloads the
   storefront, **Then** the new name is shown.

---

### Edge Cases

- A customer searches for an author name that matches no published book: a "no books found" message is shown.
- A catalog manager enters an ISBN already used by another book: the save is rejected.
- A book is missing one of the five details: it cannot be published.
- A book is out of stock: it follows the store's standard out-of-stock behavior.
- Two books have the same author written differently (for example, with different spacing or spelling):
  they are treated as different authors, because author and language are free text and only exact
  values are grouped.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST record these details for each book: author, ISBN, publisher, number of
  pages, and language.
- **FR-002**: Each book MUST have exactly one author value.
- **FR-003**: The system MUST NOT publish a book in the store unless all five details are filled.
- **FR-004**: ISBN MUST be unique across all books. Its format MUST NOT be validated.
- **FR-005**: Author, publisher, and language MUST be free text. Number of pages MUST be a positive whole number.
- **FR-006**: The book page MUST show all five details to customers.
- **FR-007**: Customers MUST be able to filter the catalog by choosing one author from a list of authors
  who have at least one published book.
- **FR-008**: Customers MUST be able to search books by author name.
- **FR-009**: When a filter or search returns no books, the store MUST show a "no books found" message.
- **FR-010**: Cart and ordering MUST use the store's existing standard cart and checkout flow.
- **FR-011**: Cash on Delivery MUST be the only payment method. No online payment MUST be offered or processed.
- **FR-012**: The store MUST show the display name "Frappe Books" by default. The store owner MUST be able
  to change it without code changes.
- **FR-013**: The system MUST provide about 10 sample books for demos. Each is a public-domain classic
  with all five details, a price, and available stock.
- **FR-014**: Sample book data MUST NOT include cover images unless they are freely licensed.

### Key Entities

- **Book**: A product sold in the store. It has the existing product information (such as name, price,
  and stock) plus author, ISBN, publisher, number of pages, and language. ISBN is unique.
- **Author**: The single author value of a book. The author filter is built from the distinct author
  values of published books.
- **Order**: A customer order created by the standard checkout. Its payment method is always Cash on Delivery.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of published books show all five details on their book page.
- **SC-002**: Filtering or searching by an author returns 100% of that author's published books and 0
  books by other authors.
- **SC-003**: A customer can go from the catalog to a list of one author's books in 3 actions or fewer.
- **SC-004**: A customer can go from a book page to an order confirmation in under 3 minutes.
- **SC-005**: 0 online payment options are shown at checkout, and 100% of orders use Cash on Delivery.
- **SC-006**: After the sample books are loaded, the catalog shows about 10 books, each with complete
  details, a price, and stock, and a full Cash on Delivery order can be demonstrated end to end.
- **SC-007**: 100% of attempts to save a duplicate ISBN or publish a book with missing details are rejected.

## Assumptions

- The store's existing product catalog, storefront, cart, and checkout are reused. This feature adds book
  details, author filtering and search, payment restriction, the display name, and sample data.
- Customer accounts and login follow the store's standard behavior. This feature does not change them.
- Delivery, shipping charges, and taxes follow the store's standard configuration. No Cash on Delivery
  fee is added.
- Author search matches whole or partial author names, ignoring letter case.
- Out-of-stock books follow the store's standard behavior.
- The display name "Frappe Books" is a placeholder and may change later.

## Out of Scope

- Real online payment gateway integration (Constitution Principle V).
- Multiple authors per book.
- ISBN format validation.
- Filtering by publisher, language, or other details.
