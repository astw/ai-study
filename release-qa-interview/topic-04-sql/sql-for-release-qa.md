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

## Part 3 — Filtering and NULL

`WHERE` decides which rows a query keeps. It runs once per row, keeps the row
only when the condition is TRUE, and runs before any grouping. That last point
is why filters on individual rows belong in `WHERE` while filters on totals
belong in `HAVING` (Part 4).

### WHERE

The simplest filter compares one column to one literal.

**SQL Server:**

```sql
SELECT card_id, deck_id, front
FROM cards
WHERE deck_id = 101;
```

This returns cards 1001 and 1002, the two rows whose `deck_id` is 101. The
statement is standard SQL as well.

The comparison operators are `=`, `<>`, `!=`, `<`, `<=`, `>`, and `>=`.
Standard SQL uses `<>` for "not equal"; SQL Server accepts both `<>` and
`!=`. Numbers are written bare and text is single-quoted.

**SQL Server:**

```sql
SELECT review_id, rating, reviewed_at
FROM reviews
WHERE rating > 3;
```

This returns reviews 10001 (5), 10002 (4), and 10005 (5). Reviews 10003 and
10007 have a `NULL` rating; the comparison is UNKNOWN for them, and `WHERE`
drops UNKNOWN rows. The rules behind that behavior appear in "NULL and
Three-Valued Logic" below.

The date form of the filter is the same in both dialects, but the literal
syntax differs:

**SQL Server:**

```sql
SELECT review_id, reviewed_at
FROM reviews
WHERE reviewed_at >= '2026-01-22';
```

**Standard SQL:**

```sql
SELECT review_id, reviewed_at
FROM reviews
WHERE reviewed_at >= TIMESTAMP '2026-01-22 00:00:00';
```

Both return the five reviews recorded on or after 2026-01-22, from 10003 to
10007. SQL Server converts the quoted string to a date/time value when it
compares it to a `DATETIME2` column; standard SQL has a typed timestamp
literal.

`WHERE` runs before the `SELECT` list is computed, so it cannot see a column
alias from `SELECT` (Part 2). Repeat the expression when the filter needs it.

### AND, OR, and NOT

`NOT` binds tighter than `AND`, and `AND` binds tighter than `OR`. The
precedence is fixed by the language, not by the order in which you typed the
clauses. Parentheses are how you state the grouping you mean.

The wrong version:

**SQL Server:**

```sql
SELECT review_id, card_id, rating
FROM reviews
WHERE card_id = 1001 OR card_id = 1002 AND rating = 5;
```

`AND` is evaluated first, so this means "card 1001, or card 1002 with rating
5". It returns reviews 10001 (5) and 10002 (4): the rating-4 review survives
because the first branch never mentions `rating`.

The corrected version adds parentheses:

**SQL Server:**

```sql
SELECT review_id, card_id, rating
FROM reviews
WHERE (card_id = 1001 OR card_id = 1002)
  AND rating = 5;
```

This returns review 10001 only. The same query is standard SQL.

`NOT` inverts a condition, but it follows the three-valued rules in the
`NULL` and Three-Valued Logic section below: `NOT UNKNOWN` is UNKNOWN, so a
negated predicate still drops rows whose column is `NULL`.

**SQL Server:**

```sql
SELECT review_id, rating
FROM reviews
WHERE rating <> 5;
```

This returns reviews 10002 (4), 10004 (3), and 10006 (2). It does not return
reviews 10003 and 10007, whose rating is `NULL`, even though they are "not
5". To include them, say so explicitly:

**SQL Server:**

```sql
SELECT review_id, rating
FROM reviews
WHERE rating <> 5
   OR rating IS NULL;
```

This returns five rows. Whether the unknown rows belong in the answer is a
product question; the query should state its choice either way.

### IN, BETWEEN, and LIKE

`IN` tests a column against a list and is shorthand for a chain of `OR`
equalities.

**SQL Server:**

```sql
SELECT review_id, card_id, user_id, rating
FROM reviews
WHERE card_id IN (1001, 1004);
```

This returns reviews 10001, 10002, 10005, and 10007. The statement is
standard SQL. `IN` uses the same equality rules as `=`, so the `NULL` trap in
"The NOT IN Trap" applies to its negated form.

`BETWEEN` tests an inclusive range: `rating BETWEEN 2 AND 4` means
`rating >= 2 AND rating <= 4`.

**SQL Server:**

```sql
SELECT review_id, rating
FROM reviews
WHERE rating BETWEEN 2 AND 4;
```

This returns reviews 10002 (4), 10004 (3), and 10006 (2): both endpoints are
included, and the two `NULL` ratings are excluded. The statement is standard
SQL.

An inclusive upper bound of a bare date is a trap for date and time columns:
`BETWEEN '2026-01-20' AND '2026-01-25'` stops at midnight at the start of
January 25, so it loses anything recorded later that day. Write the window as
a half-open range instead. This one covers January 20 through January 24:

**SQL Server:**

```sql
SELECT review_id, reviewed_at
FROM reviews
WHERE reviewed_at >= '2026-01-20'
  AND reviewed_at <  '2026-01-25';
```

This returns reviews 10001 through 10005. Review 10006, recorded at
2026-01-25 14:00:00, is outside the window because the upper bound is the
start of January 25. If the requirement were "through January 25", the upper
bound would be `< '2026-01-26'`, whereas `BETWEEN ... AND '2026-01-25'` would
silently drop review 10006 because the bare date means midnight. The
half-open form makes the intended boundary explicit, and the standard form
uses `TIMESTAMP` literals but keeps the same comparison shape.

`LIKE` matches text against a pattern. `%` stands for any run of zero or more
characters, and `_` stands for exactly one character.

**SQL Server:**

```sql
SELECT card_id, front
FROM cards
WHERE front LIKE 'What is%';
```

Every card front starts with "What is", so this returns all five cards. The
statement is standard SQL.

**SQL Server:**

```sql
SELECT user_id, email
FROM users
WHERE email LIKE '____@example.com';
```

Each `_` matches one character, so this returns `dave@example.com` and
`erin@example.com`: the two addresses with four characters before the `@`.
A pattern that starts with `%` can match anywhere in the string, which is
useful for discovery and expensive on a large table (Part 10).

To match a literal `%` or `_`, declare an escape character with `ESCAPE`.
Whether matching is case-sensitive depends on the column's collation; SQL
Server's common default collations are case-insensitive, but a case-sensitive
database or column changes the result. SQL Server also supports bracket
patterns such as `[A-C]`; standard SQL does not, so keep those out of portable
checks.

### NULL and Three-Valued Logic

SQL conditions have three possible outcomes, not two: TRUE, FALSE, and
UNKNOWN. `WHERE` keeps a row only when its condition is TRUE, so both FALSE
and UNKNOWN remove the row. A comparison involving `NULL` is UNKNOWN, because
`NULL` means "no value" and the database cannot decide whether an absent
value equals anything.

| `A` | `B` | `A AND B` | `A OR B` |
|---|---|---|---|
| TRUE | TRUE | TRUE | TRUE |
| TRUE | FALSE | FALSE | TRUE |
| TRUE | UNKNOWN | UNKNOWN | TRUE |
| FALSE | FALSE | FALSE | FALSE |
| FALSE | UNKNOWN | FALSE | UNKNOWN |
| UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |

`NOT` follows the same rule: `NOT TRUE` is FALSE, `NOT FALSE` is TRUE, and
`NOT UNKNOWN` is UNKNOWN. The practical effect is that `NULL` behaves like a
third truth value that spreads through most expressions.

**SQL Server:**

```sql
SELECT user_id, display_name
FROM users
WHERE display_name = NULL;
```

This returns no rows, not even user 3. `= NULL` is UNKNOWN for every row,
because `NULL = NULL` is UNKNOWN as well. The test for a missing value is
`IS NULL`.

**SQL Server:**

```sql
SELECT user_id, display_name
FROM users
WHERE display_name IS NULL;
```

This returns user 3. `IS NOT NULL` is the opposite test:

**SQL Server:**

```sql
SELECT review_id, rating
FROM reviews
WHERE rating IS NOT NULL;
```

This returns the five reviews with a rating. `IS NULL` and `IS NOT NULL` are
predicates, not comparisons; they always return TRUE or FALSE, never UNKNOWN.
Both forms are standard SQL.

`COALESCE` returns its first argument that is not `NULL`, which turns an
absent value into a display value or a comparison value.

**SQL Server:**

```sql
SELECT user_id,
       COALESCE(display_name, '(no name)') AS label
FROM users;
```

User 3 gets `(no name)`; the other rows keep their names. `COALESCE` is
standard SQL and accepts any number of arguments. SQL Server also has the
two-argument `ISNULL` function, which is not part of standard SQL.

`NULLIF(a, b)` returns `NULL` when `a` equals `b`, and `a` otherwise. Its most
common release-check use is guarding a division whose denominator can be
zero.

**SQL Server:**

```sql
SELECT CAST(SUM(rating) AS DECIMAL(10, 2))
       / NULLIF(COUNT(rating), 0) AS avg_rating
FROM reviews;
```

This returns the value 3.8. Without `NULLIF`, a query over a set with no rated
reviews would divide by zero and fail with an error; with it, the denominator
becomes `NULL` and the result is `NULL`. The version without the cast,
`SUM(rating) / NULLIF(COUNT(rating), 0)`, would do integer division and
return 3. Both `NULLIF` and the cast are standard SQL.

The three-valued rules are easy to forget in negative checks, which is the
subject of the next section.

### The NOT IN Trap

`NOT IN` compares a value against every item in a list. If the list contains
a `NULL`, no row passes.

**SQL Server:**

```sql
SELECT card_id
FROM cards
WHERE card_id NOT IN (1001, NULL);
```

This returns zero rows. `card_id NOT IN (1001, NULL)` expands to
`card_id <> 1001 AND card_id <> NULL`. For card 1002 the first part is TRUE
and the second is UNKNOWN, and `TRUE AND UNKNOWN` is UNKNOWN; for card 1001
the first part is FALSE. Neither result is TRUE, so `WHERE` keeps nothing.

The same trap appears when the list comes from a subquery over a nullable
column:

**SQL Server:**

```sql
SELECT review_id, rating
FROM reviews
WHERE rating NOT IN (
    SELECT rating
    FROM reviews
    WHERE user_id = 1
);
```

The subquery returns 5, NULL, and 3, with NULL repeated. The apparent
question is "which reviews have a rating that user 1 never gave?", whose
answer from the sample rows would be reviews 10002 (4) and 10006 (2). The
query returns zero rows, because the NULL in the list makes every comparison
UNKNOWN.

There are two reliable fixes. The first removes the NULLs from the list:

**SQL Server:**

```sql
SELECT review_id, rating
FROM reviews
WHERE rating NOT IN (
    SELECT rating
    FROM reviews
    WHERE user_id = 1
      AND rating IS NOT NULL
);
```

This returns reviews 10002 and 10006. The outer `NULL` ratings are still
excluded, because `NULL NOT IN (...)` is UNKNOWN; that matches the usual
reading of "a rating user 1 never gave", which implies a rating exists.

The second fix asks the question as existence rather than membership:

**SQL Server:**

```sql
SELECT r.review_id, r.rating
FROM reviews AS r
WHERE r.rating IS NOT NULL
  AND NOT EXISTS (
      SELECT 1
      FROM reviews AS u
      WHERE u.user_id = 1
        AND u.rating = r.rating
  );
```

This returns the same two reviews. `NOT EXISTS` is TRUE when the inner query
returns no row, and an inner comparison with `NULL` is UNKNOWN, which counts
as "no match" for the outer row rather than poisoning the result.
`NOT EXISTS` is the safer default for exclusion checks. The form is standard
SQL; Part 6 covers the mechanics of the subquery.

`NOT IN` is safe when the list is known to contain no `NULL`, such as a
literal list of IDs or a subquery over a `NOT NULL` column. When the list
comes from a nullable column or from a query you do not control, either add
`IS NOT NULL` to the subquery or switch to `NOT EXISTS`.

### Release QA Use

