# Release QA Interview Topic 6 — Python for Junior QA Design

**Date:** 2026-11-19
**Status:** Proposed
**Audience:** Junior release QA engineers and new graduates with little or no Python.

## Intent

Add a compact sixth interview pack: the Python a junior release QA engineer
actually uses for test scripts, file checks, API calls, and pytest runs. The
pack is deliberately basics-only and shorter than Topics 1–5: a six-part guide,
60 Q&A, 90 MCQs, and a README. Concepts carry a frequency badge so a reader can
see what is **Day-to-day**, **Frequent**, or **Situational**.

The existing Playwright guide already teaches browser automation with Python and
pytest. This pack is the language prerequisite: it does not re-teach Playwright,
and it does not cover advanced Python (metaclasses, async, decorators, typing,
packaging, or framework architecture).

## Goals

- Teach the Python syntax a junior QA engineer needs to read and write small
  test scripts.
- Organize every concept by frequency: day-to-day, frequent, or situational.
- Use the flashcards project for realistic examples: parsing `cards.md`,
  checking `cards.csv`, reading JSON, validating `quiz.html`, and calling a
  test API.
- Cover `pytest` basics: test discovery, assertions, `pytest.raises`, fixtures,
  and parametrization at an introductory level.
- Cover practical QA scripting: `pathlib`, `open`/`with`, JSON, CSV,
  exceptions, logging, `subprocess`, `argparse`, `datetime`, and `requests`.
- Provide 60 Q&A and 90 MCQs with the same hidden-answer and four-option style
  as the earlier topics, sized for a basics-only pack.
- Keep every Python example syntactically valid; no execution claims.

## Non-goals

- No advanced Python: classes beyond a brief mention, inheritance, decorators,
  generators, async, threading, multiprocessing, typing, packaging, or
  framework design.
- No Playwright or browser automation; link to `playwright-for-qa.md` instead.
- No Django/Flask/FastAPI application development.
- No database drivers or ORMs.
- No claim that any example was executed. The pack is syntax-checked only.
- No replacement for the Python documentation or the Playwright guide.

## Anti-goals

- A general Python course that drifts away from QA work.
- Advanced features presented as junior-level requirements.
- Examples that depend on production data, secrets, or a live service.
- Frequency badges used as decoration rather than a study guide.
- Questions that test trivia without a QA use.
- Claiming a test ran or passed when only the syntax was checked.

## Approaches considered

1. **Compact QA-focused pack — chosen.** Six parts, frequency badges, 60 Q&A,
   90 MCQs. Matches “basic, not too long” and the junior audience.
2. **Full 100/150 pack.** More practice, but repeats basics and conflicts with
   the requested shorter scope.
3. **Pytest/API-only pack.** Assumes Python already known; too narrow for juniors.
4. **General Python course.** Broader language coverage, but less QA-specific
   and longer than requested.

## Pack structure

Folder: `release-qa-interview/topic-06-python-for-qa/`

| File | Role |
|---|---|
| `python-for-qa.md` | Six-part guide with frequency badges, short examples, QA use, and watch-outs. |
| `qa-60.md` | 60 open questions, numbered `Q1`–`Q60`, hidden answers. |
| `mcq-90.md` | 90 four-option questions, numbered `MCQ 1`–`MCQ 90`, one answer and explanation each. |
| `README.md` | Study order, coverage, counts, badges, and practice note. |

### Guide parts

1. **Python and the QA workflow** — interpreter, running a script, virtual
   environments, `pip`, project layout, and where Python fits in release QA.
2. **Values and variables** — numbers, strings, booleans, `None`, lists,
   tuples, dictionaries, sets, indexing/slicing, type conversion.
3. **Control flow and functions** — `if`/`elif`/`else`, `for`, `while`,
   `range`, functions, arguments, return values, imports, and small modules.
4. **Files and data** — `pathlib`, `open`/`with`, text files, JSON, CSV,
   exceptions, and logging basics.
5. **Testing with pytest** — test discovery, assertions, `pytest.raises`,
   fixtures, parametrization, and reading a failure.
6. **QA scripting** — `subprocess`, `argparse`, `datetime`, `requests` for API
   checks, environment variables, and a small end-to-end check.

Each concept entry uses a frequency badge:

- **Day-to-day.** The reader will use it in most weeks.
- **Frequent.** Useful in many scripts, but not every one.
- **Situational.** Needed for a specific task; learn it when the task appears.

Each part ends with `### Release QA Use` and `### Watch-outs`.

### Running examples

- **Flashcards parser:** read `cards.md`, count cards, find a duplicate, and
  write a small report.
- **CSV/JSON checks:** read `cards.csv`, validate JSON fixtures, and compare
  counts.
- **Quiz smoke check:** read `quiz.html`, assert key strings, and optionally
  call a test API with `requests` (clearly labeled hypothetical).
- **Pytest:** a small test file for the parser and data checks.

The `flashcards/` folder is teaching material from the AI handbook and is not in
this repository. No example depends on a live service.

## Question bank design

### Q&A distribution (60)

| Part | Count |
|---|---:|
| 1 Python and the QA workflow | 10 |
| 2 Values and variables | 10 |
| 3 Control flow and functions | 10 |
| 4 Files and data | 10 |
| 5 Testing with pytest | 10 |
| 6 QA scripting | 10 |
| **Total** | **60** |

### MCQ distribution (90)

| Part | Count |
|---|---:|
| 1 Python and the QA workflow | 15 |
| 2 Values and variables | 15 |
| 3 Control flow and functions | 15 |
| 4 Files and data | 15 |
| 5 Testing with pytest | 15 |
| 6 QA scripting | 15 |
| **Total** | **90** |

### Style rules

- At least 36 of 90 MCQ stems are scenarios.
- Four options per MCQ, one `**Correct answer: X.**` explanation.
- Answer letters roughly balanced (target 22–23 each).
- No exact or number-insensitive duplicate stems.
- Q&A answers 2–5 sentences, with a short code snippet where it helps.
- Use Python 3.10+ syntax; no advanced features.
- Every Python fence must compile; no claim that it ran.
- Use the flashcards project and synthetic data only.

## Verification

- Counts, numbering, reveal balance, four options, answer lines, answer
  distribution, TOC anchors, scenario share, and duplicate stems.
- Every concept entry has exactly one frequency badge.
- Every guide part ends with `### Release QA Use` and `### Watch-outs`.
- Every Python fence compiles with `compile()`.
- No execution claim; no secrets or real customer data.
- pytest and requests examples are labeled as tool examples; they are not
  claimed to have been run.

## What is left to the builder

- Write the exact explanations, examples, questions, options, and explanations.
- Keep the examples small enough for a junior reader and consistent with the
  flashcards project.
- Run the structural and syntax checks, then a fresh whole-branch review.
