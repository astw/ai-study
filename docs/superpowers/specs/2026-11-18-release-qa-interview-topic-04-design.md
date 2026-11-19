# Release QA Interview Topic 4 — SQL Design

**Date:** 2026-11-18
**Status:** Proposed
**Audience:** Junior-to-mid release QA candidates, including new graduates with no prior SQL.

## Intent

Add a fourth standalone interview-prep pack for release QA: SQL knowledge,
100 open questions with hidden answers, and 150 multiple-choice questions with
explanations. The pack teaches SQL Server (T-SQL) as the primary track and shows
standard SQL beside it, so a candidate can work in a Microsoft environment and
still recognize portable SQL when a query moves to another database. It also introduces practical query
tuning: how to read a plan, what makes a predicate unable to use an index, and
which query habits cause avoidable reads.

The existing bank has topic 1 (test methodologies and SDLC), topic 2 (basic
networking), and topic 3 (Linux commands). This is topic 4; the folder and
branch are `topic-04-sql` and `release-qa-interview-topic-04`, stacked on the
topic-3 branch at `7de72df`.

## Goals

- Explain relational basics, `SELECT`, filtering, aggregation, joins, `UNION`
  and `UNION ALL`, subqueries, CTEs, data changes, transactions, schema
  constraints, views, indexes, and basic window functions in plain English.
- Teach SQL Server as the primary track, with standard SQL beside it: `TOP` and
  `OFFSET ... FETCH NEXT` alongside `FETCH FIRST n ROWS ONLY`, `GETDATE()`
  alongside `CURRENT_TIMESTAMP`, and `ISNULL` alongside `COALESCE`.
- Cover SQL Server forms first: `TOP`, `OFFSET ... FETCH NEXT`, `GETDATE()`/
  `SYSDATETIME()`, `ISNULL`, `+`/`CONCAT`, `IDENTITY`, `BIT`, `NVARCHAR`,
  `DATETIME2`, `IIF`, `DATEADD`/`DATEDIFF`, `STRING_AGG`, and
  `CREATE OR ALTER VIEW`, with standard SQL equivalents beside them.
- Introduce practical tuning on SQL Server: estimated and actual execution
  plans, `SET STATISTICS IO/TIME`, scans versus seeks, SARGable predicates,
  clustered/nonclustered and covering indexes, implicit conversions, leading
  wildcards, `SELECT *`, `UNION ALL` versus `UNION`, `EXISTS` versus `IN`,
  parameter sniffing, and `OPTION (RECOMPILE)`.
- Root every example in one running schema: a flashcards application with
  `users`, `decks`, `cards`, and `reviews`.
- Make the release QA angle explicit: baseline counts, duplicate detection,
  orphan rows, null checks, migration comparisons, test-data setup and cleanup,
  transaction rollback, constraint verification, and before/after plan checks.
- Provide 100 Q&A and 150 MCQs with the same reveal format, numbering, TOC, and
  answer style as topics 1–3.
- Keep explanations short enough to study but complete enough to correct a wrong
  mental model.

## Non-goals

- No deep database-administration content: no replication, backups, storage
  engines, log shipping, Availability Groups, or capacity planning.
- No stored procedures, triggers, or scheduler syntax beyond a passing mention.
- No recursive CTEs; only simple non-recursive `WITH` queries.
- No vendor administration on MySQL, PostgreSQL, or Oracle; the comparison track
  is standard SQL, not another vendor.
- No NoSQL, ORM, or application-language database code.
- No claim that the examples were executed against a database; no database is
  installed in this repository.
- No slide deck.

## Anti-goals

- A trivia bank that asks for syntax without a release QA situation.
- Questions whose options are prose restatements of the stem.
- SQL Server syntax presented as if every database accepted it, or standard
  syntax presented as if it were SQL Server-only.
- Tuning advice that sounds authoritative but is not checkable: "add an index"
  without saying which query, which column order, and what trade-off.
- Answers that are technically true but hide the trap the question is testing.
- Duplicate stems or answer sets that make the bank feel padded.

## Approaches considered

1. **Dual-track full pack — chosen.** A knowledge guide, 100 Q&A, 150 MCQs, and
   a README. SQL Server is the main path; standard SQL appears beside it, with a
   dedicated SQL Server and tuning part. Best consistency with topics 1–3 and
   the strongest interview coverage.
2. **ANSI-only full pack.** Portable but ignores the SQL Server environment many
   release QA teams use. The user explicitly asked for SQL Server coverage, so
   this no longer fits.
