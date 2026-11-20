# Python for Junior Release QA — Topic 6 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add `release-qa-interview/topic-06-python-for-qa/` with a concise six-part Python guide, 60 Q&A, 90 MCQs, and a README for junior release QA interviews.

**Architecture:** Four Markdown deliverables. Every guide concept carries one frequency badge (**Day-to-day**, **Frequent**, **Situational**) and uses the flashcards project for small, reviewable examples. The banks follow the existing hidden-answer and four-option formats. Python 3 structural checkers plus a compile check are the test suite; no example is executed.

**Tech Stack:** Markdown, Python 3.10+ syntax, pytest and requests as teaching tools, Python 3 standard library for checkers.

**Spec:** `docs/superpowers/specs/2026-11-19-release-qa-interview-topic-06-design.md`

## Global Constraints

- Branch: `release-qa-interview-topic-06`, created from `release-qa-interview-topic-04` at `67ad736`.
- Folder: `release-qa-interview/topic-06-python-for-qa/`.
- Files: `python-for-qa.md`, `qa-60.md`, `mcq-90.md`, `README.md`.
- Q&A counts: 10 per part, 6 parts, total 60.
- MCQ counts: 15 per part, 6 parts, total 90.
- Every guide concept section (`###` under a part, excluding `### Release QA Use` and `### Watch-outs`) has exactly one of the badges:
  `**Day-to-day.**`, `**Frequent.**`, `**Situational.**`.
- Every guide part ends with `### Release QA Use` and `### Watch-outs`.
- Python 3.10+ syntax only. No classes beyond a mention, decorators, generators, async, threading, typing, packaging, or framework design.
- No Playwright, Django/Flask/FastAPI, database drivers, or ORMs.
- Every Python fence must compile. No claim that any example, test, or API call ran.
- MCQ format: four options A–D, one `**Correct answer: X.**` line, one `<details>` block.
- Q&A format: `#### QN.` plus one `<details><summary>Show answer</summary>` block.
- At least 36 of 90 MCQ stems are scenarios.
- Answer letters target 22–23 each.
- No exact or number-insensitive duplicate stems.
- Use synthetic data only; no secrets or real customer data.
- Commit after each task. End commit messages with the repository's required attribution line.

## Source Contract

- `using-ai-from-zero-to-claude-code.md` for the flashcards project shape
  (`cards.md`, `flashcards.py`, `quiz.html`) and Python 3.10+ conventions.
- `playwright-for-qa.md` only for the quiz behavior contract; do not re-teach
  Playwright.
- The flashcards folder is teaching material and is not in this repository.
- The examples use synthetic cards and a hypothetical test API; no live service.

## Review Focus

1. **Frequency accuracy:** each concept's badge matches how often a junior
   release QA engineer actually uses it; day-to-day concepts are not padded
   with situational material.
2. **Python correctness:** syntax compiles, semantics are correct, and examples
   are small enough for a beginner. No advanced constructs sneaking in.
3. **pytest/requests claims:** test discovery, fixtures, parametrization, and
   request calls are described accurately; nothing is claimed to have run.
4. **Execution evidence:** examples are marked as syntax-checked teaching
   material; no “the test passed” or “the API returned” claim without a run.
5. **Scope discipline:** the pack stays basics-only and points to the Playwright
   guide for browser automation instead of duplicating it.

---

### Task 1: Branch, checkers, and guide Parts 1–2

**Files:**
- Create: `release-qa-interview/topic-06-python-for-qa/python-for-qa.md`
- Create: `.superpowers/sdd/2026-11-19-release-qa-interview-topic-06/check_guide.py`
- Create: `.superpowers/sdd/2026-11-19-release-qa-interview-topic-06/check_qa.py`
- Create: `.superpowers/sdd/2026-11-19-release-qa-interview-topic-06/check_mcq.py`
- Create: `.superpowers/sdd/2026-11-19-release-qa-interview-topic-06/check_content.py`
- Create: `.superpowers/sdd/2026-11-19-release-qa-interview-topic-06/check_all.py`
- Create: `.superpowers/sdd/2026-11-19-release-qa-interview-topic-06/progress.md`

