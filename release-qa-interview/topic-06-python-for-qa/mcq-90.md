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
