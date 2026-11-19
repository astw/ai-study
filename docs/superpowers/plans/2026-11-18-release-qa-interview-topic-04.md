# SQL for Release QA — Topic 4 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add `release-qa-interview/topic-04-sql/` with a SQL Server-first knowledge guide, 100 Q&A, 150 MCQs, and a README, covering standard SQL comparisons, joins, simple CTEs, views, indexes, and practical tuning.

**Architecture:** Four Markdown deliverables under one topic folder. The guide teaches SQL Server syntax first and standard SQL second, using one flashcards schema and one fixed sample data set. The two question banks reuse the guide's part titles and schema. Python 3 structural checkers are the test suite; no database is installed, so every SQL claim is reviewed, not executed.

**Tech Stack:** Markdown, SQL (SQL Server/T-SQL and standard SQL), Python 3 standard library.

**Spec:** `docs/superpowers/specs/2026-11-18-release-qa-interview-topic-04-design.md`

## Global Constraints

- Branch: `release-qa-interview-topic-04`, created from `release-qa-interview-topic-03` at `7de72df`; topic 3 is intentionally unmerged, so this branch is stacked.
- Folder: `release-qa-interview/topic-04-sql/`.
- Files: `sql-for-release-qa.md`, `qa-100.md`, `mcq-150.md`, `README.md`.
- SQL Server syntax comes first; the standard SQL comparison comes second. Label both.
- Excluded: `CROSS JOIN`, `MERGE`, `TRY_CONVERT`, `CROSS APPLY`, `OUTER APPLY`, `OUTPUT`, `INTERSECT`, `EXCEPT`, and recursive CTEs.
- No vendor administration, stored procedures, triggers, or scheduler syntax. No MySQL/PostgreSQL/Oracle administration.
- No claim that any example was executed. SQL Server claims are checked against Microsoft Learn; standard claims against a standard SQL reference.
- Q&A counts by part: 7, 9, 11, 11, 14, 9, 9, 9, 5, 7, 9 = 100.
- MCQ counts by part: 10, 14, 17, 17, 21, 14, 14, 14, 8, 10, 11 = 150.
- MCQ format: four options A–D, exactly one `**Correct answer: X.**` line, one `<details>` block per item.
- Q&A format: `#### QN.` plus one `<details><summary>Show answer</summary>` block.
- Answer letters target 37–38 each across the 150 MCQs.
- At least 60 of 150 MCQ stems are scenarios.
- No exact or number-insensitive duplicate stems across both banks.
- Every guide part ends with `### Release QA Use` and `### Watch-outs`.
- Code fences are balanced; SQL examples use fenced blocks marked `sql`.
- Do not use `LIMIT`, `AUTO_INCREMENT`, `IFNULL`, `NOW()`, or `GROUP_CONCAT` in examples. The portability note may name them as other-vendor forms.
- Commit after each task. End commit messages with the repository's required attribution line.

## Shared Data Contract

Every guide example and question uses these tables and rows. Do not invent a second schema.

### Standard SQL schema

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

### SQL Server schema

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

### Sample rows

`users`:

| user_id | email | display_name | created_at |
|---:|---|---|---|
| 1 | alice@example.com | Alice | 2026-01-05 09:00:00 |
| 2 | bob@example.com | Bob | 2026-01-06 10:00:00 |
| 3 | carol@example.com | NULL | 2026-01-07 11:00:00 |
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
| 10003 | 1002 | 1 | NULL | 2026-01-22 11:00:00 |
| 10004 | 1003 | 1 | 3 | 2026-01-23 12:00:00 |
| 10005 | 1004 | 2 | 5 | 2026-01-24 13:00:00 |
| 10006 | 1002 | 3 | 2 | 2026-01-25 14:00:00 |
| 10007 | 1004 | 1 | NULL | 2026-02-01 15:00:00 |

QA-only staging tables:

`legacy_users` has rows `(1, alice@example.com, Alice)`, `(2, bob@example.com, Bob)`, `(3, alice@example.com, Alice)`, `(4, carol@example.com, Carol)`. The duplicate email on user 3 is the duplicate-check exercise.

`legacy_reviews` has rows `(20001, 1001, 1, 5)`, `(20002, 9999, 1, 4)`, `(20003, 1001, 9999, 3)`, `(20004, 1002, 2, NULL)`. The missing card 9999 and missing user 9999 are the orphan-check exercise.

Facts the questions rely on: user 5 has no decks; deck 104 has no cards; card 1005 has no reviews; user 3 has a `NULL` display name; users 1 and 4 share the display name `Alice`; deck titles repeat across users; reviews 10003 and 10007 have `NULL` ratings.

## Review Focus

1. **Dialect leakage:** SQL Server-only syntax presented as standard, or standard syntax presented as SQL Server. `check_content.py` scans SQL fences for forbidden terms; each guide task reviews the SQL Server and standard labels; Part 5 must not use `USING` in a SQL Server example because SQL Server does not support it.
2. **Join multiplication:** a one-to-many join inflates `COUNT(*)`. Part 5 includes a worked count with and without `COUNT(DISTINCT ...)`, and the Q&A/MCQ banks test the trap.
3. **NULL traps:** `NOT IN` with a `NULL`, `COUNT(column)` versus `COUNT(*)`, and `LEFT JOIN ... WHERE right.col IS NULL` versus a filter in `ON`. Parts 3, 4, and 11 test all three.
4. **Tuning claims:** advice must be checkable. Part 10 names the query, predicate, index, and `STATISTICS IO` measurement; it treats `WITH (NOLOCK)` as a correctness risk, not a fix.
5. **CTE and view assumptions:** a CTE is not a temporary table and its scope ends at the statement; a plain view stores no rows and is not automatically faster. Parts 6 and 8 state both, and the banks test them.