- Turn each acceptance criterion into a `WHERE` predicate and count the
  matching rows. A filter written from ticket wording ("not published", "not
  rated") often becomes a negation, and negations drop `NULL` rows. Check
  that explicitly.
- Use prefix `LIKE 'term%'` when the requirement is "starts with"; a leading
  `%` changes both the meaning and the cost of the check.
- Write date windows as half-open ranges (`>= start AND < next_day`) so a
  record at 23:59:59 on the last day is included and the boundary is
  unambiguous.
- Write exclusion checks with `NOT EXISTS` or with `NOT IN` over a NULL-free
  subquery. A zero-row result from `NOT IN` with a nullable list is a false
  "clean" result, not evidence that the data is clean.
- Sanity-check every filter against the sample rows. If `rating > 3` and
  `rating <= 3` together do not add up to `COUNT(*)`, the missing rows are
  the `NULL` ones.
- Use `COALESCE` for readable report labels and `NULLIF` for safe
  denominators; keep both out of `WHERE` predicates on large tables when an
  index should be used (Part 10).

### Watch-outs

- `AND` binds tighter than `OR`. Parenthesize any mixed condition; the server
  will not guess your intent.
- `NULL` is compared with `IS NULL` and `IS NOT NULL`, never with `=` or `<>`.
- Negating a comparison with `<>`, `NOT IN`, `NOT LIKE`, `NOT BETWEEN`, or
  `NOT (...)` drops `NULL` rows. Negation does not add them back.
- `NOT IN` with a `NULL` anywhere in the list returns no rows. Use
  `NOT EXISTS` or filter the inner column with `IS NOT NULL`.
- `BETWEEN` includes both endpoints. On a date/time column, an inclusive
  upper bound of a bare date excludes the rest of that day.
- `LIKE` treats `%` and `_` as wildcards. Escape them with `ESCAPE` when they
  are literal, and remember that case sensitivity comes from the collation.
- `COALESCE` and `NULLIF` are standard; SQL Server's `ISNULL` is not. The two
  names are easy to confuse with the predicate `IS NULL`.

## Part 4 — Aggregating and Grouping

An aggregate function collapses many rows into one value. A query with an
aggregate and no `GROUP BY` returns a single row for the whole table; a query
with `GROUP BY` returns one row per group. QA checks use this to count
records, total and average values, and compare distributions before and after
a release.

### Aggregate Functions

The aggregate functions in this guide are `COUNT`, `SUM`, `AVG`, `MIN`, and
`MAX`. All of them ignore `NULL` inputs apart from `COUNT(*)`, which counts
rows without looking at column values.

**SQL Server:**

```sql
SELECT COUNT(*)                            AS review_count,
       COUNT(rating)                       AS rated_count,
       SUM(rating)                         AS rating_sum,
       AVG(CAST(rating AS DECIMAL(10, 2))) AS rating_avg,
       MIN(rating)                         AS lowest_rating,
       MAX(rating)                         AS highest_rating
FROM reviews;
```

This returns one row: 7 reviews, 5 of them rated, a rating sum of 19, an
average of 3.8, a lowest rating of 2, and a highest rating of 5. The average
is 19 / 5, not 19 / 7: the two `NULL` ratings are left out of the sum and
the count, so the denominator is the number of rated reviews. The cast is
needed because SQL Server's `AVG` over an `INT` column returns an `INT` and
discards the fraction, so 19 / 5 is reported as 3.

The same query is standard SQL with the same `NULL` handling. The return type
for an integer column depends on the product and can be an integer, a decimal,
or a floating-point value, so an explicit cast is the portable way to get a
predictable fractional average.

`MIN` and `MAX` are not limited to numbers: they work on text and on dates.
`MIN(created_at)` and `MAX(created_at)` are a quick "first and last record"
check on any table.

A query with an aggregate and no `GROUP BY` treats the whole table as one
group, so it always returns exactly one row, even when the filter matches
nothing.

**SQL Server:**

```sql
SELECT COUNT(*)   AS review_count,
       SUM(rating) AS rating_sum,
       AVG(rating) AS rating_avg,
       MIN(rating) AS lowest,
       MAX(rating) AS highest
FROM reviews
WHERE 1 = 0;
```

This returns one row containing 0, `NULL`, `NULL`, `NULL`, and `NULL`.
`COUNT` returns 0, but the other aggregates return `NULL` because they have
no values to work on; `SUM` over an empty or all-`NULL` set is `NULL`, not 0.
A report that adds those columns without `COALESCE` shows a blank instead of
zero. The statement is standard SQL.

### COUNT(*) and COUNT(column)

The three count forms answer three different questions:

- `COUNT(*)` counts rows.
- `COUNT(column)` counts rows where that column is not `NULL`.
- `COUNT(DISTINCT column)` counts distinct, non-`NULL` values.

**SQL Server:**

```sql
SELECT COUNT(*)                AS review_count,
       COUNT(rating)           AS rated_count,
       COUNT(DISTINCT card_id) AS reviewed_cards
FROM reviews;
```

This returns 7, 5, and 4. Seven reviews exist, five carry a rating, and four
distinct cards (1001, 1002, 1003, and 1004) were reviewed. The `NULL` ratings
are not counted as a value.

The difference between a distinct row and a distinct count is another
release-check trap:

**SQL Server:**

```sql
SELECT COUNT(*)                     AS user_count,
       COUNT(display_name)          AS names_present,
       COUNT(DISTINCT display_name) AS distinct_names
FROM users;
```

This returns 5, 4, and 3. `SELECT DISTINCT display_name` (Part 2) returns four
rows including `NULL`, but `COUNT(DISTINCT display_name)` ignores `NULL` and
returns three. "How many different names appear in the result?" and "how many
distinct names are stored?" are different numbers.

`COUNT` never returns `NULL`: it returns 0 when there is nothing to count.
That makes it the safest aggregate for a baseline query.

The forms diverge sharply after a join, when one row on the one side matches
many rows on the many side. This query counts cards and reviews per deck:

**SQL Server:**

```sql
SELECT decks.deck_id,
       decks.title,
       COUNT(*)                          AS joined_rows,
       COUNT(DISTINCT cards.card_id)     AS reviewed_cards,
       COUNT(DISTINCT reviews.review_id) AS review_count
FROM decks
JOIN cards   ON cards.deck_id = decks.deck_id
JOIN reviews ON reviews.card_id = cards.card_id
GROUP BY decks.deck_id, decks.title
ORDER BY decks.deck_id;
```

| deck_id | title | joined_rows | reviewed_cards | review_count |
|---:|---|---:|---:|---:|
| 101 | Biology 101 | 4 | 2 | 4 |
| 102 | Spanish Verbs | 1 | 1 | 1 |
| 103 | Biology 101 | 2 | 1 | 2 |

Deck 101 has two cards, but the join produces four rows because those two
cards have four reviews between them. `COUNT(*)` reports 4, which is the
number of joined rows, not the number of cards.
`COUNT(DISTINCT cards.card_id)` reports 2, the number of cards that have at
least one review. `COUNT(DISTINCT reviews.review_id)` reports 4, the number
of reviews. Deck 104 does not appear because it has no cards, and card 1005
does not appear because it has no reviews; an inner join keeps only matches
(Part 5 shows the `LEFT JOIN` form that preserves them). The join syntax here
is a preview; the guidance that matters is that `COUNT(*)` after a
one-to-many join counts rows, not entities.

### GROUP BY

`GROUP BY` divides the rows into groups that share the same values in the
listed columns, then evaluates the aggregates once per group.

**SQL Server:**

```sql
SELECT deck_id, COUNT(*) AS card_count
FROM cards
GROUP BY deck_id;
```

This returns three rows: deck 101 with 2 cards, deck 102 with 1, and deck 103
with 2. Deck 104 does not appear, because `GROUP BY` groups the rows that
exist; it does not invent an empty group. A report that must list every deck
starts from `decks` and uses a `LEFT JOIN` (Part 5). The statement is standard
SQL.

Grouping by two columns makes one group per combination:

**SQL Server:**

```sql
SELECT user_id, rating, COUNT(*) AS review_count
FROM reviews
GROUP BY user_id, rating;
```

This returns six rows: user 1 with rating 5 (one review), user 1 with `NULL`
(two reviews), user 1 with rating 3 (one), user 2 with rating 4 (one), user 2
with rating 5 (one), and user 3 with rating 2 (one). `NULL` forms its own
group, so the two unrated reviews by user 1 count together. The group key is
the pair, not either column alone.

Every column in the `SELECT` list must either be inside an aggregate or
appear in `GROUP BY`. This statement is rejected by SQL Server and by
standard SQL:

```sql
SELECT deck_id, front, COUNT(*) AS card_count
FROM cards
GROUP BY deck_id;
```

`front` differs between cards in the same deck, so the database cannot return
one value for the group. Add the column to `GROUP BY`, as the
`GROUP BY user_id, rating` example above does with its second column, or
aggregate it.

### HAVING

`WHERE` filters rows before grouping; `HAVING` filters groups after
aggregation. An aggregate cannot appear in `WHERE`, because the groups do not
exist yet when `WHERE` runs.

**SQL Server:**

```sql
SELECT deck_id, COUNT(*) AS card_count
FROM cards
GROUP BY deck_id
HAVING COUNT(*) > 1;
```

This returns decks 101 and 103, the only decks with more than one card.
`HAVING COUNT(*) > 1` reads as "keep groups whose count exceeds one". The
statement is standard SQL.

The two filters can appear in the same query, and each runs at its own stage:

**SQL Server:**

```sql
SELECT user_id, COUNT(*) AS good_reviews
FROM reviews
WHERE rating >= 4
GROUP BY user_id
HAVING COUNT(*) > 1;
```

The `WHERE` clause removes rows before grouping, including the `NULL` ratings;
the remaining rows are user 1 with one review (rating 5) and user 2 with two
reviews (ratings 4 and 5). The `HAVING` clause then removes user 1, leaving
user 2. Moving the row condition to `HAVING` would make the query invalid,
because `rating` is neither grouped nor aggregated; row conditions belong in
`WHERE` and group conditions in `HAVING`.

A `SELECT` alias is not available in `HAVING`, just as it is not available in
`WHERE` or `GROUP BY`: repeat the aggregate there. `ORDER BY` is the only
clause that can use a select-list alias.

### Release QA Use

- Start with one `COUNT(*)` per table and compare it with the expected number
  for the environment. `COUNT` returns 0 rather than `NULL`, so a clean miss
  is visible.
- Count entities, not joined rows. After any one-to-many join, use
  `COUNT(DISTINCT key)` for the entity you mean, or the count inflates.
- Group by `email` with `HAVING COUNT(*) > 1` to find duplicate imports
  before a migration; Part 11 turns this into a reusable pattern.
- Compare rating averages across releases with the same `WHERE` clause and
  the same denominator. `AVG` ignores `NULL`, so a release that starts
  recording unrated reviews can change what the average means without
  changing the arithmetic.
- Check distributions with `GROUP BY`, such as public versus private decks
  through `is_public`, to confirm that a feature flag did not shift the mix.
  On SQL Server, `is_public` is `BIT`; group on the column, and read 1 and 0
  as TRUE and FALSE.
- Reconcile the parts against the whole: the sum of a `GROUP BY` count column
  should equal the table's `COUNT(*)` when no filter removes rows. If it does
  not, the query is losing groups, often through a join or a `NULL` filter.
- Treat an empty aggregate result as data. `SUM` returning `NULL` after a
  filter is a finding about the filter, not a rendering bug; decide whether
  the report should show 0 and use `COALESCE` if so.

### Watch-outs

- `COUNT(*)` counts rows, `COUNT(column)` counts non-`NULL` values, and
  `COUNT(DISTINCT column)` counts distinct non-`NULL` values. They answer
  three different questions.
- A one-to-many join multiplies rows before grouping. `COUNT(*)` after a join
  is the number of joined rows, not the number of parents or children.
- `SUM`, `AVG`, `MIN`, and `MAX` ignore `NULL` values in their input. `AVG`
  divides by the count of non-`NULL` values, which may not be the row count
  you expected.
- `SUM` over an empty or all-`NULL` set is `NULL`, not 0. Only `COUNT`
  returns 0.
- SQL Server's `AVG` over an `INT` column returns an `INT` and discards the
  fraction; cast to a decimal type when a fractional average matters.
- Every nonaggregated column in `SELECT` must appear in `GROUP BY`. The
  server rejects the query otherwise.
- `WHERE` filters rows and cannot contain an aggregate; `HAVING` filters
  groups and runs after `GROUP BY`. Put each condition in the clause that
  matches its stage.
- A select-list alias works in `ORDER BY` but not in `WHERE`, `GROUP BY`, or
  `HAVING`.
- Grouping on a nullable column puts `NULL` values into one group. Filter
  them out in `WHERE` if the report should not show an "unknown" bucket.
- `GROUP BY` only groups rows that exist. Empty parents and empty children
  disappear unless a `LEFT JOIN` keeps them (Part 5).

## Part 5 — Joins and UNION

Parts 2 to 4 read one table at a time, apart from the join preview in Part 4
that showed why `COUNT(*)` can inflate. This part makes joins the subject. A
**join** combines rows from two tables through a relationship the tables
share. `UNION` does something different: it stacks the rows of two result
sets on top of each other. The two operations answer different questions,
and mixing them up is a common source of wrong counts. Every example uses
the four flashcards tables and the fixed sample rows from Part 1, so each
stated result can be traced to specific rows.

Two terms first. In `FROM decks AS d INNER JOIN cards AS c`, `decks` is the
**left** side and `cards` is the **right** side. The `ON` clause states the
relationship: `ON c.deck_id = d.deck_id` matches a card to the deck whose
`deck_id` equals the card's `deck_id`. A row with no partner on the other
side is **unmatched**. Each join type is a rule about what happens to
unmatched rows.

Join keys follow the foreign keys from Part 1: `decks.user_id` to
`users.user_id`, `cards.deck_id` to `decks.deck_id`, `reviews.card_id` to
`cards.card_id`, and `reviews.user_id` to `users.user_id`. Join on those
pairs. Joining on `title` or `display_name` is tempting because the sample
rows repeat values, but text is not a key: users 1 and 4 share the display
name Alice, and decks 101 and 103 share the title Biology 101.

### INNER JOIN

**Definition.** `INNER JOIN` returns only rows that have a match on both
sides. An unmatched row from either table is dropped. `JOIN` on its own
means `INNER JOIN`.

**Syntax.** The second table follows the first table in `FROM`, and each
additional table gets its own `JOIN ... ON ...` clause. `ON` carries the key
comparison. In SQL Server, a join without `ON` is a syntax error; standard
SQL also allows `USING`, shown below.

**SQL Server:**

```sql
SELECT d.deck_id, d.title, c.card_id, c.front
FROM decks AS d
INNER JOIN cards AS c ON c.deck_id = d.deck_id
ORDER BY d.deck_id, c.card_id;
```

This is standard SQL as well: `INNER JOIN ... ON` is the portable form, and
the sample rows make the result easy to check by hand.

**Expected rows.** Five rows, one per card: 1001 and 1002 under deck 101,
1003 under deck 102, and 1004 and 1005 under deck 103. Deck 104 (Empty Deck)
has no cards, so it produces no row. The count equals `COUNT(*)` on `cards`
only because every card has a deck; the statement returns matched
combinations, not a fixed number of either table's rows.

**Release QA use.** Prove that records exist together: "every card in the
release belongs to a deck", "every review on the new screen names a card".
An inner join is also the right shape when a parent with no children is
irrelevant, such as a content report that lists only decks that actually
hold cards.

**Watch-out.** An inner join cannot prove that a child is missing. A deck
with no cards returns no row at all, so "no row" and "the deck was never
created" look the same. When the requirement is "every deck must appear",
use a left join and look for the `NULL`-extended row.

### LEFT JOIN

**Definition.** `LEFT JOIN` (also written `LEFT OUTER JOIN`) returns every
row from the left table. A left row with matches on the right produces one
row per match; a left row with no match produces one row with `NULL` in
every column of the right table.

**Syntax.** `FROM decks AS d LEFT JOIN cards AS c ON c.deck_id = d.deck_id`.
The table named in `FROM` is the preserved side. Standard SQL accepts both
`LEFT JOIN` and `LEFT OUTER JOIN`, and SQL Server accepts both spellings
too.

**SQL Server:**

```sql
SELECT d.deck_id, d.title, c.card_id, c.front
FROM decks AS d
LEFT JOIN cards AS c ON c.deck_id = d.deck_id
ORDER BY d.deck_id, c.card_id;
```

**Expected rows.** Six rows: the five matched rows from the inner join, plus
one row for deck 104 with `NULL` in `c.card_id`, `c.front`, and every other
`cards` column. Deck 104 is preserved, not dropped, but no card information
exists for it.

To find the empty deck, turn the left join into an **anti-join**: keep the
rows where the right side did not match.

**SQL Server:**

```sql
SELECT d.deck_id, d.title
FROM decks AS d
LEFT JOIN cards AS c ON c.deck_id = d.deck_id
WHERE c.card_id IS NULL
ORDER BY d.deck_id;
```

**Expected rows.** One row: deck 104, Empty Deck. `c.card_id` is the primary
key of `cards`, so a real card row can never have a `NULL` there; a `NULL`
in the result can only mean "no card matched this deck".

The null test must use a column that cannot be `NULL` in the right table.
The next query has the same shape but tests `r.rating`, which is nullable.

**SQL Server:**

```sql
SELECT u.user_id, r.review_id, r.rating
FROM users AS u
LEFT JOIN reviews AS r ON r.user_id = u.user_id
WHERE r.rating IS NULL
ORDER BY u.user_id, r.review_id;
```

**Expected rows.** Four rows: reviews 10003 and 10007, which belong to user
1 and carry no rating, plus one `NULL`-extended row each for users 4 and 5.
The result suggests that user 1 has no reviews, which is false. Testing
`r.review_id IS NULL` instead returns only users 4 and 5, the two users with
no reviews.

**SQL Server:**

```sql
SELECT u.user_id
FROM users AS u
LEFT JOIN reviews AS r ON r.user_id = u.user_id
WHERE r.review_id IS NULL
ORDER BY u.user_id;
```

**Release QA use.** Empty-state and coverage checks. "Every deck must be
listed in the deck picker" becomes a left join from the expected decks to
the actual cards, filtered with `IS NULL`; the result is the list of decks
with no cards. Deck 104 is the model: a legitimate empty deck appears as one
`NULL`-extended row, not as a missing deck. The same shape checks optional
relationships, such as cards that no one has reviewed.

**Watch-out.** Three rules. Test a `NOT NULL` key (`c.card_id`,
`r.review_id`), not a nullable value column. Keep the null test in `WHERE`,
not in `ON`: `ON c.card_id IS NULL` never matches, so the query returns
every deck instead of the empty one. And a `WHERE` condition on the
right-hand table after the join, such as `WHERE c.front LIKE 'What is D%'`,
removes the `NULL`-extended rows and turns the left join back into an inner
join.

### RIGHT JOIN

**Definition.** `RIGHT JOIN` (also written `RIGHT OUTER JOIN`) is the mirror
image of `LEFT JOIN`: every row from the right table is preserved, and a
right row with no match produces one row with `NULL` in every column of the
left table.

**Syntax.** `FROM reviews AS r RIGHT JOIN cards AS c ON c.card_id =
r.card_id`. The table named after `RIGHT JOIN` is the preserved side.
Standard SQL and SQL Server both accept `RIGHT JOIN` and
`RIGHT OUTER JOIN`.

**SQL Server:**

```sql
SELECT c.card_id, c.front, r.review_id, r.rating
FROM reviews AS r
RIGHT JOIN cards AS c ON c.card_id = r.card_id
ORDER BY c.card_id, r.review_id;
```

**Expected rows.** Eight rows. Cards 1001, 1002, and 1004 have two reviews
each, card 1003 has one, and card 1005 has none. Every review matches a
card, because the foreign key guarantees it, so all seven reviews appear;
card 1005 appears once with `NULL` in `r.review_id` and `r.rating`. The
result contains every review plus the unmatched card.

**Why it is often rewritten as a left join.** `A RIGHT JOIN B` returns
exactly the same rows as `B LEFT JOIN A`; the two statements differ only in
which table is written first. Rewriting makes the preserved table the first
one read.

```sql
SELECT c.card_id, c.front, r.review_id, r.rating
FROM cards AS c
LEFT JOIN reviews AS r ON r.card_id = c.card_id
ORDER BY c.card_id, r.review_id;
```

The result is the same eight rows. Teams standardize on left joins for three
reasons: the preserved table is visually first, a chain of `LEFT JOIN`s
reads in one direction, and mixing `LEFT` and `RIGHT` in one query makes the
reader hold two mental models at once.

**Release QA use.** Use the right join when an existing query already starts
from `reviews` and the cards must survive: `FROM reviews AS r RIGHT JOIN
cards AS c` keeps every card, including card 1005, and leaves the query's
first table in place. In practice, write it as the left join above; the
result is identical and the next reader does not have to reverse it.

**Watch-out.** `RIGHT JOIN` is not wrong, but it is easy to misread. The
preserved side is the right-hand one, so a `WHERE` predicate on the left
table removes the `NULL`-extended rows exactly as it would in a left join.
When a query mixes both directions, write down which table each join
preserves before you edit or extend it.

### FULL OUTER JOIN

**Definition.** `FULL OUTER JOIN` (also written `FULL JOIN`) preserves
unmatched rows from both sides. A match produces one row; an unmatched left
row appears once with `NULL`s in the right columns, and an unmatched right
row appears once with `NULL`s in the left columns.

**Syntax.** `FROM users AS u FULL OUTER JOIN decks AS d ON d.user_id =
u.user_id`. Both SQL Server and standard SQL accept `FULL OUTER JOIN`. Check
the target product before reusing the statement: it is standard, but not
every database implements it.

**SQL Server:**

```sql
SELECT u.user_id, u.display_name, d.deck_id, d.title
FROM users AS u
FULL OUTER JOIN decks AS d ON d.user_id = u.user_id
ORDER BY u.user_id, d.deck_id;
```

**Expected rows.** Six rows. Four are matches: user 1 with decks 101 and
102, user 2 with deck 103, and user 3 with deck 104. Two are unmatched
users: users 4 and 5 own no decks, so their `d.deck_id` and `d.title` are
`NULL`. No deck is unmatched, because the foreign key guarantees that every
deck names an existing user.

To find only the unmatched rows on either side, keep the full join and
filter for the `NULL`s.

**SQL Server:**

```sql
SELECT u.user_id AS user_side, d.deck_id AS deck_side
FROM users AS u
FULL OUTER JOIN decks AS d ON d.user_id = u.user_id
WHERE u.user_id IS NULL OR d.deck_id IS NULL
ORDER BY user_side, deck_side;
```

**Expected rows.** Two rows, users 4 and 5. No row has a `NULL` `user_side`,
because the sample has no deck without an owner. The query still guards both
directions, which is the point: compare two key sets when either side may
contain extras.

**Release QA use.** Compare key sets in both directions: a migration that
maps old users to new users, an import file checked against a table, or two
environments compared for missing rows. A left join answers "what is missing
on the right?" for one chosen side; a full outer join answers both questions
in one pass. In this schema it lists users who own nothing and decks that
have no owner, and the second list is empty only because the foreign key
holds. Part 11 applies the same shape to staging tables that have no
constraints.

**Watch-out.** A `WHERE` predicate on either table can collapse the outer
join. `WHERE d.deck_id = 104` keeps the matched row for deck 104 and drops
the `NULL`-extended users; `WHERE d.deck_id IS NULL` keeps only the users
with no deck. Test a non-null key on each side — `u.user_id IS NULL OR
d.deck_id IS NULL` — when both directions matter. On large tables, filter
each input before the join rather than after it, so the full join works on
the smallest possible row sets.

### SELF JOIN

**Definition.** A **self join** joins a table to itself. It is not a
separate keyword: you write an ordinary join, give the same table two
different aliases, and compare rows of that table with other rows of the
same table.

**Syntax.** `FROM cards AS a INNER JOIN cards AS b ON b.deck_id =
a.deck_id`. The aliases are required: without them, the second reference to
`cards` is ambiguous and the query fails.

**Example: two cards in the same deck.**

**SQL Server:**

```sql
SELECT a.deck_id,
       a.card_id AS card_a,
       b.card_id AS card_b
FROM cards AS a
INNER JOIN cards AS b ON b.deck_id = a.deck_id
                     AND b.card_id > a.card_id
ORDER BY a.deck_id, a.card_id, b.card_id;
```

The statement is standard SQL as well.

**Expected rows.** Two rows: `(101, 1001, 1002)` and `(103, 1004, 1005)`.
Deck 101 holds cards 1001 and 1002, and deck 103 holds 1004 and 1005; deck
102 holds only card 1003, so it produces no pair. The condition `b.card_id >
a.card_id` does two jobs: it stops a card from pairing with itself, and it
keeps each pair once instead of returning both `(1001, 1002)` and
`(1002, 1001)`. Without it, deck 101 alone would return four rows: two
self-pairs and both orderings.

**Example: two reviews on the same card.**

**SQL Server:**

```sql
SELECT a.card_id,
       a.review_id AS review_a,
       a.user_id   AS user_a,
       b.review_id AS review_b,
       b.user_id   AS user_b
FROM reviews AS a
INNER JOIN reviews AS b ON b.card_id = a.card_id
                       AND b.review_id > a.review_id
ORDER BY a.card_id, a.review_id;
```

**Expected rows.** Three rows: reviews 10001 and 10002 on card 1001,
reviews 10003 and 10006 on card 1002, and reviews 10005 and 10007 on card
1004. Card 1003 has one review and card 1005 has none, so neither produces a
pair. The `review_id` inequality plays the same role as the card inequality
above.

**Release QA use.** Find inconsistencies that only make sense as a pair: two
cards in the same deck with the same front (add `AND b.front = a.front`),
two reviews of the same card by the same user (add `AND a.user_id =
b.user_id`), or duplicate rows created by an import. The pair form returns
the evidence, both record IDs, which a grouped count cannot show.

**Watch-out.** A self join multiplies: a table with n rows can produce n²
combinations, and a deck with n cards produces n² rows before the inequality
and n(n - 1) / 2 pairs after it. Keep a strict inequality on the key so each
unordered pair appears once and no row pairs with itself, and always alias
both sides.

### Join Chains and ON vs USING

**A join chain** adds one table at a time, with each `ON` connecting the new
table to a table already in the query. The flashcards schema chains users →
decks → cards → reviews.

**SQL Server:**

```sql
SELECT u.user_id,
       u.display_name,
       d.deck_id,
       d.title,
       c.card_id,
       c.front,
       r.review_id,
       r.rating
FROM users AS u
INNER JOIN decks   AS d ON d.user_id = u.user_id
INNER JOIN cards   AS c ON c.deck_id = d.deck_id
INNER JOIN reviews AS r ON r.card_id = c.card_id
ORDER BY u.user_id, d.deck_id, c.card_id, r.review_id;
```

The statement is standard SQL as well.

**Expected rows.** The select list's `u.user_id` is the deck owner, reached
through `decks.user_id`, not the author stored in `reviews.user_id`: review
10006 sits in user 1's deck 101 but was written by user 3. Seven rows, one per
review: five for user 1 (deck 101 has cards 1001 and 1002 with four reviews
between them, and deck 102 has card 1003 with one) and two for user 2 (deck
103 has card 1004 with two reviews).
The chain drops every parent with no child anywhere below it: users 4 and 5
have no decks; user 3 owns deck 104, which has no cards; and card 1005 has
no reviews. The finest table, `reviews`, sets the row count.

The written order of inner joins does not change the result; the optimizer
is free to reorder them. The order does matter once an outer join is in the
chain. A `LEFT JOIN` followed by an `INNER JOIN` on the null-extended table
drops the preserved rows again. If the goal is "every deck, with its cards
and reviews when they exist", every later join must also be a `LEFT JOIN`,
and the final grain must be stated before the query is run.

An `ON` clause may carry more than the key. `ON c.deck_id = d.deck_id AND
c.front LIKE 'What is D%'` changes which rows count as a match. In an inner
join that is equivalent to putting the filter in `WHERE`; in an outer join
it is not, because rows that fail the extra condition become unmatched rows
instead of disappearing.

**ON versus USING.** `ON` names the key comparison. Standard SQL also offers
a shorthand, `USING`, for the case where both tables give the key the same
column name. This schema qualifies: `decks.deck_id` and `cards.deck_id`
share a name.

**SQL Server:**

```sql
SELECT d.deck_id, d.title, c.card_id
FROM decks AS d
INNER JOIN cards AS c ON c.deck_id = d.deck_id;
```

This returns five rows, one per card. The join column must be qualified as
`d.deck_id` or `c.deck_id`; an unqualified `deck_id` is ambiguous because
both tables have that column name.

**Standard SQL:**

```sql
SELECT deck_id, title, card_id
FROM decks AS d
INNER JOIN cards AS c USING (deck_id);
```

**SQL Server does not accept `USING`.** It is a syntax error there; T-SQL
joins use `ON`. The `USING` form is standard SQL only, and it changes the
output shape: the join column appears once, so `deck_id` is unambiguous
without a qualifier. The row count is the same five rows. `USING` also
requires the two key columns to have the same name; when they do not, only
`ON` works.

### Join Multiplication

A one-to-many join multiplies rows. `decks` to `cards` is one-to-many (deck
101 has two cards), and `cards` to `reviews` is one-to-many (card 1001 has
two reviews). Each join repeats the parent row once per matching child, so a
count taken after the join is a count of combinations.

Start with the deck-to-card join and ask for three counts.

**SQL Server:**

```sql
SELECT COUNT(*)                  AS joined_rows,
       COUNT(DISTINCT d.deck_id) AS decks,
       COUNT(DISTINCT c.card_id) AS cards
FROM decks AS d
INNER JOIN cards AS c ON c.deck_id = d.deck_id;
```

**Expected rows.** One row: 5, 3, and 5. There are five joined rows, three
decks that have at least one card, and five cards. Deck 101 contributes two
rows because it holds two cards, so `COUNT(*)` counts that deck twice.
`COUNT(DISTINCT d.deck_id)` recovers the number of decks, and
`COUNT(DISTINCT c.card_id)` counts the cards. A report that asked "how many
decks have content?" and used `COUNT(*)` would answer 5, which is wrong.

Add reviews and the multiplication compounds.

**SQL Server:**

```sql
SELECT d.deck_id,
       d.title,
       COUNT(*)                  AS joined_rows,
       COUNT(DISTINCT c.card_id) AS reviewed_cards
FROM decks AS d
INNER JOIN cards   AS c ON c.deck_id = d.deck_id
INNER JOIN reviews AS r ON r.card_id = c.card_id
GROUP BY d.deck_id, d.title
ORDER BY d.deck_id;
```

**Expected rows.** Three rows: deck 101 with 4 joined rows and 2 distinct
cards, deck 102 with 1 and 1, and deck 103 with 2 and 1. Deck 101 has two
cards but four joined rows, because its two cards carry four reviews. Deck
103 also has two cards, but only card 1004 has reviews, so
`COUNT(DISTINCT c.card_id)` reports 1 and means "cards with at least one
review", not "cards in the deck". Deck 104 is absent because the inner joins
require a card and a review.

`COUNT(DISTINCT key)` repairs a count. It does not repair a sum: on this
chain `SUM(r.rating)` counts each review once, but `SUM(c.card_id)` repeats a
card's id once per review, because the card row is duplicated. When one
query needs counts from more than one child table, pre-aggregate each child
to one row per parent, then join the summaries.

**SQL Server:**

```sql
SELECT d.deck_id,
       d.title,
       card_counts.card_count,
       review_counts.review_count
FROM decks AS d
LEFT JOIN (
    SELECT deck_id, COUNT(*) AS card_count
    FROM cards
    GROUP BY deck_id
) AS card_counts ON card_counts.deck_id = d.deck_id
LEFT JOIN (
    SELECT cards.deck_id, COUNT(*) AS review_count
    FROM cards
    INNER JOIN reviews ON reviews.card_id = cards.card_id
    GROUP BY cards.deck_id
) AS review_counts ON review_counts.deck_id = d.deck_id
ORDER BY d.deck_id;
```

**Expected rows.** Four rows: deck 101 with 2 cards and 4 reviews, deck 102
with 1 and 1, deck 103 with 2 and 2, and deck 104 with `NULL` and `NULL`.
Each subquery returns at most one row per deck, so the outer joins cannot
multiply. The `LEFT JOIN` keeps deck 104, which has no cards and no reviews;
an inner join would drop it. The subquery syntax is Part 6 material; the
point here is the shape: aggregate the many side first, then join once.

### UNION and UNION ALL

A join matches rows from two tables side by side. `UNION` combines result
sets top to bottom, stacking their rows into one result. Both branches must
return the same number of columns, with compatible types in each position,
and the columns line up by position rather than by name.

**SQL Server:**

```sql
SELECT user_id FROM decks
UNION
SELECT user_id FROM reviews
ORDER BY user_id;
```

**Expected rows.** Three rows: 1, 2, and 3. Those are the distinct user IDs
that appear in `decks` or in `reviews`; the repeated values inside each
table collapse into one. The `ORDER BY` applies to the combined result, not
to either branch. The statement is standard SQL as well.

`UNION ALL` keeps every row.

**SQL Server:**

```sql
SELECT user_id FROM decks
UNION ALL
SELECT user_id FROM reviews
ORDER BY user_id;
```

**Expected rows.** Eleven rows: four from `decks` (user IDs 1, 1, 2, and 3)
and seven from `reviews` (1, 2, 1, 1, 2, 3, and 1). Sorted, the result has
six 1s, three 2s, and two 3s. `UNION` answers "which distinct values
appear?"; `UNION ALL` answers "which rows came from each source?" and keeps
the duplicates that are often the evidence.

The rules that decide whether a `UNION` runs at all:

- **Same shape.** Each branch must select the same number of columns, and
  each column position must hold a compatible type. When the types differ,
  the server applies its conversion rules by position, so a number and a
  text value may convert, or may fail when a value does not parse. Do not
  rely on the conversion; select matching types.
- **Position, not name.** The result takes its column names from the first
  branch. If the second branch selects `card_id` where the first selects
  `deck_id`, both values stack under the name `deck_id`. The server checks
  type and count; it cannot check that the two names mean the same thing.
- **Duplicate removal.** `UNION` removes duplicate rows from the combined
  result, comparing the whole selected row. `NULL` counts as equal to
  `NULL` for this purpose, so two `NULL`s collapse into one. `UNION ALL`
  performs no comparison and returns every row from both branches.
- **Cost.** Duplicate removal requires the server to sort or hash the
  combined rows, so `UNION` costs more than `UNION ALL`; `UNION ALL` can
  stream both branches. Use `UNION` only when the question is about
  distinct values.
- **One `ORDER BY`.** A single `ORDER BY` at the end applies to the whole
  result. An individual branch cannot have its own final `ORDER BY` unless
  the branch is wrapped as a subquery.

### Release QA Use

- Choose the join by what must survive. Inner join when only matched pairs
  matter; left join when every parent must appear; full outer join when
  either side may contain extras. State the expected grain before writing
  the query: one row per card, per deck, or per review.
- Build coverage checks as anti-joins. Left join the expected set to the
  actual set and filter `IS NULL` on a non-null key from the right table.
  Deck 104 is the model: the correct check returns exactly that one deck,
  with `NULL` card columns. A zero-row inner join proves nothing about
  missing children.
- Count the entity, not the joined rows. After a one-to-many join,
  `COUNT(*)` counts combinations. Use `COUNT(DISTINCT key)` when one query
  must answer, or pre-aggregate each child to one row per parent and join
  the summaries. Deck 101, with two cards and four reviews, makes the
  difference visible in this sample.
- Walk the foreign keys when you chain. users → decks → cards → reviews
  returns seven rows for the seven reviews; more rows mean a key is not
  unique or a table was joined twice. Check the count against the finest
  table, not against the first one.
- Compare key sets with `FULL OUTER JOIN` and `IS NULL` on both sides.
  "Which users own no deck, and which decks have no owner?" is one query
  instead of two, and it does not assume which side is allowed to be empty.
- Use `UNION ALL` for reconciliation counts and `UNION` for distinct value
  lists. A count per source preserves duplicate evidence; collapsing
  duplicates first hides the import that created them.
- Verify both sides of every join key before trusting the result. A join
  between different types or different collations can convert values,
  ignore an index, or fail outright, and a plausible-looking row set does
  not prove the match rule was the intended one.

### Watch-outs

- `INNER JOIN` drops unmatched rows from both sides. A missing child is
  invisible, not `NULL`; use a left join and a null test to see it.
- A `LEFT JOIN` is only as good as its null test: use a `NOT NULL` key from
  the right table, keep the test in `WHERE`, and remember that filtering the
  right table in `WHERE` turns the outer join back into an inner join.
- `ON` controls matching and `WHERE` controls the result. In an inner join
  the two placements often agree; in an outer join they do not, because an
  `ON` condition can turn a row into an unmatched one instead of removing
  it.
- `RIGHT JOIN` is a left join with the tables swapped. Prefer the left form
  so the preserved table comes first and a chain of joins reads in one
  direction.
- `FULL OUTER JOIN` preserves unmatched rows on both sides, and a `WHERE`
  predicate on either table can reduce it to an inner join or a one-sided
  anti-join. Use `u.user_id IS NULL OR d.deck_id IS NULL` when both
  directions matter, and filter each input before the join on large tables.
- A self join needs two aliases and multiplies: n rows can produce n²
  combinations. Add a strict key inequality so each pair appears once and
  no row pairs with itself.
- `COUNT(*)` after a one-to-many join counts joined rows, not parents or
  children. `COUNT(DISTINCT key)` fixes a count but not a `SUM`; when
  several child tables meet in one query, pre-aggregate each one first.
- SQL Server does not support `JOIN ... USING`; use `ON`. `USING` is
  standard SQL, requires same-named key columns, and merges the join column
  into one output column.
- `UNION` requires the same column count with compatible types in each
  position, aligns columns by position, and takes its labels from the first
  branch. `UNION` removes duplicates and costs more; `UNION ALL` keeps them.
  Choosing the wrong one either hides duplicates or double-counts them.

## Part 6 — Subqueries and Simple CTEs

Parts 2 to 5 built each query from clauses. A **subquery** is a `SELECT`
statement nested inside another statement, and a **common table expression**
(CTE) is a named subquery written before the main statement with `WITH`. Both
let you answer a question in steps. A subquery is usually the right tool for a
single comparison or an existence check; a CTE is usually the right tool when
an intermediate result needs a name or is used more than once.

This part covers non-recursive CTEs only. A recursive CTE refers to itself to
walk a hierarchy, and it is out of scope for this guide and the question
banks. Every example uses the Part 1 sample rows, and each stated result can
be traced to those rows; no example was executed.

### Scalar Subqueries

A scalar subquery returns exactly one column and at most one row, so the
database can use it anywhere a single value is allowed: a comparison, a
`SELECT` list, or the right-hand side of `SET` in an `UPDATE` (Part 7). If the
subquery returns more than one row, the statement fails; if it returns no row,
the value is `NULL`.

The usual QA question is "which rows are above the overall average?"

**SQL Server:**

```sql
SELECT review_id, rating
FROM reviews
WHERE rating > (
    SELECT AVG(CAST(rating AS DECIMAL(10, 2)))
    FROM reviews
);
```

**Expected rows.** Three rows: reviews 10001 (rating 5), 10002 (4), and 10005
(5). The subquery returns one value, 3.8: the five non-null ratings sum to 19,
and the average is 19 / 5. The two `NULL` ratings are excluded from the
average, and they also fail the outer comparison because `NULL > 3.8` is
UNKNOWN rather than TRUE (Part 3). The cast still matters: `AVG` over an
`INT` column returns an `INT` in SQL Server, so without it the subquery
reports 3 rather than 3.8, and comparisons such as `>=` can change; for this
`>` test on integer ratings the same rows pass either way. The statement is
standard SQL as well.

A scalar subquery can also supply a value to every output row:

**SQL Server:**

```sql
SELECT review_id,
       rating,
       (SELECT AVG(CAST(rating AS DECIMAL(10, 2))) FROM reviews) AS overall_avg
FROM reviews;
```

This returns seven rows, one per review, with `overall_avg` 3.8 on every row,
including the two rows whose own `rating` is `NULL`. Because the subquery does
not refer to the outer `reviews` row, its value does not change from row to
row. The statement is standard SQL as well.

### IN and EXISTS

`IN (subquery)` is a membership test: the outer value must equal one of the
values the subquery returns. The subquery must return exactly one column but
may return any number of rows; duplicates in that list do not duplicate the
outer rows. `EXISTS (subquery)` is an existence test: it is TRUE when the
subquery returns at least one row and FALSE when it returns none. The select
list of an `EXISTS` subquery is ignored, which is why `SELECT 1` is the
conventional choice.

The first question is "which decks have at least one card?"

**SQL Server:**

```sql
SELECT deck_id, title
FROM decks
WHERE deck_id IN (
    SELECT deck_id
    FROM cards
);
```

**Expected rows.** Three rows: decks 101 (Biology 101), 102 (Spanish Verbs),
and 103 (Biology 101). Deck 104 (Empty Deck) is absent because no card names
it. The inner list is 101, 101, 102, 103, 103; `IN` compares membership, so
the repeats change nothing. `cards.deck_id` is `NOT NULL`, which keeps this
form free of the `NULL` trap; Part 3 explains what a `NULL` in the list would
do to the negated version. The statement is standard SQL as well.

The same question as an existence test:

**SQL Server:**

```sql
SELECT d.deck_id, d.title
FROM decks AS d
WHERE EXISTS (
    SELECT 1
    FROM cards AS c
    WHERE c.deck_id = d.deck_id
);
```

**Expected rows.** The same three rows. The inner query refers to `d.deck_id`,
the outer row, so it is a correlated subquery; for each deck the server checks
whether at least one card matches. `EXISTS` needs only one matching row, so
the inner query does not have to count anything and `SELECT 1` means "I only
need to know whether a row exists". A deck with five cards still produces one
outer row, because the test is per outer row, not a join. The statement is
standard SQL as well.

For the empty deck, negate the existence test:

**SQL Server:**

```sql
SELECT d.deck_id, d.title
FROM decks AS d
WHERE NOT EXISTS (
    SELECT 1
    FROM cards AS c
    WHERE c.deck_id = d.deck_id
);
```

**Expected rows.** One row: deck 104, Empty Deck. `NOT EXISTS` is TRUE when
the inner query returns no row. A `NULL` inside the inner comparison is
UNKNOWN, which does not count as a match, so `NOT EXISTS` remains TRUE for a
deck that truly has no cards. That property makes it the safe form for
absence checks. The equivalent `NOT IN` query returns the same row here:

**SQL Server:**

```sql
SELECT deck_id, title
FROM decks
WHERE deck_id NOT IN (
    SELECT deck_id
    FROM cards
);
```

It is safe only because `cards.deck_id` is `NOT NULL`, so the subquery cannot
return a `NULL`. If the subquery returns a `NULL`, the `NOT IN` version
returns zero rows (Part 3), and a zero-row "no empty decks" result would be a
false clean result. Both statements are standard SQL.

### Correlated Subqueries

A **correlated subquery** references a column from the outer query, so its
result can differ for every outer row. The server may rewrite the query into a
join internally, but the mental model is: for each outer row, run the inner
query with that row's values. The latest review per card is the standard
example.

**SQL Server:**

```sql
SELECT r.review_id, r.card_id, r.rating, r.reviewed_at
FROM reviews AS r
WHERE r.reviewed_at = (
    SELECT MAX(r2.reviewed_at)
    FROM reviews AS r2
    WHERE r2.card_id = r.card_id
)
ORDER BY r.card_id, r.review_id;
```

**Expected rows.** Four rows: review 10002 for card 1001 (rating 4), review
10006 for card 1002 (rating 2), review 10004 for card 1003 (rating 3), and
review 10007 for card 1004 (rating `NULL`). The inner query computes the
latest `reviewed_at` for the card named by the current outer row, so an outer
row survives only when it is that card's latest. Card 1005 has no reviews and
does not appear. Review 10007 shows that the latest review does not need a
rating; the query filters on time, not on `rating`. If two reviews share the
latest timestamp, both survive, because `MAX` returns a value, not a single
row identity. Add a deterministic tiebreaker, or use `ROW_NUMBER` (Part 9),
when the check expects exactly one row. The statement is standard SQL as well.

The same correlated shape answers "which cards have no reviews?"

**SQL Server:**

```sql
SELECT c.card_id, c.front
FROM cards AS c
WHERE NOT EXISTS (
    SELECT 1
    FROM reviews AS r
    WHERE r.card_id = c.card_id
);
```

**Expected rows.** One row: card 1005, "What is a gene?". Cards 1001, 1002,
1003, and 1004 each have at least one review. Here the correlation is the
`c.card_id` reference inside the inner `WHERE`; `NOT EXISTS` is TRUE only when
no review matches the current card. The statement is standard SQL as well.

### Simple CTEs

A common table expression (CTE) gives a name to a subquery and places it
before the statement that uses it. The shape is `WITH name AS (query)`
followed by the main statement. The name exists for one statement: it can be
used anywhere in the statement that follows, including more than once, and it
is gone when that statement ends. This guide and the question banks use
non-recursive CTEs only; a recursive CTE that refers to itself is out of
scope.

The reference example counts cards per deck and keeps empty decks:

**SQL Server:**

```sql
WITH deck_card_counts AS (SELECT deck_id, COUNT(*) AS card_count FROM cards GROUP BY deck_id) SELECT d.title, COALESCE(c.card_count, 0) AS card_count FROM decks AS d LEFT JOIN deck_card_counts AS c ON c.deck_id = d.deck_id;
```

**Expected rows.** Four rows, in no particular order because the statement has
no `ORDER BY` (Part 2): Biology 101 with 2, Spanish Verbs with 1, Biology 101
with 2, and Empty Deck with 0. The CTE groups `cards` by `deck_id` and returns
101 → 2, 102 → 1, and 103 → 2; deck 104 has no row in that result. The
`LEFT JOIN` starts from `decks`, so deck 104 survives, and `COALESCE` turns
its `NULL` count into 0. Two rows show the title Biology 101, because decks
101 and 103 share that title (Part 1); the statement selects only the title,
so the report cannot tell them apart. Select `d.deck_id` as well when each row
must be identifiable. The statement is standard SQL as well; the one-line
layout above is the reference form, and the same statement can be wrapped
across lines without changing its meaning.

In SQL Server, the statement before a `WITH` must end with a semicolon. A
missing terminator produces a syntax error near the word `with` that points at
the wrong statement, so end the previous statement explicitly.

### Multiple CTEs

A single `WITH` clause may define several CTEs, separated by commas. Later
definitions can refer to earlier ones, and the main statement can use any of
them. Multiple CTEs keep separate aggregates separate: each one is computed
from its own tables before the joins combine them.

**SQL Server:**

```sql
WITH card_counts AS (
    SELECT deck_id, COUNT(*) AS card_count
    FROM cards
    GROUP BY deck_id
),
review_counts AS (
    SELECT c.deck_id, COUNT(*) AS review_count
    FROM cards AS c
    INNER JOIN reviews AS r ON r.card_id = c.card_id
    GROUP BY c.deck_id
)
SELECT d.deck_id,
       d.title,
       COALESCE(cc.card_count, 0) AS card_count,
       COALESCE(rc.review_count, 0) AS review_count
FROM decks AS d
LEFT JOIN card_counts  AS cc ON cc.deck_id = d.deck_id
LEFT JOIN review_counts AS rc ON rc.deck_id = d.deck_id
ORDER BY d.deck_id;
```

**Expected rows.** Four rows:

| deck_id | title | card_count | review_count |
|---:|---|---:|---:|
| 101 | Biology 101 | 2 | 4 |
| 102 | Spanish Verbs | 1 | 1 |
| 103 | Biology 101 | 2 | 2 |
| 104 | Empty Deck | 0 | 0 |

`card_counts` produces 101 → 2, 102 → 1, and 103 → 2, as before.
`review_counts` groups the reviews by the deck of their card: deck 101 has
cards 1001 and 1002, which carry reviews 10001, 10002, 10003, and 10006, so 4;
deck 102 has card 1003 with review 10004, so 1; deck 103 has card 1004 with
reviews 10005 and 10007, so 2, and card 1005 contributes nothing because it
has no reviews. The inner join in `review_counts` drops card 1005 and deck
104, and the grouping then counts reviews per deck. Each CTE returns at most
one row per deck, so the two left joins cannot multiply rows: this is the
pre-aggregate-then-join shape from Part 5 with names instead of nested tables.
The `COALESCE` calls give deck 104 zeros instead of the `NULL`s that a left
join would supply. If the second CTE needed the first, it could reference
`card_counts` by name, because definitions are read in order within the same
`WITH` clause. The statement is standard SQL as well.

### CTE vs Subquery

The simple CTE and a nested subquery answer the same question with the same
result. The nested form puts the aggregate in the `FROM` clause as a derived
table:

**SQL Server:**

```sql
SELECT d.title,
       COALESCE(c.card_count, 0) AS card_count
FROM decks AS d
LEFT JOIN (
    SELECT deck_id, COUNT(*) AS card_count
    FROM cards
    GROUP BY deck_id
) AS c ON c.deck_id = d.deck_id;
```

**Expected rows.** The same four rows: Biology 101 with 2, Spanish Verbs with
1, Biology 101 with 2, and Empty Deck with 0. The two statements differ in
structure, not result. The CTE's real gain is the name: `deck_card_counts`
says what the intermediate rows mean, while the derived table is only `c`.

| Question | CTE | Nested subquery |
|---|---|---|
| Where does the intermediate query appear? | Before the main statement, under a name | Inside `FROM`, as a derived table |
| Does it need an alias? | The CTE name is the alias | Yes, the derived table needs `c` or `AS c` |
| Can the main statement use it more than once? | Yes, by name | Only by writing it again |
| How does it read? | Top-down: define, then use | Inside-out: read the nesting |
| Does it guarantee one evaluation? | No | No |

The last row is the one QA checks most often get wrong. A CTE is not a
materialized result. In SQL Server the optimizer generally expands the CTE
into the statement as if it were the equivalent subquery, so referencing it
twice can mean evaluating it twice, and a CTE alone is not a performance
improvement. If an expensive intermediate result must be computed once, store
it in a table or restructure the query; a CTE or a plain view is only a name
(Part 8 returns to views, and Part 10 covers tuning).

The nested form is standard SQL as well, as is the CTE form. In SQL Server the
derived table in `FROM` needs an alias; a CTE at the top level uses its own
name instead.

### Release QA Use

- Turn each acceptance question into the smallest subquery that answers it.
  "Which decks have cards?" is `IN` or `EXISTS`; "which decks have none?" is
  `NOT EXISTS`. A zero-row result from the wrong form is a false clean result,
  not evidence.
- Use a scalar subquery when one row must be compared with a table-wide
  baseline, such as a rating against the overall average. The `NULL` handling
  of the aggregate applies before the outer comparison.
- Use a correlated subquery for a per-group question such as the latest review
  per card. State what should happen on a tie, and add a tiebreaker when the
  check expects exactly one row.
- Name intermediate results with CTEs when a check has several steps. Each CTE
  is a step you can describe in the bug report, and multiple CTEs keep card
  counts and review counts separate so neither join multiplies the other.
- Remember that a CTE lives for one statement. If a result must feed a second
  check, run the statement again or store the result; the name does not
  survive.
- Do not treat a CTE as an optimization. Measure the plan and the reads
  (Part 10) before claiming that a rewrite made a check faster.

### Watch-outs

- A CTE is not a temp table. It stores no rows of its own, has no index or
  statistics of its own, and has no life beyond the statement that defines
  it.
- The scope of a CTE ends at the end of its statement. The next statement
  cannot reference the name, even in the same batch.
- A CTE referenced twice may be evaluated twice. SQL Server generally expands
  it into the statement, so a CTE is a naming device, not a cache and not a
  materialized intermediate result.
- Recursive CTEs are out of scope for this guide and the question banks. Every
  `WITH` example here is non-recursive.
- A scalar subquery must return one column and at most one row. More rows
  raise an error; zero rows produce `NULL`, which can silently turn a
  comparison into UNKNOWN.
- A `NOT IN` subquery whose result contains a `NULL` returns no rows. Use
  `NOT EXISTS`, or filter the inner column with `IS NOT NULL`.
- `EXISTS` ignores the select list; `SELECT 1` states the intent. A correlated
  subquery can be slow when it runs per outer row, so compare it with a join
  when the table is large (Part 10).
- A latest-per-group subquery returns every row tied for the maximum. Add a
  unique tiebreaker when the check expects one row per group.
- In SQL Server, the statement before a `WITH` must end with a semicolon; a
  missing terminator produces a misleading syntax error near `with`.

## Part 7 — Changing Data and Transactions

Parts 2 to 6 read data. This part changes it. `INSERT` adds rows, `UPDATE`
changes values, and `DELETE` removes rows. Each statement has to answer three
questions before it runs: which rows does it touch, what changes, and how do
you undo it if the answer is wrong. **Autocommit** is the default in SQL
Server and in most databases: each statement is its own transaction and is
saved as soon as it succeeds. That is why an `UPDATE` without a `WHERE` is not
an experiment; it is a permanent change to every row.

A **transaction** groups statements so they can all be saved or all undone.
This part shows the SQL Server forms first and the standard SQL forms second.
Each example starts from the Part 1 sample rows and is independent of the
others; the statements would change those rows if run, and none was executed
here.

### INSERT

`INSERT INTO table (columns) VALUES (values)` adds one row. The column list
and the value list must have the same length and compatible types, and each
value is assigned to the column in the same position.

**SQL Server:**

```sql
INSERT INTO users (user_id, email, display_name, created_at)
VALUES (6, 'frank@example.com', 'Frank', '2026-02-15 09:00:00');
```

**Expected effect.** User 6 is added. The column list names all four columns;
`display_name` is nullable, so it could be omitted and would then be `NULL`,
but the three `NOT NULL` columns must be supplied. `user_id` is written
explicitly because the schema has no identity or default on it (Part 1); a
table that generates its own keys would omit it.

**Standard SQL:**

```sql
INSERT INTO users (user_id, email, display_name, created_at)
VALUES (6, 'frank@example.com', 'Frank', TIMESTAMP '2026-02-15 09:00:00');
```

The shape is the same; standard SQL adds a typed `TIMESTAMP` literal.

The column list is not optional for safe work. `INSERT INTO users VALUES (...)`
depends on the column order in the table. Add a column, or change the order in
a migration, and the statement either fails or writes values into the wrong
columns. Always name the columns.

`INSERT ... SELECT` adds one row per row the query returns. It is how a QA
script copies, transforms, or stages data without listing values one at a
time.

**SQL Server:**

```sql
INSERT INTO decks (deck_id, user_id, title, is_public, created_at)
SELECT 200 + user_id, user_id, 'Welcome Deck', 0, '2026-02-15 09:00:00'
FROM users
WHERE user_id IN (4, 5);
```

**Expected effect.** Two rows are inserted: deck 204 for user 4 and deck 205
for user 5. The `SELECT` returns two rows, and each becomes one insert; the
expression `200 + user_id` derives keys in a reserved QA range, away from the
sample decks 101 to 104. `is_public` is `BIT`, so `0` means `FALSE` (Part 1).

**Standard SQL:**

```sql
INSERT INTO decks (deck_id, user_id, title, is_public, created_at)
SELECT 200 + user_id,
       user_id,
       'Welcome Deck',
       FALSE,
       TIMESTAMP '2026-02-15 09:00:00'
FROM users
WHERE user_id IN (4, 5);
```

The standard form differs in the boolean literal and uses a typed `TIMESTAMP`
literal.

A constraint can reject the whole statement. This negative-test insert tries
to record a rating of 6:

**SQL Server:**

```sql
INSERT INTO reviews (review_id, card_id, user_id, rating, reviewed_at)
VALUES (10008, 1005, 1, 6, '2026-02-15 09:00:00');
```

The check constraint `ck_reviews_rating` allows a non-null rating only between
1 and 5 (Part 1), so the statement is rejected and no row is added. SQL Server
reports a check-constraint conflict as error 547, and the message names the
constraint, the table, and the column. The other constraints reject other
mistakes in the same way: a `card_id` of 9999 violates `fk_reviews_card`, a
`user_id` of 99 violates `fk_reviews_user`, a duplicate `review_id` violates
the primary key, and a missing `NOT NULL` value violates that column's rule
(SQL Server error 515). Standard SQL describes the same classes with SQLSTATE
codes such as 23514 (check), 23503 (foreign key), 23505 (unique), and 23502
(not null).

Error text is evidence. A bug report that says "the API could not save the
review" is weaker than one that records the constraint name, the rejected
value, and the server's message. The exact text varies by product and version,
so quote it rather than paraphrasing.

Because one statement is atomic, a multi-row `INSERT ... SELECT` that hits one
bad row stores none of its rows. Validate the source query and its constraints
before running the insert, and compare the affected-row count with the count
the `SELECT` alone returned.

### UPDATE

`UPDATE table SET column = value WHERE condition` changes the matching rows.
The `WHERE` clause uses the same rules as a `SELECT` filter (Part 3); without
it, every row matches.

**SQL Server:**

```sql
UPDATE reviews
SET rating = 5
WHERE review_id = 10002;
```

**Expected effect.** Review 10002 changes from 4 to 5; one row is affected.
The other six reviews keep their values. The statement is standard SQL as
well.

Now remove the `WHERE`:

**SQL Server:**

```sql
UPDATE reviews
SET rating = 5;
```

**Expected effect.** Every row in `reviews` gets a rating of 5: seven rows are
affected, including reviews 10003 and 10007, whose `NULL` ratings are
replaced. The original distribution is gone. Under autocommit the change is
permanent; outside a transaction there is no statement-level undo. This is the
single most destructive typo in SQL, and it is the reason the next paragraph
exists.

Before an `UPDATE`, run its `WHERE` as a `SELECT`:

**SQL Server:**

```sql
SELECT COUNT(*)
FROM reviews
WHERE review_id = 10002;
```

The count is the number of rows the update should affect. Run the update, then
compare the affected-row message with the count. `(1 row affected)` matches;
`(0 rows affected)` means the `WHERE` matched nothing; `(7 rows affected)`
means the `WHERE` was too broad or was never applied. On SQL Server the same
count is available as `@@ROWCOUNT` immediately after the statement. The
statement is standard SQL.

An `UPDATE` can take its row set from a subquery, which is how one change
targets the children of a selected parent:

**SQL Server:**

```sql
UPDATE reviews
SET rating = 5
WHERE card_id IN (
    SELECT card_id
    FROM cards
    WHERE deck_id = 101
);
```

**Expected effect.** Four rows change: reviews 10001, 10002, 10003, and 10006,
the reviews on cards 1001 and 1002 in deck 101. The subquery returns the
deck's card IDs, and `IN` selects the reviews that name one of them.
`cards.card_id` is the primary key and cannot be `NULL`, so the membership
test has no `NULL` trap. The statement is standard SQL as well.

### DELETE

`DELETE FROM table WHERE condition` removes the matching rows. The table and
its columns remain; only the rows go.

**SQL Server:**

```sql
DELETE FROM reviews
WHERE rating IS NULL;
```

**Expected effect.** Two rows are deleted: reviews 10003 and 10007, the two
reviews with no rating. The predicate is `IS NULL`, not `= NULL`, because a
comparison with `NULL` is UNKNOWN and would delete nothing (Part 3). The
statement is standard SQL as well.

Without a `WHERE`, `DELETE` empties the table:

**SQL Server:**

```sql
DELETE FROM reviews;
```

**Expected effect.** All seven rows are deleted. The table still exists, and
its constraints and columns are unchanged, but it holds no rows. Under
autocommit the change is permanent. `DELETE` removes rows; it does not remove
the table, which is DDL (Part 8).

A subquery decides which rows to delete. This is the shape used to tear down
test data in foreign-key order:

**SQL Server:**

```sql
DELETE FROM reviews
WHERE card_id IN (
    SELECT card_id
    FROM cards
    WHERE deck_id = 102
);
```

**Expected effect.** One row is deleted: review 10004, the only review on card
1003 in deck 102. To remove deck 102 completely, the order is reviews, then
cards, then the deck. Each child table points at its parent with a foreign
key, so deleting a parent first is rejected while matching children remain.
The statement is standard SQL as well.

The same shape has a `NULL` trap when the subquery returns a `NULL`: the
predicate is UNKNOWN for every outer row, so the delete removes zero rows. If
the check is a cleanup that depends on `NOT IN`, a zero-row result can look
like success while the rows remain. Use `NOT EXISTS` or make the subquery
return no `NULL` values.

### Transactions

A transaction is a unit of work that ends in either `COMMIT` or `ROLLBACK`.
`COMMIT` makes every change in the transaction permanent; `ROLLBACK` undoes
every change back to the start of the transaction, or back to a savepoint
(below). If the connection closes or the server fails mid-transaction, the
unfinished transaction rolls back. That all-or-nothing rule is why a test
setup can be discarded as one unit. A transaction belongs to one connection,
so another session cannot join it, and under the default isolation level it
cannot see the transaction's uncommitted rows.

SQL Server first. `BEGIN TRANSACTION` starts a transaction, and `UPDATE`,
`DELETE`, and `INSERT` after it belong to that transaction until `COMMIT` or
`ROLLBACK`.

**SQL Server:**

```sql
BEGIN TRANSACTION;

UPDATE reviews
SET rating = 5
WHERE review_id = 10002;

SELECT review_id, rating
FROM reviews
WHERE review_id = 10002;

ROLLBACK TRANSACTION;
```

**Expected effect.** The `SELECT` inside the transaction shows review 10002
with rating 5, because a transaction sees its own changes. The `ROLLBACK`
then undoes the update, and review 10002 holds rating 4 again. Under the
default isolation level, other sessions do not see the uncommitted 5, and the
open transaction can hold locks that block them, so keep transactions short
and always close them.

To keep the change instead, commit it:

**SQL Server:**

```sql
BEGIN TRANSACTION;

INSERT INTO users (user_id, email, display_name, created_at)
VALUES (6, 'frank@example.com', 'Frank', '2026-02-15 09:00:00');

COMMIT TRANSACTION;
```

**Expected effect.** User 6 is added and stays added. `COMMIT` ends the
transaction; a later `ROLLBACK` cannot undo it. SQL Server accepts
`COMMIT TRANSACTION`, `COMMIT TRAN`, and `COMMIT`; `ROLLBACK TRANSACTION` and
`ROLLBACK` are both accepted, while the `BEGIN` form needs `TRANSACTION` or
`TRAN`.

The standard SQL forms are different words for the same steps:

**Standard SQL:**

```sql
START TRANSACTION;

UPDATE reviews
SET rating = 5
WHERE review_id = 10002;

ROLLBACK;
```

and to keep the work:

**Standard SQL:**

```sql
START TRANSACTION;

INSERT INTO users (user_id, email, display_name, created_at)
VALUES (6, 'frank@example.com', 'Frank', TIMESTAMP '2026-02-15 09:00:00');

COMMIT;
```

Standard SQL uses `START TRANSACTION`, `COMMIT`, and `ROLLBACK`; it does not
use SQL Server's `BEGIN TRANSACTION`. The words are not interchangeable across
products: some databases accept `BEGIN` as a synonym, but a statement that
starts with `BEGIN TRANSACTION` is T-SQL syntax, and one that starts with
`START TRANSACTION` is the standard form.

**Test-data cleanup.** The safe pattern for a check that runs in one session
is to create the fixtures and discard them with the transaction that created
them:

**SQL Server:**

```sql
BEGIN TRANSACTION;

-- Setup
INSERT INTO users (user_id, email, display_name, created_at)
VALUES (900, 'qa@example.com', 'QA User', '2026-02-15 09:00:00');

INSERT INTO decks (deck_id, user_id, title, is_public, created_at)
VALUES (900, 900, 'QA Deck', 0, '2026-02-15 09:00:00');

-- The check runs here, in the same session.

ROLLBACK TRANSACTION;
```

**Expected effect.** The setup rows exist while the check runs and are gone
after the rollback; no fixture is left behind. The same-session condition is
part of the pattern: another connection cannot see uncommitted rows under the
default isolation level, and a UI test running in a browser session is another
connection. For a cross-session test, commit the setup, run the test, and then
remove the rows by their known keys in child-to-parent order, checking the
counts afterward:

**SQL Server:**

```sql
BEGIN TRANSACTION;

DELETE FROM decks
WHERE deck_id = 900;

DELETE FROM users
WHERE user_id = 900;

COMMIT;
```

The deck must go before the user because `fk_decks_user` points from the deck
to the user. A cleanup that deletes nothing and a cleanup that succeeds both
return without an error; a `SELECT COUNT(*) ... WHERE user_id = 900` that
returns 0 is the evidence that the rows are gone.

**Shared environments.** A transaction protects a change only until it is
committed, and it does not protect other people from your locks. On a shared
test server another tester can read, change, or delete the same rows, and a
`ROLLBACK` cannot recover work that was committed outside your transaction.
Before any destructive statement in a shared environment, get approval and
confirm which environment you are connected to. Prefer a dedicated database or
schema; run the `SELECT` scope check first; keep the statement in a
transaction; and commit only the change the test is meant to produce. A
production database should not grant a QA account write access at all; if one
does, that is a finding.

A constraint error inside a transaction has its own trap. In SQL Server the
invalid statement is rolled back, but by default the transaction stays open.
The error is reported, the connection still holds the transaction and its
locks, and the next statement runs inside that transaction. After any error,
roll back deliberately (or commit the valid earlier work), and read the error
text before retrying. Some products abort the whole transaction on a statement
error; SQL Server's default is the statement-level behavior, so do not assume
another database behaves the same way.

### Savepoints

A savepoint is a named marker inside a transaction. Rolling back to it undoes
only the work done after the marker; earlier work stays, and the transaction
is still open. It is not a commit.

**SQL Server:**

```sql
BEGIN TRANSACTION;

INSERT INTO users (user_id, email, display_name, created_at)
VALUES (6, 'frank@example.com', 'Frank', '2026-02-15 09:00:00');

SAVE TRANSACTION after_user_insert;

UPDATE decks
SET is_public = 1
WHERE deck_id = 104;

ROLLBACK TRANSACTION after_user_insert;

COMMIT TRANSACTION;
```

**Expected effect.** The update of deck 104 is undone, so deck 104 is private
again (`is_public` 0, its Part 1 value), while user 6 is committed and remains.
`SAVE TRANSACTION` defines the marker; `ROLLBACK TRANSACTION after_user_insert`
undoes everything after it; the transaction is still active, and the final
`COMMIT` keeps the insert. If the final `COMMIT` were
replaced by `ROLLBACK`, user 6 would be removed too.

The standard form uses `SAVEPOINT` and `ROLLBACK TO SAVEPOINT`:

**Standard SQL:**

```sql
START TRANSACTION;

INSERT INTO users (user_id, email, display_name, created_at)
VALUES (6, 'frank@example.com', 'Frank', TIMESTAMP '2026-02-15 09:00:00');

SAVEPOINT after_user_insert;

UPDATE decks
SET is_public = TRUE
WHERE deck_id = 104;

ROLLBACK TO SAVEPOINT after_user_insert;

COMMIT;
```

**Expected effect.** The same outcome: the deck update is undone and user 6 is
kept. `SAVEPOINT name` creates the marker; `ROLLBACK TO SAVEPOINT name` undoes
work after it; the transaction remains open until `COMMIT`. Standard SQL also
has `RELEASE SAVEPOINT name`, which discards a marker without undoing its
work. SQL Server has no `RELEASE SAVEPOINT`; its savepoints disappear when the
transaction ends.

Do not use a second `BEGIN TRANSACTION` as a savepoint. SQL Server counts
nested `BEGIN TRANSACTION` calls, and an inner `COMMIT` only decrements the
count; it does not make the work permanent, and `ROLLBACK` without a savepoint
undoes the whole transaction. `SAVE TRANSACTION` is the tool for undoing part
of a transaction.

### Release QA Use

- Run every change as a loop: `SELECT` the scope and count it, predict the
  affected count, run the change, compare the affected-row message, verify the
  new state with another `SELECT`, and clean up. Each step produces evidence
  for the report.
- Build fixtures with explicit keys in a reserved range, such as users and
  decks 900 or above, so test rows are easy to find and remove and cannot
  collide with sample or production-like rows.
- Clean up in child-to-parent order: reviews, then cards, then decks, then
  users. A parent delete is rejected while children remain; a child delete
  first is the ordinary foreign-key-safe order.
- Wrap multi-statement changes in a transaction so the whole change is saved
  or undone. When the check runs in the same session, roll back the setup to
  leave no fixtures; when another connection runs the test, commit the setup
  and delete it by key afterward.
- Use a savepoint when a multi-step check must undo one step but keep the
  earlier setup. A second `BEGIN TRANSACTION` is not a savepoint in SQL
  Server.
- Treat constraint errors as test results. Record the error number or
  SQLSTATE, the constraint name, the table, the rejected value, and the
  server's message; a negative test passes when it gets exactly that rejection.
- Never run destructive statements on a shared or production environment
  without written approval and a verified scope. Prefer a dedicated test
  database, take a backup or snapshot when the environment allows it, and
  leave write access off the QA account when it is not required.

### Watch-outs

- `UPDATE` and `DELETE` without `WHERE` touch every row. Autocommit makes the
  change permanent; outside a transaction there is no statement-level undo.
- The affected-row count is evidence. `(0 rows affected)` often means the
  `WHERE` matched nothing through a wrong key, a `NULL`, or a type mismatch;
  an unexpectedly large count means the `WHERE` was too broad.
- `DELETE` with `NOT IN` over a subquery that returns a `NULL` deletes
  nothing. Use `NOT EXISTS` or filter the inner column; a zero-row delete is
  not proof the data was clean.
- Delete children before parents. A foreign key rejects a parent delete while
  matching children remain, and the error text names the relationship.
- A transaction stays open until `COMMIT` or `ROLLBACK`. An open transaction
  holds locks, blocks other sessions, and hides its changes from them; close it
  even after an error.
- A constraint violation rejects the statement; in SQL Server the transaction
  can stay open by default. Read the error text and roll back deliberately.
- A savepoint is not a commit. `ROLLBACK TRANSACTION marker` keeps earlier
  work but the transaction remains open; a final `COMMIT` or `ROLLBACK` is
  still required.
- `INSERT INTO table VALUES (...)` without a column list depends on column
  order. A schema change can break the statement or put values in the wrong
  columns.
- A multi-row `INSERT ... SELECT` that violates one constraint inserts no
  rows: the statement is rejected as a unit. Validate and count the source
  rows before the insert.
- Cleanup must be verified. Run `SELECT COUNT(*)` after cleanup and expect
  zero rows; a cleanup that deleted nothing looks the same as a successful one
  otherwise.

## Part 8 — Schema, Constraints, Indexes, and Views

Parts 2 to 7 worked with rows. This part works with the definitions that hold
the rows. **DDL** (data definition language) creates and alters tables, views,
and indexes, and drops them again. A release changes DDL when it adds a
column, tightens a rule, or introduces an object that reports depend on. DDL
is the part of a release that outlives any single row: a wrong `UPDATE` can be
corrected row by row, but a missing constraint silently accepts bad rows in
every later release.

This part reuses the Part 1 schema and its sample rows. The view and the
indexes are additions on top of that schema, and the table definitions are the
ones Part 1 printed. No example was executed.

### CREATE TABLE

`CREATE TABLE` names a table and defines its columns. Each column has a name,
a data type, and, when needed, a constraint. The finished definition is a
contract that every later `INSERT` and `UPDATE` must satisfy (Part 7).

`reviews` is the best single example because it carries every constraint kind
this schema uses. **SQL Server:**

```sql
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

The column definitions are separated by commas; the table-level constraints
follow the columns. `review_id INT PRIMARY KEY` is a column constraint, and
`CONSTRAINT fk_reviews_card ...` is a named table constraint. Names are worth
the extra words: SQL Server reports the constraint name when it rejects a row
(Part 7), and a later migration needs the name to drop or change the rule. An
unnamed constraint gets a server-generated name that is hard to quote in a bug
report and hard to reference in a script.

A table can reference only a table that already exists, so the creation order
is `users`, then `decks`, then `cards`, then `reviews`. A migration script
that creates or alters these tables must follow the same order, and the
cleanup order is the reverse (Part 7). The types in the two blocks are the
Part 1 mapping: `INT`/`INTEGER`, `NVARCHAR`/`VARCHAR`, `DATETIME2`/`TIMESTAMP`.

Most DDL in SQL Server can run inside a transaction and roll back with it
(Part 7), which is how a test schema change is tried and undone in one
session. Some other products commit DDL implicitly, so check the behavior of
the target database before assuming that a `ROLLBACK` will remove a table.

### Constraints

A constraint is a rule the database checks so that an application cannot save
a row that breaks it. Treat each one as a test oracle: a negative test supplies
a value that breaks the rule and expects the named error (Part 7). This part
covers the six constraint kinds; the shared schema uses four of them, and the
other two appear in the syntax variants below.

**Primary key.** The primary key identifies one row. It combines two rules:
values must be unique, and they may not be `NULL` (Part 1).
`review_id INT PRIMARY KEY` declares it as a column constraint; a composite
key is written as a table constraint, `CONSTRAINT pk_name PRIMARY KEY
(col_a, col_b)`. A duplicate `review_id` or a `NULL` `review_id` is rejected.
In SQL Server a primary key also creates a unique index, clustered by default,
so the key is the table's default physical order; the Indexes section returns
to that.

**Foreign key.** `fk_reviews_card` and `fk_reviews_user` require the child row
to name an existing parent. Inserting review 10008 with `card_id` 9999 is
rejected because card 9999 does not exist. The same constraint protects the
parent side: deleting card 1001 while its two reviews remain is rejected until
the child rows go (Part 7). A foreign key is a correctness rule, not an
index; SQL Server does not create an index on the child column, so the check
can scan `reviews` unless one exists.

**UNIQUE.** A unique constraint rejects duplicate values in a column or in a
combination of columns. This schema has none; `users.email` is the natural
candidate. The staging table `legacy_users` (introduced in Part 11) holds two
rows with `alice@example.com`, and a `UNIQUE` constraint on `email` is what
turns that duplicate from a query finding (Part 11) into a rejected insert.
The variant below is a syntax illustration, not the shared definition:

**SQL Server:**

```sql
CREATE TABLE users (
    user_id      INT PRIMARY KEY,
    email        NVARCHAR(255) NOT NULL UNIQUE,
    display_name NVARCHAR(100),
    created_at   DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
);
```

**Standard SQL:**

```sql
CREATE TABLE users (
    user_id      INTEGER PRIMARY KEY,
    email        VARCHAR(255) NOT NULL UNIQUE,
    display_name VARCHAR(100),
    created_at   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

The `UNIQUE` word on the column is shorthand for a table-level unique
constraint on that column. A combination rule is
`CONSTRAINT uq_name UNIQUE (col_a, col_b)`.

**UNIQUE and NULL.** This is a portability trap. The standard's uniqueness
rule compares non-`NULL` values, and because `NULL` is not equal to anything,
the standard permits more than one `NULL` in a unique column. SQL Server
treats `NULL`s as equal for a `UNIQUE` constraint, so a single-column unique
constraint accepts at most one `NULL`. Products differ in the details, so the
durable rule is the one this schema follows: declare unique columns
`NOT NULL`. `users.email` is `NOT NULL` in the shared schema and in both
variants above.

**NOT NULL.** `NOT NULL` requires a value. In this schema only
`users.display_name` and `reviews.rating` omit it. An `INSERT` that omits
`display_name` stores `NULL` and succeeds; an `INSERT` that omits `email` or
writes `NULL` to it is rejected. A column declared without `NOT NULL` is
nullable by default. When a migration adds `NOT NULL` to an existing column,
every existing row is validated, so a table that already holds a `NULL`
rejects the change.

**CHECK.** `ck_reviews_rating` is `CHECK (rating BETWEEN 1 AND 5)`. An insert
or update that sets `rating` to 0 or 6 is rejected. A `NULL` rating passes,
and this is the point QA checks most often miss: a check constraint rejects a
row only when its condition is FALSE. For a `NULL` rating, `NULL BETWEEN 1 AND
5` is UNKNOWN (Part 3), and the database accepts UNKNOWN as well as TRUE. The
constraint therefore means "a rating, when present, is 1 to 5", not "every
review has a rating". Reviews 10003 and 10007 exist with `NULL` ratings. If
the product requires a rating, that is a separate `NOT NULL` rule or an
application rule, and the gap between the two is a finding.

**DEFAULT.** The `users` variant above also shows `DEFAULT`. A default
supplies a value when the `INSERT` omits the column. It does not apply when
the statement writes an explicit `NULL`: a nullable column keeps the `NULL`,
and a `NOT NULL` column rejects the statement. SQL Server's
`SYSUTCDATETIME()` returns the server's UTC clock as a `DATETIME2`; standard
SQL has `CURRENT_TIMESTAMP`. A default moves the value's source from the
client to the server, so a check that compares `created_at` with the test
run's start time is comparing the server clock, which may differ in time zone
or offset. A default is also invisible at the `INSERT`, so a test that
exercises it must omit the column deliberately.

The six kinds, with the places this schema uses them:

| Constraint | Rule | In this schema |
|---|---|---|
| `PRIMARY KEY` | Unique and not null; identifies one row | Every table |
| `FOREIGN KEY` | The child value names an existing parent | Four foreign keys |
| `UNIQUE` | No duplicate values | None; `email` is the candidate |
| `NOT NULL` | A value is required | All but `display_name`, `rating` |
| `CHECK` | The condition is not FALSE | `ck_reviews_rating` |
| `DEFAULT` | Fills the column when the insert omits it | None |

**Adding constraints to existing data.** `ALTER TABLE ... ADD CONSTRAINT`
changes a table that already holds rows, and the database validates those
rows by default. Adding `UNIQUE (email)` to a table that has already received
the `legacy_users` rows from Part 11 fails on the duplicate Alice address;
adding `NOT NULL` to a column that holds `NULL`s fails on the first such row.
That is why constraint additions usually come after cleanup, and why the DDL
step of a migration is part of the test: the failure is evidence about the
data, not only about the script.

### Views

A view is a named query stored in the database. It has a name and a column
list, and each time it is referenced the database evaluates its definition
against the current base tables. A view is not a copy of the rows.

SQL Server can create or replace a view in one statement. **SQL Server:**

```sql
CREATE OR ALTER VIEW v_deck_card_counts AS
SELECT d.deck_id,
       d.title,
       COUNT(c.card_id) AS card_count
FROM decks AS d
LEFT JOIN cards AS c ON c.deck_id = d.deck_id
GROUP BY d.deck_id, d.title;
```

`CREATE OR ALTER VIEW` is available from SQL Server 2016 SP1 onward; earlier
versions create with `CREATE VIEW` and change with `ALTER VIEW`. The standard
form has no "or alter": **Standard SQL:**

```sql
CREATE VIEW v_deck_card_counts AS
SELECT d.deck_id,
       d.title,
       COUNT(c.card_id) AS card_count
FROM decks AS d
LEFT JOIN cards AS c ON c.deck_id = d.deck_id
GROUP BY d.deck_id, d.title;
```

A `CREATE OR REPLACE VIEW` form exists in some products but is not standard
SQL. In SQL Server, `CREATE VIEW` and `CREATE OR ALTER VIEW` must be the only
statement in their batch, so a script creates the view first and queries it in
a later batch. Removing a view takes `DROP VIEW v_deck_card_counts;` in SQL
Server and in standard SQL; it deletes the definition only and leaves every
base-table row in place.

The view returns one row per deck with the deck's ID, its title, and its
number of cards. It starts from `decks` and uses `LEFT JOIN`, so a deck with
no cards survives. The count is `COUNT(c.card_id)`, not `COUNT(*)`: the left
join produces one row for deck 104 with every `cards` column `NULL`, and
`COUNT(*)` would count that row as 1, while `COUNT(column)` ignores the `NULL`
(Part 4).

**SQL Server and standard SQL:**

```sql
SELECT deck_id, title, card_count
FROM v_deck_card_counts
ORDER BY deck_id;
```

**Expected rows.**

| deck_id | title | card_count |
|---:|---|---:|
| 101 | Biology 101 | 2 |
| 102 | Spanish Verbs | 1 |
| 103 | Biology 101 | 2 |
| 104 | Empty Deck | 0 |

Two rows show Biology 101 because decks 101 and 103 share the title; `deck_id`
is selected so the two remain distinguishable, the same point Part 6 made
about the CTE that counted cards per deck.

The base-table query returns the same four rows:

**SQL Server and standard SQL:**

```sql
SELECT d.deck_id,
       d.title,
       COUNT(c.card_id) AS card_count
FROM decks AS d
LEFT JOIN cards AS c ON c.deck_id = d.deck_id
GROUP BY d.deck_id, d.title
ORDER BY d.deck_id;
```

The view's body and this query differ only by the `ORDER BY`; the result is
identical row for row. In SQL Server, querying the view is logically the same
as pasting its definition into the query, and the optimizer is free to combine
the two. That leads to four facts every QA engineer should hold:

- **A view stores no rows.** It stores a definition and a column list. When
  deck 104 gains a card, the next query of the view reports 1 without any
  change to the view. A view with a `GROUP BY`, like this one, is read-only;
  a simple view without aggregation can be updatable, and then an `INSERT`,
  `UPDATE`, or `DELETE` through the view changes the base table.
- **A view is not automatically faster.** It runs its query every time. A
  view with a join and an aggregate does the same work as the base query. Do
  not treat a view as a cache. Products do offer materialized views, which
  store a result and must be refreshed, and SQL Server has a restricted form
  called an indexed view; neither is the plain view defined here, and
  creating one is a schema change that needs the same review as an index.
- **Nested views hide logic.** A view may select from another view. Each
  layer can filter, join, or collapse rows, and the outer definition does not
  show what the inner one did. When a release check disagrees with the screen,
  read every view in the chain before blaming the base table; a filter added
  to a lower view changes every report above it.
- **View permissions can differ from base-table permissions.** A view can be
  a narrower doorway than its tables: a login may query the view without
  direct access to the base tables, or lose the view while keeping the table
  grant. Test a permission change by querying the view as the restricted
  login, not only as its owner.

One more SQL Server behavior: `SELECT *` inside a view is expanded when the
view is created, and the view stores that column list. A column added to the
base table later does not appear in the view until the view is changed or its
metadata is refreshed. Name the columns explicitly in a view that another
system reads, for the same reason Part 2 gives for release checks.

### Indexes

An index is a structure the database keeps beside a table so that it can find
rows without reading every page. The table is the source of truth; an index
is a derived structure that the optimizer may choose to use.

**Clustered and nonclustered.** In SQL Server, a **clustered index** defines
the physical order of the table's rows: its leaf level is the data. A table
can have only one clustered index, because the rows can be stored in only one
order. A **nonclustered index** is a separate structure with sorted key
columns and a pointer to the row: the clustered key on a clustered table, or
a row identifier on a heap. A table can have many nonclustered indexes. In
this schema each primary key is a clustered index by default, so `cards` is
physically ordered by `card_id`.

The first index a QA engineer usually proposes is on a foreign-key column,
because SQL Server does not create one with the foreign key (Part 1). Both
the join `cards.deck_id = decks.deck_id` and a parent delete that checks child
rows can use it.

**SQL Server:**

```sql
CREATE NONCLUSTERED INDEX ix_cards_deck_id
    ON cards (deck_id);
```

**Portable form (not standard SQL):**

```sql
CREATE INDEX ix_cards_deck_id
    ON cards (deck_id);
```

Indexes are outside the SQL standard, so the second fence is labeled portable
rather than standard. Most products accept a form close to this one, but the
keywords and defaults are vendor-specific; check the product's documentation
before relying on them.

In SQL Server, `CREATE INDEX` without a type word creates a nonclustered
index; the word is spelled out above to make the choice visible. The portable
form has no `CLUSTERED` or `NONCLUSTERED` keyword, so the product's default
index type applies.

With the index, a query can seek the rows for one deck instead of scanning
every card:

**SQL Server and standard SQL:**

```sql
SELECT card_id, front
FROM cards
WHERE deck_id = 101;
```

The result is cards 1001 and 1002. On a table this small the optimizer may
still choose a table scan, because reading five rows is cheaper than reading
the index and then the rows. The index earns its cost as the table grows, so
the evidence that it is used is the execution plan (Part 10), not a judgment
from five sample rows.

**Key order.** An index with more than one key column sorts by the first key,
then by the second within equal first values, and so on. That order is why
the leftmost column matters. This index:

**SQL Server:**

```sql
CREATE NONCLUSTERED INDEX ix_cards_deck_created
    ON cards (deck_id, created_at)
    INCLUDE (front, back);
```

sorts by `deck_id` first and by `created_at` within a deck. A query that
filters on `deck_id = 101` can seek to the deck's entries, and because the
entries are already ordered by `created_at`, `ORDER BY created_at` inside that
deck can read them in order. A query that filters only on
`created_at >= '2026-01-17'` has no equality on the leftmost key, so the index
cannot seek to the matching rows; the engine can scan the whole index, which
may or may not be cheaper than scanning the table.

**Included columns and covering indexes.** `INCLUDE (front, back)` stores
those columns in the index's leaf level without making them part of the sort
key. They cannot be used to seek or to order rows; they exist so a query can
read their values from the index. An index that contains every column a query
references is a **covering index** for that query: the engine answers it from
the index alone and never visits the table. For example:

**SQL Server and standard SQL:**

```sql
SELECT card_id, front, back
FROM cards
WHERE deck_id = 101
ORDER BY created_at;
```

`ix_cards_deck_created` covers this query: `deck_id` and `created_at` are key
columns, `front` and `back` are included, and `card_id` comes with every
nonclustered index on this table because it is the clustered key. `INCLUDE`
is SQL Server syntax; the portable `CREATE INDEX` form has no included-column
clause, and products that support covering indexes spell it differently.
Covering is a property of one query, not of the index: the same index may not
cover the next query.

**Write cost.** Every index is maintained by every `INSERT`, `UPDATE`, and
`DELETE` on the table. A new row adds an entry to each index, a change to an
indexed column moves an entry, and a delete removes one. More indexes mean
more work per write, more storage, and more log. A wide covering index that
includes `front` and `back` duplicates the text of every card, so it can grow
close to the size of the table. The optimizer also gets more choices, and a
plan change can make a query slower even when the new index looked helpful in
isolation.

**Shared environments.** Creating an index is a schema change, not a
query-level tune-up. It consumes storage, can take time proportional to the
table, can block or slow other sessions while it builds, and changes the
optimizer's choices for every query on the table. On a shared test server,
other testers share those effects. Capture the slow query, its plan, and its
reads (Part 10), propose the index with that evidence, and get approval before
creating it. The same rule applies to dropping an index: another team's query
may depend on it.

### Release QA Use

- Treat the DDL as the test oracle. Every primary key, foreign key, unique
  rule, check, and not-null rule is a negative test with a named expected
  error (Part 7); a test that passes with no error has not exercised the rule.
- Test the boundary values, not only the happy path. For
  `ck_reviews_rating`, try 0, 1, 5, 6, and `NULL`: 0 and 6 must be rejected, 1
  and 5 must be accepted, and `NULL` must be accepted only if an unrated
  review is legal. That last case separates "invalid rating" from "missing
  rating".
- Before a migration adds a constraint, run the query that would find the rows
  it will reject: duplicate emails behind a proposed `UNIQUE`, `NULL`s behind
  a proposed `NOT NULL`, orphan keys behind a proposed foreign key. The
  constraint failure is then a predicted result with evidence attached.
- Read the view definition, not only its output, when a number is wrong.
  Expand every nested view to the base tables and check the filters, joins,
  and `GROUP BY` at each layer.
- Treat a view as a read interface, not an optimization. A check that queries
  the base table and a check that queries the view should return the same
  rows; if they do not, one of them is reading a different definition.
- Propose an index with the query, the plan, and the reads that justify it,
  and name the write cost. Do not create or drop an index on a shared or
  production environment without approval.
- Check dependencies before dropping or renaming a column or table. A view or
  index that references it can break. A non-schema-bound view can outlive an
  object it references: dropping or renaming that object can succeed, and the
  failure appears when the view is queried. Creating a view against an object
  that does not yet exist fails at creation.

### Watch-outs

- A `CHECK` constraint rejects FALSE only. `NULL` produces UNKNOWN, which
  passes, so `ck_reviews_rating` still allows an unrated review.
- `UNIQUE` and `NULL` do not mean the same thing in every product. SQL Server
  treats `NULL`s as equal, so a single-column unique constraint accepts at
  most one `NULL`; keep unique columns `NOT NULL`.
- A `DEFAULT` applies only when the insert omits the column. An explicit
  `NULL` stays `NULL`, and the value comes from the server clock, not the
  client.
- A foreign key needs the parent row first. Creation order and cleanup order
  both follow the dependency; a foreign key is not an index.
- A constraint added to a table with existing data validates that data.
  Adding `UNIQUE` over duplicates or `NOT NULL` over `NULL`s fails until the
  rows are fixed.
- A view stores no rows and is not automatically faster. Nested views hide
  filters and joins, and `SELECT *` in a SQL Server view freezes the column
  list at creation.
- A table has one clustered index and can have many nonclustered indexes. The
  leftmost key column decides which seeks work; `INCLUDE` is SQL Server
  syntax; covering is relative to one query.
- Every index adds work to every write and consumes storage. Do not add or
  drop indexes in a shared environment without approval.

## Part 9 — Window Functions

Parts 4 and 6 answered per-group questions by collapsing rows with `GROUP BY`
or by running a correlated subquery once per row. A **window function** answers
those questions without collapsing rows: it computes a value over a set of
related rows, the **window**, and attaches the result to each row. A review can
show its own rating and its card's average beside it, and the result still has
one row per review.

The shape is `function(...) OVER (PARTITION BY ... ORDER BY ...)`. The
`PARTITION BY` clause divides the rows into independent windows, the `ORDER BY`
clause orders the rows inside each window, and an optional frame narrows the
window further. SQL Server and standard SQL share this shape for every
function in this part, so each example is labeled **SQL Server and standard
SQL:** and is valid unchanged in both. Every stated result is derived from the
Part 1 sample rows; no example was executed.

### ROW_NUMBER

`ROW_NUMBER()` numbers the rows inside each window, starting at 1, in the
order the `OVER` clause specifies. The function never gives two rows the same
number, but when the ordering produces a tie, it does not promise which tied
row gets the smaller number. The rows are numbered; they are not sorted by the
result.

The standard use is "the latest row per group". This query finds the most
recent review of each card:

**SQL Server and standard SQL:**

```sql
WITH ranked_reviews AS (
    SELECT review_id,
           card_id,
           user_id,
           rating,
           reviewed_at,
           ROW_NUMBER() OVER (
               PARTITION BY card_id
               ORDER BY reviewed_at DESC
           ) AS rn
    FROM reviews
)
SELECT review_id, card_id, rating, reviewed_at
FROM ranked_reviews
WHERE rn = 1
ORDER BY card_id;
```

**Expected rows.**

| review_id | card_id | rating | reviewed_at |
|---:|---:|---:|---|
| 10002 | 1001 | 4 | 2026-01-21 10:00:00 |
| 10006 | 1002 | 2 | 2026-01-25 14:00:00 |
| 10004 | 1003 | 3 | 2026-01-23 12:00:00 |
| 10007 | 1004 | NULL | 2026-02-01 15:00:00 |

The window is partitioned by `card_id`, so the numbering restarts for each
card, and `ORDER BY reviewed_at DESC` puts the newest review first, so
`rn = 1` is the latest. Card 1005 has no reviews, so it has no partition and
no row. The filter `rn = 1` sits in the outer query because a window function
is evaluated after `WHERE`; the alias `rn` does not exist when the CTE's
`WHERE` would run, and the server rejects the reference. The result matches
the correlated subquery in Part 6, which returned reviews 10002, 10006,
10004, and 10007.

The tie rule is explicit in this form. If two reviews of a card share the
latest `reviewed_at`, `ROW_NUMBER` still returns one row and picks between
them arbitrarily. Add a unique tiebreaker such as `review_id DESC` inside the
`OVER` ordering to make the choice repeatable. If every tied row must survive,
use `RANK` below and keep rank 1.

Without `PARTITION BY`, the window is the whole result set and the numbering
runs from 1 to the row count.

### RANK and DENSE_RANK

`RANK()` and `DENSE_RANK()` also number rows by the `OVER` ordering, but they
give tied rows the same number. They differ in what happens after a tie:
`RANK` skips the numbers the tied rows would have used, so the sequence has
gaps; `DENSE_RANK` does not skip, so the sequence has none. The card count per
deck provides a tie: decks 101 and 103 each hold two cards.

**SQL Server and standard SQL:**

```sql
SELECT deck_id,
       COUNT(*) AS card_count,
       RANK() OVER (ORDER BY COUNT(*) DESC) AS rank_value,
       DENSE_RANK() OVER (ORDER BY COUNT(*) DESC) AS dense_rank_value
FROM cards
GROUP BY deck_id
ORDER BY card_count DESC, deck_id;
```

**Expected rows.**

| deck_id | card_count | rank_value | dense_rank_value |
|---:|---:|---:|---:|
| 101 | 2 | 1 | 1 |
| 103 | 2 | 1 | 1 |
| 102 | 1 | 3 | 2 |

The two tied decks share rank 1. `RANK` gives the next deck 3, because two
rows have already occupied positions 1 and 2; `DENSE_RANK` gives it 2 because
it counts distinct positions, not rows. Deck 104 is absent because `GROUP BY`
groups only the rows in `cards` and deck 104 has no cards (Part 4). The window
functions run over the grouped rows, which is why the `ORDER BY` inside
`OVER` can use the aggregate `COUNT(*)`; the window sees the result of
`GROUP BY`, not the raw table.

`ROW_NUMBER` would number the same three rows 1, 2, and 3, with the tied
decks ordered arbitrarily unless the `OVER` ordering names a tiebreaker. Pick
the function from the question: `ROW_NUMBER` to choose exactly one row,
`RANK` for competition ranking with gaps, and `DENSE_RANK` for positions with
no gaps.

### PARTITION BY

`PARTITION BY` divides the rows into independent windows before the function
runs. Each partition starts its numbering or total from scratch; without the
clause, every row is in one window. The partition columns and the `ORDER BY`
columns serve different purposes: the partition defines the groups, and the
order defines the sequence inside each group.

This query numbers the reviews twice, once across the whole table and once
within each card:

**SQL Server and standard SQL:**

```sql
SELECT review_id,
       card_id,
       reviewed_at,
       ROW_NUMBER() OVER (ORDER BY reviewed_at) AS overall_position,
       ROW_NUMBER() OVER (
           PARTITION BY card_id
           ORDER BY reviewed_at
       ) AS position_in_card
FROM reviews
ORDER BY reviewed_at;
```

**Expected rows.**

| review_id | card_id | reviewed_at | overall_position | position_in_card |
|---:|---:|---|---:|---:|
| 10001 | 1001 | 2026-01-20 09:00:00 | 1 | 1 |
| 10002 | 1001 | 2026-01-21 10:00:00 | 2 | 2 |
| 10003 | 1002 | 2026-01-22 11:00:00 | 3 | 1 |
| 10004 | 1003 | 2026-01-23 12:00:00 | 4 | 1 |
| 10005 | 1004 | 2026-01-24 13:00:00 | 5 | 1 |
| 10006 | 1002 | 2026-01-25 14:00:00 | 6 | 2 |
| 10007 | 1004 | 2026-02-01 15:00:00 | 7 | 2 |

The first window has no `PARTITION BY`, so it is one set of seven rows and the
review timestamps are strictly increasing, giving positions 1 to 7. The
second restarts at each card: review 10003 is the first review of card 1002
even though it is the third review overall, and review 10005 is the first of
card 1004 even though it is the fifth overall. Both position columns stay
beside every detail row; no row is collapsed.

Two ways to get this wrong: leave out `PARTITION BY` and compare positions
across groups that should be separate, or partition by a column that is unique
per row, such as `review_id`, which makes every window a single row and every
number 1.

### SUM OVER

A window aggregate computes the aggregate over the window and repeats it on
every row. `SUM(rating) OVER (PARTITION BY card_id)` is the card's total
rating attached to each review of that card. Unlike `GROUP BY`, it does not
reduce the result to one row per card.

**SQL Server and standard SQL:**

```sql
SELECT review_id,
       card_id,
       rating,
       SUM(rating) OVER (PARTITION BY card_id) AS card_rating_sum
FROM reviews
ORDER BY card_id, review_id;
```

**Expected rows.**

| review_id | card_id | rating | card_rating_sum |
|---:|---:|---:|---:|
| 10001 | 1001 | 5 | 9 |
| 10002 | 1001 | 4 | 9 |
| 10003 | 1002 | NULL | 2 |
| 10006 | 1002 | 2 | 2 |
| 10004 | 1003 | 3 | 3 |
| 10005 | 1004 | 5 | 5 |
| 10007 | 1004 | NULL | 5 |

The per-card totals add up to the Part 4 overall rating sum of 19: card 1001
sums to 9, card 1002 to 2, card 1003 to 3, and card 1004 to 5. `SUM` ignores
`NULL`, so the two unrated reviews contribute nothing: review 10003 shows the
card total of 2 even though its own rating is `NULL`, and review 10007 shows
5. The total repeats on every review row; the select list changed, not the
row count. A `GROUP BY` would return four rows and lose the individual
reviews.

Adding an `ORDER BY` inside `OVER` makes the sum cumulative, and the frame
says which rows the aggregate sees:

**SQL Server and standard SQL:**

```sql
SELECT review_id,
       card_id,
       reviewed_at,
       rating,
       SUM(rating) OVER (
           PARTITION BY card_id
           ORDER BY reviewed_at
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS running_rating_sum
FROM reviews
ORDER BY card_id, reviewed_at;
```

**Expected rows.**

| review_id | card_id | reviewed_at | rating | running_rating_sum |
|---:|---:|---|---:|---:|
| 10001 | 1001 | 2026-01-20 09:00:00 | 5 | 5 |
| 10002 | 1001 | 2026-01-21 10:00:00 | 4 | 9 |
| 10003 | 1002 | 2026-01-22 11:00:00 | NULL | NULL |
| 10006 | 1002 | 2026-01-25 14:00:00 | 2 | 2 |
| 10004 | 1003 | 2026-01-23 12:00:00 | 3 | 3 |
| 10005 | 1004 | 2026-01-24 13:00:00 | 5 | 5 |
| 10007 | 1004 | 2026-02-01 15:00:00 | NULL | 5 |

The frame `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` means "from the
first row of the partition through this row". Card 1001 reaches 9 at its
second review. Card 1002's first review has no rating, so its running sum is
`NULL` until review 10006 adds 2; the running sum of a set that contains only
`NULL` is `NULL`, not 0 (Part 4). The frame is standard SQL and the shape is
the same in SQL Server.

Without an explicit frame, an `ORDER BY` inside `OVER` still produces a
running aggregate, but the default frame is a `RANGE` frame that includes all
rows with the same `ORDER BY` value. With distinct timestamps here the two
frames agree; with tied timestamps they can produce different totals. State
the frame when the requirement depends on row-by-row accumulation, and name
the column that breaks ties.

### LAG and LEAD

`LAG(column, offset, default)` returns a value from an earlier row in the same
partition, and `LEAD` returns one from a later row. The offset defaults to 1.
The third argument is returned only when the requested row does not exist in
the partition. Both functions need an `ORDER BY` inside `OVER`; without a
defined order there is no previous or next row.

This query compares each review with the reviews before and after it on the
same card:

**SQL Server and standard SQL:**

```sql
SELECT review_id,
       card_id,
       reviewed_at,
       rating,
       LAG(rating, 1, 0) OVER (
           PARTITION BY card_id
           ORDER BY reviewed_at
       ) AS previous_rating,
       LEAD(rating, 1, 0) OVER (
           PARTITION BY card_id
           ORDER BY reviewed_at
       ) AS next_rating
FROM reviews
ORDER BY card_id, reviewed_at;
```

**Expected rows.**

| review_id | card_id | reviewed_at | rating | previous_rating | next_rating |
|---:|---:|---|---:|---:|---:|
| 10001 | 1001 | 2026-01-20 09:00:00 | 5 | 0 | 4 |
| 10002 | 1001 | 2026-01-21 10:00:00 | 4 | 5 | 0 |
| 10003 | 1002 | 2026-01-22 11:00:00 | NULL | 0 | 2 |
| 10006 | 1002 | 2026-01-25 14:00:00 | 2 | NULL | 0 |
| 10004 | 1003 | 2026-01-23 12:00:00 | 3 | 0 | 0 |
| 10005 | 1004 | 2026-01-24 13:00:00 | 5 | 0 | NULL |
| 10007 | 1004 | 2026-02-01 15:00:00 | NULL | 5 | 0 |

Read the edge values carefully. The first review of each card has no earlier
row, so `previous_rating` is the supplied default 0; the last review of each
card has no later row, so `next_rating` is 0. Review 10006 is the exception
that proves the rule: its `previous_rating` is `NULL`, not 0, because review
10003 exists and its rating is `NULL`. The third argument fills a missing
row, not a missing value. Review 10005 shows a `NULL` next rating for the same
reason: review 10007 exists. The 0 sentinel is safe here only because
`ck_reviews_rating` forbids a real rating of 0 (Part 8); if 0 were valid, the
column could not tell "no row" from "a row whose value is 0".

Set the offset to look further back, such as `LAG(rating, 2, 0)` for the
review before the previous one. If the default is omitted, a missing row
returns `NULL`, the same value a real `NULL` rating produces. That ambiguity
is often fine in a report and never fine in a check that must tell the two
cases apart.

Typical uses are comparing consecutive ratings to find a drop, checking that
timestamps increase, finding the first time a state changed, and measuring a
gap between events. Because the functions read another row, the order must be
deterministic: add a unique tiebreaker to the `OVER` ordering when timestamps
can repeat.

### Release QA Use

- Use `ROW_NUMBER` with a filter for the latest or first record per key.
  Partition by the key, order by the timestamp with a unique tiebreaker, and
  filter the result in an outer query or CTE.
- State the tie policy before writing the query. `ROW_NUMBER` chooses one
  row, `RANK` keeps every tied row, and `DENSE_RANK` ranks distinct values. A
  check that expects one row per key fails visibly when it uses `RANK` and the
  data contains a tie.
- Use `SUM OVER` when a report or a bug attachment needs the detail rows and
  the group total together. The window preserves the individual reviews, and a
  running total shows where a value changed.
- Use `LAG` and `LEAD` to test ordering rules: timestamps that must increase,
  duplicate events, a rating that changes without an intervening action, or a
  sequence that must advance by one. Decide whether a `NULL` means "no row" or
  "a row with a `NULL` value", and pass a default when the difference matters.
- Filter window results outside `WHERE`. Apply the condition in an outer query
  or CTE, and use `HAVING` for a condition on a grouped aggregate.
- Window functions run after `GROUP BY`, so a window over `COUNT(*)` or
  `SUM(...)` operates on the grouped rows. That is how a rank-per-deck report
  combines a group total with a rank without a second join.
- Make the check reproducible: name a unique `ORDER BY` key inside `OVER`,
  select the ordering columns, and state the partition in the bug report. A
  result chosen from an arbitrary tie cannot be reproduced.

### Watch-outs

- Window functions are evaluated after `WHERE`, `GROUP BY`, and `HAVING`, and
  before `ORDER BY`. They cannot appear in `WHERE`; filter the result in an
  outer query or CTE.
- `ROW_NUMBER` gives every row a different number but breaks ties
  arbitrarily. Add a unique tiebreaker inside `OVER` when the chosen row must
  be repeatable.
- `RANK` leaves gaps after a tie and `DENSE_RANK` does not. Choose the one the
  requirement describes, and write down the tie rule.
- Without `PARTITION BY`, the window is the whole result. Partitioning by a
  unique column produces one-row windows.
- `SUM(...) OVER (...)` repeats the total on every row; it does not collapse
  rows. A one-row-per-group report still needs `GROUP BY`.
- With an `ORDER BY`, the default frame is a `RANGE` frame that includes
  peers; it can differ from a row-by-row `ROWS` frame when the ordering ties.
- `LAG` and `LEAD` need `ORDER BY` inside `OVER`. The default argument applies
  only when the row is missing; a stored `NULL` stays `NULL`.
- A window-function alias cannot be used later in the same `SELECT` list or
  in `WHERE`. Wrap the first stage in a CTE when the logic needs two.
- SQL Server requires `ORDER BY` in `OVER` for `ROW_NUMBER`, `RANK`,
  `DENSE_RANK`, `LAG`, and `LEAD`; `SUM` accepts a window without one.

## Part 10 — SQL Server Dialect and Tuning

Parts 1 to 9 introduced SQL Server forms first and standard SQL forms second,
one feature at a time. This part gathers those differences into one translation
table, then turns to performance: how a SQL Server execution plan is read, how
one execution is measured, and which query and index shapes let the optimizer
use an index.

Two rules frame the part. A translation is not a guarantee: every row of the
dialect table is a place where the result must be rechecked, not only the
spelling. And a tuning claim needs four things — the query, the predicate, the
index, and the measurement — where the measurement is an execution plan or a
statistics comparison. "Faster" without that evidence is a guess, and a guess
is not a release finding.

No database is installed in this repository, and no statement here was
executed. The tuning examples describe what to capture and how to compare it;
they do not report readings from the sample rows. The sample tables are also
tiny — five cards and seven reviews — so the optimizer may scan even when an
index exists. Evidence for an index or a rewrite has to come from a realistic
copy of the data.

### SQL Server vs Standard SQL

The table puts SQL Server first and standard SQL second. Each row is a syntax
translation; the paragraphs after the table cover the rows where the
translation changes behaviour, not only spelling.

| What you need | SQL Server (T-SQL) | Standard SQL |
|---|---|---|
| Limit the result | `SELECT TOP (n) ...`, or `ORDER BY ... OFFSET m ROWS FETCH NEXT n ROWS ONLY` | `SELECT ... FETCH FIRST n ROWS ONLY`; `OFFSET ... FETCH NEXT` is also standard |
| Current date and time | `GETDATE()` (a `DATETIME`) or `SYSDATETIME()` (a `DATETIME2`), server local time | `CURRENT_TIMESTAMP` |
| Replace a `NULL` | `ISNULL(expr, replacement)` | `COALESCE(a, b, ...)` |
| Concatenate text | `+`, or `CONCAT(a, b, ...)` | `a \|\| b` |
| Generate a key | `IDENTITY(1,1)` | `GENERATED ALWAYS AS IDENTITY` (or explicit IDs) |
| Store a boolean | `BIT` | `BOOLEAN` |
| Store text | `NVARCHAR(n)` | `VARCHAR(n)` |
| Store a date and time | `DATETIME2` | `TIMESTAMP` |
| Choose a value conditionally | `IIF(condition, a, b)` | `CASE WHEN condition THEN a ELSE b END` |
| Do date arithmetic | `DATEADD(part, n, date)`, `DATEDIFF(part, start, end)` | `date + INTERVAL 'n' DAY`; subtracting two timestamps gives an interval |
| Aggregate rows into text | `STRING_AGG(expr, ',')` | No single standard equivalent in this guide |

**`TOP` and `FETCH`.** `TOP (n)` is SQL Server-only and belongs in the
`SELECT` list. `OFFSET ... FETCH NEXT` is standard and SQL Server accepts it,
but SQL Server requires `ORDER BY` with it. `FETCH FIRST n ROWS ONLY` is the
shortest standard form used in this guide. A limit without a deterministic
`ORDER BY` returns an arbitrary set; add a unique tiebreaker when the sample
must be reproducible (Part 2).

**Watch the name `TIMESTAMP`.** In SQL Server, `TIMESTAMP` is a synonym for
`ROWVERSION`: an automatically generated binary value used for change
tracking, not a date or a time. A SQL Server column declared `TIMESTAMP` holds
no date, and comparing it with a date forces a conversion that is either an
error or a meaningless result. Use `DATETIME2` for a date and time on SQL
Server; the shared SQL Server schema does. Standard SQL's `TIMESTAMP` is the
date and time type, which is why the two schema versions use different type
names for the same idea.

**Concatenation and `NULL`.** SQL Server's `+` operator returns `NULL` when
either operand is `NULL`. `CONCAT` treats `NULL` as an empty string. Standard
SQL's `||` returns `NULL` when either side is `NULL`, so it matches `+`, not
`CONCAT`. Part 2's label for user 3, whose `display_name` is `NULL`, is the
test case: a translation from `CONCAT` to `||` changes the label from text with
an empty name part to `NULL`. To keep the `CONCAT` behaviour in standard SQL,
wrap a nullable argument in `COALESCE(display_name, '')`; to get the `||`
behaviour in SQL Server, use `+`, remembering that `+` is also arithmetic.

**`ISNULL` and `COALESCE`.** `ISNULL(expr, replacement)` takes exactly two
arguments and is SQL Server-only. `COALESCE(a, b, ...)` is standard, accepts
any number of arguments, and also works in SQL Server, which makes it the
portable choice. Their result types differ: `ISNULL` follows the first
argument's type (except when the first argument is the literal `NULL`), so a
replacement longer than the first argument can be truncated, while `COALESCE`
returns the type chosen by data type precedence across all arguments. For a
check that compares labels, a truncation or a type change is a result
difference, not formatting.

**`GETDATE`, `SYSDATETIME`, and `CURRENT_TIMESTAMP`.** `GETDATE()` returns a
`DATETIME`; `SYSDATETIME()` returns a `DATETIME2` with more fractional-second
precision. Both return the server's local clock, not the client's.
`CURRENT_TIMESTAMP` is standard and, in SQL Server, is equivalent to
`GETDATE()`. SQL Server evaluates `GETDATE()` and `SYSDATETIME()` once per
statement, so every row of one statement sees the same value; the risk is
across separate statements, where the clock moves. When a check makes several
statements that must agree on a boundary, capture the time into a variable and
compare every statement against it, or compare against a known literal. For
UTC, Part 8 used `SYSUTCDATETIME()`; check the target product's own UTC
function before translating that call.

**`IDENTITY` and explicit IDs.** `IDENTITY(1,1)` makes SQL Server generate the
next value on an insert. The standard spellings are `GENERATED ALWAYS AS
IDENTITY` and `GENERATED BY DEFAULT AS IDENTITY`. The shared schema uses
explicit IDs instead, because a known ID makes a sample row, a foreign-key
check, and a bug report reproducible. An identity column generates a different
ID on every test run, so a check that hard-codes an ID must read the generated
value back first.

**`IIF` and `CASE`.** `IIF(condition, a, b)` is SQL Server shorthand for a
two-branch `CASE`. `CASE WHEN condition THEN a ELSE b END` is standard and
works in SQL Server too, so `CASE` is the portable form. A `NULL` condition is
not TRUE, so both forms take the false branch; `IIF` takes exactly three
arguments, so use `CASE` when the logic needs more than one condition.

**`DATEADD`, `DATEDIFF`, and intervals.** `DATEADD(day, 7, created_at)` adds
seven days. The standard form adds an interval:
`created_at + INTERVAL '7' DAY`. Subtraction differs more:
`DATEDIFF(day, start, end)` counts day boundaries crossed, not complete days,
so `DATEDIFF(day, '2026-01-01 23:59', '2026-01-02 00:01')` is 1 even though
one minute passed. Standard timestamp subtraction returns an interval, which
measures elapsed time. For a duration check, state the part and the boundary
rule; for exact elapsed time, subtract in the application or use the smallest
relevant part and test the boundary.

**`STRING_AGG`.** `STRING_AGG(expr, separator)` aggregates rows into one
string, with an optional `WITHIN GROUP (ORDER BY ...)` for order. No single
standard equivalent is used in this guide; other products have their own
aggregate (Oracle's `LISTAGG`, MySQL's `GROUP_CONCAT`), spelled differently. A
query that uses `STRING_AGG` is a portability point, and a check that depends
on the separator or the order must state both.

**The type rows.** `NVARCHAR(n)` stores Unicode text; `VARCHAR(n)` uses the
database's code page. `BIT` stores `0` or `1`, not `TRUE` or `FALSE`, and a
report that displays a boolean must translate it. `DATETIME2` is the SQL Server
date and time type; `TIMESTAMP` is not (see the warning above). The standard
schema uses `VARCHAR`, `BOOLEAN`, and `TIMESTAMP`; the SQL Server schema uses
`NVARCHAR`, `BIT`, and `DATETIME2`.

### Reading Execution Plans

An execution plan is the set of operators SQL Server uses to run one
statement. Each operator reads, joins, sorts, or returns rows, and the arrows
show rows moving from the data sources to the result. The plan is the evidence
for how a query was answered; the result rows are not.

**Estimated and actual plans.** SQL Server can produce an estimated plan
without running the statement, and an actual plan while it runs. The estimated
plan shows the operators, estimated row counts, and the warnings the optimizer
can predict without running the statement, such as an implicit conversion or a
missing-index suggestion. The actual plan adds actual row counts, the number of
executions of each operator, and run-time warnings such as a tempdb spill. The
percentages beside operators are estimated costs, even in an actual plan; they
locate expensive operators but are not measured time. An estimated plan is
safe to capture on a production server because it does not execute; an actual
plan of an `INSERT`, `UPDATE`, or `DELETE` does execute the change, so capture
it only where the change is allowed and can be rolled back.

**Read it from the result back to the data.** Start at the leftmost operator,
the one that returns the result, and follow the arrows to the right. A thicker
arrow means more rows. Click an operator to see its properties: the object
(table or index), the seek predicates, the residual predicate,
`Number of Rows Read`, `Actual Number of Rows`, `Estimated Number of Rows`,
and `Number of Executions`.

| Operator | What it means | What to check |
|---|---|---|
| Table Scan | Reads every row of a heap. | Whether an index could seek the predicate; whether most rows are genuinely needed. |
| Index Scan | Reads the entries of an index. | Whether a predicate could seek a range; rows read versus rows returned. |
| Index Seek | Uses the index keys to locate a range. | Which predicate supplied the seek; a seek that reads many rows to return few has a residual predicate. |
| Key Lookup / RID Lookup | For each row found in a nonclustered index, fetches the remaining columns from the table. | `Number of Executions`; whether the query is covered. |
| Sort | Orders rows for `ORDER BY`, `DISTINCT`, or a merge join. | Whether an index's key order could remove the sort; tempdb spill warnings. |
| Hash Match | Builds a hash table for a join or aggregate. | Estimated versus actual rows; memory grant warnings. |
| Nested Loops | Runs the inner input once per outer row. | Executions of the inner side; a loop over thousands of rows is suspect. |
| Filter | Applies a predicate after rows are read. | Why the predicate did not seek; rows read versus rows returned. |

**Estimated versus actual rows.** The most useful comparison is the estimated
row count on an operator against the actual row count. A large gap is the
first thing to explain: stale statistics, a predicate the optimizer cannot
estimate, a correlated expression, or parameter sniffing (below). The gap
often explains a join order, a scan choice, or a memory grant. Read it before
proposing an index.

**Warnings.** A yellow triangle on an operator is a warning. Common ones are
an implicit conversion, a tempdb spill from a sort or hash, and a join without
a predicate. Read the tooltip and put its text in the ticket; the warning
often names the column and the conversion that the plan could not use.

**Missing-index suggestions.** A plan may add a green `Missing Index` hint that
names a table, the equality and inequality columns it would use, and the
included columns. Treat it as a hint, not a command: it is generated for this
one statement and this one data set, several hints can propose overlapping or
redundant indexes, and it does not price the write and storage cost. Copy the
suggested definition into a scratch copy, measure the logical reads with and
without it, and keep it only if the reads improve and the team accepts the
write cost.

**A plan is not a correctness check.** A fast query can return the wrong rows,
and a plan can be efficient for the wrong question. Check the result against
the requirement separately, then use the plan to explain the cost.

**Scans and seeks.** A scan is not automatically a problem and a seek is not
automatically a win. A scan is efficient when the query needs most of the rows
or the table is small. A seek followed by many key lookups can cost more than
a scan, because each lookup fetches a row from the table. Read the row counts
and the lookup executions, not only the operator name.

**Sorts and hashes.** A Sort with a tempdb spill warning or a Hash Match with
a large memory grant can dominate a statement. An index in the right key order
can remove a Sort, but a sort-free plan is not always possible. Compare the
cost and the reads rather than assuming that either operator is bad.

### Measuring with STATISTICS IO and TIME

`SET STATISTICS IO ON` and `SET STATISTICS TIME ON` make SQL Server report
what one execution did. They are session settings: they stay on for later
statements until set off, and they return messages, not rows.

**SQL Server:**

```sql
SET STATISTICS IO ON;
SET STATISTICS TIME ON;

SELECT card_id, front
FROM cards
WHERE deck_id = 103
ORDER BY created_at;

SET STATISTICS IO OFF;
SET STATISTICS TIME OFF;
```

The batch above is the shape of the measurement; no database is installed
here, and no output is claimed. Read the `STATISTICS IO` message for `cards`:

- **Scan count** is the number of scans or seeks the plan performed against
  the table or index, not a count of rows, pages, or table opens. A nested
  loops join can run an inner seek once per outer row, so a count above 1 is a
  clue to read the plan.
- **Logical reads** is the number of 8 KB pages read from the buffer cache.
  This is the comparison metric: it counts the pages the plan touched, so it
  does not depend on whether they were already cached or on how busy the
  server was. Compare logical reads for the same query and data before and
  after a change.
- **Physical reads** is pages read from disk, and **read-ahead reads** is
  pages prefetched. Both depend on the cache state, so a cold first run and a
  warm second run are not comparable. Compare logical reads instead, or state
  the cache state deliberately.
- **Lob logical reads** counts large-object pages; this schema has none, so
  expect zero.

The `STATISTICS TIME` message has two parts. The parse and compile line is the
cost of turning the text into a plan; the execution line reports CPU time and
elapsed time. CPU time is processor work summed across threads; elapsed time
is wall clock, including waits and other load. Use CPU as the work measure,
logical reads as the page measure, and note elapsed time as the user-visible
result; do not treat one as the other. The parse and compile line is also
where the per-call cost of `OPTION (RECOMPILE)` appears.

**The comparison method.** Use the same query, the same data, and the same
cache state, and change one thing at a time. Capture the actual plan and the
`STATISTICS IO`/`TIME` messages before the change, apply one change (a rewrite
or an index), and capture them again on the same dataset. Keep the first run
separate from the repeat: the first may do physical reads, and the second may
be fully cached. State the row counts, the cache state, and the server
conditions in the ticket. On the sample tables the counts are tiny and the
optimizer may scan anyway; a comparison at five rows does not predict
production.

**What the numbers cannot tell you.** Logical reads do not measure waits,
blocking, or network time; a query with low reads can still be slow because it
waits on a lock. They also do not measure correctness. A query that returns
the wrong rows can have excellent reads.

### SARGable Predicates

A predicate is **SARGable** when the optimizer can use an index to search for
the matching rows instead of reading every row and testing the predicate. The
term comes from "search argument able". The usual shape is a bare column on
one side of the comparison and a constant, variable, or parameter on the
other; when a function or a conversion wraps the column, the sorted index
cannot be used as the search argument.

The four checks below cover most slow release queries. Each names the query,
the predicate, the index, and the measurement; none promises a speedup,
because the result depends on data volume, selectivity, and the plan.

**1. Use a date range instead of a function on the date.** The first query
applies `YEAR` to the indexed column, so the optimizer cannot seek on
`created_at`:

**SQL Server:**

```sql
SELECT card_id
FROM cards
WHERE YEAR(created_at) = 2026;
```

The second query compares the column itself with a half-open range, which can
be a seek:

**SQL Server:**

```sql
SELECT card_id
FROM cards
WHERE created_at >= '2026-01-01'
  AND created_at < '2027-01-01';
```

Index, for both queries to consider:

**SQL Server:**

```sql
CREATE NONCLUSTERED INDEX ix_cards_created_at
    ON cards (created_at);
```

The predicate is the difference: `YEAR(created_at) = 2026` computes a value
from the indexed column for every row, while the range leaves `created_at`
bare. With the index, the range form can produce an Index Seek; the function
form produces an Index Scan (or a table scan) with a residual filter.
Measurement: with `SET STATISTICS IO ON`, compare logical reads for `cards`,
and read the operator in the actual plan (Index Scan versus Index Seek). Both
statements return all five cards, which were all created in January 2026. The
range also fixes a correctness bug: `BETWEEN '2026-01-01' AND '2026-12-31'`
stops at midnight on December 31 and misses the rest of that day, while
`< '2027-01-01'` includes the whole year.

**2. Do not start a `LIKE` pattern with a wildcard.** A leading wildcard gives
the index no starting point, so every entry must be tested:

**SQL Server and standard SQL:**

```sql
SELECT card_id, front
FROM cards
WHERE front LIKE '%cell%';
```

An anchored pattern can be turned into a range:

**SQL Server and standard SQL:**

```sql
SELECT card_id, front
FROM cards
WHERE front LIKE 'What%';
```

Index, for the anchored form to consider:

**SQL Server:**

```sql
CREATE NONCLUSTERED INDEX ix_cards_front
    ON cards (front);
```

The predicate is the pattern: `%cell%` has no anchor, so the plan scans the
index or the table; `What%` has a prefix, so the plan can seek the matching
range. Measurement: read the actual plan for an Index Scan/Table Scan versus
an Index Seek, and compare logical reads for `cards` and rows read versus rows
returned. `%cell%` returns card 1001; `What%` returns all five cards. A
substring search is a real requirement that a B-tree index cannot answer;
full-text search is a different feature, and the scan may be the honest plan
for the requirement.

**3. Do not put a function on the indexed column.** The cast is computed for
every row before the comparison, so the clustered key cannot be seeked:

**SQL Server:**

```sql
SELECT card_id
FROM cards
WHERE CAST(card_id AS NVARCHAR(10)) = N'1001';
```

The bare comparison can seek the clustered primary key:

**SQL Server and standard SQL:**

```sql
SELECT card_id
FROM cards
WHERE card_id = 1001;
```

The predicate is the difference: the cast wraps `card_id`, which is the
clustered key; the bare equality leaves it alone. The first plan shows a
Clustered Index Scan with a Compute Scalar or Filter; the second can show a
Clustered Index Seek. Measurement: the operator in the actual plan and logical
reads for `cards`. Both return card 1001. A function on the constant side is
fine: `WHERE card_id = CAST(N'1001' AS INT)` converts one value rather than
every row.

**4. Align data types to avoid an implicit conversion.** SQL Server converts
the side with the lower data type precedence. When that side is the column, an
index on the column cannot be seeked. Here the variable is `DECIMAL`, which has
higher precedence than the `INT` column, so `deck_id` is the column that
converts:

**SQL Server:**

```sql
DECLARE @deck_id DECIMAL(10, 0) = 101;
SELECT card_id
FROM cards
WHERE deck_id = @deck_id;
```

Declaring the variable with the column's type keeps the conversion on the
argument side:

**SQL Server:**

```sql
DECLARE @deck_id INT = 101;
SELECT card_id
FROM cards
WHERE deck_id = @deck_id;
```

The index is `ix_cards_deck_id` on `cards (deck_id)` from Part 8. The predicate
is `deck_id = @deck_id`: in the first query the `INT` column is converted to
`DECIMAL` for every row, so the index on `deck_id` cannot be seeked; in the
second the variable matches the column and the index can be seeked. The first
plan shows the conversion on `deck_id` and, in current versions, may add a
conversion warning; the second does not. Measurement: the actual
plan and `STATISTICS IO` logical reads for `cards`. Both return cards 1001 and
1002. If a third-party tool sends a `DECIMAL`, casting the argument to `INT`
also moves the conversion off the column, but only when the value is known to
be a whole number.

**The claim rule.** Every check above names the query, the predicate, the
index, and the measurement. None of them says "this is faster": the evidence
is the plan and the logical reads on the same data, and the sample tables are
too small to supply it.

### Indexes and Covering Queries

Part 8 defined the structures: a clustered index's leaf level is the table's
data, a nonclustered index is a separate structure with sorted keys and a row
locator, and a covering index contains every column a query reads. This
section uses those structures to explain two plans: a seek that reads the
right rows in the right order, and a seek that has to visit the table for
columns the index does not hold.

**Key order: equality first, then the order column.** An index on
`(card_id, reviewed_at)` sorts by `card_id` first and by `reviewed_at` within a
card. The query below filters on the first key and orders by the second:

**SQL Server:**

```sql
CREATE NONCLUSTERED INDEX ix_reviews_card_reviewed
    ON reviews (card_id, reviewed_at)
    INCLUDE (user_id, rating);
```

**SQL Server and standard SQL:**

```sql
SELECT review_id, user_id, rating
FROM reviews
WHERE card_id = 1001
ORDER BY reviewed_at;
```

Expected rows: review 10001 with rating 5, then review 10002 with rating 4.
`card_id = 1001` is an equality on the leftmost key, so the seek goes straight
to the card's entries; those entries are ordered by `reviewed_at`, so the
`ORDER BY` needs no Sort. `user_id` and `rating` are included, and `review_id`
is the clustered key, which every nonclustered index on this table carries.
The query is covered. Measurement: the actual plan should show an Index Seek
with no Key Lookup and no Sort; `STATISTICS IO` reports the logical reads for
`reviews`. Compare that with the plan for the same query before the index:
capture both, on the same data. On seven reviews the optimizer may scan; the
comparison becomes meaningful with volume.

**The leftmost key limits the seek.** The same index does not help a query
that filters only on the second key:

**SQL Server and standard SQL:**

```sql
SELECT review_id
FROM reviews
WHERE reviewed_at >= '2026-01-24';
```

There is no predicate on `card_id`, so the index cannot seek its `reviewed_at`
entries; the plan may scan the index or the table and filter. An index with
`reviewed_at` first would give the predicate a seek. Measurement: the actual
plan (Index Scan versus Index Seek) and logical reads for `reviews`. The
result is reviews 10005, 10006, and 10007. The rule is the leftmost prefix: an
index can seek on a prefix of its keys, starting with the first.

**Key lookup and covering.** This illustration assumes the narrow index
`ix_cards_deck_id` from Part 8 and that Part 8's wider
`ix_cards_deck_created ON cards (deck_id, created_at) INCLUDE (front, back)`
has not been created. If the wider index exists, the query below is already
covered, so do not add another index for it. Under the narrow-index
assumption, the index lets the query find the two cards in deck 101, but
`front` is not in the index:

**SQL Server and standard SQL:**

```sql
SELECT card_id, front
FROM cards
WHERE deck_id = 101;
```

`card_id` is the clustered key, so it is present in the index; `front` is not.
The plan may show an Index Seek followed by a Key Lookup for each returned
row, or the optimizer may choose a scan on five rows. Measurement: read the
actual plan for a Key Lookup, and check its `Number of Executions` against the
number of rows the seek returned; check the logical reads for `cards`. The Key
Lookup's cost grows with the number of rows, which is why a covering index is
worth considering for a query that returns many rows.

If the wider Part 8 index does not exist, replace the narrow index: drop
`ix_cards_deck_id` with approval and create one that adds `front` to the
leaf. Do not keep both, because the two have the same key and differ only in
the included column:

**SQL Server:**

```sql
CREATE NONCLUSTERED INDEX ix_cards_deck_front
    ON cards (deck_id)
    INCLUDE (front);
```

Under the narrow-index assumption, the same query is now answered from the
index alone: no Key Lookup, and the logical reads for `cards` count only the
index pages. Part 8's wider `ix_cards_deck_created` covers this query too, and
it covers `SELECT *` on `cards`; if it exists, use it and add nothing.
Measurement: compare the actual plans and the logical reads before and after,
on the same data. The `INCLUDE` columns are stored at the leaf and cannot be
used to seek or to order rows; they exist so the query can read their values
without visiting the table.

**Write cost.** Every index is maintained by every `INSERT`, `UPDATE`, and
`DELETE` on the table. The covering index above stores the `front` text for
every card, so it duplicates that text, grows with it, and must be updated
whenever `front` changes. More indexes mean more work per write, more storage,
and more log. A new index also changes the optimizer's choices for every query
on the table. Propose an index with the query, the plan, and the reads that
justify it, and name the write cost; get approval before creating or dropping
one on a shared or production system (Part 8).

### Query Habits

These habits either prevent a wrong result or reduce work. The performance
habits still need the same measurement as the rest of the part.

**Avoid `SELECT *`.** Name the columns the check needs. A result whose column
list is fixed is stable when a release adds a column, and a query that names
its columns can be covered by a narrower index. With the narrow
`ix_cards_deck_front` from the previous section, `SELECT card_id, front FROM
cards WHERE deck_id = 101` is covered: `card_id` is the clustered key,
`deck_id` is the key, and `front` is included. `SELECT *` also reads `back`
and `created_at`, so the narrow index cannot cover it; the plan needs a Key
Lookup (or a scan) and touches more pages. Part 8's wider
`ix_cards_deck_created` is the exception on this table: it includes `front`
and `back` and carries `created_at` and `card_id`, so it can cover `SELECT *`
on `cards`; that is a property of a wide index, not a benefit of `SELECT *`.
The rule is about the query and the index together: `SELECT *` prevents a
narrow covering index, and an index containing every selected column can
still cover it. Measurement: the actual plan (Key Lookup present or absent)
and the logical reads for `cards`. On five cards the optimizer may scan either
way; the difference is the columns and the lookup count at volume.

**Use `UNION ALL` unless deduplication is required.** `UNION` removes
duplicate rows from the combined result; `UNION ALL` keeps every row and
concatenates the inputs. The requirement decides which is correct. The QA
staging table `legacy_users` (Part 11) holds user 1 and user 2 again, plus a
second Alice row for user 3 with the same email:

**SQL Server and standard SQL:**

```sql
SELECT user_id, email FROM users
UNION ALL
SELECT user_id, email FROM legacy_users;
```

This returns 9 rows: 5 users and 4 legacy rows, including the repeated IDs and
the duplicate email. `UNION` returns 7 rows, because it removes rows that are
identical in every selected column; the two Alice emails survive because their
`user_id` values differ. Measurement: the `UNION` plan contains a Distinct
Sort or a Hash Match aggregate, the `UNION ALL` plan does not; compare logical
reads and row counts. If the question is "one row per value", `UNION` is
right; if duplicates are expected or harmless, `UNION ALL` avoids the
deduplication work. The recheck is the row count: 9 versus 7.

**Prefer `EXISTS` to `NOT IN` when `NULL` is possible.** Part 3 showed the
trap: if the subquery returns a `NULL`, `NOT IN` compares every outer value
with `NULL`, and the result is UNKNOWN, so the query returns no rows.
`NOT EXISTS` asks the question as existence:

**SQL Server and standard SQL:**

```sql
SELECT c.card_id
FROM cards AS c
WHERE NOT EXISTS (
    SELECT 1
    FROM reviews AS r
    WHERE r.card_id = c.card_id
);
```

This returns card 1005, the card without reviews. The subquery's `card_id` is
`NOT NULL` here, so `NOT IN` would also return the right row in this case; the
habit matters when the column is nullable or the subquery is not under your
control. `EXISTS` asks whether at least one row matches, so the engine can
stop at the first match; the `NOT EXISTS` plan may show an anti semi join.
Measurement: compare the actual plans and logical reads, but decide
correctness first. The
select list of an `EXISTS` subquery is irrelevant to the result; `SELECT 1`
and `SELECT *` are equivalent for existence.

**Filter rows in `WHERE`, not `HAVING`.** `WHERE` filters rows before grouping;
`HAVING` filters groups after. A predicate on a grouping column can be written
either way, and the result is the same:

**SQL Server and standard SQL:**

```sql
SELECT card_id, COUNT(*) AS review_count
FROM reviews
WHERE card_id = 1001
GROUP BY card_id;
```

The `HAVING card_id = 1001` version returns the same row, 1001 with 2 reviews,
but it filters after the aggregate. The `WHERE` form states the intent and
gives the optimizer a row predicate it can use before grouping. Measurement:
compare the actual plans and logical reads; if the plans are identical, the
rewrite changed nothing, which is a valid finding. Part 4 covers `HAVING`.

**Do not use `WITH (NOLOCK)` as a tuning fix.** `WITH (NOLOCK)` is a SQL Server
table hint equivalent to `READUNCOMMITTED` for that reference:

**SQL Server:**

```sql
SELECT COUNT(*) AS card_count
FROM cards WITH (NOLOCK);
```

The hint lets the statement skip shared locks, but it can read uncommitted
rows that later roll back, read the same row twice or miss a row when pages
move during a scan, and return a count that was never true at any single
moment. `WITH (NOLOCK)` is a correctness risk, not a tuning fix. It also does
not guarantee zero blocking: a schema change can still block the reader. For
release evidence, run the check under the default isolation level, or at a
level you name, and report that level. If you must use the hint on a busy
system, label the result provisional and rerun before filing. The standard
defines isolation levels but no table hint, so `WITH (NOLOCK)` is T-SQL.

### Parameter Sniffing and OPTION (RECOMPILE)

A parameterized statement is compiled into a plan, and SQL Server can cache
that plan for reuse. The optimizer estimates row counts from the parameter
values supplied at compilation, and those estimates drive the join order, the
choice between a seek and a scan, and the memory grant. If the first call's
values are atypical, the cached plan can be a poor fit for later calls with
different values. That is **parameter sniffing**.

The statement below is the shape the application sends, with `@card_id`
supplied as a parameter (a prepared statement or a procedure; this guide does
not define the procedure):

**SQL Server:**

```sql
SELECT review_id, rating
FROM reviews
WHERE card_id = @card_id
ORDER BY reviewed_at;
```

With the `ix_reviews_card_reviewed` index from the previous section, one plan
might suit a card with a handful of reviews and be the wrong choice for a card
with thousands, or the reverse. The seven sample reviews cannot reproduce that
difference; the scenario needs production-like skew. SQL Server 2022's
Parameter Sensitive Plan optimization can keep more than one plan variant for
a statement whose values are skewed, when the database compatibility level
enables it; it reduces the problem for some queries, but it does not replace
the measurement.

**Evidence for sniffing.** Run the same statement with at least two parameter
values: one typical and one extreme. Read the actual plan for each execution.
The sign is a large gap between the plan's `Estimated Number of Rows` (from
the value used at compilation) and `Actual Number of Rows` (from the current
value), with the same cached plan shape for both. `SET STATISTICS IO ON` and
`SET STATISTICS TIME ON` then show the logical reads and CPU time for each
value. A claim of sniffing needs that comparison; a single slow execution does
not prove it.

**`OPTION (RECOMPILE)` as a targeted fix.** The hint makes SQL Server compile
the statement on each execution with the current parameter values, and the
plan is not cached for that statement:

**SQL Server:**

```sql
SELECT review_id, rating
FROM reviews
WHERE card_id = @card_id
ORDER BY reviewed_at
OPTION (RECOMPILE);
```

Each execution gets a plan fitted to its own value. The cost is a compile on
every execution; the parse and compile line of `STATISTICS TIME` shows it. Use
the hint for the one statement whose cached plan the evidence shows is wrong
for the values in use, not as a default on every query and not for a statement
executed thousands of times per second. It is a T-SQL query hint with no
standard equivalent. It also treats the symptom rather than the distribution:
an index, refreshed statistics, or a rewrite may be the better fix, and each
needs its own measurement.

### Release QA Use

- When a release check is slow, capture the query text, its parameter values,
  the actual plan, the index definitions, the `STATISTICS IO` logical reads,
  and the `STATISTICS TIME` CPU time. Attach them to the ticket; a claim
  without them is not actionable.
- Compare the same query and data before and after one change, and state the
  row count and cache state. Do not compare a cold first run with a warm
  second run, and do not call a five-row result a performance finding.
- Use the dialect table when translating a check, then verify the row count,
  not only that the statement parses. The `NULL` rules for `+`, `CONCAT`,
  `ISNULL`/`COALESCE`, and `TIMESTAMP` change results, not just syntax.
- Review a slow predicate against the four SARGable shapes before proposing
  an index: a date range, no leading wildcard, no function on the column, and
  aligned data types. Name the index and the measurement in the proposal.
- Propose a covering index with the query, the plan, the logical reads before
  and after, and the write cost. Get approval before creating or dropping an
  index on a shared or production system (Part 8).
- Use `UNION ALL` when duplicates are expected or harmless and `UNION` when
  the requirement is distinct rows. Use `EXISTS`/`NOT EXISTS` for exclusion
  checks over nullable columns; check the row count as well as the plan.
- Treat a parameter-sniffing plan as a hypothesis until the statement is
  measured with at least two parameter values. If the evidence supports it,
  propose `OPTION (RECOMPILE)` for that one statement and record the compile
  cost.
- Do not use `WITH (NOLOCK)` to make a check finish. A count that can read
  uncommitted, duplicated, or missing rows is not evidence; record the
  isolation level used for any release result.
- Report the before and after values for logical reads and CPU time on the
  same dataset. "Faster" without them is not a finding, and this guide's tiny
  sample tables cannot supply them.

### Watch-outs

- SQL Server `TIMESTAMP` is `ROWVERSION`, not a date or time. Use `DATETIME2`;
  a `TIMESTAMP` column cannot store the `created_at` values in this guide.
- SQL Server `+` returns `NULL` if either string is `NULL`; `CONCAT` treats
  `NULL` as an empty string; standard `||` returns `NULL` if either side is
  `NULL`. A translated label can change from text to `NULL`.
- `TOP (n)` and `FETCH FIRST n ROWS ONLY` are different syntaxes. `TOP`
  without `ORDER BY` returns an arbitrary set, and `OFFSET ... FETCH NEXT`
  requires `ORDER BY` in SQL Server.
- The estimated plan's cost percentages are estimates, not measured time.
  Actual row counts require the actual plan, and capturing an actual plan of a
  data-changing statement executes it.
- A scan is not automatically bad and a seek is not automatically good. A seek
  that feeds thousands of key lookups can cost more than a scan; read the row
  counts.
- Logical reads are the comparison metric; physical reads and elapsed time
  depend on cache state and load. A single run, especially the first after a
  restart, is not evidence.
- `OPTION (RECOMPILE)` costs a compile on every execution. It is a targeted fix
  for one statement, not a default, and it has no standard equivalent.
- `WITH (NOLOCK)` can return uncommitted, duplicated, or missing rows; it is a
  correctness risk, not a tuning fix. It can also still be blocked by a schema
  change.
- `SELECT *` prevents a narrow covering index; an index containing every
  selected column can still cover it, at a write cost. It also changes the
  result when the schema changes. `UNION` deduplicates while `UNION ALL` does
  not, and `NOT IN` over a nullable column can return no rows.
- Every index adds write work and storage; a wide `INCLUDE` duplicates data.
  Covering is a property of one query, not of the index.
- A function, a cast, or a type mismatch on the indexed column prevents a
  seek; check the plan for the conversion and align the types.

## Part 11 — Release QA Query Patterns

Parts 1 to 10 taught the language one feature at a time. This part turns those
features into repeatable release checks: a baseline count, a duplicate scan, an
orphan scan, a null audit, a before-and-after comparison, a distribution, a
disposable fixture, a saved view, and a review of the query itself. Each check
has the same four parts: the question it answers, the query, the rows expected
on the sample data, and the decision rule for a release.

Two QA staging tables stand in for an import file. They are not part of the
application schema, and the database does not enforce the application's foreign
keys or uniqueness rules on them, which is exactly why they can hold the bad
rows the checks below are built to find.

`legacy_users(user_id, email, display_name)`:

| user_id | email | display_name |
|---:|---|---|
| 1 | alice@example.com | Alice |
| 2 | bob@example.com | Bob |
| 3 | alice@example.com | Alice |
| 4 | carol@example.com | Carol |

`legacy_reviews(review_id, card_id, user_id, rating)`:

| review_id | card_id | user_id | rating |
|---:|---:|---:|---:|
| 20001 | 1001 | 1 | 5 |
| 20002 | 9999 | 1 | 4 |
| 20003 | 1001 | 9999 | 3 |
| 20004 | 1002 | 2 | `NULL` |

For practice, create the staging tables with the application's column types.
The two staging tables have no foreign keys, and `legacy_users` has no unique
constraint on `email`, so the checks below have bad rows to find:

**SQL Server:**

```sql
CREATE TABLE legacy_users (
    user_id      INT PRIMARY KEY,
    email        NVARCHAR(255) NOT NULL,
    display_name NVARCHAR(100)
);

CREATE TABLE legacy_reviews (
    review_id INT PRIMARY KEY,
    card_id   INT NOT NULL,
    user_id   INT NOT NULL,
    rating    INT
);
```

**Standard SQL:** replace `INT` with `INTEGER` and `NVARCHAR` with `VARCHAR`;
nothing else changes.

Users 1 and 3 share `alice@example.com`. Review 20002 names card 9999, which
does not exist, and review 20003 names user 9999, which does not exist. A
staging table that accepted those rows has done its job; the import is not
trusted until the checks below pass.

### Baseline Counts

A release baseline starts with one question per table: how many rows does the
table hold now? Run the same query before the deployment and after it, and keep
both results with the build identifier and the time each ran.

**SQL Server and standard SQL:**

```sql
SELECT 'users' AS table_name, COUNT(*) AS row_count FROM users
UNION ALL
SELECT 'decks', COUNT(*) FROM decks
UNION ALL
SELECT 'cards', COUNT(*) FROM cards
UNION ALL
SELECT 'reviews', COUNT(*) FROM reviews
ORDER BY table_name;
```

**Expected results.** The same four rows both times, because the sample data
does not change during a release:

| table_name | before | after |
|---|---:|---:|
| cards | 5 | 5 |
| decks | 4 | 4 |
| reviews | 7 | 7 |
| users | 5 | 5 |

`COUNT(*)` counts rows, not non-`NULL` values (Part 4). The sum of the four
counts is not a meaningful total across different entities; each row is its own
baseline. Run the query in every environment you are comparing, because a test
environment with different sample data cannot be compared row for row with
production.

**Decision rule.** Equal counts before and after are necessary, not sufficient.
A release that moves a card from one deck to another keeps the `cards` count at
5 while changing deck 101 and deck 103; a release that deletes one review and
inserts another keeps `reviews` at 7. Counts detect added and removed rows, not
changed or swapped rows. The Before and After Comparisons section below adds a
comparison at the key level.

A count that changes may also be expected. The report should say "4 users
before, 4 after" or "4 before, 5 after, expected because the seed adds user 6",
so a reader can tell a planned change from a regression. A count without an
expected value is a fact, not yet a finding.

**Deck-level baseline from a view.** The four-table count says how many cards
exist, not how they are spread across decks. `v_deck_card_counts` (Part 8) gives
one row per deck, including decks with no cards:

**SQL Server and standard SQL:**

```sql
SELECT deck_id, title, card_count
FROM v_deck_card_counts
WHERE card_count = 0
ORDER BY deck_id;
```

**Expected rows.** One row: deck 104, Empty Deck, 0. The view starts from
`decks` and counts `c.card_id`, so an empty deck survives with a count of 0
instead of disappearing or counting as 1 (Part 8). Query the view after the
release as well; a deck that loses its last card appears here, while the
four-table `COUNT(*)` on `cards` alone reports only that one card disappeared,
not which deck lost it.

The same view gives a compact release summary:

**SQL Server and standard SQL:**

```sql
SELECT COUNT(*) AS deck_count,
       SUM(card_count) AS card_total,
       SUM(CASE WHEN card_count = 0 THEN 1 ELSE 0 END) AS empty_decks
FROM v_deck_card_counts;
```

**Expected row.** One row: 4 decks, 5 cards in total, 1 empty deck. `card_total`
should equal `COUNT(*)` on `cards` (5) before and after the release, because
every card belongs to exactly one deck; if the two disagree, either the view or
the base table changed, and the difference is the finding. Keep the view's
definition under review: a view stores no rows, so a change to its `LEFT JOIN`
or its `COUNT` changes every result built on it.

### Duplicate Detection

A duplicate check asks one question at the grain of a rule: which values appear
more than once in the columns that must be unique? The rule decides the
`GROUP BY` columns, and the query's result is evidence for or against the rule.
`HAVING COUNT(*) > 1` keeps only groups that repeat.

**Email in the staging table.** The application intends one account per email,
but `legacy_users` has no unique constraint, so an import can violate the rule.
Group by `email`:

**SQL Server and standard SQL:**

```sql
SELECT email, COUNT(*) AS row_count
FROM legacy_users
GROUP BY email
HAVING COUNT(*) > 1
ORDER BY email;
```

**Expected rows.** One row:

| email | row_count |
|---|---:|
| alice@example.com | 2 |

Users 1 and 3 both use `alice@example.com`. The query answers "which emails are
repeated", not "which user row is correct". The report also needs the user IDs
of the candidates: a second query such as `SELECT user_id, email FROM
legacy_users WHERE email = 'alice@example.com' ORDER BY user_id` lists them,
and the owner decides which row survives before a `UNIQUE` constraint is added
(Part 8).

**Deck titles per user.** The product rule is one title per user's deck list;
two users may both have a deck called Biology 101. Group by the rule's pair,
`(title, user_id)`:

**SQL Server and standard SQL:**

```sql
SELECT title, user_id, COUNT(*) AS deck_count
FROM decks
GROUP BY title, user_id
HAVING COUNT(*) > 1
ORDER BY title, user_id;
```

**Expected rows.** None. Decks 101 and 103 share the title Biology 101 but
belong to users 1 and 2, so each `(title, user_id)` pair appears once. The check
passes.

Grouping by `title` alone would return Biology 101 with a count of 2 and flag a
duplicate that the rule allows. That is not a false positive in the database;
it is a different question. Before you call a row a duplicate, write down the
exact uniqueness rule and group by its columns. If the rule is "titles are
unique across the whole product", the same sample fails, and the report should
state the rule, not only the count.

### Orphan Detection

An orphan row names a parent that does not exist. The application's foreign keys
prevent orphans in `decks`, `cards`, and `reviews`, but `legacy_reviews` is a
staging table with no foreign keys, so it can hold `card_id` 9999 and `user_id`
9999. The anti-join pattern keeps every child row with `LEFT JOIN` and then
keeps only the rows where the parent side is `NULL`.

**SQL Server and standard SQL:**

```sql
SELECT lr.review_id,
       lr.card_id,
       lr.user_id,
       CASE WHEN c.card_id IS NULL THEN 'missing card' ELSE 'ok' END AS card_status,
       CASE WHEN u.user_id IS NULL THEN 'missing user' ELSE 'ok' END AS user_status
FROM legacy_reviews AS lr
LEFT JOIN cards AS c ON c.card_id = lr.card_id
LEFT JOIN users AS u ON u.user_id = lr.user_id
WHERE c.card_id IS NULL OR u.user_id IS NULL
ORDER BY lr.review_id;
```

**Expected rows.** Two rows:

| review_id | card_id | user_id | card_status | user_status |
|---:|---:|---:|---|---|
| 20002 | 9999 | 1 | missing card | ok |
| 20003 | 1001 | 9999 | ok | missing user |

Review 20002 fails the `cards` lookup, so `c.card_id` is `NULL`; review 20003
fails the `users` lookup, so `u.user_id` is `NULL`. Reviews 20001 and 20004
match on both sides and are removed by the `WHERE` clause.

**Why both joins in one query.** Each `LEFT JOIN` keeps all four legacy rows
and adds the parent columns. The `WHERE` keeps a row when either parent is
missing, so one pass reports both kinds of orphan. The two parent keys are
primary keys, so each child row matches at most one card and one user, and the
joins cannot multiply rows. If a parent side could repeat, deduplicate it or use
`EXISTS` before joining, or the report would list one orphan several times.

**The wrong tools.** `NOT IN` over a column that can be `NULL` returns no rows
when the list contains a `NULL` (Part 3). The `LEFT JOIN ... IS NULL` shape has
no such trap: it does not compare every child value with a `NULL`, it tests
whether the join found a parent. `NOT EXISTS` is the other safe shape (Part 10).
Do not check only one parent: a review with a valid card and a missing user is
still an orphan.

### Required-Field Nulls

A null check is only meaningful against a named rule. The schema has two
nullable columns, and each one allows two different reports:

- `users.display_name` is nullable. A `NULL` is legal in the schema. If the
  product says a user must have a display name, the `NULL` is a product bug; if
  the product allows an unnamed user, it is not. The schema cannot tell you
  which rule the product enforces.
- `reviews.rating` is nullable. `ck_reviews_rating` requires a non-`NULL`
  rating to be between 1 and 5, and a `NULL` passes because the check condition
  is UNKNOWN (Part 8). If the product requires a rating for a completed review,
  a `NULL` is a product bug; if an unrated review is a valid state, it is not.

**Display names.**

**SQL Server and standard SQL:**

```sql
SELECT user_id, email
FROM users
WHERE display_name IS NULL
ORDER BY user_id;
```

**Expected rows.** One row: user 3, `carol@example.com`. The sample contains
this row on purpose, so the query returning a row is not a release failure by
itself. Report it with the rule: "one of five users has no display name; the
schema allows it and the product rule does not require it" or "the product rule
requires it and one user violates it". The second sentence is a finding; the
first is a description.

**Ratings.**

**SQL Server and standard SQL:**

```sql
SELECT review_id, card_id, user_id
FROM reviews
WHERE rating IS NULL
ORDER BY review_id;
```

**Expected rows.** Two rows: reviews 10003 and 10007. The same distinction
applies. `ck_reviews_rating` is not a `NOT NULL` rule; it only bounds a value
that exists.

A compact audit counts the filled and missing values in one pass:

**SQL Server and standard SQL:**

```sql
SELECT COUNT(*) AS review_count,
       COUNT(rating) AS rated_count,
       COUNT(*) - COUNT(rating) AS unrated_count
FROM reviews;
```

**Expected row.** One row: 7 reviews, 5 rated, 2 unrated. `COUNT(rating)`
ignores `NULL` and `COUNT(*)` counts every row, so the difference is the number
of missing ratings (Part 4). A release that starts recording unrated reviews
changes `unrated_count`; a release that backfills ratings changes `rated_count`
and leaves the total at 7.

**Required columns.** Every column other than `users.display_name` and
`reviews.rating` is declared `NOT NULL`; primary keys are non-null as well. A
query for `NULL` in one of those columns should return zero rows. If it returns
a row, either the environment's table is missing the constraint or the data
predates it; check the column definition before reporting the row as bad data.
It is a schema finding, not a product-data finding.

**Do not hide the finding.** `COALESCE(rating, 0)` in the check turns a missing
rating into a rating of 0, which is outside `ck_reviews_rating` and would be a
different value. Use `COALESCE` in a display layer after the check has reported
the missing row, never in the predicate that is supposed to detect it. `= NULL`
never matches; the predicate is `IS NULL` (Part 3).

### Before and After Comparisons

Counts answer "did the number change?"; a key-level comparison answers "which
row changed?" The shape is a `FULL OUTER JOIN` on the key, with `IS NULL` tests
for rows that exist on only one side. That covers three outcomes in one result:
a key only in the baseline, a key only in the current data, and a key on both
sides with a different value.

The example uses a release boundary of 2026-02-01 00:00:00. The baseline side
counts reviews recorded before that instant; the current side counts every
review now. On the sample rows, review 10007 is the only one recorded after the
boundary.

**SQL Server:**

```sql
WITH before_release AS (
    SELECT card_id, COUNT(*) AS review_count
    FROM reviews
    WHERE reviewed_at < '2026-02-01 00:00:00'
    GROUP BY card_id
),
after_release AS (
    SELECT card_id, COUNT(*) AS review_count
    FROM reviews
    GROUP BY card_id
)
SELECT COALESCE(b.card_id, a.card_id) AS card_id,
       b.review_count AS before_count,
       a.review_count AS after_count
FROM before_release AS b
FULL OUTER JOIN after_release AS a ON a.card_id = b.card_id
WHERE b.card_id IS NULL
   OR a.card_id IS NULL
   OR b.review_count <> a.review_count
ORDER BY COALESCE(b.card_id, a.card_id);
```

The statement is standard SQL; the only dialect difference is the cutoff
literal, which standard SQL writes as `TIMESTAMP '2026-02-01 00:00:00'`.
`COALESCE(b.card_id, a.card_id)` keeps the key visible whichever side supplied
it.

**Expected rows.** One row:

| card_id | before_count | after_count |
|---:|---:|---:|
| 1004 | 1 | 2 |

Card 1004 had review 10005 before the boundary and gained review 10007 after
it; its count rose from 1 to 2. Cards 1001, 1002, and 1003 have the same count
on both sides and are removed by the `WHERE` clause. Card 1005 has no reviews on
either side, so it is in neither CTE and disappears before the join.

**Why both `IS NULL` tests.** The `WHERE` clause has three conditions, and the
first two are not decoration. If a card had reviews before the release and none
after it, `a.card_id` would be `NULL` and `a.review_count` would be `NULL`;
`b.review_count <> a.review_count` is then UNKNOWN, not TRUE, and the third
condition alone would drop the row. `a.card_id IS NULL` keeps it. The mirror
case, a card whose first reviews arrived during the release, is kept by
`b.card_id IS NULL`. Without the two `IS NULL` tests, the query reports only
changed values and silently loses the rows that appeared or disappeared.

**What the comparison does not prove.** It compares counts, so a release that
changes a rating without adding or removing a review produces no row here. For a
value-level check, put the key and the value in each CTE and compare the value
columns with the same `IS NULL` care. Choose the comparison from the claim the
release makes: "no card lost a review" is a count claim; "no rating decreased"
needs the values.

**When the baseline is a table.** In a real release the baseline is captured
before the deployment, often into a QA-owned snapshot table or a saved query
result. Alias that source as `before_release` and the live table or view as
`after_release`; the join and the `IS NULL` tests do not change. The baseline
must come from the same database and the same key definition as the live side,
or the comparison reports differences that are really environment differences.
A set difference reports keys from one side only and cannot place the before
and after values side by side; the full outer join reports both directions and
the change in one row.

**A plan and logical-read comparison.** A data comparison answers whether rows
changed; a plan comparison answers whether the same query got cheaper. Take
`SELECT card_id, front FROM cards WHERE deck_id = 103;` and capture the actual
plan and the `STATISTICS IO` message for `cards` (the batch is in Part 10).
Then capture both again with the wider index from Part 8
(`ix_cards_deck_created`) in place on the table:

| Capture | Operators on `cards` | What the `STATISTICS IO` line shows |
|---|---|---|
| With only `ix_cards_deck_id` | Index Seek, then one Key Lookup per row for `front` | Index pages plus a table page for each lookup |
| With `ix_cards_deck_created` | One Index Seek, no Key Lookup | Index pages only; the two `Logical reads` figures are the comparison |

Record both operator lists and both `Logical reads` figures with the row count
and the cache state. On the five sample rows the optimizer may scan either
way, so the sample does not predict production; the method — same query, same
data, one change, two captures — is what transfers.

### Status Distributions

A distribution groups rows by a status column and counts each group. It answers
"did the mix change?" rather than "did the total change?" The two status columns
in this schema are `decks.is_public` and `reviews.rating`.

**Visibility.**

**SQL Server and standard SQL:**

```sql
SELECT is_public, COUNT(*) AS deck_count
FROM decks
GROUP BY is_public
ORDER BY is_public;
```

**Expected rows.**

| is_public | deck_count |
|---:|---:|
| 0 | 2 |
| 1 | 2 |

Decks 102 and 104 are private and decks 101 and 103 are public. The expected
table shows the SQL Server output: on SQL Server `is_public` is `BIT`, so the
group values are 0 and 1. Under the standard schema the column is `BOOLEAN`, so
the same two groups display as `FALSE` and `TRUE`. A report should translate
either form to private and public, but the check should group on the column
rather than on a label the application computes. A release that changes one
deck's visibility moves one unit from one group to the other and keeps the total
at four; the total alone would not show it.

**Ratings.**

**SQL Server and standard SQL:**

```sql
SELECT rating, COUNT(*) AS review_count
FROM reviews
GROUP BY rating
ORDER BY rating;
```

**Expected rows.**

| rating | review_count |
|---:|---:|
| `NULL` | 2 |
| 2 | 1 |
| 3 | 1 |
| 4 | 1 |
| 5 | 2 |

The five rated reviews spread over ratings 2 to 5, and two reviews have no
rating. The sum of the counts is 7, the table's `COUNT(*)`; when it is not, the
query has lost a group, often because a join removed rows or a `WHERE` clause
filtered before grouping (Part 4). SQL Server places the `NULL` group first in
ascending order; the standard does not fix where `NULL` sorts, so do not read
the position as a product fact. The counts and the reconciliation are the
evidence.

**Decision rule.** Record the expected distribution with the baseline, not only
the total. A release that starts writing every new deck as private changes the
`is_public` split while the deck count stays the same; a release that stops
collecting ratings changes the `NULL` group. Investigate a shift by listing the
rows in the changed group, not by re-running the count.

### Test Data Setup and Cleanup

A check that needs a row the sample does not contain creates a fixture. The safe
pattern is one transaction: insert the fixtures, run the check in the same
session, and roll back. The rollback removes every inserted row at once, and the
fixtures never become committed data. Reserved keys, such as 900 and above, make
the fixture rows easy to recognize and count; the setup, the check, and the
cleanup verification use the same keys.

**SQL Server:**

```sql
BEGIN TRANSACTION;

INSERT INTO users (user_id, email, display_name, created_at)
VALUES (900, 'qa@example.com', 'QA User', '2026-02-15 09:00:00');

INSERT INTO decks (deck_id, user_id, title, is_public, created_at)
VALUES (900, 900, 'QA Deck', 0, '2026-02-15 09:00:00');

INSERT INTO cards (card_id, deck_id, front, back, created_at)
VALUES (900, 900, 'QA front', 'QA back', '2026-02-15 09:00:00');

INSERT INTO reviews (review_id, card_id, user_id, rating, reviewed_at)
VALUES (900, 900, 900, 5, '2026-02-15 09:00:00');

-- The check runs here, in the same session.

SELECT 'users' AS table_name, COUNT(*) AS fixture_count
FROM users
WHERE user_id = 900
UNION ALL
SELECT 'decks', COUNT(*) FROM decks WHERE deck_id = 900
UNION ALL
SELECT 'cards', COUNT(*) FROM cards WHERE card_id = 900
UNION ALL
SELECT 'reviews', COUNT(*) FROM reviews WHERE review_id = 900
ORDER BY table_name;

ROLLBACK TRANSACTION;
```

**Expected rows.** Inside the transaction the check returns four rows, one per
table, each with a count of 1. The inserts run parent-first so each foreign key
finds its parent: user 900, then deck 900, then card 900, then review 900.
After the rollback, the same `SELECT` returns four rows with a count of 0. That
second result is the evidence that the fixtures are gone; keep it with the
release notes.

The standard form uses `START TRANSACTION` and `ROLLBACK` (Part 7). The inserts
change in two places: `is_public` takes `FALSE` instead of `0`, because the
standard schema declares it `BOOLEAN` (Part 1), and each `created_at` or
`reviewed_at` value takes the typed form `TIMESTAMP '2026-02-15 09:00:00'`. The
check is the same. A fixture in a transaction is visible only to the session
that created it. That is a feature for a database check and a limit for a
browser test: the browser opens another connection and cannot see the
uncommitted rows, so a cross-session test commits the fixtures and then deletes
them by their reserved keys, child table first, with the same verification
query at the end (Part 7).

**Never leave fixtures behind.** A committed fixture is ordinary data: it counts
in every baseline, appears in every distribution, and can satisfy a later check
that should have failed. If a test must commit its fixture, delete it in
child-to-parent order (`reviews`, `cards`, `decks`, `users`) and run the
verification query until it returns zeros. If the session dies mid-check, do
not assume the rows are gone; reconnect and query the reserved keys. Use a
transaction and roll it back for every check that can stay in one session.

### Query Review Checklist

Run this review on a check before you share it, and again when a check returns
an unexpected result. Each row is a question, the condition that passes it, and
the part that teaches the detail.

| Review question | What passing looks like | Where |
|---|---|---|
| Is the join type correct? | `INNER JOIN` when only matches matter; `LEFT JOIN` when the parent must survive; `FULL OUTER JOIN` when either side may be missing. A `WHERE` predicate on the right table turns a left join into an inner join unless it admits `NULL`. | Part 5 |
| Is `NULL` handled? | `IS NULL` and `IS NOT NULL`, never `= NULL`; `NOT IN` is not used when the list or subquery can contain `NULL`; `COUNT(column)` ignores `NULL` while `COUNT(*)` counts rows; a `NULL` in the result is either a finding or a declared valid state. | Part 3 |
| Can rows multiply? | One-to-many joins are counted with `COUNT(DISTINCT key)` or pre-aggregated before the join; the expected row count is written down and matches the grain of the question. | Parts 4 and 5 |
| Is each filter in the right clause? | Row conditions in `WHERE`, group conditions in `HAVING`, join conditions in `ON`; an outer join's preserved side is not filtered away in `WHERE`. | Parts 4 and 5 |
| Is the order deterministic? | `ORDER BY` names every column that matters and ends with a unique tiebreaker; no check depends on the server's default order. | Part 2 |
| Is the result measured? | The query states its expected row count and the actual count is recorded; a performance claim adds the plan and logical reads. | Part 10 |

**Correct join type.** The most common wrong result is not a syntax error; it is
the right columns from the wrong join. A `LEFT JOIN` that is supposed to keep
empty decks and is followed by `WHERE c.card_id = 1001` silently drops every
deck without that card. State which side must survive before choosing the join.

**`NULL` handling.** `NULL` is not a value to compare with `=`; it is a state to
test with `IS NULL` (Part 3). Check the aggregate as well: `COUNT(*)` and
`COUNT(column)` answer different questions after a left join.

**Row multiplication.** A join to a child table returns one row per child, not
one row per parent. Before publishing a count, ask whether one input row can
appear more than once; if it can, count the distinct key or aggregate first
(Parts 4 and 5).

**Filters in the right clause.** A row condition in `HAVING` may be legal and
still wrong, because it filters after grouping. A condition in the `ON` clause
of a left join is not a filter on the left table; it controls only which right
rows match. Put each condition where its stage runs (Parts 4 and 5).

**Deterministic ordering.** The sample order is part of the evidence. Without a
unique `ORDER BY`, two runs can disagree and a reader cannot reproduce the
result (Part 2). Sort by the key, not only by a label that can repeat.

**Measurement.** A row count of zero is evidence only when the query would have
returned a row if the defect existed; a query that fails returns an error, not
zero. Record the query text, the environment, the time, and the row count. For a
performance claim, add the actual plan and the logical reads (Part 10). A check
that was not measured is an opinion.

### Release QA Use

- Capture the four-table baseline before the deployment and again after it;
  store both results with the build identifier, environment, and timestamp.
  Compare table by table, not only in total.
- Run the duplicate checks before an import and after it. Report the repeated
  key, the count, and the rows behind it; a duplicate email is a finding, and a
  duplicate title is a finding only when the stated rule covers cross-user
  repeats.
- Run the orphan checks on every staging table that will feed the live schema.
  A row with a missing parent is rejected by the live foreign key, so catching
  it in staging turns a failed migration into a fixable import.
- Pair every null check with the rule it tests: the schema allows the `NULL`, or
  the product requires a value. Write which one in the report; a `NULL` that the
  schema allows is not automatically a bug.
- Compare before and after at the key level with a full outer join, and look at
  all three result shapes: missing from the current side, new on the current
  side, and present on both with a changed value.
- Record the expected distribution for `is_public` and ratings. A distribution
  shift is a finding even when the table count is unchanged.
- Create fixtures in one transaction with reserved keys, run the check, and roll
  back. Verify the fixture count is zero afterward and attach the verification
  to the release notes.
- Use `v_deck_card_counts` for per-deck card counts instead of copying its join
  into each test. Query it for empty decks and for the summary counts, and
  compare its output before and after the release.
- Review every query against the checklist before attaching it to a bug report.
  The reviewer should be able to point to the join type, the `NULL` handling,
  the row count, the filter clauses, the ordering, and the measurement.
- Hand the next engineer the query and the expected result, not only the
  screenshot. A release check that cannot be rerun is an anecdote.

### Watch-outs

- Equal counts do not mean equal data. A move, a swap, or a delete-and-insert
  leaves the count unchanged; compare keys and values when the release can
  modify rows.
- Group duplicates by the columns in the rule. Grouping `decks` by `title`
  alone flags decks 101 and 103, which the product allows because they belong
  to different users.
- `COUNT(*)` counts the `NULL`-extended row that a left join produces;
  `COUNT(column)` does not. `COUNT(*)` on the base query behind
  `v_deck_card_counts` would report one card for empty deck 104 (Part 8).
- A `LEFT JOIN ... IS NULL` orphan check depends on the parent key being
  unique. If the parent side can repeat, the join multiplies the child and the
  report lists one orphan more than once.
- `= NULL` never matches. Use `IS NULL`. `NOT IN` over a list that contains
  `NULL` returns no rows, so the orphan and exclusion checks use a join or
  `NOT EXISTS` (Part 3).
- In a full outer join comparison, `NULL <> value` is UNKNOWN. Keep the
  `IS NULL` tests for both key columns, or the comparison silently drops the
  rows that appeared or disappeared.
- A transaction fixture is invisible to other sessions. A browser test on
  another connection will not see it; commit and clean up explicitly if the
  test must cross sessions.
- A committed fixture is real data. It inflates counts and distributions, can
  satisfy a check that should fail, and can break a later insert with a primary
  key conflict.
- A view stores no rows. `v_deck_card_counts` reflects the current base tables
  on every query, and a change to its definition changes every check that uses
  it (Part 8).
- The `NULL` group in a rating distribution is data, not noise. Filter it only
  when the rule says unrated reviews are out of scope, and reconcile the sum of
  the groups with `COUNT(*)`.
- No statement in this guide was executed, and no database is bundled. The
  expected rows come from the fixed sample data; run every check against your
  own server and compare the result.

## Dialect Portability

SQL Server is the primary track in this guide. SQL Server (T-SQL) syntax comes
first, and the SQL Server examples are written for current SQL Server. Standard
SQL is the comparison track: where the two differ, the standard form comes
second, so a reader can recognize the portable shape. Other databases may
differ. This guide does not promise that a third database accepts any statement
shown here, and it does not cover any other product's administration or
dialect.

The forms `LIMIT`, `AUTO_INCREMENT`, `IFNULL`, `NOW()`, and `GROUP_CONCAT` are
examples of other-vendor syntax that this guide does not teach. Each has its own
spelling and behavior in its own product; the SQL Server and standard forms in
this guide are not a translation table for it. Before moving a statement to
another product, read that product's documentation, run the statement against a
copy of the data, and compare the rows and types, not only whether it parsed.