**Interfaces:**
- Consumes: the approved design and this plan.
- Produces: the branch, checker CLI, and guide Parts 1–2.

- [ ] **Step 1: Create the branch and workspace**

```bash
git switch -c release-qa-interview-topic-06 release-qa-interview-topic-04
mkdir -p .superpowers/sdd/2026-11-19-release-qa-interview-topic-06
```

Write `progress.md` with first line:
`# SDD ledger — plan: docs/superpowers/plans/2026-11-19-release-qa-interview-topic-06.md`

- [ ] **Step 2: Write the failing guide test**

Create `check_guide.py` with:
- `--parts` and `--all`; missing part fails.
- `--toc` slug check.
- Balanced code fences.
- Exact per-part headings from this plan.
- `### Release QA Use` and `### Watch-outs` in every requested part.
- Exactly one frequency badge in every concept `###` section, excluding those
  two tail sections.
- Required terms per part (Part 1: `venv`, `pip`, `python`; Part 2: `list`,
  `dict`, `string`; Part 3: `function`, `for`; Part 4: `pathlib`, `json`,
  `csv`, `exception`; Part 5: `pytest`, `assert`, `fixture`; Part 6:
  `requests`, `subprocess`).
- Every `python` fence compiles with `compile()`.
- No forbidden execution claims: `this pack ran`, `the test passed`,
  `the api returned`.

Run:
`python .superpowers/sdd/2026-11-19-release-qa-interview-topic-06/check_guide.py --parts 1 2`
Expected: FAIL with a missing-guide error.

- [ ] **Step 3: Write the guide title, intro, TOC, and Parts 1–2**

Title: `# Python for Junior Release QA`.
Intro: audience, frequency badges, flashcards examples, Python 3.10+,
syntax-checked-only caveat, link to the Playwright guide for browser automation.
TOC links all six parts.

Part 1 headings:
`## Part 1 — Python and the QA Workflow`, `### Why Python for Release QA`, `### Running a Script`, `### Virtual Environments and pip`, `### Project Layout`, `### Release QA Use`, `### Watch-outs`.

Part 2 headings:
`## Part 2 — Values and Variables`, `### Numbers and Strings`, `### Booleans and None`, `### Lists and Tuples`, `### Dictionaries and Sets`, `### Indexing and Slicing`, `### Type Conversion`, `### Release QA Use`, `### Watch-outs`.

Content:
- Part 1: interpreter, `python script.py`, `venv`, `pip install`, a small
  project layout, and where Python fits in release QA.
- Part 2: the basic types with small flashcards examples: card counts,
  duplicate questions, tags, and lookup by card id.
- Every concept section gets a frequency badge.
- No advanced constructs.

- [ ] **Step 4: Run the guide check**

Run:
`python .superpowers/sdd/2026-11-19-release-qa-interview-topic-06/check_guide.py --parts 1 2`
Expected: `guide checks passed`.

- [ ] **Step 5: Compile the checkers**

Run:
`python -m py_compile .superpowers/sdd/2026-11-19-release-qa-interview-topic-06/check_*.py`
Expected: exit 0.

- [ ] **Step 6: Commit**

```bash
git add docs/superpowers/specs/2026-11-19-release-qa-interview-topic-06-design.md \
        docs/superpowers/plans/2026-11-19-release-qa-interview-topic-06.md \
        release-qa-interview/topic-06-python-for-qa/python-for-qa.md
git commit -m "feat: add Python guide parts 1-2 and checkers"
```

---

### Task 2: Guide Parts 3–4

**Files:**
- Modify: `release-qa-interview/topic-06-python-for-qa/python-for-qa.md`

**Interfaces:**
- Consumes: Part 1–2 terminology.
- Produces: control-flow, functions, files, and data sections.

- [ ] **Step 1: Add Part 3**

