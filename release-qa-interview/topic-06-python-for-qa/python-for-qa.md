# Python for Junior Release QA

This is a short, practical Python guide for junior release QA engineers. It
covers only the Python you need to read and write small test scripts: values,
containers, control flow, functions, files, JSON/CSV, pytest basics, and a few
QA scripting tools. Every concept is marked with one frequency badge:

- **Day-to-day.** You will use it in most weeks.
- **Frequent.** Useful in many scripts, not every one.
- **Situational.** Learn it when the task needs it.

The examples use Maya's flashcards project (`cards.md`, `cards.csv`,
`quiz.html`, `flashcards.py`) from `using-ai-from-zero-to-claude-code.md`. The
project is teaching material and is not in this repository. Python code is
syntax-checked only; no example, test, or API call was executed for this guide.
For browser automation, see `playwright-for-qa.md`; this pack is the language
prerequisite, not a Playwright tutorial.

## Contents

- [Part 1 — Python and the QA Workflow](#part-1--python-and-the-qa-workflow)
- [Part 2 — Values and Variables](#part-2--values-and-variables)
- [Part 3 — Control Flow and Functions](#part-3--control-flow-and-functions)
- [Part 4 — Files and Data](#part-4--files-and-data)
- [Part 5 — Testing with pytest](#part-5--testing-with-pytest)
- [Part 6 — QA Scripting](#part-6--qa-scripting)

## Part 1 — Python and the QA Workflow

### Why Python for Release QA

**Day-to-day.** Python is readable, comes with a large standard library, and has
good test and HTTP libraries. For release QA it is useful for:

- checking a file, a log, or an export;
- turning a repeated manual check into a small script;
- validating JSON or CSV data;
- calling a test API and checking the response;
- writing pytest checks that run locally or in CI.

It is not the best tool for every job. A shell one-liner, a SQL query, or a
browser tool may be simpler. Python is a good default when the logic has several
steps, needs data structures, or should be reviewed and reused.

```python
cards = ["What is a cell?", "What is DNA?", "What is a gene?"]
print(f"There are {len(cards)} cards.")
```

### Running a Script

**Day-to-day.** Save the code in a `.py` file and run it with Python:

```bash
python check_cards.py
```

On macOS or Linux, `python3` is often the command. You can also open an
interactive session with `python` and try one line at a time. A script exits
with status 0 on success and a non-zero status on failure; that status is what
CI reads.

```python
# check_cards.py
cards = ["What is a cell?", "What is DNA?"]
if len(cards) == 0:
    raise SystemExit("No cards found")
print(f"Found {len(cards)} cards")
```

### Virtual Environments and pip

**Day-to-day.** A virtual environment keeps a project's packages separate from
the rest of the machine. Create one, activate it, and install the tools the
project needs:

```bash
python -m venv .venv
# Windows: .\.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install pytest requests
```

Record the dependencies in `requirements.txt` so another person can recreate
the environment. Activate the environment before running the tests; a common
failure is installing `pytest` into one Python and running another.

### Project Layout

**Frequent.** A small QA project is easier to review when the parts have a
place:

```text
project/
  cards.md
  cards.csv
  quiz.html
  check_cards.py
  requirements.txt
  tests/
    test_cards.py
```

Keep data fixtures out of production paths, put tests under `tests/`, and keep
one-off scripts under `scripts/`. The layout is a convention, not a rule; the
goal is that another QA engineer can find the test and the data.

### Release QA Use

Use Python to replace a repeated manual check with a small, reviewable script:
count cards, find duplicates, validate a JSON fixture, check an HTML marker, or
call a test API. Keep the script deterministic, print a clear result, and return
a non-zero exit code on failure so CI can trust it.

### Watch-outs

- `python` may be Python 2 on old machines; use `python3` or check the version.
- Installing packages globally can create version conflicts; use a venv.
- A script that prints “OK” without checking anything is not a test.
- Do not run a downloaded script without reading it.
- This guide's code is syntax-checked, not executed.

## Part 2 — Values and Variables

### Numbers and Strings

**Day-to-day.** Python has integers (`int`) and floating-point numbers
(`float`). Strings hold text and support f-strings, `len`, `lower`, `strip`,
`split`, and many other methods.

```python
card_count = 12
average_rating = 4.25
question = "  What is a cell?  "
print(question.strip().lower())
print(f"{card_count} cards, average {average_rating}")
```

Strings are immutable: methods return a new string rather than changing the
original.

### Booleans and None

**Day-to-day.** A boolean is `True` or `False`. `None` means “no value” and is
different from `0`, `""`, or `False`. Conditions use truthiness: empty
containers and `None` are falsy; non-empty strings and lists are truthy.

```python
has_source = False
source = None
if source is None:
    print("No source recorded")
```

Use `is None` when you mean the absence of a value, and `==` when you mean
equality of values.

### Lists and Tuples

**Day-to-day.** A list is an ordered, mutable collection. A tuple is ordered
and immutable. Use a list for cards you will append to, and a tuple for a fixed
pair such as `(question, answer)`.

```python
cards = ["What is a cell?", "What is DNA?"]
cards.append("What is a gene?")
print(cards[0])
pair = ("What is DNA?", "Genetic material")
```

Lists are common for parsed rows, test inputs, and collected failures. Tuples
are useful when the shape should not change.

### Dictionaries and Sets

**Day-to-day.** A dictionary maps keys to values and is the natural shape for a
record. A set stores unique values and is useful for duplicate checks.

```python
card = {"id": 1, "question": "What is a cell?", "answer": "The basic unit of life"}
print(card["question"])
questions = ["What is DNA?", "What is DNA?", "What is a gene?"]
unique = set(questions)
print(len(unique))
```

A dictionary lookup by a missing key raises `KeyError`; use `.get("key")` when
the key may be absent. A set loses order, which is fine for uniqueness checks.

### Indexing and Slicing

**Day-to-day.** Python indexes start at 0. Negative indexes count from the end.
A slice takes a start, stop (exclusive), and optional step.

```python
cards = ["one", "two", "three", "four"]
print(cards[0])      # one
print(cards[-1])     # four
print(cards[1:3])    # ['two', 'three']
print(cards[:2])     # ['one', 'two']
```

The stop index is exclusive. Off-by-one errors are common in pagination and
“first N cards” checks.

### Type Conversion

**Frequent.** `int()`, `float()`, and `str()` convert between basic types. CSV
and JSON values often arrive as strings, so convert before comparing numbers.
Invalid input raises `ValueError`.

```python
raw = "12"
count = int(raw)
print(count + 1)
rating = float("4.5")
print(f"Rating: {rating}")
```

Validate before converting when the input is untrusted, and give a clear error
when the value is not a number.

### Release QA Use

Use the basic types to represent cards, counts, tags, and lookup results. Choose
a list for ordered rows, a dictionary for a record, and a set for uniqueness.
Convert CSV strings to numbers before arithmetic, and use `is None` for missing
values.

### Watch-outs

- Lists are mutable; passing one to a function can change the caller's data.
- `None` is not the same as `0` or `""`.
- `dict["missing"]` raises `KeyError`; use `.get()` when appropriate.
- Slices exclude the stop index.
- `int("4.5")` fails; use `float()` for decimals.
- A set removes duplicates but also loses order.

## Part 3 — Control Flow and Functions

### if, elif, and else

**Day-to-day.** Conditionals choose a branch. Compare values with `==`, `!=`,
`<`, `<=`, `>`, and `>=`; combine conditions with `and`, `or`, and `not`.
Indentation defines the block.

```python
status = "failed"
if status == "failed":
    print("Block the release")
elif status == "running":
    print("Wait for the run to finish")
else:
    print("Review the result")
```

Keep the condition close to the product rule. A branch that says “failed” but
checks only one field can mislead the reader.

### for Loops and range

**Day-to-day.** A `for` loop visits each item in a list, dictionary, or other
iterable. `range(n)` produces the numbers `0` to `n - 1`; `enumerate()` adds an
index.

```python
cards = ["What is a cell?", "What is DNA?", "What is a gene?"]
for index, card in enumerate(cards, start=1):
    print(index, card)

failures = 0
for card in cards:
    if "?" not in card:
        failures += 1
print(f"Missing question marks: {failures}")
```

Use a `for` loop when the number of items comes from the data. Avoid changing a
list while you are looping over it.

### while Loops

**Frequent.** A `while` loop repeats until a condition becomes false. It is
useful for a retry with a limit, but it needs a clear stop condition.

```python
attempts = 0
while attempts < 3:
    attempts += 1
    print(f"Attempt {attempts}")
```

If the condition never changes, the loop never ends. Prefer a `for` loop over a
fixed range when you already know the maximum number of attempts.

### Functions and Arguments

**Day-to-day.** A function groups a step you want to reuse and name. Parameters
are inputs; defaults make optional arguments explicit.

```python
def normalize(text, lower=True):
    cleaned = text.strip()
    return cleaned.lower() if lower else cleaned

print(normalize("  What is DNA?  "))
```

Use a function when the same logic appears twice or when a step deserves a name.
Keep the function small enough to read in one screen.

### Return Values

**Day-to-day.** `return` sends a value back to the caller. A function can return
one value or a tuple of values. Returning a result is easier to test than
printing inside the function.

```python
def summarize(cards):
    total = len(cards)
    missing_answers = 0
    for card in cards:
        if not card.get("answer"):
            missing_answers += 1
    return total, missing_answers

total, missing = summarize([{"answer": "A"}, {"answer": ""}])
print(total, missing)
```

The caller decides what to do with the result: print it, assert on it, or write
it to a report.

### Imports and Small Modules

**Frequent.** `import` brings in the standard library or your own module. Keep
reusable helpers in a small file and import them from the test or script.

```python
# helpers.py
def count_cards(cards):
    return len(cards)

# check_cards.py
from helpers import count_cards

print(count_cards(["one", "two"]))
```

Import only what you need, and keep module names lowercase with underscores. A
local module is found when it sits next to the script or on `PYTHONPATH`.

### Release QA Use

Use conditionals to encode release rules, loops to process cards or failures,
functions to make a check reusable, and imports to share helpers between a
script and its tests. Return values make the behavior easy to assert.

### Watch-outs

- Indentation is syntax in Python; a misindented block changes behavior.
- Changing a list while looping over it can skip items.
- A `while` loop without a changing condition can hang.
- A function that prints instead of returning is harder to test.
- Import errors often mean the script is running from the wrong directory.

## Part 4 — Files and Data

### pathlib

**Day-to-day.** `pathlib.Path` gives you a readable way to build and inspect
paths. It works on Windows, macOS, and Linux without manual slash handling.

```python
from pathlib import Path

path = Path("data") / "cards.md"
print(path.exists())
print(path.parent)
text = path.read_text(encoding="utf-8")
print(len(text))
```

Use `/` to join path parts. Check `.exists()` before reading when a missing file
is a legitimate test case; otherwise let a clear error surface.

### Reading and Writing Text

**Day-to-day.** Use `with open(...)` so the file closes even if an error occurs.
Always pass an encoding when the file may contain non-ASCII text.

```python
from pathlib import Path

path = Path("report.txt")
with path.open("w", encoding="utf-8") as handle:
    handle.write("cards: 12\n")

with path.open(encoding="utf-8") as handle:
    for line in handle:
        print(line.rstrip())
```

`read_text()` and `write_text()` are shorter for small files. Use the `with`
form for large files or line-by-line processing.

### JSON

**Frequent.** JSON is a common fixture and API format. `json.loads()` parses a
string; `json.dumps()` produces a string; `json.load()` and `json.dump()` work
with files.

```python
import json

payload = '{"id": 1, "question": "What is DNA?"}'
card = json.loads(payload)
print(card["question"])

encoded = json.dumps(card, indent=2)
print(encoded)
```

A JSON decode error means the input is not valid JSON; show the offending
fixture and the position rather than guessing.

### CSV

**Frequent.** `csv.DictReader` turns each row into a dictionary keyed by the
header. Values arrive as strings, so convert numbers explicitly.

```python
import csv

with open("cards.csv", newline="", encoding="utf-8") as handle:
    rows = list(csv.DictReader(handle))

print(len(rows))
for row in rows:
    print(row["question"])
```

Use `newline=""` when opening a CSV file so the `csv` module handles line
endings correctly.

### Exceptions

**Day-to-day.** An exception is Python's way of reporting an error. Catch the
specific error you can handle; let the rest surface with a clear message.

```python
from pathlib import Path

path = Path("cards.md")
try:
    text = path.read_text(encoding="utf-8")
except FileNotFoundError:
    raise SystemExit(f"Missing fixture: {path}")
```

Avoid a bare `except:` that hides every error. If you catch, either recover or
raise a message that tells the next person what to fix.

### Logging Basics

**Situational.** `print()` is fine for a small script. `logging` is better when
you need levels, timestamps, or a record that can be filtered.

```python
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

logger.info("Checking cards")
logger.warning("Two cards have no source")
```

Do not log secrets, tokens, or customer data. A log is often copied into a
ticket or a CI artifact.

### Release QA Use

Use `pathlib` and `with` to read fixtures safely, JSON and CSV to parse test
data, exceptions to fail with a useful message, and logging for a script that
runs in CI. A good failure says which file, which row, and what was expected.

### Watch-outs

- Reading a file without an encoding can fail on non-ASCII text.
- CSV values are strings; convert before comparing numbers.
- A bare `except:` hides the error you need to debug.
- `json.loads()` expects a string; `json.load()` expects a file object.
- Do not write secrets or customer data to a log.
- A missing file is a test result only when the test expects it.
