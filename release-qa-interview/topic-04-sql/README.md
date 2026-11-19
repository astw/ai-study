# Release QA Interview Prep — SQL

A practical SQL guide for a junior-to-mid release QA interview. It assumes no
prior SQL and uses one running example throughout: the flashcards application
from the AI study guide, where a student saves decks of cards, studies them, and
records reviews.

## Files

| File | Contents |
|---|---|
| `sql-for-release-qa.md` | Eleven-part guide: SQL Server first, standard SQL comparisons, flashcards examples, release QA patterns, and tuning |
| `qa-100.md` | 100 open questions with hidden answers, one part per guide part |
| `mcq-150.md` | 150 multiple-choice questions with hidden answers and explanations, one part per guide part |
| `README.md` | This file |

## Who it is for

Release QA engineers preparing for a junior-to-mid interview, and anyone moving
from manual testing into database checks. No prior SQL is assumed: the guide
starts with tables, rows, and keys, and teaches every statement it uses. You do
not need a database to read the guide, but you do need one to practice.

## Dialects

SQL Server (T-SQL) is the primary track. Examples appear under a
`**SQL Server:**` label first. A statement that standard SQL also accepts may
carry the `**SQL Server and standard SQL:**` label, or be shown once under
`**SQL Server:**` with a prose note that the standard form is the same. When
standard SQL differs, the portable form follows under `**Standard SQL:**`.
Where no standard form exists, the label says so: index DDL is outside the SQL
standard, so its portable form uses `**Portable form (not standard SQL):**`.
A statement shown under one dialect's label is not a promise that the other
dialect accepts it, and this folder makes no claim about MySQL, PostgreSQL,
Oracle, or any other third database.

## Study order

1. Read one part of `sql-for-release-qa.md`.
2. Answer the matching part of `qa-100.md` before opening the hidden answer.
3. Take the matching part of `mcq-150.md`, choose one option, then read the
   explanation.
4. Practice the statements in your own SQL Server database: create the schema
   from Part 1, load the exact rows from Practice data below, and use a
   transaction for anything that changes data.

The banks have 100 Q&A and 150 MCQs. The Q&A count per part ranges from 5 to 14;
the MCQ count ranges from 8 to 21.

## Coverage

| Part | Topic | Q&A | MCQs |
|---|---|---:|---:|
| 1 | Relational Basics — tables, rows, columns, keys, NULL, data types, the flashcards schema | 7 | 10 |
| 2 | Reading Data with SELECT — SELECT, aliases, expressions, DISTINCT, ORDER BY, limiting rows | 9 | 14 |
| 3 | Filtering and NULL — WHERE, AND/OR/NOT, IN, BETWEEN, LIKE, three-valued logic, the NOT IN trap | 11 | 17 |
| 4 | Aggregating and Grouping — COUNT, SUM, AVG, MIN, MAX, GROUP BY, HAVING | 11 | 17 |
| 5 | Joins and UNION — inner, left, right, full outer, and self joins, join chains, multiplication, UNION | 14 | 21 |
| 6 | Subqueries and Simple CTEs — scalar subqueries, IN and EXISTS, correlated subqueries, CTEs | 9 | 14 |
| 7 | Changing Data and Transactions — INSERT, UPDATE, DELETE, transactions, savepoints | 9 | 14 |
| 8 | Schema, Constraints, Indexes, and Views — CREATE TABLE, constraints, views, indexes | 9 | 14 |
| 9 | Window Functions — ROW_NUMBER, RANK and DENSE_RANK, PARTITION BY, SUM OVER, LAG and LEAD | 5 | 8 |
| 10 | SQL Server Dialect and Tuning — dialect table, execution plans, STATISTICS IO/TIME, SARGable predicates, indexes, parameter sniffing | 7 | 10 |
| 11 | Release QA Query Patterns — baselines, duplicates, orphans, nulls, before/after, distributions, fixtures, checklist | 9 | 11 |
| **Total** | | **100** | **150** |

## The flashcards schema

Every guide example and every question uses these four tables and the same
sample rows.

| Table | Columns | Keys and nullability |
|---|---|---|
| `users` | `user_id`, `email`, `display_name`, `created_at` | Primary key `user_id`; `display_name` nullable; all other columns required |
| `decks` | `deck_id`, `user_id`, `title`, `is_public`, `created_at` | Primary key `deck_id`; foreign key `user_id` → `users(user_id)`; all columns required |
| `cards` | `card_id`, `deck_id`, `front`, `back`, `created_at` | Primary key `card_id`; foreign key `deck_id` → `decks(deck_id)`; all columns required |
| `reviews` | `review_id`, `card_id`, `user_id`, `rating`, `reviewed_at` | Primary key `review_id`; foreign keys `card_id` → `cards(card_id)` and `user_id` → `users(user_id)`; `rating` nullable, and a non-null rating must be 1–5 |