Headings:
`## Part 3 — Control Flow and Functions`, `### if, elif, and else`, `### for Loops and range`, `### while Loops`, `### Functions and Arguments`, `### Return Values`, `### Imports and Small Modules`, `### Release QA Use`, `### Watch-outs`.

Content:
- Conditionals for card counts and status checks.
- `for` over lists/dicts; `range`; simple accumulation.
- `while` with a clear stop condition; avoid infinite loops.
- Functions with parameters, defaults, and return values.
- Imports from the standard library and a small local module.
- Small examples only; no comprehensions beyond a mention if needed.

- [ ] **Step 2: Add Part 4**

Headings:
`## Part 4 — Files and Data`, `### pathlib`, `### Reading and Writing Text`, `### JSON`, `### CSV`, `### Exceptions`, `### Logging Basics`, `### Release QA Use`, `### Watch-outs`.

Content:
- `Path` for paths; `read_text`/`write_text`.
- `open` with `with`; encoding.
- `json.loads`/`json.dumps`; a JSON fixture.
- `csv.DictReader` for `cards.csv`.
- `try`/`except` for missing files and bad data; raise clear errors.
- `logging` vs `print`; log levels; no secrets in logs.
- QA examples: validate a fixture, compare counts, fail with a useful message.

- [ ] **Step 3: Run and commit**

Run:
`python .superpowers/sdd/2026-11-19-release-qa-interview-topic-06/check_guide.py --parts 1 2 3 4`
Expected: `guide checks passed`.

```bash
git add release-qa-interview/topic-06-python-for-qa/python-for-qa.md
git commit -m "feat: add Python control flow and data guide"
```

---

### Task 3: Guide Parts 5–6 and README

**Files:**
- Modify: `release-qa-interview/topic-06-python-for-qa/python-for-qa.md`
- Create: `release-qa-interview/topic-06-python-for-qa/README.md`

**Interfaces:**
- Consumes: all guide parts.
- Produces: the completed guide and README.

- [ ] **Step 1: Add Part 5**

Headings:
`## Part 5 — Testing with pytest`, `### Test Discovery`, `### Assertions`, `### pytest.raises`, `### Fixtures`, `### Parametrization`, `### Reading a Failure`, `### Release QA Use`, `### Watch-outs`.

Content:
- Test file/function naming; running `pytest`.
- `assert` with a useful message.
- `pytest.raises` for expected failures.
- A simple fixture for a temporary `cards.md`.
- `@pytest.mark.parametrize` for several inputs.
- Reading the failing assertion and the traceback.
- QA examples: parser tests, empty data, duplicate questions, malformed lines.

- [ ] **Step 2: Add Part 6**

Headings:
`## Part 6 — QA Scripting`, `### subprocess`, `### argparse`, `### datetime`, `### requests for API Checks`, `### Environment Variables`, `### A Small End-to-End Check`, `### Release QA Use`, `### Watch-outs`.

Content:
- `subprocess.run` with a list of arguments; check the return code.
- `argparse` for a script path and an optional flag.
- `datetime` for timestamps and simple comparisons.
- `requests.get`/`post` with a timeout and status check; a hypothetical
  test API, clearly labeled.
- Environment variables for base URLs; never hard-code secrets.
- An end-to-end script: read `cards.md`, validate, call the test API, print a
  summary.
- No claim that the API or tests ran.

- [ ] **Step 3: Write README**

Include: contents, audience, frequency badges, study order, counts 60/90,
six-part coverage table, running examples, Python 3.10+ and `pytest`/`requests`
note, syntax-checked-only caveat, and a pointer to `playwright-for-qa.md` for
browser automation.

- [ ] **Step 4: Run and commit**

Run:
`python .superpowers/sdd/2026-11-19-release-qa-interview-topic-06/check_guide.py --all --toc`
Expected: `guide checks passed`.

Run:
`python .superpowers/sdd/2026-11-19-release-qa-interview-topic-06/check_content.py`
Expected: guide coverage passes; bank files missing are expected.

```bash
git add release-qa-interview/topic-06-python-for-qa/
git commit -m "feat: complete Python guide and README"
```