---

### Task 1: Branch, checkers, and guide Parts 1–2

**Files:**
- Create: `release-qa-interview/topic-04-sql/sql-for-release-qa.md`
- Create: `.superpowers/sdd/2026-11-18-release-qa-interview-topic-04/check_guide.py`
- Create: `.superpowers/sdd/2026-11-18-release-qa-interview-topic-04/check_qa.py`
- Create: `.superpowers/sdd/2026-11-18-release-qa-interview-topic-04/check_mcq.py`
- Create: `.superpowers/sdd/2026-11-18-release-qa-interview-topic-04/check_content.py`
- Create: `.superpowers/sdd/2026-11-18-release-qa-interview-topic-04/check_all.py`
- Create: `.superpowers/sdd/2026-11-18-release-qa-interview-topic-04/progress.md`

**Interfaces:**
- Consumes: the approved design and this plan.
- Produces: the branch, the checker CLI, and guide Parts 1–2 with the shared schema.

- [ ] **Step 1: Create the branch and workspace**

```bash
git switch -c release-qa-interview-topic-04 release-qa-interview-topic-03
mkdir -p .superpowers/sdd/2026-11-18-release-qa-interview-topic-04
```

Write `progress.md` with the first line:
`# SDD ledger — plan: docs/superpowers/plans/2026-11-18-release-qa-interview-topic-04.md`

- [ ] **Step 2: Write the failing guide test**

Create `check_guide.py` with these checks:

- `--parts` accepts one or more integers; a missing part fails.
- `--toc` compares every `](#anchor)` link against headings, using a slug that lowercases, removes punctuation except spaces and hyphens, and replaces spaces with hyphens.
- Code fences are even.
- Requested parts contain the exact headings listed in the task.
- Every requested part contains `### Release QA Use` and `### Watch-outs`.
- Forbidden SQL tokens fail inside SQL code fences: `CROSS JOIN`, `MERGE`, `TRY_CONVERT`, `CROSS APPLY`, `OUTER APPLY`, `OUTPUT`, `INTERSECT`, `EXCEPT`. Do not scan English prose for `EXCEPT` or `OUTPUT`.
- When Part 6 is requested or `--all` is used, it must contain `WITH deck_card_counts`.
- When Part 8 is requested or `--all` is used, it must contain `CREATE VIEW` and `CREATE INDEX`.
- When Part 10 is requested or `--all` is used, it must contain `STATISTICS IO`, `SARGable`, and `OPTION (RECOMPILE)`.

Run:
`python .superpowers/sdd/2026-11-18-release-qa-interview-topic-04/check_guide.py --parts 1 2`
Expected: FAIL with a missing-guide error.

- [ ] **Step 3: Write the guide title, intro, TOC, and Parts 1–2**

Use `# SQL for Release QA` as the title. The intro names the audience, the SQL Server-first/standard-second convention, the flashcards schema, and the no-execution caveat. The TOC links all eleven parts.

Part 1 headings exactly:
`## Part 1 — Relational Basics`, `### Tables, Rows, and Columns`, `### Keys`, `### NULL and Data Types`, `### The Flashcards Schema`, `### Release QA Use`, `### Watch-outs`.

Part 2 headings exactly:
`## Part 2 — Reading Data with SELECT`, `### SELECT and FROM`, `### Aliases and Expressions`, `### DISTINCT`, `### ORDER BY`, `### Limiting Rows`, `### Release QA Use`, `### Watch-outs`.

Content requirements:
- Part 1 includes the standard and SQL Server DDL from the Shared Data Contract, a key table, and the sample rows summary.
- Part 1 explains one-to-many relationships and why `decks.user_id` references `users.user_id`.
- Part 2 shows `SELECT`, aliases, expressions, `DISTINCT`, `ORDER BY`, and limiting rows.
- Limiting rows shows SQL Server `TOP (n)` and `OFFSET ... FETCH NEXT` first, then standard `FETCH FIRST n ROWS ONLY`.
- State that `TOP`, `OFFSET ... FETCH NEXT`, and `FETCH FIRST` need `ORDER BY` for deterministic results; `TOP` without it is not a stable selection.
- Every SQL fence is labeled `**SQL Server:**` or `**Standard SQL:**`.
- Both parts end with `### Release QA Use` and `### Watch-outs`.

- [ ] **Step 4: Run the guide check**

Run:
`python .superpowers/sdd/2026-11-18-release-qa-interview-topic-04/check_guide.py --parts 1 2`
Expected: `guide checks passed`.

- [ ] **Step 5: Compile the checkers**

Run:
`python -m py_compile .superpowers/sdd/2026-11-18-release-qa-interview-topic-04/check_*.py`
Expected: exit 0.

- [ ] **Step 6: Commit**

```bash
git add docs/superpowers/specs/2026-11-18-release-qa-interview-topic-04-design.md \
        docs/superpowers/plans/2026-11-18-release-qa-interview-topic-04.md \
        release-qa-interview/topic-04-sql/sql-for-release-qa.md
git commit -m "feat: add SQL guide parts 1-2 and topic 4 checkers"
```