3. **Compact pack.** 50 Q&A and 75 MCQs. Faster, but too little practice for
   joins, aggregation, SQL Server differences, and tuning.
4. **Lab-first pack.** A runnable schema, exercises, and a smaller question
   bank. Strongest hands-on learning, but the repository has no database to
   verify against and SQL Server is not installable here. The guide still
   includes the schema and sample rows, so readers can practice in their own
   client.

## Pack structure

Folder: `release-qa-interview/topic-04-sql/`

| File | Role |
|---|---|
| `sql-for-release-qa.md` | Eleven-part knowledge guide with SQL Server syntax first, standard SQL comparisons beside it, flashcards examples, release QA use, and tuning. |
| `qa-100.md` | 100 open questions, numbered `Q1`–`Q100`, hidden answers. |
| `mcq-150.md` | 150 four-option questions, numbered `MCQ 1`–`MCQ 150`, one answer and explanation each. |
| `README.md` | Study order, coverage table, counts, and practice guidance. |

### Guide parts

1. **Relational basics** — tables, rows, columns, keys, data types, `NULL`, and
   how the flashcards schema fits together.
2. **Reading data with `SELECT`** — `SELECT`, `FROM`, aliases, expressions,
   `DISTINCT`, `ORDER BY`, `TOP`, `OFFSET ... FETCH NEXT`, and standard
   `FETCH FIRST`, plus choosing columns instead of `*`.
3. **Filtering and `NULL`** — `WHERE`, `AND`/`OR`/`NOT`, `IN`, `BETWEEN`, `LIKE`,
   `IS NULL`, three-valued logic, and the `NOT IN` + `NULL` trap.
4. **Aggregating and grouping** — `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`, `GROUP BY`,
   `HAVING`, `COUNT(*)` versus `COUNT(column)`, and aggregate `NULL` behavior.
5. **Joins and `UNION`** — inner, left, right, full outer, and self joins;
   multi-table join chains; `ON` versus `USING`; join multiplication and
   row-count expectations; `UNION` and `UNION ALL`. Every join type gets its own
   definition, syntax, flashcards example, expected row count, release QA use,
   and watch-out.
6. **Subqueries and simple CTEs** — scalar, `IN`, `EXISTS`, and correlated
   subqueries; non-recursive CTEs with `WITH`, including one CTE and multiple
   CTEs in the same statement. Recursive CTEs are out of scope.
7. **Changing data and transactions** — `INSERT`, `UPDATE`, `DELETE`,
   `START TRANSACTION`, `COMMIT`, `ROLLBACK`, `SAVEPOINT`, and safe test-data
   cleanup.
8. **Schema, constraints, indexes, and views** — `CREATE TABLE`, primary and
   foreign keys, `UNIQUE`, `NOT NULL`, `CHECK`, `DEFAULT`, `CREATE VIEW`,
   `CREATE OR ALTER VIEW`, and what clustered and nonclustered indexes do.
9. **Window functions** — `ROW_NUMBER`, `RANK`, `DENSE_RANK`, `SUM ... OVER`,
   `LAG`, and `LEAD`, focused on deduplication and latest-row checks.
10. **SQL Server dialect and tuning** — SQL Server-versus-standard syntax table;
    `TOP`, `OFFSET ... FETCH NEXT`, `GETDATE()`, `ISNULL`, `IIF`, `IDENTITY`,
    `BIT`, `NVARCHAR`, `DATETIME2`, `DATEADD`/`DATEDIFF`, and `STRING_AGG`; then
    execution plans, `SET STATISTICS IO/TIME`, scans versus seeks, SARGable
    predicates, covering indexes, implicit conversions, leading wildcards,
    `SELECT *`, `UNION ALL`, `EXISTS` versus `IN`, parameter sniffing, and
    `OPTION (RECOMPILE)`.
11. **Release QA query patterns** — baseline counts, duplicate detection, orphan
    rows, required-field nulls, before/after comparisons, status distributions,
    plan and logical-read comparisons, and a query-review checklist.

Each concept entry uses a consistent shape: what it does, SQL Server syntax
first, standard syntax where it differs, a flashcards example, a release QA use,
and a watch-out. The guide ends with a portability note: SQL Server is the
primary track, standard SQL is the portable comparison, and neither guarantees
that a third database will accept the same statement.

### Running schema