---

### Task 4: Q&A Parts 1–3

**Files:**
- Create: `release-qa-interview/topic-06-python-for-qa/qa-60.md`

**Interfaces:**
- Consumes: guide Parts 1–3.
- Produces: Q1–Q30.

- [ ] **Step 1: Add the Q&A shell and Parts 1–3**

Headings/counts:
`## Part 1 — Python and the QA Workflow (10 questions)`, `## Part 2 — Values and Variables (10 questions)`, `## Part 3 — Control Flow and Functions (10 questions)`.

Topics:
- Part 1: why Python, interpreter, running a script, venv, pip, project layout,
  imports, pytest entry point, where scripts fit in release QA, what Python is
  not for.
- Part 2: int/float, strings, f-strings, booleans, None, lists, tuples, dicts,
  sets, indexing/slicing, type conversion, mutability, choosing a container.
- Part 3: if/elif/else, truthiness, for, range, while, break/continue,
  functions, arguments/defaults, return values, imports, small modules.

Answers 2–5 sentences with short snippets. No execution claim. Add Contents
links for all six parts.

- [ ] **Step 2: Run and commit**

Run:
`python .superpowers/sdd/2026-11-19-release-qa-interview-topic-06/check_qa.py --parts 1:10 2:10 3:10 --total 30`
Expected: 30 questions, sequential, 30 balanced reveals.

```bash
git add release-qa-interview/topic-06-python-for-qa/qa-60.md
git commit -m "feat: add Python Q&A parts 1-3"
```

---

### Task 5: Q&A Parts 4–6

**Files:**
- Modify: `release-qa-interview/topic-06-python-for-qa/qa-60.md`

**Interfaces:**
- Consumes: guide Parts 4–6; Q1–Q30.
- Produces: Q31–Q60 and the complete Q&A bank.

- [ ] **Step 1: Add Parts 4–6**

Headings/counts:
`## Part 4 — Files and Data (10 questions)`, `## Part 5 — Testing with pytest (10 questions)`, `## Part 6 — QA Scripting (10 questions)`.

Topics:
- Part 4: `pathlib`, `with`, encoding, JSON, CSV, exceptions, logging, missing
  files, bad data, secrets in logs.
- Part 5: test discovery, assertions, `pytest.raises`, fixtures, parametrize,
  failing output, test isolation, temporary files, what not to test, pytest vs
  unittest.
- Part 6: `subprocess`, return codes, `argparse`, `datetime`, `requests`,
  timeouts, environment variables, secrets, end-to-end checks, when not to
  script it.

- [ ] **Step 2: Run and commit**

Run:
`python .superpowers/sdd/2026-11-19-release-qa-interview-topic-06/check_qa.py --parts 1:10 2:10 3:10 4:10 5:10 6:10 --total 60 --toc`
Expected: 60 questions, sequential, 60 balanced reveals, TOC resolves.

```bash
git add release-qa-interview/topic-06-python-for-qa/qa-60.md
git commit -m "feat: complete Python Q&A bank"
```

---

### Task 6: MCQ Parts 1–3

**Files:**
- Create: `release-qa-interview/topic-06-python-for-qa/mcq-90.md`

**Interfaces:**
- Consumes: guide Parts 1–3.
- Produces: MCQ 1–45.

- [ ] **Step 1: Add the MCQ shell and Parts 1–3**

Headings/counts:
`## Part 1 — Python and the QA Workflow (15 questions)`, `## Part 2 — Values and Variables (15 questions)`, `## Part 3 — Control Flow and Functions (15 questions)`.

Topics follow Q&A Parts 1–3, with scenario items for running scripts, choosing
containers, reading loops, and fixing small functions. At least 18 of these 45
stems are scenarios. Four options, one answer line. Track letters; the final 90
must land at 22–23 each.

- [ ] **Step 2: Run and commit**

Run:
`python .superpowers/sdd/2026-11-19-release-qa-interview-topic-06/check_mcq.py --parts 1:15 2:15 3:15 --total 45`
Expected: 45 questions, four options each, 45 answer lines, balanced reveals.