The sample rows are 5 users, 4 decks, 5 cards, and 7 reviews. They include the
cases the questions depend on: user 5 owns no decks, deck 104 has no cards, card
1005 has no reviews, user 3 has a `NULL` display name, users 1 and 4 share the
display name Alice, decks 101 and 103 share the title Biology 101 under
different users, and reviews 10003 and 10007 have `NULL` ratings. Part 1 gives
both the SQL Server DDL and the standard SQL DDL; Part 11 adds two QA staging
tables for the duplicate and orphan exercises.

## Practice

No database is bundled with this folder, and no example was executed to produce
it. There is no SQL Server, MySQL, or PostgreSQL instance in this repository,
and the expected rows are derived from the fixed sample data, not observed from
a server.

To reproduce a result: create the schema from Part 1, load the exact rows in
Practice data below (the summary table in Part 1 is not a row-by-row data set),
and create the two staging tables from Part 11 for the duplicate and orphan
checks. Run each statement in a scratch database or a transaction and compare
the result with the guide's expected rows. Check syntax against Microsoft Learn
(or another current reference) and against the server version you are testing;
SQL Server versions differ in features such as `CREATE OR ALTER VIEW`. For
anything that changes data, use a transaction and roll it back, and never point
the destructive examples at production.

## Practice data

These are the exact rows used by every example and question. `NULL` marks a
missing value, `TRUE` and `FALSE` are the readable boolean values, and a SQL
Server `BIT` column stores them as 1 and 0. The timestamps use
`YYYY-MM-DD hh:mm:ss` in the SQL Server track; the standard track writes each
as a typed `TIMESTAMP '...'` literal.

`users`:

| user_id | email | display_name | created_at |
|---:|---|---|---|
| 1 | alice@example.com | Alice | 2026-01-05 09:00:00 |
| 2 | bob@example.com | Bob | 2026-01-06 10:00:00 |
| 3 | carol@example.com | `NULL` | 2026-01-07 11:00:00 |
| 4 | dave@example.com | Alice | 2026-02-01 12:00:00 |
| 5 | erin@example.com | Erin | 2026-02-10 13:00:00 |

`decks`:

| deck_id | user_id | title | is_public | created_at |
|---:|---:|---|---|---|
| 101 | 1 | Biology 101 | TRUE | 2026-01-10 09:00:00 |
| 102 | 1 | Spanish Verbs | FALSE | 2026-01-11 09:30:00 |
| 103 | 2 | Biology 101 | TRUE | 2026-01-12 10:00:00 |
| 104 | 3 | Empty Deck | FALSE | 2026-02-01 10:00:00 |

`cards`:

| card_id | deck_id | front | back | created_at |
|---:|---:|---|---|---|
| 1001 | 101 | What is a cell? | The basic unit of life | 2026-01-15 09:00:00 |
| 1002 | 101 | What is DNA? | Genetic material | 2026-01-16 09:00:00 |
| 1003 | 102 | What is the word for book? | el libro | 2026-01-17 09:00:00 |
| 1004 | 103 | What is osmosis? | Water movement across a membrane | 2026-01-18 09:00:00 |
| 1005 | 103 | What is a gene? | A unit of heredity | 2026-01-19 09:00:00 |

`reviews`:

| review_id | card_id | user_id | rating | reviewed_at |
|---:|---:|---:|---:|---|
| 10001 | 1001 | 1 | 5 | 2026-01-20 09:00:00 |
| 10002 | 1001 | 2 | 4 | 2026-01-21 10:00:00 |
| 10003 | 1002 | 1 | `NULL` | 2026-01-22 11:00:00 |
| 10004 | 1003 | 1 | 3 | 2026-01-23 12:00:00 |
| 10005 | 1004 | 2 | 5 | 2026-01-24 13:00:00 |
| 10006 | 1002 | 3 | 2 | 2026-01-25 14:00:00 |
| 10007 | 1004 | 1 | `NULL` | 2026-02-01 15:00:00 |

Part 11 defines `legacy_users` and `legacy_reviews` with `CREATE TABLE` and
lists their rows. The exact rows above are the values every expected result in
the guide and the banks is derived from.