```
users(user_id, email, display_name, created_at)
decks(deck_id, user_id, title, is_public, created_at)
cards(card_id, deck_id, front, back, created_at)
reviews(review_id, card_id, user_id, rating, reviewed_at)
```

`users.user_id`, `decks.deck_id`, `cards.card_id`, and `reviews.review_id` are
primary keys. `decks.user_id` and `reviews.user_id` reference `users.user_id`;
`cards.deck_id` references `decks.deck_id`; `reviews.card_id` references
`cards.card_id`. Sample rows include at least one user with no decks, one deck
with no cards, one card with no reviews, one `NULL` display name, two users with
the same display name (not a unique field), and reviews with `NULL` ratings. A
separate legacy-import exercise discusses duplicate emails before a `UNIQUE`
constraint is added, so the sample data does not contradict the schema.

Every example uses these tables and the same sample values, so a reader can
follow one story from `SELECT` through joins, window functions, and SQL Server
tuning.

### Join coverage

| Join | What it returns | Release QA use |
|---|---|---|
| `INNER JOIN` | Only rows with a match on both sides. | Verify that related records exist on both sides of a migration. |
| `LEFT [OUTER] JOIN` | Every left row, with `NULL` in right columns when there is no match. | Find decks with no cards, or users with no reviews. |
| `RIGHT [OUTER] JOIN` | Every right row, with `NULL` in left columns when there is no match. | Find reviews whose card or user is missing; often rewritten as a left join. |
| `FULL [OUTER] JOIN` | All rows from both sides, with `NULL`s where either side has no match. | Compare two data sets and find unmatched rows on both sides. |
| `SELF JOIN` | A table joined to itself with two aliases. | Compare a row with another row in the same table, such as an earlier review. |

The guide also covers join chains across three or more tables, `ON` versus
`USING`, and the row multiplication that happens when a one-to-many join is
counted without `DISTINCT` or pre-aggregation. `UNION` and `UNION ALL` are taught
next to joins but distinguished from them: joins combine columns horizontally,
while `UNION` combines rows vertically.

### Views and indexes

Views and indexes are taught as schema objects a release QA engineer will meet,
not as DBA internals:

- **View:** a named, saved query. Standard SQL uses `CREATE VIEW` and `DROP
  VIEW`; SQL Server deployment scripts commonly use `CREATE OR ALTER VIEW` so
  the object can be recreated safely. A view does not store rows (a plain view
  is not a table), and it is not automatically faster than the query it wraps.
- **Release QA use for views:** save a repeated check such as deck-card counts
  or orphan reviews, query the view before and after a migration, and give the
  team one readable definition instead of copying a long join into every test.
- **View watch-outs:** nested views hide logic; a change to a base table can
  break a view; permissions on the view and its base tables still matter.
- **Index:** a structure that speeds reads at the cost of writes and storage.
  Clustered indexes define the table's row order; nonclustered indexes are
  separate structures. Key-column order matters, and included columns can make
  a nonclustered index covering for a query.
- **Release QA use for indexes:** check whether a slow verification query has a
  supporting index, compare logical reads before and after adding one, and do
  not add indexes to a shared environment without approval.

### CTE coverage

A common table expression (CTE) is a named query that exists for one statement.
It makes a multi-step check readable without creating a table or repeating a
subquery. SQL Server and standard SQL share the same `WITH` shape, so the guide
shows one example and labels it as valid in both.

```sql
WITH deck_card_counts AS (
    SELECT deck_id, COUNT(*) AS card_count
    FROM cards
    GROUP BY deck_id
)
SELECT d.title, COALESCE(c.card_count, 0) AS card_count
FROM decks AS d
LEFT JOIN deck_card_counts AS c ON c.deck_id = d.deck_id;
```

The guide also shows two CTEs in one `WITH` clause, for example a card-count CTE
and a review-count CTE joined in the final `SELECT`, and compares a CTE with the
equivalent nested subquery. Part 6 includes at least 3 Q&A and 4 MCQs on CTEs.

CTE watch-outs: a CTE is not a temporary table and is not stored after the
statement; its scope ends at the semicolon; a CTE referenced twice may be
evaluated twice; and recursive CTEs are out of scope for this pack.

### SQL Server and tuning coverage

The SQL Server track is deliberately practical, not a DBA course. Every
comparison table puts the SQL Server form in the first column and the standard
SQL form in the second:

