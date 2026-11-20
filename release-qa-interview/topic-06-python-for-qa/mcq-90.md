# Python for Junior Release QA — MCQs

90 multiple-choice questions on the Python basics a junior release QA engineer
needs. Pick an option before revealing the answer. Examples use the flashcards
project and synthetic data. Every snippet is syntax-checked only; no test or
script was executed for this bank.

## Contents

- [Part 1 — Python and the QA Workflow (15 questions)](#part-1--python-and-the-qa-workflow-15-questions)
- [Part 2 — Values and Variables (15 questions)](#part-2--values-and-variables-15-questions)
- [Part 3 — Control Flow and Functions (15 questions)](#part-3--control-flow-and-functions-15-questions)
- [Part 4 — Files and Data (15 questions)](#part-4--files-and-data-15-questions)
- [Part 5 — Testing with pytest (15 questions)](#part-5--testing-with-pytest-15-questions)
- [Part 6 — QA Scripting (15 questions)](#part-6--qa-scripting-15-questions)

## Part 1 — Python and the QA Workflow (15 questions)

#### MCQ 1. A tester needs to check a JSON fixture, count cards, and compare two files. Why is Python a reasonable choice?

A. It handles multi-step data checks with readable code and a large standard library
B. It is the only language that can read files
C. It runs without an interpreter
D. It replaces the need for tests

<details>
<summary>Show answer</summary>

**Correct answer: A.** Python is readable and has good file, JSON, and test libraries. A shell one-liner is better for a single operation.

</details>

#### MCQ 2. What does the Python interpreter do?

A. Compiles the script to a standalone binary
B. Reads and runs Python code
C. Installs packages automatically
D. Creates a virtual environment

<details>
<summary>Show answer</summary>

**Correct answer: B.** The interpreter runs the code. Package installation and virtual environments are separate tools.

</details>

#### MCQ 3. A tester saved `check_cards.py` and wants to run it. Which command is correct?

A. `run check_cards.py`
B. `python --install check_cards.py`
C. `python check_cards.py`
D. `check_cards.py --python`

<details>
<summary>Show answer</summary>

**Correct answer: C.** `python check_cards.py` runs the script. On some systems the command is `python3`.

</details>

#### MCQ 4. A script exits with status 0. What does CI usually infer?

A. The script failed
B. The script was skipped
C. The script needs a dependency
D. The script succeeded

<details>
<summary>Show answer</summary>

**Correct answer: D.** Zero conventionally means success; non-zero means failure.

</details>

#### MCQ 5. Why create a virtual environment for a QA project?

A. To keep the project's packages separate from other Python projects
B. To make Python run faster
C. To avoid writing tests
D. To compile Python to C

<details>
<summary>Show answer</summary>

**Correct answer: A.** A venv isolates dependencies. It does not change the language's speed or remove the need for tests.

</details>

#### MCQ 6. Which command installs pytest into the active environment?

A. `python -m venv pytest`
B. `python -m pip install pytest`
C. `pytest --install python`
D. `pip env pytest`

<details>
<summary>Show answer</summary>

**Correct answer: B.** `python -m pip install pytest` uses the active interpreter's pip.

</details>

#### MCQ 7. What is `requirements.txt` for?

A. Storing test results
B. Listing the project's Python source files
C. Recording dependencies so another person or CI can recreate them
D. Storing production secrets

<details>
<summary>Show answer</summary>

**Correct answer: C.** It records dependencies. Secrets do not belong in it.

</details>

#### MCQ 8. Which layout is easiest for another QA engineer to review?

A. Every file in the home directory
B. Only a notebook
C. A single 2,000-line script
D. A script at the root, tests under `tests/`, and fixtures under `data/`

<details>
<summary>Show answer</summary>

**Correct answer: D.** A predictable layout makes the test, data, and dependency list easy to find.

</details>

#### MCQ 9. A script next to `helpers.py` uses `from helpers import count_cards`. Why might it fail?

A. The script is running from a different working directory or the module is not on the path
B. Python cannot import local files
C. `count_cards` must be a class
D. `helpers.py` must be installed with pip

<details>
<summary>Show answer</summary>

**Correct answer: A.** Python searches the script directory and the configured paths. Run from the right folder or fix the path.

</details>

#### MCQ 10. What does `pytest` do in a QA workflow?

A. Installs the application
B. Discovers and runs tests, reporting failures with a non-zero exit status
C. Replaces the browser
D. Deploys to production

<details>
<summary>Show answer</summary>

**Correct answer: B.** pytest is a test runner. It does not deploy or install the application.

</details>

#### MCQ 11. A tester needs to copy one file and then verify it exists. Which approach is simplest?

A. A 100-line Python framework
B. A database migration
C. A shell command, possibly with a short Python check
D. A browser automation script

<details>
<summary>Show answer</summary>

**Correct answer: C.** A single file operation does not need a Python framework. Use Python when the logic grows.

</details>

#### MCQ 12. A machine's `python` command runs Python 2. What should the tester try?

A. `python --upgrade`
B. `pip python3`
C. `python2 --force`
D. `python3 check_cards.py`

<details>
<summary>Show answer</summary>

**Correct answer: D.** `python3` usually points at the Python 3 interpreter. Check the version before running.

</details>

#### MCQ 13. Why is installing every package globally risky?

A. It can create version conflicts between projects
B. It deletes the standard library
C. It prevents scripts from running
D. It changes the file encoding

<details>
<summary>Show answer</summary>

**Correct answer: A.** Global installs are shared by all projects. A virtual environment isolates them.

</details>

#### MCQ 14. A ticket includes a downloaded Python script and asks you to run it. What should you do first?

A. Run it with administrator rights
B. Read the script, check what it does, and only run it if the source is trusted
C. Disable the antivirus
D. Commit it without reading

<details>
<summary>Show answer</summary>

**Correct answer: B.** A script is code with your permissions. Review it before running it.

</details>

#### MCQ 15. The guide says its Python is “syntax-checked only.” What does that mean?

A. Every example ran and passed
B. The examples were deployed
C. The code was parsed for syntax but not executed
D. The tests were skipped

<details>
<summary>Show answer</summary>

**Correct answer: C.** Syntax checking proves the code parses; it does not prove behavior or test results.

</details>

## Part 2 — Values and Variables (15 questions)

#### MCQ 16. Which value is a float?

A. `4.25`
B. `12`
C. `"4.25"`
D. `True`

<details>
<summary>Show answer</summary>

**Correct answer: A.** A float has a decimal part. `12` is an int, and `"4.25"` is a string.

</details>

#### MCQ 17. How do you insert `count` into a message?

A. `print("Found " + count)`
B. `print(f"Found {count} cards")`
C. `print("Found {count} cards")`
D. `print(count + " cards")`

<details>
<summary>Show answer</summary>

**Correct answer: B.** The f-string evaluates the expression inside the braces.

</details>

#### MCQ 18. Which statement about `None` is correct?

A. `None` is the same as `0`
B. `None` is the same as `False`
C. `None` means no value and is different from `0` and `False`
D. `None` can only be used in strings

<details>
<summary>Show answer</summary>

**Correct answer: C.** Use `is None` for a missing value. `0` and `False` are different values.

</details>

#### MCQ 19. A tester is collecting failure messages in order. Which container fits best?

A. A set
B. A tuple
C. A dictionary
D. A list

<details>
<summary>Show answer</summary>

**Correct answer: D.** A list preserves order and can grow with `append`.

</details>

#### MCQ 20. When is a tuple a good choice for a card pair?

A. When the pair is a fixed `(question, answer)` shape that should not change
B. When the values must be appended to
C. When the values are looked up by key
D. When the values must be unique

<details>
<summary>Show answer</summary>

**Correct answer: A.** A tuple is immutable and expresses a fixed shape.

</details>

#### MCQ 21. A quiz record has an id, question, and answer. Which type best represents it?

A. A string
B. A dictionary with those keys
C. A single integer
D. A set of three values

<details>
<summary>Show answer</summary>

**Correct answer: B.** A dictionary maps field names to values, which is the natural record shape.

</details>

#### MCQ 22. A tester wants to know how many unique questions a file contains. Which tool is best?

A. A list count
B. A tuple
C. A set
D. A float

<details>
<summary>Show answer</summary>

**Correct answer: C.** `len(set(questions))` counts unique values. A set also loses order.

</details>

#### MCQ 23. What is `cards[-1]`?

A. The first card
B. An error
C. The card at index 1
D. The last card

<details>
<summary>Show answer</summary>

**Correct answer: D.** Negative indexes count from the end; `-1` is the last item.

</details>

#### MCQ 24. What does `cards[1:3]` return?

A. The first three cards
B. Indexes 1, 2, and 3
C. Only index 3
D. Indexes 1 and 2; the stop is exclusive

<details>
<summary>Show answer</summary>

**Correct answer: D.** The start is included and the stop is excluded.

</details>

#### MCQ 25. A CSV column contains `"12"`. Why does `count + 1` fail?

A. CSV values are strings; convert with `int()` first
B. Python cannot add numbers
C. The CSV is encrypted
D. `count` must be a float

<details>
<summary>Show answer</summary>

**Correct answer: A.** CSV readers return strings. Convert the value before arithmetic.

</details>

#### MCQ 26. What happens with `int("4.5")`?

A. It returns 4.5
B. It returns 4
C. It raises `ValueError`
D. It returns `None`

<details>
<summary>Show answer</summary>

**Correct answer: C.** `int()` does not parse a decimal string; use `float("4.5")`.

</details>

#### MCQ 27. A function appends to a list passed by the caller. What is the risk?

A. The list becomes a tuple
B. The caller's list changes unexpectedly
C. Python raises a syntax error
D. The function cannot return a value

<details>
<summary>Show answer</summary>

**Correct answer: B.** Lists are mutable. Copy the list when the function should not change the original.

</details>

#### MCQ 28. Which value is falsy in a condition?

A. An empty list
B. A non-empty string
C. `1`
D. A non-empty dictionary

<details>
<summary>Show answer</summary>

**Correct answer: A.** Empty containers are falsy. Non-empty containers and non-zero numbers are truthy.

</details>

#### MCQ 29. A tester needs a lookup from card id to question. Which container is the natural choice?

A. A tuple of pairs
B. A list of booleans
C. A float
D. A dictionary keyed by card id

<details>
<summary>Show answer</summary>

**Correct answer: D.** A dictionary gives direct key lookup.

</details>

#### MCQ 30. A dictionary may not contain `"source"`. How do you read it safely?

A. `card["source"]`
B. `card.source`
C. `card.get("source")`
D. `card.find("source")`

<details>
<summary>Show answer</summary>

**Correct answer: C.** `.get()` returns `None` when the key is absent instead of raising `KeyError`.

</details>

## Part 3 — Control Flow and Functions (15 questions)

#### MCQ 31. A status can be `passed`, `failed`, or `running`. Which structure fits?

A. `if` / `elif` / `else`
B. A single multiplication
C. A set
D. A file handle

<details>
<summary>Show answer</summary>

**Correct answer: A.** The three branches map cleanly to `if`, `elif`, and `else`.

</details>

#### MCQ 32. How do you visit every card in a list?

A. `if card in cards:`
B. `for card in cards:`
C. `while cards:`
D. `cards.loop()`

<details>
<summary>Show answer</summary>

**Correct answer: B.** A `for` loop iterates over the items.

</details>

#### MCQ 33. What does `range(3)` produce?

A. `1, 2, 3`
B. `0, 1, 2, 3`
C. `0, 1, 2`
D. `3`

<details>
<summary>Show answer</summary>

**Correct answer: C.** `range` stops before the given value.

</details>

#### MCQ 34. A tester needs each card and its position. Which loop is best?

A. `for card in cards:`
B. `while cards:`
C. `for _ in range(len(cards)):`
D. `for index, card in enumerate(cards, start=1):`

<details>
<summary>Show answer</summary>

**Correct answer: D.** `enumerate` gives the index and the value without manual counting.

</details>

#### MCQ 35. A retry should run at most three times. Which loop fits?

A. `while attempts < 3:` with `attempts += 1` inside
B. `while True:` with no exit
C. `for card in cards:`
D. `if attempts < 3:`

<details>
<summary>Show answer</summary>

**Correct answer: A.** The condition and the increment give a clear stop. A `for` over `range(3)` also works.

</details>

#### MCQ 36. What does `break` do inside a loop?

A. Skips the current iteration
B. Exits the loop immediately
C. Restarts the loop
D. Converts the loop to a function

<details>
<summary>Show answer</summary>

**Correct answer: B.** `break` exits; `continue` skips to the next iteration.

</details>

#### MCQ 37. Which line defines a function?

A. `function count_cards(cards):`
B. `count_cards = def(cards)`
C. `def count_cards(cards):`
D. `func count_cards(cards):`

<details>
<summary>Show answer</summary>

**Correct answer: C.** Python uses `def name(parameters):` to define a function.

</details>

#### MCQ 38. Why return a value instead of printing it inside a function?

A. Printing always raises an error
B. Python cannot print from a function
C. Return statements are required in every function
D. Returned values are easier to assert on and reuse

<details>
<summary>Show answer</summary>

**Correct answer: D.** Returned values are testable and reusable; printing is a side effect.

</details>

#### MCQ 39. Why is `def add(item, items=[]):` risky?

A. The default list is shared across calls
B. Lists cannot be default arguments
C. Python rejects the syntax
D. It makes the function private

<details>
<summary>Show answer</summary>

**Correct answer: A.** Mutable defaults persist between calls; use `None` and create a new list inside.

</details>

#### MCQ 40. How do you use a helper from `helpers.py`?

A. `import helpers.py`
B. `from helpers import count_cards`
C. `include helpers`
D. `require("helpers")`

<details>
<summary>Show answer</summary>

**Correct answer: B.** The module name has no `.py` in the import.

</details>

#### MCQ 41. A card's `source` may be `None`. Which check is clearest?

A. `if source == 0:`
B. `if source:`
C. `if source is None:`
D. `if source == "None":`

<details>
<summary>Show answer</summary>

**Correct answer: C.** `is None` expresses the missing value directly.

</details>

#### MCQ 42. Why is changing a list while iterating over it risky?

A. Python always raises `SyntaxError`
B. The list becomes a tuple
C. The loop runs forever by design
D. Items can be skipped or processed twice

<details>
<summary>Show answer</summary>

**Correct answer: D.** Mutating during iteration can skip or duplicate items; loop over a copy instead.

</details>

#### MCQ 43. Which function name is clearest?

A. `find_duplicate_questions`
B. `do_stuff`
C. `helper`
D. `x`

<details>
<summary>Show answer</summary>

**Correct answer: A.** A name that describes the result is easier to review and reuse.

</details>

#### MCQ 44. A script cannot import a local module. What is the most likely fix?

A. Rename the module to uppercase
B. Run from the directory that contains the module or add it to the path
C. Install the module from PyPI
D. Convert the module to a class

<details>
<summary>Show answer</summary>

**Correct answer: B.** Local imports depend on the working directory and `sys.path`.

</details>

#### MCQ 45. What does `for key in card:` produce when `card` is a dictionary?

A. The values
B. Pairs of keys and values
C. The indexes
D. The keys

<details>
<summary>Show answer</summary>

**Correct answer: D.** Iterating a dictionary yields its keys. Use `.items()` for key/value pairs.

</details>

## Part 4 — Files and Data (15 questions)

#### MCQ 46. A tester needs `data/cards.md` on Windows, macOS, and Linux. Which path construction is most portable?

A. `"data" + ":" + "cards.md"`
B. `"data" + "\\" + "cards.md"`
C. `"data/cards.md"` passed to `open` only
D. `Path("data") / "cards.md"`

<details>
<summary>Show answer</summary>

**Correct answer: D.** `pathlib.Path` handles separators portably.

</details>

#### MCQ 47. Why use `with open(...)` for a fixture?

A. It makes the file read-only
B. It closes the file even if an exception occurs
C. It encrypts the file
D. It converts the file to JSON

<details>
<summary>Show answer</summary>

**Correct answer: B.** `with` manages the file handle and closes it reliably.

</details>

#### MCQ 48. A log contains accented characters. Which read is safest?

A. `path.read_text()`
B. `open(path).read()`
C. `path.read_text(encoding="utf-8")`
D. `path.read_bytes().decode("latin-1")`

<details>
<summary>Show answer</summary>

**Correct answer: C.** Pass the encoding explicitly; UTF-8 is the usual choice for a UTF-8 fixture.

</details>

#### MCQ 49. Which function parses a JSON string?

A. `json.dump`
B. `json.load`
C. `json.parse_file`
D. `json.loads`

<details>
<summary>Show answer</summary>

**Correct answer: D.** `json.loads` parses a string; `json.load` reads a file object.

</details>

#### MCQ 50. A test has an open JSON file object. Which call reads it?

A. `json.load(handle)`
B. `json.loads(handle)`
C. `json.read(handle)`
D. `json.file(handle)`

<details>
<summary>Show answer</summary>

**Correct answer: A.** `json.load` accepts a file object; `json.loads` accepts a string.

</details>

#### MCQ 51. How do you read `cards.csv` into dictionaries keyed by header?

A. `csv.reader` with manual indexes
B. `csv.DictReader(handle)`
C. `json.load(handle)`
D. `Path.read_text().split(",")`

<details>
<summary>Show answer</summary>

**Correct answer: B.** `DictReader` maps each row to a dictionary using the header.

</details>

#### MCQ 52. Why open a CSV with `newline=""`?

A. To make the file smaller
B. To convert values to numbers
C. So the `csv` module handles line endings correctly
D. To encrypt the file

<details>
<summary>Show answer</summary>

**Correct answer: C.** `newline=""` avoids double newline handling on different platforms.

</details>

#### MCQ 53. A fixture may be missing. Which exception should you catch?

A. `Exception`
B. `KeyboardInterrupt`
C. `SystemExit`
D. `FileNotFoundError`

<details>
<summary>Show answer</summary>

**Correct answer: D.** Catch the specific error you can handle; let unexpected errors surface.

</details>

#### MCQ 54. Why is a bare `except:` risky?

A. It catches every error, including programming mistakes, and hides the cause
B. It makes the script slower
C. It cannot catch file errors
D. It only works on Windows

<details>
<summary>Show answer</summary>

**Correct answer: A.** Catch the narrow exception you expect; a bare except can swallow real bugs.

</details>

#### MCQ 55. When is `logging` better than `print`?

A. When the script is one line
B. When the script runs in CI and needs levels, timestamps, or filterable records
C. When the output must be hidden
D. When the script has no errors

<details>
<summary>Show answer</summary>

**Correct answer: B.** `logging` is for structured, filterable output; `print` is fine for a small local script.

</details>

#### MCQ 56. What must never appear in a log?

A. A file path
B. A test name
C. A token, password, or customer secret
D. A timestamp

<details>
<summary>Show answer</summary>

**Correct answer: C.** Logs are copied into tickets and CI artifacts; secrets and customer data stay out.

</details>

#### MCQ 57. How do you test a missing-file case safely?

A. Point at a nonexistent path in a temporary directory and assert the specific error
B. Create the file and delete it after the test
C. Use the production database
D. Ignore the error and mark the test as passed

<details>
<summary>Show answer</summary>

**Correct answer: A.** The test should expect the specific missing-file behavior without touching real fixtures.

</details>

#### MCQ 58. What should a file-validation failure say?

A. The file, row or key, expected value, and actual value
B. Only “failed”
C. Only the test name
D. A stack trace with secrets

<details>
<summary>Show answer</summary>

**Correct answer: A.** Specific context lets the next person reproduce and fix the problem.

</details>

#### MCQ 59. A CSV column contains `"12"`. What should the script do before adding 1?

A. Convert it with `str()`
B. Convert it with `int()`
C. Compare it to `None`
D. Convert it to a list

<details>
<summary>Show answer</summary>

**Correct answer: B.** CSV values are strings; `int()` produces a number for arithmetic.

</details>

#### MCQ 60. Which write is safest for a small UTF-8 report?

A. `open("report.txt", "w")` without a close
B. `Path("report.txt").write_text("ok")` without encoding
C. `with open("report.txt", "w", encoding="utf-8") as handle: handle.write("ok")`
D. `print("ok")`

<details>
<summary>Show answer</summary>

**Correct answer: C.** The `with` form closes reliably and sets the encoding explicitly.

</details>

## Part 5 — Testing with pytest (15 questions)

#### MCQ 61. Which file will pytest discover by default?

A. `tests/test_cards.py`
B. `tests/cards_test.py` only
C. `tests/check_cards.py`
D. `tests/cards.py`

<details>
<summary>Show answer</summary>

**Correct answer: A.** pytest discovers `test_*.py` (and `*_test.py`) files with `test_*` functions.

</details>

#### MCQ 62. Which assertion message is most useful?

A. `assert count == 3`
B. `assert count == 3, f"Expected 3 cards, found {count}"`
C. `assert count`
D. `assert True`

<details>
<summary>Show answer</summary>

**Correct answer: B.** It states the rule and the actual value.

</details>

#### MCQ 63. A test expects invalid input to raise `ValueError`. What should it use?

A. A bare `try`
B. `assert False`
C. `with pytest.raises(ValueError):`
D. `pytest.skip`

<details>
<summary>Show answer</summary>

**Correct answer: C.** `pytest.raises` checks the specific expected exception.

</details>

#### MCQ 64. What is a pytest fixture?

A. A test file
B. A production dependency
C. A command-line flag
D. Setup data or a resource that a test requests by name

<details>
<summary>Show answer</summary>

**Correct answer: D.** Fixtures prepare what a test needs, such as a temporary file.

</details>

#### MCQ 65. Which fixture gives a test a temporary directory?

A. `tmp_path`
B. `temp_file`
C. `workspace`
D. `fixture_dir`

<details>
<summary>Show answer</summary>

**Correct answer: A.** `tmp_path` is built into pytest and is cleaned up automatically.

</details>

#### MCQ 66. What does `@pytest.mark.parametrize` do?

A. Skips a test
B. Runs the same test with several input/expected pairs
C. Creates a fixture
D. Installs a package

<details>
<summary>Show answer</summary>

**Correct answer: B.** Each case appears separately in the output.

</details>

#### MCQ 67. A pytest run shows one failing assertion after another. Which should you read first?

A. The last line of the summary
B. The longest traceback
C. The first failing test and its assertion values
D. The coverage report

<details>
<summary>Show answer</summary>

**Correct answer: C.** The first failure is usually the cause; later failures may be consequences.

</details>

#### MCQ 68. Why should tests be independent?

A. So they run faster
B. So they never fail
C. So they do not need assertions
D. So they can run alone and in any order

<details>
<summary>Show answer</summary>

**Correct answer: D.** Independence makes failures reproducible and avoids hidden ordering dependencies.

</details>

#### MCQ 69. A test function calls no assertions and just prints. What is it?

A. Not a meaningful test
B. A fixture
C. A parametrized test
D. A passing test

<details>
<summary>Show answer</summary>

**Correct answer: A.** Without an assertion, the test does not check behavior.

</details>

#### MCQ 70. Why can shared mutable fixture state cause problems?

A. It makes the test file too short
B. Tests can depend on order and interfere with each other
C. pytest cannot read lists
D. It changes the Python version

<details>
<summary>Show answer</summary>

**Correct answer: B.** Each test should get isolated data; shared state causes order-dependent failures.

</details>

#### MCQ 71. Which should a unit test not depend on?

A. A local synthetic fixture
B. A temporary file
C. A live production service without a controlled endpoint
D. A parametrized input

<details>
<summary>Show answer</summary>

**Correct answer: C.** Test your code against a controlled test endpoint or a fake; production is not a unit-test dependency.

</details>

#### MCQ 72. How does pytest differ from unittest?

A. pytest cannot run assertions
B. unittest cannot use fixtures
C. pytest only works with Django
D. pytest uses plain functions and `assert`, with fixtures and parametrization built in

<details>
<summary>Show answer</summary>

**Correct answer: D.** pytest is shorter for small suites; unittest uses classes and `self.assert*`.

</details>

#### MCQ 73. Which test name is clearest?

A. `test_empty_cards_file_reports_zero`
B. `test_1`
C. `test_stuff`
D. `test_it`

<details>
<summary>Show answer</summary>

**Correct answer: A.** A descriptive name tells the reviewer what behavior is protected.

</details>

#### MCQ 74. Where does pytest show the actual value that failed an assertion?

A. Only in the test name
B. In the failing assertion output
C. In the requirements file
D. In the git log

<details>
<summary>Show answer</summary>

**Correct answer: B.** The failure output shows the assertion and the values.

</details>

#### MCQ 75. A test fails, and the fix is to delete the assertion. What should the reviewer do?

A. Accept it
B. Delete the test
C. Ignore the failure
D. Treat it as a weakened test until the product rule justifies the change

<details>
<summary>Show answer</summary>

**Correct answer: D.** Removing the check can hide the failure; the test must still verify required behavior.

</details>

## Part 6 — QA Scripting (15 questions)

#### MCQ 76. How should a Python script run another program with arguments?

A. `subprocess.run(["python", "--version"], capture_output=True, text=True)`
B. `subprocess.run("python --version")` only
C. `os.system("python --version")` for all cases
D. `run("python")`

<details>
<summary>Show answer</summary>

**Correct answer: A.** Pass a list to avoid shell quoting problems and capture the output.

</details>

#### MCQ 77. A subprocess returns `1`. What does that usually mean?

A. Success
B. Failure
C. The program was skipped
D. The output was empty

<details>
<summary>Show answer</summary>

**Correct answer: B.** Zero is success; non-zero is failure.

</details>

#### MCQ 78. Why capture stdout and stderr from a subprocess?

A. To make the command faster
B. To hide the output
C. To include the evidence in a failure message
D. To install dependencies

<details>
<summary>Show answer</summary>

**Correct answer: C.** Captured output lets the report show what the command printed.

</details>

#### MCQ 79. A QA script needs a file path and a `--strict` flag. Which tool fits?

A. `json`
B. `csv`
C. `datetime`
D. `argparse`

<details>
<summary>Show answer</summary>

**Correct answer: D.** `argparse` defines positional and optional arguments with help text.

</details>

#### MCQ 80. Which call gives the current local date and time?

A. `time.sleep()`
B. `datetime.now()`
C. `date.today()` only
D. `datetime.strftime()`

<details>
<summary>Show answer</summary>

**Correct answer: B.** `datetime.now()` returns the current local date and time; `strftime` formats a value.

</details>

#### MCQ 81. Why use timezone-aware datetimes when comparing systems?

A. They make the output shorter
B. They remove the need for timestamps
C. Naive local times can be ambiguous across time zones
D. They convert numbers to strings

<details>
<summary>Show answer</summary>

**Correct answer: C.** Timezone-aware values make cross-system comparisons meaningful.

</details>

#### MCQ 82. Why set a timeout on `requests.get`?

A. To make the response larger
B. To skip the status check
C. To convert JSON automatically
D. To avoid hanging the test run when the service does not respond

<details>
<summary>Show answer</summary>

**Correct answer: D.** A timeout turns a hung service into a clear failure.

</details>

#### MCQ 83. What does `response.raise_for_status()` do?

A. Raises an exception for a 4xx or 5xx response
B. Returns the JSON body
C. Sets a timeout
D. Deletes the response

<details>
<summary>Show answer</summary>

**Correct answer: A.** It turns an HTTP error status into an exception.

</details>

#### MCQ 84. How should a script get its base URL?

A. Hard-code the production URL
B. Read it from an environment variable with a safe default
C. Put it in a test name
D. Store it in a log

<details>
<summary>Show answer</summary>

**Correct answer: B.** Environment variables separate configuration from code and avoid hard-coded environments.

</details>

#### MCQ 85. Where should an API token go?

A. In the Python source
B. In the README
C. In an approved secret store or environment variable, never in the repo
D. In a log line

<details>
<summary>Show answer</summary>

**Correct answer: C.** Secrets stay out of source, docs, and logs; use an approved store.

</details>

#### MCQ 86. What makes an end-to-end QA script idempotent?

A. It changes production data every run
B. It creates a new user each run
C. It prints more output
D. It can run repeatedly without leaving state behind

<details>
<summary>Show answer</summary>

**Correct answer: D.** Idempotent checks do not accumulate or corrupt state.

</details>

#### MCQ 87. Why is building a shell string from user input risky?

A. The input can inject shell commands or break quoting
B. Python cannot run shell strings
C. The shell is always slower
D. It disables subprocess

<details>
<summary>Show answer</summary>

**Correct answer: A.** Pass a list of arguments instead of interpolating untrusted text.

</details>

#### MCQ 88. An API returns HTTP 200. Is the payload automatically correct?

A. Yes, 200 means the data is valid
B. No; validate the body against the contract
C. Only if the response is JSON
D. Only if a timeout was set

<details>
<summary>Show answer</summary>

**Correct answer: B.** A 200 status does not prove the payload's fields or values are correct.

</details>

#### MCQ 89. When is a Python script not worth writing?

A. When the check has several steps
B. When the logic needs tests
C. When a shell one-liner or existing tool already does the job
D. When the data is JSON

<details>
<summary>Show answer</summary>

**Correct answer: C.** A script adds maintenance and review surface; use the simplest tool that works.

</details>

#### MCQ 90. What makes a QA script trustworthy?

A. It prints “OK” without checking anything
B. It hides failures
C. It uses production data by default
D. It checks a real condition, fails clearly, and is reproducible

<details>
<summary>Show answer</summary>

**Correct answer: D.** A trustworthy check has a real assertion, a clear non-zero failure, and evidence.

</details>