Ledger line: `Task 1: complete (commits <base7>..<head7>, tests: check_guide.py --parts 1 2 → guide checks passed)`.

---

### Task 2: Guide Parts 3–4

**Files:**
- Modify: `release-qa-interview/topic-04-sql/sql-for-release-qa.md`

**Interfaces:**
- Consumes: the shared schema and Part 1–2 terminology.
- Produces: filtering, `NULL`, and aggregation sections used by the question banks.

- [ ] **Step 1: Add Part 3**

Headings:
`## Part 3 — Filtering and NULL`, `### WHERE`, `### AND, OR, and NOT`, `### IN, BETWEEN, and LIKE`, `### NULL and Three-Valued Logic`, `### The NOT IN Trap`, `### Release QA Use`, `### Watch-outs`.

Cover:
- `WHERE` filters rows before grouping.
- `AND` binds tighter than `OR`; show parentheses.
- `IN`, `BETWEEN`, and `LIKE` with `%` and `_`.
- `NULL = NULL` is unknown; use `IS NULL`.
- `NOT IN (1, NULL)` returns no rows; show the trap and the `NOT EXISTS` alternative.
- `COALESCE` and `NULLIF`.
- SQL Server examples first; standard equivalents second.

- [ ] **Step 2: Add Part 4**

Headings:
`## Part 4 — Aggregating and Grouping`, `### Aggregate Functions`, `### COUNT(*) and COUNT(column)`, `### GROUP BY`, `### HAVING`, `### Release QA Use`, `### Watch-outs`.

Cover:
- `COUNT(*)`, `COUNT(column)`, `COUNT(DISTINCT column)`.
- `SUM`, `AVG`, `MIN`, `MAX`, and `NULL` behavior.
- `GROUP BY` one and two columns.
- `WHERE` versus `HAVING`.
- Aggregate without `GROUP BY`.
- A deck-card count example that shows `COUNT(*)` versus `COUNT(DISTINCT ...)` after a join.

- [ ] **Step 3: Run the guide check**

Run:
`python .superpowers/sdd/2026-11-18-release-qa-interview-topic-04/check_guide.py --parts 1 2 3 4`
Expected: `guide checks passed`.

- [ ] **Step 4: Commit**

```bash
git add release-qa-interview/topic-04-sql/sql-for-release-qa.md
git commit -m "feat: add SQL guide filtering and aggregation"
```

Ledger line with the test command and result.

---

### Task 3: Guide Part 5 — Joins and UNION

**Files:**
- Modify: `release-qa-interview/topic-04-sql/sql-for-release-qa.md`

**Interfaces:**
- Consumes: `users`, `decks`, `cards`, `reviews`.
- Produces: the join examples and row-count rules used by Q&A and MCQ Parts 5.

- [ ] **Step 1: Add Part 5**

Headings:
`## Part 5 — Joins and UNION`, `### INNER JOIN`, `### LEFT JOIN`, `### RIGHT JOIN`, `### FULL OUTER JOIN`, `### SELF JOIN`, `### Join Chains and ON vs USING`, `### Join Multiplication`, `### UNION and UNION ALL`, `### Release QA Use`, `### Watch-outs`.

Content requirements:
- `INNER JOIN`: decks and cards; only decks with cards.
- `LEFT JOIN`: all decks, `NULL` card columns for deck 104; then `WHERE c.card_id IS NULL` to find it.
- `RIGHT JOIN`: all reviews plus unmatched cards; explain why it is often rewritten as a left join.
- `FULL OUTER JOIN`: compare two key sets, such as users and decks, and find unmatched rows on both sides.
- `SELF JOIN`: two aliases of `cards` in the same deck, or two reviews on the same card.
- Join chains: users → decks → cards → reviews.
- `ON` versus `USING`: SQL Server supports `ON`; standard SQL also supports `USING`; show `USING` only in the standard example and state that SQL Server does not accept it.
- Join multiplication: show `COUNT(*)` after joining decks to cards, then `COUNT(DISTINCT c.card_id)` or a pre-aggregated subquery; deck 101 has two cards, so the difference is visible.
- `UNION` versus `UNION ALL`: same column count and compatible types; `UNION` removes duplicates and costs more; `UNION ALL` keeps them.
- No `CROSS JOIN`.

- [ ] **Step 2: Run the guide check**

Run:
`python .superpowers/sdd/2026-11-18-release-qa-interview-topic-04/check_guide.py --parts 1 2 3 4 5`
Expected: `guide checks passed`.

- [ ] **Step 3: Commit**

```bash
git add release-qa-interview/topic-04-sql/sql-for-release-qa.md
git commit -m "feat: add SQL guide joins and union"
```

---

### Task 4: Guide Parts 6–7 — Subqueries, CTEs, data changes, transactions

**Files:**
- Modify: `release-qa-interview/topic-04-sql/sql-for-release-qa.md`

**Interfaces:**
- Consumes: the shared schema and the join examples.
- Produces: the CTE example `WITH deck_card_counts` and transaction rules used by Q&A and MCQ Parts 6–7.

- [ ] **Step 1: Add Part 6**

Headings:
`## Part 6 — Subqueries and Simple CTEs`, `### Scalar Subqueries`, `### IN and EXISTS`, `### Correlated Subqueries`, `### Simple CTEs`, `### Multiple CTEs`, `### CTE vs Subquery`, `### Release QA Use`, `### Watch-outs`.

