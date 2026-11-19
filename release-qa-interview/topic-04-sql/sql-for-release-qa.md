# SQL for Release QA

A practical SQL guide for a junior-to-mid release QA interview. It assumes no
prior SQL and uses one running example: the flashcards application from the AI
study guide, where a student saves decks of cards, studies them, and records
reviews.

**Dialects.** SQL Server (T-SQL) is the primary track because many release QA
teams test Microsoft applications. SQL Server examples come first and are
labeled `**SQL Server:**`; when standard SQL differs, the portable form comes
second and is labeled `**Standard SQL:**`. A statement shown under one label is
not a promise that the other dialect, or a third database, accepts it.

**No execution.** No database is installed in this repository, and no example
was executed. The statements are written for current SQL Server and compared
with standard SQL; check Microsoft Learn and your team's server version before
running anything against real data.

The examples use four tables with fixed sample rows — `users`, `decks`,
`cards`, and `reviews` — and the guide, the Q&A, and the MCQs all use the same
rows.

## Contents

- [Part 1 — Relational Basics](#part-1--relational-basics)
- [Part 2 — Reading Data with SELECT](#part-2--reading-data-with-select)
- [Part 3 — Filtering and NULL](#part-3--filtering-and-null)
- [Part 4 — Aggregating and Grouping](#part-4--aggregating-and-grouping)
- [Part 5 — Joins and UNION](#part-5--joins-and-union)
- [Part 6 — Subqueries and Simple CTEs](#part-6--subqueries-and-simple-ctes)
- [Part 7 — Changing Data and Transactions](#part-7--changing-data-and-transactions)
- [Part 8 — Schema, Constraints, Indexes, and Views](#part-8--schema-constraints-indexes-and-views)
- [Part 9 — Window Functions](#part-9--window-functions)
- [Part 10 — SQL Server Dialect and Tuning](#part-10--sql-server-dialect-and-tuning)
- [Part 11 — Release QA Query Patterns](#part-11--release-qa-query-patterns)

## Part 1 — Relational Basics

Everything else in this guide builds on four ideas: a table is a set of rows
with the same columns, a key identifies a row, a foreign key points at a row in
another table, and `NULL` means "no value" rather than zero or empty text.

### Tables, Rows, and Columns

A relational database stores data in tables. A table has a fixed list of
columns, and each column has a name and a data type. A row supplies a value, or
`NULL`, for every column.

- A **table** is a named relation: one kind of thing, such as `users` or
  `cards`.
- A **row** is one record: one user, one card.
- A **column** is one attribute: `email`, `front`, `rating`.

The column list is fixed by the schema; the row set is not. Adding a user adds
a row, not a column. That sounds obvious, but it explains most schema mistakes:
a design that needs a new column for each new value, such as `deck_1`,
`deck_2`, and so on, usually needs a second table instead.

A query returns a result set, which is also table-shaped: columns and rows.
Part 2 shows how to produce one.

### Keys

A **primary key** is a column, or a combination of columns, that uniquely
identifies each row. The database enforces two rules: no two rows may share the
key value, and the key may not be `NULL`. Each table in this schema has a
single-column primary key: `user_id`, `deck_id`, `card_id`, and `review_id`.

A **foreign key** is a column that refers to a primary key (or a unique key) in
another table. The database enforces that the referenced row exists.
`decks.user_id` may only contain a value that appears in `users.user_id`, so a
deck cannot belong to a user who does not exist.

| Key | Table | Column(s) | References | What it guarantees |
|---|---|---|---|---|
| Primary key | `users` | `user_id` | — | One row per user |
| Primary key | `decks` | `deck_id` | — | One row per deck |
| Primary key | `cards` | `card_id` | — | One row per card |
| Primary key | `reviews` | `review_id` | — | One row per review |
| Foreign key `fk_decks_user` | `decks` | `user_id` | `users(user_id)` | Every deck names an existing user |
| Foreign key `fk_cards_deck` | `cards` | `deck_id` | `decks(deck_id)` | Every card belongs to an existing deck |
| Foreign key `fk_reviews_card` | `reviews` | `card_id` | `cards(card_id)` | Every review names an existing card |
| Foreign key `fk_reviews_user` | `reviews` | `user_id` | `users(user_id)` | Every review names an existing user |
| Check constraint `ck_reviews_rating` | `reviews` | `rating` | — | A non-null rating is between 1 and 5 |

A **unique key** is a column, or a combination of columns, whose values must
not repeat. This schema has no separate unique key, so every non-key column may
repeat. That is deliberate: users 1 and 4 share the display name Alice, and
decks 101 and 103 share the title Biology 101. Part 11 shows how a
duplicate-email check works when an import adds data that the schema does not
yet constrain.

A foreign key is not a uniqueness rule: many decks may point at user 1. It is
also not an index. SQL Server does not automatically create an index on a
foreign-key column, so a join or a delete that checks child rows can still be
slow. Part 10 returns to that point.

### NULL and Data Types

`NULL` marks a missing or unknown value. It is not `0`, not an empty string,
and not equal to itself: `NULL = NULL` evaluates to UNKNOWN, and `WHERE` keeps
only rows whose condition is TRUE. That is why this guide uses `IS NULL`,
never `= NULL`. Part 3 covers the full three-valued logic.

Two columns in this schema are nullable:

- `users.display_name` — a user may not have supplied a name.
- `reviews.rating` — a review may have been recorded without a rating.

Everything else is `NOT NULL`. The check constraint `ck_reviews_rating` permits
a `NULL` rating because its condition is UNKNOWN for that row, and SQL Server
accepts a row whose CHECK condition is TRUE or UNKNOWN. Part 11 discusses why
"allowed by the schema" is not the same as "allowed by the product".

The two DDL blocks in the next section use different types for the same idea:

| What it stores | SQL Server | Standard SQL | Note |
|---|---|---|---|
| Whole number | `INT` | `INTEGER` | Identifiers and counts |
| Short text | `NVARCHAR(n)` | `VARCHAR(n)` | `NVARCHAR` stores Unicode text |
| Longer text | `NVARCHAR(500)` | `VARCHAR(500)` | Maximum length in characters |
| Date and time | `DATETIME2` | `TIMESTAMP` | See the warning below |
| Boolean | `BIT` | `BOOLEAN` | `BIT` stores `0` or `1` |

**Watch the name `TIMESTAMP`.** In standard SQL, `TIMESTAMP` is a date and
time. In SQL Server, `TIMESTAMP` is a synonym for `ROWVERSION`: an
automatically generated binary value used for change tracking, not a date at
all. This schema uses `DATETIME2` on SQL Server and `TIMESTAMP` in the standard
version. If you see `TIMESTAMP` on a SQL Server column, do not read it as a
date.

Text types matter too. `NVARCHAR` stores Unicode, so it handles names and
characters outside the server's default code page. A length such as
`NVARCHAR(255)` is a maximum, not a promise that the value fills it.

### The Flashcards Schema

The application has four tables. A user owns decks, a deck contains cards, and
a user reviews cards. `reviews` connects users and cards, with a rating and a
timestamp.

**SQL Server:**

```sql
CREATE TABLE users (
    user_id      INT PRIMARY KEY,
    email        NVARCHAR(255) NOT NULL,
    display_name NVARCHAR(100),
    created_at   DATETIME2 NOT NULL
);

CREATE TABLE decks (
    deck_id    INT PRIMARY KEY,
    user_id    INT NOT NULL,
    title      NVARCHAR(200) NOT NULL,
    is_public  BIT NOT NULL,
    created_at DATETIME2 NOT NULL,
    CONSTRAINT fk_decks_user FOREIGN KEY (user_id) REFERENCES users (user_id)
);

CREATE TABLE cards (
    card_id    INT PRIMARY KEY,
    deck_id    INT NOT NULL,
    front      NVARCHAR(500) NOT NULL,
    back       NVARCHAR(500) NOT NULL,
    created_at DATETIME2 NOT NULL,
    CONSTRAINT fk_cards_deck FOREIGN KEY (deck_id) REFERENCES decks (deck_id)
);

CREATE TABLE reviews (
    review_id   INT PRIMARY KEY,
    card_id     INT NOT NULL,
    user_id     INT NOT NULL,
    rating      INT,
    reviewed_at DATETIME2 NOT NULL,
    CONSTRAINT fk_reviews_card FOREIGN KEY (card_id) REFERENCES cards (card_id),
    CONSTRAINT fk_reviews_user FOREIGN KEY (user_id) REFERENCES users (user_id),
    CONSTRAINT ck_reviews_rating CHECK (rating BETWEEN 1 AND 5)
);
```

**Standard SQL:**

```sql
CREATE TABLE users (
    user_id      INTEGER PRIMARY KEY,
    email        VARCHAR(255) NOT NULL,
    display_name VARCHAR(100),
    created_at   TIMESTAMP NOT NULL
);

CREATE TABLE decks (
    deck_id    INTEGER PRIMARY KEY,
    user_id    INTEGER NOT NULL,
    title      VARCHAR(200) NOT NULL,
    is_public  BOOLEAN NOT NULL,
    created_at TIMESTAMP NOT NULL,
    CONSTRAINT fk_decks_user FOREIGN KEY (user_id) REFERENCES users (user_id)
);

CREATE TABLE cards (
    card_id    INTEGER PRIMARY KEY,
    deck_id    INTEGER NOT NULL,
    front      VARCHAR(500) NOT NULL,
    back       VARCHAR(500) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    CONSTRAINT fk_cards_deck FOREIGN KEY (deck_id) REFERENCES decks (deck_id)
);

CREATE TABLE reviews (
    review_id   INTEGER PRIMARY KEY,
    card_id     INTEGER NOT NULL,
    user_id     INTEGER NOT NULL,
    rating      INTEGER,
    reviewed_at TIMESTAMP NOT NULL,
    CONSTRAINT fk_reviews_card FOREIGN KEY (card_id) REFERENCES cards (card_id),
    CONSTRAINT fk_reviews_user FOREIGN KEY (user_id) REFERENCES users (user_id),
    CONSTRAINT ck_reviews_rating CHECK (rating BETWEEN 1 AND 5)
);
```

**Sample rows.** The tables hold these fixed rows, and the Q&A and MCQ banks
use the same values.

| Table | Rows | What is in it |
|---|---:|---|
| `users` | 5 | 1 Alice, 2 Bob, 3 Carol with no display name, 4 Dave whose display name is also Alice, 5 Erin |
| `decks` | 4 | 101 Biology 101 (user 1, `TRUE`), 102 Spanish Verbs (user 1, `FALSE`), 103 Biology 101 (user 2, `TRUE`), 104 Empty Deck (user 3, `FALSE`) |
| `cards` | 5 | 1001 and 1002 in deck 101; 1003 in deck 102; 1004 and 1005 in deck 103 |
| `reviews` | 7 | 10001 and 10002 on card 1001; 10003 and 10006 on card 1002; 10004 on card 1003; 10005 and 10007 on card 1004; ratings 10003 and 10007 are `NULL` |

The sample data is chosen to make boundary cases visible:

- user 5 owns no decks;
- deck 104 contains no cards;
- card 1005 has no reviews;
- user 3 has a `NULL` display name;
- users 1 and 4 share the display name Alice;
- the title Biology 101 appears on decks 101 and 103, owned by different users;
- reviews 10003 and 10007 have `NULL` ratings.

**One-to-many relationships.** Each user owns zero or more decks, but each deck
belongs to exactly one user. That is a one-to-many relationship: one parent
row, many child rows. The foreign key sits on the many side, in `decks.user_id`,
and points at the primary key `users.user_id` on the one side. If the schema
instead stored a list of deck IDs inside a user row, the list would repeat, be
hard to search, and could not be checked by a foreign key. The one-to-many
shape keeps one fact in one place.

The same pattern repeats down the schema:

- `decks.user_id` → `users.user_id`: one user, many decks.
- `cards.deck_id` → `decks.deck_id`: one deck, many cards.
- `reviews.card_id` → `cards.card_id`: one card, many reviews.
- `reviews.user_id` → `users.user_id`: one user, many reviews.

`reviews` has two foreign keys because a review has two parents: the card being
reviewed and the user writing the review. Counts show the many side: user 1
owns two decks, user 5 owns none, deck 101 has two cards, deck 104 has none,
card 1001 has two reviews, and card 1005 has none. When Part 5 joins `cards` to
`reviews`, the result has seven rows even though there are only five cards,
because cards 1001, 1002, and 1004 each have two reviews. That row
multiplication is the single most common counting bug in release checks.

### Release QA Use

- Read the schema before you write a check. The primary keys tell you what
  identifies one row; the foreign keys tell you which orphan rows an import
  could create; the `NOT NULL` columns tell you what the product treats as
  required.
- Use the nullable columns to design explicit null checks. "No rows with a
  missing email" and "no rows with a missing display name" are different
  checks, because only the second column allows `NULL`.
- Compare column types before comparing values. Comparing an `INT` column to a
  quoted string can force an implicit conversion and change which rows match,
  or which index the server can use (Part 10).
- Treat the foreign keys as the relationships to verify after a migration:
  every deck has a user, every card has a deck, and every review has a card and
  a user.
- The simplest release baseline is one `COUNT(*)` per table. Part 4 shows the
  query; Part 11 shows what to do with the numbers.

### Watch-outs

- `NULL` is not zero and not an empty string. `NULL = NULL` is UNKNOWN; use
  `IS NULL` and `IS NOT NULL`.
- A foreign key prevents orphan rows, but it does not prevent duplicates. Two
  decks can share a title, and two users can share a display name.
- SQL Server does not automatically index foreign-key columns. A foreign key
  is a correctness rule, not a performance feature.
- `TIMESTAMP` is a SQL Server `ROWVERSION` value, not a date. Use `DATETIME2`
  for timestamps.
- The sample rows show `TRUE` and `FALSE` for readability. A SQL Server `BIT`
  value is written as `1` or `0`.
- A `NULL` rating can be legal in the schema and still be a product bug. Decide
  which rule you are testing before you report it.

## Part 2 — Reading Data with SELECT

`SELECT` asks for columns and `FROM` names the table. Everything else in this
part changes which columns appear, in what order, or how many rows come back.

### SELECT and FROM

The smallest useful query names the columns you want and the table they come
from.

**SQL Server:**

```sql
SELECT user_id, email, display_name
FROM users;
```

The same statement is standard SQL: `SELECT`, `FROM`, and the column list are
common to both dialects. The result has three columns and five rows, one per
user, in an order the server is free to choose because the query has no
`ORDER BY`.

A column list is also a contract. If a later release adds a `phone_number`
column to `users`, this query still returns three columns. A `SELECT *` query
would start returning four, which can break a test that compares column counts
or an export that expects a fixed shape.

**SQL Server:**

```sql
SELECT *
FROM decks;
```

`SELECT *` is convenient for a quick look in a test database. Keep it out of
checks that another person or another system reads, because the result changes
whenever the schema does. This statement is the same in standard SQL.

The written clause order is fixed: `SELECT` comes first and `FROM` follows. The
logical order in which the server processes a query is different: `FROM` finds
the rows, `WHERE` filters them, `GROUP BY` groups them, `HAVING` filters the
groups, `SELECT` computes the output columns, and `ORDER BY` sorts the result.
That order explains a rule you meet in Part 3: a column alias created in
`SELECT` cannot be used in `WHERE`, because `WHERE` runs before the alias
exists.

### Aliases and Expressions

An **alias** renames a column in the result. Use `AS` to make the intent
explicit, especially when the column is an expression; without an alias, many
clients show a server-generated name that changes between dialects or versions.

**SQL Server:**

```sql
SELECT card_id,
       front,
       LEN(front) AS front_length
FROM cards;
```

**Standard SQL:**

```sql
SELECT card_id,
       front,
       CHAR_LENGTH(front) AS front_length
FROM cards;
```

`LEN` and `CHAR_LENGTH` both count characters in the text column, but they
differ on trailing spaces: SQL Server `LEN` ignores trailing spaces, while
standard `CHAR_LENGTH` counts them. When a length check must match a
specification, decide which behavior the specification means.

Expressions can also do arithmetic. This statement is the same in SQL Server
and standard SQL, so it is labeled once:

**SQL Server:**

```sql
SELECT review_id,
       rating,
       rating * 2 AS doubled_rating
FROM reviews;
```

Because `rating` is nullable, reviews 10003 and 10007 return `NULL` for
`doubled_rating`: arithmetic with `NULL` produces `NULL`, not zero.

String concatenation differs by dialect. SQL Server uses `+` or the `CONCAT`
function; standard SQL uses `||`.

**SQL Server:**

```sql
SELECT user_id,
       CONCAT(display_name, ' <', email, '>') AS label
FROM users;
```

**Standard SQL:**

```sql
SELECT user_id,
       display_name || ' <' || email || '>' AS label
FROM users;
```

`CONCAT` treats a `NULL` argument as an empty string, so user 3 gets a label
with an empty name part. Standard `||` returns `NULL` if either operand is
`NULL`. SQL Server's `+` operator behaves like `||` for this purpose: a `NULL`
on either side makes the whole result `NULL`. That difference is a classic
"works for some rows, blank for others" bug, and Part 10 lists it in the
dialect table.

Do not write `WHERE doubled_rating > 5`; the alias does not exist yet when
`WHERE` is evaluated. Repeat the expression or wrap the query in a subquery,
which Part 6 covers.

### DISTINCT

`DISTINCT` removes duplicate rows from the result. It applies to the whole
selected row, not to the first column.

**SQL Server:**

```sql
SELECT DISTINCT display_name
FROM users;
```

This returns four rows, in no particular order: `NULL`, Alice, Bob, and Erin.
The two users named Alice collapse into one row, and the `NULL` value counts as
one distinct value. The same statement is standard SQL.

Add a second column and the result changes, because each pair is now compared:

**SQL Server:**

```sql
SELECT DISTINCT deck_id, title
FROM decks;
```

This returns all four decks. The title Biology 101 repeats, but the pairs
`(101, Biology 101)` and `(103, Biology 101)` are different, so `DISTINCT`
keeps both. "Deduplicate by title" and "deduplicate by title and deck" are
different queries, and adding a column to the select list can turn a
deduplicated result back into a full one.

`DISTINCT` hides duplicates rather than explaining them. When a release check
asks whether a value appears twice, use a grouped count (Part 4) instead;
`DISTINCT` answers with one row and tells you nothing about the count.

### ORDER BY

Without `ORDER BY`, a result set has no guaranteed order. The server may return
rows in any order, and it may use a different order for the same query after
statistics change, an index is added, or the plan changes. If order matters to
the check, say so in the query.

**SQL Server:**

```sql
SELECT card_id, deck_id, created_at
FROM cards
ORDER BY deck_id ASC, created_at DESC;
```

`ASC` is the default; `DESC` reverses the key. The query sorts by deck first
(101, 101, 102, 103, 103) and, within each deck, newest card first. Standard
SQL has the same `ORDER BY` shape.

Ordering by a nullable column exposes a dialect difference:

**SQL Server:**

```sql
SELECT user_id, display_name
FROM users
ORDER BY display_name, user_id;
```

SQL Server sorts `NULL` first in ascending order, so user 3 comes first, then
the two Alices ordered by `user_id`, then Bob and Erin. The SQL standard does
not require a particular position for `NULL` in `ORDER BY`; another database
may put nulls last. The `user_id` tiebreaker matters too: the two Alices tie on
`display_name`, and without a second key their relative order is not
guaranteed.

### Limiting Rows

SQL Server uses `TOP` to return the first n rows. `TOP` belongs in the
`SELECT` list.

**SQL Server:**

```sql
SELECT TOP (3) card_id, front
FROM cards
ORDER BY created_at DESC;
```

The query returns the three newest cards: 1005, 1004, and 1003. The other SQL
Server form is `OFFSET ... FETCH NEXT`, which skips rows and then takes a page;
SQL Server requires an `ORDER BY` for it.

**SQL Server:**

```sql
SELECT card_id, front
FROM cards
ORDER BY created_at ASC
OFFSET 2 ROWS FETCH NEXT 2 ROWS ONLY;
```

This skips the two oldest cards (1001 and 1002) and returns the next two (1003
and 1004).

Standard SQL has a shorter form:

**Standard SQL:**

```sql
SELECT card_id, front
FROM cards
ORDER BY created_at ASC
FETCH FIRST 2 ROWS ONLY;
```

This returns cards 1001 and 1002.

**All three forms need `ORDER BY` for a deterministic result.** `TOP` without
`ORDER BY` is not a stable selection: the server may return any n rows, and a
second run, a different plan, or a parallel scan can return a different set.
`OFFSET ... FETCH NEXT` requires `ORDER BY` in SQL Server. `FETCH FIRST` runs
without it, but the rows it picks are arbitrary, so add `ORDER BY` when the
result feeds a test. Even with `ORDER BY`, ties remain a risk: if two rows
share the last sort key, either can fall inside or outside the limit. Add a
unique tiebreaker, such as the primary key, when the sample must be
reproducible.

`TOP` is SQL Server syntax. Standard SQL uses `FETCH FIRST n ROWS ONLY`. The
`OFFSET ... FETCH NEXT` form is standard as well and is accepted by current
SQL Server versions, but the shortest SQL Server form is `TOP`, and the
shortest standard form in this guide is `FETCH FIRST`.

### Release QA Use

- Capture a reproducible sample for a bug report by ordering on a stable key
  and taking a fixed number of rows. "First 20 cards by `created_at`, then
  `card_id`" can be re-run; "first 20 cards" cannot.
- Check whether a value repeats by grouping and counting, not by adding
  `DISTINCT` and hoping the single row means "clean". Part 4 shows the grouped
  form.
- Give exported columns readable aliases so a tester reading a CSV or a test
  comparison can match the names the specification uses.
- Use `SELECT` with an explicit column list in checks that another system
  consumes; `SELECT *` turns a column addition into an unexpected schema
  change.
- Use `ORDER BY` plus a limit to inspect the newest reviews or the latest deck
  before checking a migration result.

### Watch-outs

- No `ORDER BY` means no guaranteed order. "It came back in insertion order
  last time" is not a rule.
- `TOP` without `ORDER BY` returns an arbitrary set of rows; it is not a stable
  selection. Ties also make `TOP` with `ORDER BY` non-deterministic unless you
  add a unique tiebreaker.
- `DISTINCT` applies to the whole row. Adding a column can stop duplicates
  from collapsing.
- A column alias belongs to the `SELECT` list and cannot be used in `WHERE`.
  Repeat the expression or use a subquery.
- Expressions propagate `NULL`: `rating * 2` is `NULL` when `rating` is
  `NULL`, and concatenation with `+` or `||` returns `NULL` when either side is
  `NULL`. SQL Server `CONCAT` is the exception that treats `NULL` as an empty
  string.
- `LEN` in SQL Server ignores trailing spaces; standard `CHAR_LENGTH` counts
  them. A length check must say which one it means.
- `FETCH FIRST` without `ORDER BY` is allowed by some databases but still
  arbitrary. Do not treat "it returned two rows" as a deterministic result.