- **Syntax differences:** `TOP` and `OFFSET ... FETCH NEXT`; `GETDATE()` and
  `SYSDATETIME()`; `ISNULL` versus `COALESCE`; `+` and `CONCAT` for strings;
  `IDENTITY`, `BIT`, `NVARCHAR`, `DATETIME2`; `IIF`, `DATEADD`, `DATEDIFF`,
  `STRING_AGG`; `CREATE OR ALTER VIEW`.
- **Reading plans:** estimated versus actual plans, scans versus seeks, key
  lookups, sort and hash operators, estimated versus actual row counts, and
  missing-index and conversion warnings.
- **Measuring:** `SET STATISTICS IO ON`, `SET STATISTICS TIME ON`, and comparing
  logical reads before and after a query change.
- **Making predicates SARGable:** avoid wrapping indexed columns in functions;
  use range comparisons for dates; avoid leading-wildcard `LIKE`; keep data types
  aligned to avoid implicit conversion; prefer `EXISTS` over `NOT IN` when
  `NULL` is possible.
- **Indexes:** clustered versus nonclustered, key order, included columns,
  covering indexes, and the write-cost trade-off of adding another index.
- **Query habits:** avoid `SELECT *`; use `UNION ALL` unless deduplication is
  required; understand parameter sniffing and when `OPTION (RECOMPILE)` is a
  targeted fix; treat `WITH (NOLOCK)` as a correctness risk, not a tuning
  shortcut.

Tuning claims stay checkable: every example names the query, the predicate, the
index, and the measurement that would show a difference. The guide does not
promise a speedup without a plan or statistics comparison.

## Question bank design

### Q&A distribution (100)

| Part | Count |
|---|---:|
| 1 Relational basics | 7 |
| 2 `SELECT` | 9 |
| 3 Filtering and `NULL` | 11 |
| 4 Aggregation | 11 |
| 5 Joins and `UNION` | 14 |
| 6 Subqueries and simple CTEs | 9 |
| 7 Data changes and transactions | 9 |
| 8 Schema, constraints, indexes, views | 9 |
| 9 Window functions | 5 |
| 10 SQL Server dialect and tuning | 7 |
| 11 Release QA patterns | 9 |
| **Total** | **100** |

### MCQ distribution (150)

| Part | Count |
|---|---:|
| 1 Relational basics | 10 |
| 2 `SELECT` | 14 |
| 3 Filtering and `NULL` | 17 |
| 4 Aggregation | 17 |
| 5 Joins and `UNION` | 21 |
| 6 Subqueries and simple CTEs | 14 |
| 7 Data changes and transactions | 14 |
| 8 Schema, constraints, indexes, views | 14 |
| 9 Window functions | 8 |
| 10 SQL Server dialect and tuning | 10 |
| 11 Release QA patterns | 11 |
| **Total** | **150** |

### Style rules

- At least 60 of 150 MCQ stems are scenarios, not definitions.
- Four options per MCQ, exactly one correct answer, and a `**Correct answer: X.**`
  explanation that names the trap in the distractors.
- Answer letters are roughly balanced across A–D (target 37–38 each).
- No exact or number-insensitive duplicate stems across the Q&A and MCQ files.
- Options are commands, clauses, or result descriptions as appropriate; no
  option is a prose echo of the stem.
- Q&A answers are 2–5 sentences, with one concrete query or result where it
  helps.
- Use uppercase SQL keywords consistently in examples; table and column names
  stay lowercase.
- SQL Server and standard variants are labeled, with the SQL Server form first.

## Verification

Structural checks, run from a plan workspace:

- Counts, sequential numbering, and per-part totals for both banks.
- Balanced `<details>` reveal blocks in the Q&A and one answer line per MCQ.
- Four options per MCQ and answer-letter distribution.
- Markdown TOC anchors resolve.
- Exact and fuzzy duplicate-stem detection (numbers normalized).
- Scenario-share heuristic and explanation-presence checks.
- Dialect checks: SQL Server examples are labeled and come first; standard
  examples are labeled and do not use SQL Server-only syntax; syntax that is
  neither SQL Server nor standard is excluded.
- Every SQL fenced block is read for syntax; SQL Server claims are checked
  against Microsoft Learn. No database is installed, so no execution claim is
  made.

## What is left to the builder

- Write the exact explanations, examples, questions, options, and explanations.
- Choose the sample rows that make the release QA patterns concrete while
  keeping the data small enough to reason about.
- Keep the guide and question banks consistent with the same schema and values.
- Verify SQL Server syntax and tuning claims against current Microsoft
  documentation.
- Run the structural checks and a fresh-context review before finishing the
  branch.