Content requirements:
- Scalar subquery: compare a rating with the overall average.
- `IN` and `EXISTS`: decks with cards; decks with no cards using `NOT EXISTS`.
- Correlated subquery: latest review per card, or cards with no reviews.
- Simple CTE exactly:
  `WITH deck_card_counts AS (SELECT deck_id, COUNT(*) AS card_count FROM cards GROUP BY deck_id) SELECT d.title, COALESCE(c.card_count, 0) AS card_count FROM decks AS d LEFT JOIN deck_card_counts AS c ON c.deck_id = d.deck_id;`
- Multiple CTEs: card counts and review counts in one `WITH`.
- CTE versus nested subquery: same result, clearer names.
- Watch-outs: a CTE is not a temp table; scope ends at the statement; a CTE referenced twice may be evaluated twice; recursive CTEs are out of scope.

- [ ] **Step 2: Add Part 7**

Headings:
`## Part 7 — Changing Data and Transactions`, `### INSERT`, `### UPDATE`, `### DELETE`, `### Transactions`, `### Savepoints`, `### Release QA Use`, `### Watch-outs`.

Content requirements:
- `INSERT` one row and `INSERT ... SELECT`.
- `UPDATE` with a `WHERE`; show the danger of omitting it.
- `DELETE` with a `WHERE`; show a subquery-based delete.
- SQL Server `BEGIN TRANSACTION`, `COMMIT`, `ROLLBACK`, `SAVE TRANSACTION` first; standard `START TRANSACTION`, `COMMIT`, `ROLLBACK`, `SAVEPOINT` second.
- Test-data cleanup: wrap setup and cleanup in a transaction and roll back; never run destructive changes in a shared environment without approval.
- Mention that constraints can reject a change and that the error text matters to QA.

- [ ] **Step 3: Run the guide check**

Run:
`python .superpowers/sdd/2026-11-18-release-qa-interview-topic-04/check_guide.py --parts 1 2 3 4 5 6 7`
Expected: `guide checks passed`.

- [ ] **Step 4: Commit**

```bash
git add release-qa-interview/topic-04-sql/sql-for-release-qa.md
git commit -m "feat: add SQL guide subqueries, CTEs, and transactions"
```

---

### Task 5: Guide Parts 8–9 — Schema, views, indexes, window functions

**Files:**
- Modify: `release-qa-interview/topic-04-sql/sql-for-release-qa.md`

**Interfaces:**
- Consumes: the shared schema and DDL.
- Produces: view and index examples used by Q&A and MCQ Parts 8–9.

- [ ] **Step 1: Add Part 8**

Headings:
`## Part 8 — Schema, Constraints, Indexes, and Views`, `### CREATE TABLE`, `### Constraints`, `### Views`, `### Indexes`, `### Release QA Use`, `### Watch-outs`.

Content requirements:
- `CREATE TABLE` in SQL Server first and standard second.
- Primary key, foreign key, `UNIQUE`, `NOT NULL`, `CHECK`, `DEFAULT`.
- State that a `CHECK` constraint passes a `NULL` because the result is unknown, and that `UNIQUE` and `NULL` behavior differs across databases; keep unique columns `NOT NULL` in this schema.
- `CREATE VIEW` standard; SQL Server `CREATE OR ALTER VIEW` first.
- A view example `v_deck_card_counts` that returns deck title and card count; query it and compare with the base-table query.
- Views store no rows, are not automatically faster, and nested views hide logic.
- `CREATE INDEX` for a nonclustered index on `cards(deck_id)`; explain clustered versus nonclustered, key order, included columns, and covering indexes.
- Index trade-off: reads improve, writes and storage cost more; do not add indexes in a shared environment without approval.

- [ ] **Step 2: Add Part 9**

Headings:
`## Part 9 — Window Functions`, `### ROW_NUMBER`, `### RANK and DENSE_RANK`, `### PARTITION BY`, `### SUM OVER`, `### LAG and LEAD`, `### Release QA Use`, `### Watch-outs`.

Content requirements:
- `ROW_NUMBER() OVER (PARTITION BY card_id ORDER BY reviewed_at DESC)` to pick the latest review per card.
- `RANK` and `DENSE_RANK` differences.
- `SUM(...) OVER (PARTITION BY ...)` for running or grouped totals.
- `LAG` and `LEAD` for comparing consecutive reviews.
- SQL Server and standard SQL share the same window-function shape; label the example as valid in both.
- Watch-outs: window functions run after `WHERE`/`GROUP BY`; filter the window result in an outer query or CTE, not in `WHERE`.

- [ ] **Step 3: Run the guide check**

Run:
`python .superpowers/sdd/2026-11-18-release-qa-interview-topic-04/check_guide.py --parts 1 2 3 4 5 6 7 8 9`
Expected: `guide checks passed`.

- [ ] **Step 4: Commit**

```bash
git add release-qa-interview/topic-04-sql/sql-for-release-qa.md
git commit -m "feat: add SQL guide views, indexes, and window functions"
```

---

### Task 6: Guide Part 10 — SQL Server dialect and tuning

**Files:**
- Modify: `release-qa-interview/topic-04-sql/sql-for-release-qa.md`

**Interfaces:**
- Consumes: the shared schema and examples from Parts 1–9.
- Produces: the dialect table and tuning rules used by Q&A and MCQ Part 10.

- [ ] **Step 1: Add Part 10**