```bash
git add release-qa-interview/topic-06-python-for-qa/mcq-90.md
git commit -m "feat: add Python MCQs parts 1-3"
```

---

### Task 7: MCQ Parts 4–6

**Files:**
- Modify: `release-qa-interview/topic-06-python-for-qa/mcq-90.md`

**Interfaces:**
- Consumes: guide Parts 4–6; MCQ 1–45.
- Produces: MCQ 46–90 and the complete MCQ bank.

- [ ] **Step 1: Add Parts 4–6**

Headings/counts:
`## Part 4 — Files and Data (15 questions)`, `## Part 5 — Testing with pytest (15 questions)`, `## Part 6 — QA Scripting (15 questions)`.

Topics follow Q&A Parts 4–6, with scenarios for missing files, JSON/CSV
parsing, pytest failures, subprocess return codes, request timeouts, and
environment variables. At least 18 of these 45 stems are scenarios. Final
answer letters 22–23 each; adjust option order without changing content.

- [ ] **Step 2: Run and commit**

Run:
`python .superpowers/sdd/2026-11-19-release-qa-interview-topic-06/check_mcq.py --parts 1:15 2:15 3:15 4:15 5:15 6:15 --total 90 --toc --letter-bounds`
Expected: 90 questions, four options each, 90 answer lines, TOC resolves,
letters 22–23 each.

```bash
git add release-qa-interview/topic-06-python-for-qa/mcq-90.md
git commit -m "feat: complete Python MCQ bank"
```

---

### Task 8: Cross-file checks, final review, and finish

**Files:**
- Test: `.superpowers/sdd/2026-11-19-release-qa-interview-topic-06/check_all.py`
- Modify: guide, Q&A, MCQ, README for review fixes.

- [ ] **Step 1: Run the full suite**

Run:
`python .superpowers/sdd/2026-11-19-release-qa-interview-topic-06/check_all.py`
Expected: guide checks pass; Q&A 60; MCQ 90; content checks pass; scenario
≥36/90; zero duplicate stems; letters 22–23 each; every Python fence compiles.

- [ ] **Step 2: Dispatch the whole-branch reviewer**

Generate the review package for `67ad736..HEAD` and dispatch one fresh reviewer
on the most capable model with the design, plan, Review Focus, and ledger. Ask
for Critical/Important/Minor findings. Point the reviewer at the frequency-badge
accuracy and Python-correctness checks.

- [ ] **Step 3: Fix the findings in one wave**

Fix Critical/Important findings in one pass. Add a regression check where the
finding is structural; verify Python snippets compile. Run `check_all.py` after
the pass. Record each fix in the ledger.

- [ ] **Step 4: Record deferred minors and rulings**

Append every `Final: minor (deferred):` and `Final: Ruling:` line to the ledger.
The final message must list them.

- [ ] **Step 5: Commit the fix wave**

```bash
git add release-qa-interview/topic-06-python-for-qa/
git commit -m "docs: apply Python topic final review fixes"
```

- [ ] **Step 6: Delete the workspace and finish**

After the review is clean and the fixes are committed, delete
`.superpowers/sdd/2026-11-19-release-qa-interview-topic-06/` and invoke
`superpowers:finishing-a-development-branch`. The base branch is
`release-qa-interview-topic-04`. Present the three integration options and wait
for the user's choice.

## Self-Review

- **Spec coverage:** Parts 1–6 map to Tasks 1–3; Q&A and MCQ distributions map
  to Tasks 4–7; verification and review map to Task 8.
- **Step scan:** each task names exact files, headings, counts, and a check
  command with an expected result.
- **Type consistency:** part titles, counts, and checker CLI match; Q&A 60 and
  MCQ 90.
- **Review Focus:** frequency accuracy, Python correctness, pytest/requests
  claims, execution evidence, and scope discipline each have a task and a check.
- **Proportion:** the plan carries the source contract and checks; it does not
  write the prose, examples, or questions.
