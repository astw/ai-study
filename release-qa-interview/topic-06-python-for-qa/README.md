# Python for Junior Release QA — Topic 6

A short, practical Python pack for junior release QA engineers. It covers only
the language basics and QA scripting a beginner needs, with each concept marked
**Day-to-day**, **Frequent**, or **Situational**.

## What is here

| File | Contents |
|---|---|
| `python-for-qa.md` | Six-part guide: Python/venv, values, control flow and functions, files and data, pytest, and QA scripting. |
| `qa-60.md` | 60 open questions with hidden answers. |
| `mcq-90.md` | 90 multiple-choice questions with answers and explanations. |
| `README.md` | This file. |

## Who it is for

New graduates and junior release QA engineers who have little or no Python. It
assumes no prior programming experience. The goal is to be able to read and
write small scripts, validate fixtures, and run a basic pytest suite.

## Frequency badges

- **Day-to-day.** Used in most weeks.
- **Frequent.** Useful in many scripts, not every one.
- **Situational.** Learn it when a task needs it.

The badge tells you what to study first. It is not a difficulty rating.

## Study order

1. Read `python-for-qa.md` part by part.
2. Answer `qa-60.md` with the answers hidden; explain each answer aloud.
3. Take `mcq-90.md`; review every explanation, not just the score.
4. Re-read the weak parts and retry the missed questions.

## Coverage

| Part | Guide section | Q&A | MCQs |
|---|---|---:|---:|
| 1 | Python and the QA workflow | 10 | 15 |
| 2 | Values and variables | 10 | 15 |
| 3 | Control flow and functions | 10 | 15 |
| 4 | Files and data | 10 | 15 |
| 5 | Testing with pytest | 10 | 15 |
| 6 | QA scripting | 10 | 15 |
| **Total** | | **60** | **90** |

## Running examples

The examples use Maya's flashcards project (`cards.md`, `cards.csv`,
`quiz.html`, `flashcards.py`) from `using-ai-from-zero-to-claude-code.md`. The
project is teaching material and is not in this repository. The API URLs are
hypothetical test endpoints.

The pack uses Python 3.10+ and introduces `pytest` and `requests` as QA tools.
Install them in a virtual environment:

```bash
python -m venv .venv
# Windows: .\.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install pytest requests
```

## Practice note

Every Python example is syntax-checked only; no example, test, or API call was
executed for this pack. Do not treat a snippet as evidence that a test passed.
Run your own code in your own environment.

For browser automation with Python and pytest, continue with
`playwright-for-qa.md`. This pack is the language prerequisite, not a Playwright
tutorial.