Headings:
`## Part 10 — SQL Server Dialect and Tuning`, `### SQL Server vs Standard SQL`, `### Reading Execution Plans`, `### Measuring with STATISTICS IO and TIME`, `### SARGable Predicates`, `### Indexes and Covering Queries`, `### Query Habits`, `### Parameter Sniffing and OPTION (RECOMPILE)`, `### Release QA Use`, `### Watch-outs`.

Content requirements:
- Dialect table with SQL Server first and standard SQL second:
  `TOP (n)` / `OFFSET ... FETCH NEXT` vs `FETCH FIRST n ROWS ONLY`;
  `GETDATE()` / `SYSDATETIME()` vs `CURRENT_TIMESTAMP`;
  `ISNULL` vs `COALESCE`;
  `+` / `CONCAT` vs `||`;
  `IDENTITY(1,1)` vs `GENERATED ... AS IDENTITY` (or explicit IDs);
  `BIT` vs `BOOLEAN`;
  `NVARCHAR` vs `VARCHAR`;
  `DATETIME2` vs `TIMESTAMP`;
  `IIF` vs `CASE`;
  `DATEADD` / `DATEDIFF` vs interval arithmetic;
  `STRING_AGG` has no single standard equivalent in this guide.
- Warn that SQL Server `TIMESTAMP` is a rowversion type, not a date/time; use `DATETIME2` for timestamps.
- Warn that SQL Server `+` returns `NULL` if either string is `NULL`, while `CONCAT` treats `NULL` as an empty string; standard `||` returns `NULL` if either side is `NULL`.
- Plans: estimated versus actual, scans versus seeks, key lookup, sort/hash, estimated versus actual rows.
- `SET STATISTICS IO ON` and `SET STATISTICS TIME ON`; logical reads are the comparison metric.
- SARGable predicates: date range instead of `YEAR(created_at) = 2026`; no leading-wildcard `LIKE`; no function on an indexed column; data types aligned to avoid implicit conversion.
- Indexes: clustered/nonclustered, key order, included columns, covering index, write cost.
- Query habits: avoid `SELECT *`; use `UNION ALL` unless deduplication is required; `EXISTS` instead of `NOT IN` when `NULL` is possible.
- Parameter sniffing and `OPTION (RECOMPILE)` as a targeted fix, with the compile-cost caveat.
- `WITH (NOLOCK)` is a correctness risk, not a tuning fix.
- Every tuning claim names the query, predicate, index, and measurement. Do not promise a speedup without a plan or statistics comparison.

- [ ] **Step 2: Run the guide check**

Run:
`python .superpowers/sdd/2026-11-18-release-qa-interview-topic-04/check_guide.py --parts 1 2 3 4 5 6 7 8 9 10`
Expected: `guide checks passed`.

- [ ] **Step 3: Commit**

```bash
git add release-qa-interview/topic-04-sql/sql-for-release-qa.md
git commit -m "feat: add SQL Server dialect and tuning guide"
```

---

### Task 7: Guide Part 11, portability note, and README

**Files:**
- Modify: `release-qa-interview/topic-04-sql/sql-for-release-qa.md`
- Create: `release-qa-interview/topic-04-sql/README.md`

**Interfaces:**
- Consumes: all guide parts and the shared data contract.
- Produces: the completed guide and reader entry point.

- [ ] **Step 1: Add Part 11**

Headings:
`## Part 11 — Release QA Query Patterns`, `### Baseline Counts`, `### Duplicate Detection`, `### Orphan Detection`, `### Required-Field Nulls`, `### Before and After Comparisons`, `### Status Distributions`, `### Test Data Setup and Cleanup`, `### Query Review Checklist`, `### Release QA Use`, `### Watch-outs`.

Content requirements:
- Baseline counts per table before and after a release.
- Duplicate detection on `legacy_users.email` and on `decks(title, user_id)`; show `GROUP BY ... HAVING COUNT(*) > 1`.
- Orphan detection on `legacy_reviews` for missing `card_id` and `user_id` using `LEFT JOIN ... IS NULL`.
- Required-field nulls: `users.display_name` is allowed to be null; `reviews.rating` is nullable but may be a product rule; distinguish schema rules from product rules.
- Before/after comparison with `FULL OUTER JOIN` on keys and `IS NULL` checks; no `EXCEPT`.
- Status distributions for `is_public` and ratings.
- Test data setup and cleanup in a transaction; roll back; never leave fixtures behind.
- View-based check with `v_deck_card_counts`.
- Query review checklist: correct join type, `NULL` handling, row multiplication, filters in the right clause, deterministic ordering, measurement.

- [ ] **Step 2: Add the portability note**

At the end of the guide, state: SQL Server is the primary track; standard SQL is the comparison; other databases may differ. Name `LIMIT`, `AUTO_INCREMENT`, `IFNULL`, `NOW()`, and `GROUP_CONCAT` only as examples of forms this guide does not teach. No third-database guarantee.

- [ ] **Step 3: Write README**

Include: what the folder contains, who it is for, the SQL Server-first/standard-second convention, the study order (guide → Q&A → MCQs), the counts (100 Q&A, 150 MCQs), the 11-part coverage table, the flashcards schema, and a practice note that no database is bundled and no example was executed here.

- [ ] **Step 4: Run the guide and README checks**

Run:
`python .superpowers/sdd/2026-11-18-release-qa-interview-topic-04/check_guide.py --all --toc`
Expected: `guide checks passed`.

Run:
`python .superpowers/sdd/2026-11-18-release-qa-interview-topic-04/check_content.py`
Expected: content checks pass for the guide, including CTE, view, index, and tuning coverage.

