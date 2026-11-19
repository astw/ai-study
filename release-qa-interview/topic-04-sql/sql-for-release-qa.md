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

`NOT` inverts a condition, but it follows the three-valued rules from the
next section: `NOT UNKNOWN` is UNKNOWN, so a negated predicate still drops
rows whose column is `NULL`.

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

The inclusive upper bound is a trap for date and time columns. This filter
looks like "the last five days" but loses rows recorded later on the final
day:

**SQL Server:**

```sql
SELECT review_id, reviewed_at
FROM reviews
WHERE reviewed_at >= '2026-01-20'
  AND reviewed_at <  '2026-01-25';
```

This half-open range returns reviews 10001 through 10005. Review 10006,
recorded at 2026-01-25 14:00:00, is excluded because it is not before
2026-01-25 00:00:00; a `BETWEEN ... AND '2026-01-25'` version would exclude
it too, because the bare date means midnight. The half-open form makes the
intended boundary explicit. The standard form uses `TIMESTAMP` literals but
keeps the same comparison shape.

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
one value for the group. Add the column to `GROUP BY`, which is what makes
the deck/rating example work, or aggregate it.

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