- [ ] **Step 5: Commit**

```bash
git add release-qa-interview/topic-04-sql/sql-for-release-qa.md \
        release-qa-interview/topic-04-sql/README.md
git commit -m "feat: complete SQL guide and README"
```

---

### Task 8: Q&A Parts 1–4

**Files:**
- Create: `release-qa-interview/topic-04-sql/qa-100.md`

**Interfaces:**
- Consumes: guide Parts 1–4 and the shared data contract.
- Produces: Q1–Q38 with hidden answers and a TOC.

- [ ] **Step 1: Add the Q&A shell and Parts 1–4**

Part headings and counts:
`## Part 1 — Relational Basics (7 questions)`, `## Part 2 — Reading Data with SELECT (9 questions)`, `## Part 3 — Filtering and NULL (11 questions)`, `## Part 4 — Aggregating and Grouping (11 questions)`.

Question topics:
- Part 1: table/row/column; primary key; foreign key; `NULL`; data types; one-to-many; reading a schema.
- Part 2: `SELECT`/`FROM`; aliases; `DISTINCT`; `ORDER BY`; SQL Server `TOP`; `OFFSET ... FETCH NEXT`; standard `FETCH FIRST`; expressions; `SELECT *` versus named columns.
- Part 3: `WHERE`; `AND`/`OR` precedence; `IN`; `BETWEEN`; `LIKE`; `IS NULL`; three-valued logic; `NOT IN` + `NULL`; `COALESCE`; `NULLIF`; parenthesizing a filter.
- Part 4: `COUNT(*)`; `COUNT(column)`; `COUNT(DISTINCT)`; `SUM`/`AVG`; `MIN`/`MAX`; `GROUP BY`; `HAVING`; `WHERE` vs `HAVING`; `NULL` in aggregates; multiple grouping columns; aggregate without `GROUP BY`.

Each answer is 2–5 sentences. Where syntax differs, show SQL Server first and standard second. Add the TOC links for all eleven parts now, even though later parts do not exist yet.

- [ ] **Step 2: Run the Q&A check**

Run:
`python .superpowers/sdd/2026-11-18-release-qa-interview-topic-04/check_qa.py --parts 1:7 2:9 3:11 4:11 --total 38`
Expected: counts match, total 38, sequential numbering, 38 balanced reveal blocks.

- [ ] **Step 3: Commit**

```bash
git add release-qa-interview/topic-04-sql/qa-100.md
git commit -m "feat: add SQL Q&A parts 1-4"
```

---

### Task 9: Q&A Parts 5–8

**Files:**
- Modify: `release-qa-interview/topic-04-sql/qa-100.md`

**Interfaces:**
- Consumes: guide Parts 5–8; Q1–Q38 already numbered.
- Produces: Q39–Q79.

- [ ] **Step 1: Add Parts 5–8**

Part headings and counts:
`## Part 5 — Joins and UNION (14 questions)`, `## Part 6 — Subqueries and Simple CTEs (9 questions)`, `## Part 7 — Changing Data and Transactions (9 questions)`, `## Part 8 — Schema, Constraints, Indexes, and Views (9 questions)`.

Question topics:
- Part 5: each join type; expected row counts; `ON` vs `USING` and SQL Server's lack of `USING`; join chains; `LEFT JOIN ... WHERE IS NULL`; filtering in `ON` vs `WHERE`; join multiplication; `UNION` vs `UNION ALL`; column compatibility; duplicate removal.
- Part 6: scalar subquery; `IN`; `EXISTS`; `NOT EXISTS`; correlated subquery; simple CTE; multiple CTEs; CTE vs subquery; CTE scope and reuse.
- Part 7: `INSERT`; `INSERT ... SELECT`; `UPDATE`; `UPDATE` with subquery; `DELETE`; `DELETE` with subquery; transactions; `ROLLBACK`/`SAVEPOINT`; test-data cleanup.
- Part 8: `CREATE TABLE`; primary/foreign keys; `UNIQUE`; `NOT NULL`; `CHECK`/`DEFAULT`; `CREATE VIEW`; `CREATE OR ALTER VIEW`; index basics; view caveats.

- [ ] **Step 2: Run the Q&A check**

Run:
`python .superpowers/sdd/2026-11-18-release-qa-interview-topic-04/check_qa.py --parts 1:7 2:9 3:11 4:11 5:14 6:9 7:9 8:9 --total 79`
Expected: total 79, sequential numbering, 79 balanced reveal blocks.

- [ ] **Step 3: Commit**

```bash
git add release-qa-interview/topic-04-sql/qa-100.md
git commit -m "feat: add SQL Q&A parts 5-8"
```

---

### Task 10: Q&A Parts 9–11

**Files:**
- Modify: `release-qa-interview/topic-04-sql/qa-100.md`

**Interfaces:**
- Consumes: guide Parts 9–11; Q1–Q79 already numbered.
- Produces: Q80–Q100 and a complete Q&A bank.

- [ ] **Step 1: Add Parts 9–11**

Part headings and counts:
`## Part 9 — Window Functions (5 questions)`, `## Part 10 — SQL Server Dialect and Tuning (7 questions)`, `## Part 11 — Release QA Query Patterns (9 questions)`.

Question topics:
- Part 9: `ROW_NUMBER`; `RANK` vs `DENSE_RANK`; `PARTITION BY`; `SUM OVER`; `LAG`/`LEAD`.
- Part 10: `TOP` vs `FETCH FIRST`; `GETDATE()` vs `CURRENT_TIMESTAMP`; `ISNULL` vs `COALESCE`; SQL Server types (`BIT`, `NVARCHAR`, `DATETIME2`); execution plans; `STATISTICS IO`/`TIME`; SARGable predicates; covering indexes; parameter sniffing/`OPTION (RECOMPILE)`.
- Part 11: baseline counts; duplicate detection; orphan detection; required-field nulls; before/after comparison; status distributions; test data setup/cleanup; view-based checks; query review checklist.

- [ ] **Step 2: Run the full Q&A check**

Run:
`python .superpowers/sdd/2026-11-18-release-qa-interview-topic-04/check_qa.py --parts 1:7 2:9 3:11 4:11 5:14 6:9 7:9 8:9 9:5 10:7 11:9 --total 100 --toc`
Expected: total 100, sequential numbering, 100 balanced reveal blocks, TOC anchors resolve.

- [ ] **Step 3: Commit**

```bash
git add release-qa-interview/topic-04-sql/qa-100.md
git commit -m "feat: complete SQL Q&A bank"
```

---

### Task 11: MCQ Parts 1–4

**Files:**
- Create: `release-qa-interview/topic-04-sql/mcq-150.md`

**Interfaces:**
- Consumes: guide Parts 1–4 and the shared data contract.
- Produces: MCQ 1–58 with four options, answers, and explanations.

- [ ] **Step 1: Add the MCQ shell and Parts 1–4**

Part headings and counts:
`## Part 1 — Relational Basics (10 questions)`, `## Part 2 — Reading Data with SELECT (14 questions)`, `## Part 3 — Filtering and NULL (17 questions)`, `## Part 4 — Aggregating and Grouping (17 questions)`.

Question topics:
- Part 1: keys, relationships, `NULL`, data types, schema reading, row/column terms.
- Part 2: `SELECT`, aliases, `DISTINCT`, `ORDER BY`, `TOP`, `OFFSET ... FETCH NEXT`, standard `FETCH FIRST`, expressions, column choice.
- Part 3: `WHERE`, precedence, `IN`, `BETWEEN`, `LIKE`, `IS NULL`, `NOT IN` + `NULL`, `COALESCE`, `NULLIF`, three-valued logic.
- Part 4: `COUNT(*)`, `COUNT(column)`, `COUNT(DISTINCT)`, `SUM`/`AVG`, `GROUP BY`, `HAVING`, `WHERE` vs `HAVING`, `NULL` aggregates, multiple grouping columns.

At least 20 of these 58 stems are scenarios. Use commands, clauses, or result descriptions as options; do not restate the stem. Add the TOC links for all eleven parts now.

- [ ] **Step 2: Run the MCQ check**

Run:
`python .superpowers/sdd/2026-11-18-release-qa-interview-topic-04/check_mcq.py --parts 1:10 2:14 3:17 4:17 --total 58`
Expected: counts match, total 58, four options per item, 58 answer lines, balanced reveal blocks.

- [ ] **Step 3: Commit**

```bash
git add release-qa-interview/topic-04-sql/mcq-150.md
git commit -m "feat: add SQL MCQs parts 1-4"
```

---

### Task 12: MCQ Parts 5–7

**Files:**
- Modify: `release-qa-interview/topic-04-sql/mcq-150.md`

**Interfaces:**
- Consumes: guide Parts 5–7; MCQ 1–58 already numbered.
- Produces: MCQ 59–107.

- [ ] **Step 1: Add Parts 5–7**

Part headings and counts:
`## Part 5 — Joins and UNION (21 questions)`, `## Part 6 — Subqueries and Simple CTEs (14 questions)`, `## Part 7 — Changing Data and Transactions (14 questions)`.

Question topics:
- Part 5: each join type; result sets; `ON` vs `USING`; SQL Server's lack of `USING`; join chains; `LEFT JOIN ... IS NULL`; filter placement; join multiplication; `UNION` vs `UNION ALL`; column compatibility.
- Part 6: scalar subquery; `IN`; `EXISTS`; `NOT EXISTS`; correlated subquery; simple CTE; multiple CTEs; CTE vs subquery; CTE scope.
- Part 7: `INSERT`; `INSERT ... SELECT`; `UPDATE`; `UPDATE` with subquery; `DELETE`; `DELETE` with subquery; transaction boundaries; `ROLLBACK`/`SAVEPOINT`; cleanup.

At least 20 of these 49 stems are scenarios.

- [ ] **Step 2: Run the MCQ check**

Run:
`python .superpowers/sdd/2026-11-18-release-qa-interview-topic-04/check_mcq.py --parts 1:10 2:14 3:17 4:17 5:21 6:14 7:14 --total 107`
Expected: total 107, four options per item, 107 answer lines, balanced reveal blocks.

- [ ] **Step 3: Commit**

```bash
git add release-qa-interview/topic-04-sql/mcq-150.md
git commit -m "feat: add SQL MCQs parts 5-7"
```

---

### Task 13: MCQ Parts 8–11

**Files:**
- Modify: `release-qa-interview/topic-04-sql/mcq-150.md`

**Interfaces:**
- Consumes: guide Parts 8–11; MCQ 1–107 already numbered.
- Produces: MCQ 108–150 and a complete MCQ bank.

- [ ] **Step 1: Add Parts 8–11**

Part headings and counts:
`## Part 8 — Schema, Constraints, Indexes, and Views (14 questions)`, `## Part 9 — Window Functions (8 questions)`, `## Part 10 — SQL Server Dialect and Tuning (10 questions)`, `## Part 11 — Release QA Query Patterns (11 questions)`.

Question topics:
- Part 8: `CREATE TABLE`; keys; `UNIQUE`; `NOT NULL`; `CHECK`/`DEFAULT`; `CREATE VIEW`; `CREATE OR ALTER VIEW`; view caveats; clustered/nonclustered indexes; key order/included columns.
- Part 9: `ROW_NUMBER`; `RANK`/`DENSE_RANK`; `PARTITION BY`; `SUM OVER`; `LAG`/`LEAD`; filtering window results.
- Part 10: `TOP` vs `FETCH FIRST`; `GETDATE()` vs `CURRENT_TIMESTAMP`; `ISNULL` vs `COALESCE`; SQL Server types; execution plans; `STATISTICS IO`/`TIME`; SARGability; implicit conversion; covering indexes; `NOLOCK` risk; parameter sniffing.
- Part 11: baseline counts; duplicate detection; orphan detection; null checks; before/after comparison; status distributions; cleanup; view-based checks; query review checklist.

At least 20 of these 43 stems are scenarios. Answer letters across the full 150 must land at 37–38 each.

- [ ] **Step 2: Run the full MCQ check**

Run:
`python .superpowers/sdd/2026-11-18-release-qa-interview-topic-04/check_mcq.py --parts 1:10 2:14 3:17 4:17 5:21 6:14 7:14 8:14 9:8 10:10 11:11 --total 150 --toc --letter-bounds`
Expected: total 150, four options per item, 150 answer lines, 150 balanced reveal blocks, TOC anchors resolve, answer letters within 37–38 each.

- [ ] **Step 3: Commit**

```bash
git add release-qa-interview/topic-04-sql/mcq-150.md
git commit -m "feat: complete SQL MCQ bank"
```

---

### Task 14: Cross-file content check, review, and finish

**Files:**
- Test: `.superpowers/sdd/2026-11-18-release-qa-interview-topic-04/check_all.py`
- Modify: guide, Q&A, and MCQ files for review fixes.

**Interfaces:**
- Consumes: all four deliverables and all checkers.
- Produces: a green branch ready for the integration decision.

- [ ] **Step 1: Run the full suite**

Run:
`python .superpowers/sdd/2026-11-18-release-qa-interview-topic-04/check_all.py`
Expected: guide checks pass; Q&A 100; MCQ 150; content checks pass.

Content checks must report:
- scenario MCQs at least 60/150;
- zero exact duplicate stems;
- zero fuzzy duplicate stems after digits are normalized;
- every MCQ has four options and one answer line;
- answer distribution 37–38 per letter;
- no excluded SQL token inside SQL fences: `CROSS JOIN`, `MERGE`, `TRY_CONVERT`, `CROSS APPLY`, `OUTER APPLY`, `OUTPUT`, `INTERSECT`, `EXCEPT`;
- CTE, view, index, and tuning coverage present.

- [ ] **Step 2: Generate the review package and dispatch a fresh reviewer**

Run the review-package script for the branch range `7de72df..HEAD`. Dispatch one fresh-context reviewer on the most capable model with the package, the design, this plan, the Review Focus section, and the ledger's `Ruling:` lines. Ask for Critical/Important/Minor findings.

- [ ] **Step 3: Re-grade and fix Critical/Important in one pass**

Fix the Critical and Important findings yourself. For each content finding, add a check to `check_content.py` or a targeted assertion, watch it fail against the pre-fix file (use `git show HEAD:path` into a temporary `before/` directory), fix the content, and watch it pass. Run `check_all.py` after the pass. Record each fix in the ledger as `Final: fixed <finding> — <test> RED→GREEN, suite <N>/<N>`.

- [ ] **Step 4: Record deferred minors and rulings**

Append every `Final: minor (deferred):` and `Final: Ruling:` line to the ledger. The final message must list them.

- [ ] **Step 5: Commit the fix pass**

```bash
git add release-qa-interview/topic-04-sql/
git commit -m "docs: apply SQL topic final review fixes"
```

- [ ] **Step 6: Delete the workspace and finish the branch**

After the review is clean and the fixes are committed, delete `.superpowers/sdd/2026-11-18-release-qa-interview-topic-04/` and invoke `superpowers:finishing-a-development-branch`. The base branch is `release-qa-interview-topic-03`. Present the three integration options and wait for the user's choice.

## Self-Review

- **Spec coverage:** every guide part in the design maps to Tasks 1–7; the Q&A and MCQ distributions map to Tasks 8–13; the review and finish map to Task 14.
- **Step scan:** each task names its files, exact part counts, and a check command with an expected result. The shared data contract removes open choices about schema and sample values.
- **Type consistency:** the part titles, counts, and checker CLI match across tasks. The Q&A/MCQ counts sum to 100/150.
- **Review Focus:** each of the five failure modes has a named task and a content check: dialect leakage (Tasks 3, 6, 14), join multiplication (Task 3, Part 5 bank tasks), NULL traps (Tasks 2, 7, bank tasks), tuning claims (Task 6), CTE/view assumptions (Tasks 4–5, bank tasks).
- **Proportion:** the plan is longer than the spec only because it carries the shared data contract and exact check commands; it does not write the prose or the questions.
