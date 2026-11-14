# Playwright for QA

### A Practical Browser-Testing Primer for People Who Have Never Used Playwright

**Version 1.0 · November 2026**

> You do not need to become an automation engineer to start. You need to test one real user journey, understand why it passed or failed, and leave behind evidence another person can use.

---

## Contents

- [Part 1: What Playwright is — and is not](#part-1-what-playwright-is--and-is-not)
- [Part 2: From zero to your first real test](#part-2-from-zero-to-your-first-real-test)
- [Part 3: Locators and assertions](#part-3-locators-and-assertions)
- [Part 4: Test structure, fixtures, and the Page Object Model](#part-4-test-structure-fixtures-and-the-page-object-model)
- [Part 5: Network, offline, and authentication](#part-5-network-offline-and-authentication)
- [Part 6: Debugging and evidence](#part-6-debugging-and-evidence)
- [Part 7: Browsers, parallelism, and CI](#part-7-browsers-parallelism-and-ci)
- [Part 8: Test design for QA](#part-8-test-design-for-qa)
- [Part 9: The complete flashcards suite](#part-9-the-complete-flashcards-suite)
- [Part 10: Labs](#part-10-labs)
- [Appendices](#appendices)
  - [A: Cheat sheet](#appendix-a-cheat-sheet)
  - [B: Glossary](#appendix-b-glossary)
  - [C: Quiz](#appendix-c-quiz)
  - [D: Bug report template for E2E and flaky failures](#appendix-d-bug-report-template-for-e2e-and-flaky-failures)
  - [E: Running a knowledge-sharing session](#appendix-e-running-a-knowledge-sharing-session)
  - [F: Resources and what to learn next](#appendix-f-resources-and-what-to-learn-next)

---

## What this guide will do for you

By the end, you will be able to:

- Install Playwright for Python, configure pytest, and run a browser test.
- Find elements with durable locators and assert what a user sees.
- Explain auto-waiting and why `time.sleep` makes tests slower and flakier.
- Structure tests with fixtures, isolated contexts, test data, and page objects.
- Mock, delay, fail, and block network traffic to test realistic conditions.
- Reuse authenticated state without pretending you tested login.
- Debug failures with headed runs, the Inspector, screenshots, video, and traces.
- Run a cross-browser, parallel suite in CI and report failures with useful evidence.
- Decide what belongs in E2E testing and handle flaky tests responsibly.

## Who this is for

Complete beginners preparing for QA work. You know a little Python — variables, functions, imports, running a script — and you have used a browser. No prior test automation experience is assumed.

This guide uses **Playwright's Python API with pytest and `pytest-playwright`**, matching the Python flashcards project from *From Zero to Claude Code*. Playwright's **TypeScript/JavaScript API is the most common in industry**; you will see it in job postings. The concepts transfer directly.

> **The running example.** You are testing Maya's `flashcards/` project. `cards.md` is the source of truth. `flashcards.py` parses it, writes `cards.csv`, generates `quiz.html`, and supports `--check`, `--export`, and `--quiz`. `quiz.html` shows one card at a time with a **Show answer** button and a next button, and it works offline. The flashcards folder is teaching material and is not included in this repository; this guide supplies a representative page so every example has something concrete to test.

## Three rules for testers

**1. Test what a user can do, not how the DOM happens to be built.** Prefer roles, labels, visible text, and a few deliberate test IDs over long CSS chains.

**2. Wait for the application; never guess with a sleep.** Locators and assertions wait for the condition they need. A fixed sleep is either too short or too long, and it hides the real problem.

**3. Isolate tests and protect access.** Create the state each test needs, use disposable data, and keep authenticated state out of Git. Never point a destructive test at production.

---

# Part 1: What Playwright Is — and Is Not

## 1.1 Playwright in plain English

Playwright controls real browsers. You write code that says "open this page, click the button named Show answer, and check that this text appears." Playwright sends the commands and reports what happened.

It is open source, originally built at Microsoft, with APIs for Python, TypeScript/JavaScript, Java, and .NET. This guide uses the synchronous Python API:

```python
from playwright.sync_api import Page, expect
```

The browser hierarchy matters:

```
Playwright → Browser → Browser context (isolated profile) → Page (tab)
```

A **browser context** is cheap and isolated, like an incognito profile. pytest-playwright creates a fresh context for each test by default, even though the browser process is reused. Playwright drives Chromium, Firefox, and WebKit. WebKit is the engine used by Safari; Playwright ships its own patched build, not branded Safari. It can launch branded Chrome and Edge through channels.

## 1.2 What Playwright is not

- **Not a unit-test framework.** Your parser and data logic still belong in fast Python tests.
- **Not a load-testing tool.** It measures one user's experience, not thousands of concurrent users.
- **Not an accessibility certificate.** Role-based tests catch some problems; a full audit needs keyboard testing, assistive technology, and tools such as axe.
- **Not a security scanner.** Network interception helps test behavior; it does not prove security.
- **Not automatic maintenance.** Codegen is a starting point; selectors, data, and assertions need review.
- **The Python API has no built-in screenshot assertions.** You can capture screenshots, but pixel comparison needs separate tooling.

## 1.3 How it compares with Selenium and Cypress

| Concern | Playwright | Selenium | Cypress |
|---|---|---|---|
| **Languages** | Python, TypeScript/JavaScript, Java, .NET | Many, incl. Python, Java, JavaScript | Primarily JavaScript/TypeScript |
| **Browser control** | Bundled Chromium, Firefox, WebKit, driven from outside the page | W3C WebDriver with broad Grid support | Runs inside the browser event loop |
| **Waiting** | Actionability plus auto-retrying web-first assertions | Explicit and implicit waits are mostly your responsibility | Built-in retry-ability |
| **Multi-tab and origins** | First-class page and context APIs | Supported, often more setup | Improved, but historically limited |
| **Evidence** | Trace Viewer with DOM, network, console, actions | Tool- and Grid-dependent | Time-travel runner and video |
| **Best fit** | Polyglot teams wanting cross-browser, network control, traces | Existing Selenium Grids and very broad needs | JavaScript teams wanting an integrated developer experience |

All three can produce good or brittle tests. The tool does not decide whether a test is meaningful.

## 1.4 Why QA teams use it

Auto-waiting, cross-browser Chromium/Firefox/WebKit coverage, fast isolated contexts, network mocking and blocking, evidence-rich traces, parallel pytest workers, and codegen/Inspector make Playwright practical for end-to-end QA. The trade-offs are real: browser binaries are large, CI needs system dependencies, and E2E tests are slower and more expensive than unit tests.

---

# Part 2: From Zero to Your First Real Test

## 2.1 Install Python and a virtual environment

Use Python 3.10 or newer, as the flashcards project does. A current Python release is a better default than an old system Python.

If you have not built the flashcards project from *From Zero to Claude Code*, create the folder first (`mkdir flashcards`) and save the fixture from section 2.2 as `quiz.html`. The parser and card generator are not required for the Playwright examples; the browser tests only need the page.

```powershell
cd C:\Users\<you>\AI_Study\flashcards
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
cd ~/AI_Study/flashcards
python3 -m venv .venv
source .venv/bin/activate
```

If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in that terminal, then activate again. Your prompt should begin with `(.venv)`. Install the tooling and one browser, then install the rest when you need them:

```bash
python -m pip install --upgrade pip
python -m pip install pytest-playwright
python -m playwright install chromium
python -m playwright install chromium firefox webkit   # cross-browser
python -m playwright install --with-deps chromium      # Linux CI
```

`pytest-playwright` installs Playwright, the `playwright` command, and the pytest plugin; it does not install browsers. Expect several hundred megabytes per engine. Check the versions with `python -m playwright --version` and `python -m pytest --version`.

In VS Code, install the Python extension, open the `flashcards` folder, select `.venv\Scripts\python.exe`, and enable pytest discovery. Annotate tests with `page: Page` for completion and type hints. Keep `requirements-dev.txt` with `pytest`, `pytest-playwright`, `pytest-xdist`, and `pytest-rerunfailures`; pin versions after validation. Add `.venv/`, `test-results/`, `playwright/.auth/`, and `__pycache__/` to `.gitignore`.

A working layout:

```
flashcards/
├── cards.md, flashcards.py, quiz.html
├── requirements-dev.txt, pytest.ini
├── pages/quiz_page.py
├── tests/conftest.py, tests/test_quiz.py
└── test-results/          # generated, not committed
```

## 2.2 A small `quiz.html` fixture

The real generator produces a larger file, but the user contract is the same: one question, a reveal button, a next button, and a clear end state. Save this as `flashcards/quiz.html` to follow the examples. In the real project, add the `data-testid` attributes to the template inside `flashcards.py` instead of maintaining two versions.

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Flashcards quiz</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 42rem; margin: 3rem auto; padding: 0 1rem; }
    [hidden] { display: none !important; }
  </style>
</head>
<body>
  <main>
    <h1>Flashcards</h1>
    <p data-testid="progress"></p>
    <section data-testid="quiz" aria-live="polite">
      <h2 data-testid="question"></h2>
      <p data-testid="answer" hidden></p>
      <button type="button" data-testid="show-answer">Show answer</button>
      <button type="button" data-testid="next-card">Next card</button>
    </section>
    <p data-testid="empty-state" hidden>No cards available.</p>
  </main>
  <script>
    const cards = [
      { question: "What is confirmation bias?",
        answer: "The tendency to notice and trust evidence that supports what you already believe." },
      { question: "What is the anchoring effect?",
        answer: "The tendency for the first number you see to pull later estimates toward it." },
      { question: "What is the availability heuristic?",
        answer: "Judging how likely something is by how easily examples come to mind." }
    ];
    const deck = new URLSearchParams(window.location.search).get("empty") === "1" ? [] : cards;
    const progress = document.querySelector('[data-testid="progress"]');
    const quiz = document.querySelector('[data-testid="quiz"]');
    const question = document.querySelector('[data-testid="question"]');
    const answer = document.querySelector('[data-testid="answer"]');
    const showAnswer = document.querySelector('[data-testid="show-answer"]');
    const nextCard = document.querySelector('[data-testid="next-card"]');
    const emptyState = document.querySelector('[data-testid="empty-state"]');
    let index = 0;
    let revealed = false;

    function render() {
      if (deck.length === 0) {
        quiz.hidden = true;
        emptyState.hidden = false;
        progress.textContent = "";
        return;
      }
      quiz.hidden = false;
      emptyState.hidden = true;
      question.textContent = deck[index].question;
      answer.textContent = deck[index].answer;
      answer.hidden = !revealed;
      showAnswer.hidden = revealed;
      nextCard.disabled = index === deck.length - 1;
      progress.textContent = `Card ${index + 1} of ${deck.length}`;
    }

    showAnswer.addEventListener("click", () => { revealed = true; render(); });
    nextCard.addEventListener("click", () => {
      if (index < deck.length - 1) { index += 1; revealed = false; render(); }
    });
    render();
  </script>
</body>
</html>
```

The `?empty=1` parameter is a teaching-fixture convenience for the empty state. A production page should render the empty state from an empty deck, not from a test-only branch.

> **QA takeaway:** `data-testid` names are a small contract with the tests. Use purpose-based names such as `show-answer` that survive visual redesigns.

## 2.3 Serve over HTTP and write the first test

Browsers behave differently with `file://` URLs: storage, fetch, and origin rules do not match a deployed app. From `flashcards/`, run:

```bash
python -m http.server 8000
```

Open `http://127.0.0.1:8000/quiz.html` and try it. If port 8000 is busy, use 8001 and update the URL. Create `tests/test_quiz.py`:

```python
from playwright.sync_api import Page, expect

BASE_URL = "http://127.0.0.1:8000"


def test_quiz_page_loads(page: Page) -> None:
    page.goto(f"{BASE_URL}/quiz.html")
    expect(page.get_by_role("heading", name="Flashcards")).to_be_visible()
```

Run `python -m pytest -v`. If pytest says `page` is an unknown fixture, activate the venv and reinstall `pytest-playwright`. If navigation fails, check the server and port.

- **`page`** is a pytest fixture: a fresh tab in a fresh context for this test.
- **`page.goto()`** navigates and waits for the load event by default.
- **`get_by_role(...)`** returns a locator, a lazy query.
- **`expect(...).to_be_visible()`** retries until the heading is visible or 5 seconds pass.
- **`Page`** is only a type annotation.

A loading page is only a smoke test. Add the real journey:

```python
from playwright.sync_api import Page, expect

BASE_URL = "http://127.0.0.1:8000"


def test_reveal_answer_then_go_to_next_card(page: Page) -> None:
    page.goto(f"{BASE_URL}/quiz.html")
    question = page.get_by_test_id("question")
    answer = page.get_by_test_id("answer")

    expect(question).to_have_text("What is confirmation bias?")
    expect(answer).to_be_hidden()

    page.get_by_role("button", name="Show answer").click()
    expect(answer).to_be_visible()
    expect(answer).to_contain_text("notice and trust evidence")

    page.get_by_role("button", name="Next card").click()
    expect(question).to_have_text("What is the anchoring effect?")
    expect(answer).to_be_hidden()
```

This follows user intent and checks the reset after next, which is easy to break.

## 2.4 Why not `time.sleep`

A fixed sleep is a guess. If the app takes 2.3 seconds and you sleep for 2, the test fails. If it takes 0.1 seconds and you sleep for 5, every run wastes 4.9 seconds. CI machines are slower and less predictable, so the same guess becomes flaky. The test also learns nothing about what it was waiting for.

Playwright actions wait for actionability and assertions retry automatically. Use `page.goto()`, locators, and `expect`. `page.wait_for_timeout(2000)` is the same anti-pattern. If a condition genuinely has no assertion, wait for that specific state with a locator or event, not a guessed duration.

> **QA takeaway:** Replace every sleep with the observable condition you care about. If you cannot name it, the test is not ready to be written.

---

# Part 3: Locators and Assertions

## 3.1 Locator priority

A locator is a lazy query, resolved each time it is used, so it can wait for elements that do not exist yet. Use this order:

| Priority | Locator | Use for |
|---|---|---|
| 1 | `get_by_role()` | Buttons, links, headings, checkboxes, text boxes with an accessible role and name |
| 2 | `get_by_label()` | Form controls with a `<label>`, `aria-label`, or `aria-labelledby` |
| 3 | `get_by_text()` | Non-interactive text where the words are the contract |
| 4 | `get_by_test_id()` | Dynamic content with no stable user-facing identity |
| 5 | `locator("css=...")`, `locator("xpath=...")` | Last resort |

Role and label locators exercise the accessibility tree. If a button cannot be found by role and name, a screen-reader user may have the same problem. Test IDs are resilient but invisible to users; use them deliberately.

## 3.2 Common locators

```python
from playwright.sync_api import Page, expect

BASE_URL = "http://127.0.0.1:8000"


def test_locator_varieties(page: Page) -> None:
    page.goto(f"{BASE_URL}/quiz.html")
    page.get_by_role("button", name="Show answer").click()
    expect(page.get_by_test_id("answer")).to_be_visible()

    page.goto(f"{BASE_URL}/quiz.html?empty=1")
    expect(page.get_by_text("No cards available.")).to_be_visible()

    # The quiz has no form; this is the pattern for one.
    # page.get_by_label("Search cards").fill("anchoring")
```

Role names and test IDs can be regular expressions. Text matching normalizes whitespace, and role-name matching is case-insensitive substring matching unless you pass `exact=True`.

## 3.3 Strict mode, filtering, and chaining

Locators are strict: a single-element action throws a **strict mode violation** when several elements match. This prevents silently clicking the wrong button.

```python
from playwright.sync_api import Page, expect

BASE_URL = "http://127.0.0.1:8000"


def test_narrow_a_locator(page: Page) -> None:
    page.goto(f"{BASE_URL}/quiz.html")
    buttons = page.get_by_role("button")
    expect(buttons).to_have_count(2)

    # Too broad: buttons.click() raises a strict mode violation.
    page.get_by_role("button", name="Show answer").click()

    # Chain inside a known region rather than selecting by position.
    page.get_by_test_id("quiz").get_by_role("button", name="Next card").click()
```

Filtering supports `has_text`, `has_not_text`, `has`, and `has_not`; `has` and `has_not` are relative to the outer locator. Positional methods also exist: `.nth(1)` is zero-based, and `.first`/`.last` bypass strictness. Use them only for genuinely ordered collections; `page.get_by_role("button").nth(1).click()` selects today's next button and silently becomes brittle when the page changes. Prefer a unique role/name/test ID or a chained locator.

## 3.4 Test IDs

The fixture already has:

```html
<h2 data-testid="question"></h2>
<button type="button" data-testid="show-answer">Show answer</button>
```

Good test IDs are stable, unique, and purpose-based. Add them in the generator template, not after generation, and treat them as a contract. The default attribute is `data-testid`; it can be changed globally with `playwright.selectors.set_test_id_attribute("data-pw")`. Test IDs cannot verify accessible names, so keep role-based tests for critical controls.

CSS is reasonable for a stable attribute with no semantic equivalent, such as `input[name="email"]`. XPath is occasionally necessary in third-party markup. Both couple tests to DOM shape; XPath does not pierce shadow roots. Read codegen selectors critically instead of copying long generated chains.

## 3.5 Web-first assertions

`expect` assertions retry until true or the timeout expires. The **default assertion timeout is 5 seconds**; default action and navigation timeouts are **30 seconds**. Do not raise timeouts to hide a race.

| Assertion | Checks |
|---|---|
| `to_be_visible()` / `to_be_hidden()` | Visibility, including missing elements for hidden |
| `to_have_text("...")` | Exact normalized text, regex, or list |
| `to_contain_text("...")` | Text contains the value |
| `to_have_count(3)` | Number of matching elements |
| `to_be_enabled()` / `to_be_disabled()` | Enabled state, including `aria-disabled` |
| `expect(page).to_have_url(...)` | URL string or regex |
| `expect(page).to_have_title(...)` | Page title |
| `to_have_value(...)` | Form control value |

```python
import re

from playwright.sync_api import Page, expect

BASE_URL = "http://127.0.0.1:8000"


def test_page_level_assertions(page: Page) -> None:
    page.goto(f"{BASE_URL}/quiz.html")
    expect(page).to_have_url(re.compile(r"/quiz\.html$"))
    expect(page).to_have_title("Flashcards quiz")
    expect(page.get_by_test_id("progress")).to_have_text("Card 1 of 3")
    expect(page.get_by_test_id("answer")).to_be_hidden()

    show_answer = page.get_by_role("button", name="Show answer")
    expect(show_answer).to_be_visible()
    show_answer.click()
    expect(page.get_by_test_id("answer")).to_contain_text("confirmation")
```

A bare `assert locator.is_visible()` is an immediate check with no retry, and reading `inner_text()` before asserting can observe a half-rendered page. Use `expect` for anything that changes. If a known-slow operation genuinely needs longer, set `expect.set_options(timeout=10_000)` or pass a per-assertion `timeout=15_000`.

> **QA takeaway:** An assertion should describe an outcome a user can observe. `to_have_text("Card 1 of 3")` is a contract; a raw DOM count is a snapshot of today's markup.

---

# Part 4: Test Structure, Fixtures, and the Page Object Model

## 4.1 pytest-playwright fixtures and scopes

| Fixture | Scope | Purpose |
|---|---|---|
| `page` | Function | New page in a new context |
| `context` | Function | The page's isolated browser context |
| `browser` | Session | Launched browser, shared by tests in a worker |
| `browser_name` | Session | `"chromium"`, `"firefox"`, or `"webkit"` |
| `playwright` | Session | Playwright instance |
| `new_context` | Function | Factory for extra contexts, useful for multi-user tests |

`browser_type`, `browser_channel`, `is_chromium`, `is_webkit`, and `is_firefox` are also available. There is no built-in `browser_context` fixture; the context fixture is `context`.

Function scope is the safe default. A new context means cookies, storage, and permissions do not leak. A session-scoped page would create order dependence. Share only expensive immutable resources such as the browser or local server. Plugin CLI options apply to the default fixtures, not to contexts you create manually.

## 4.2 Setup, teardown, and a local server

Run the server automatically so CI and parallel workers do not depend on a manual terminal. Put this in `tests/conftest.py`:

```python
import functools
import threading
from collections.abc import Iterator
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        pass


@pytest.fixture(scope="session")
def quiz_base_url() -> Iterator[str]:
    root = Path(__file__).resolve().parent.parent
    handler = functools.partial(QuietHandler, directory=str(root))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join()
```

Port `0` chooses a free port for each worker. The code before `yield` is setup; after it is teardown. Use the fixture:

```python
from playwright.sync_api import Page, expect


def test_smoke(page: Page, quiz_base_url: str) -> None:
    response = page.goto(f"{quiz_base_url}/quiz.html")
    assert response is not None
    assert response.status == 200
    expect(page.get_by_role("heading", name="Flashcards")).to_be_visible()
```

For a larger app, start the real server with a readiness check instead of `http.server`.

## 4.3 Test data and independence

Tests should create or select their own data. Do not rely on a previous test's clicks. For a stable UI contract, an independent expected-data list is readable and deterministic:

```python
import pytest


@pytest.fixture
def expected_cards() -> list[tuple[str, str]]:
    return [
        ("What is confirmation bias?", "The tendency to notice and trust evidence that supports what you already believe."),
        ("What is the anchoring effect?", "The tendency for the first number you see to pull later estimates toward it."),
        ("What is the availability heuristic?", "Judging how likely something is by how easily examples come to mind."),
    ]
```

In a real app, create unique records through an API or setup step, then clean them up. Never depend on test order, leftover rows, or a shared logged-in page. Module scope is for read-only data that is expensive to create; session scope needs a clear owner and teardown.

## 4.4 The Page Object Model

A **Page Object Model (POM)** centralizes locators and user actions so tests read as intentions instead of clicks. Create `pages/quiz_page.py`:

```python
from playwright.sync_api import Page


class FlashcardsQuizPage:
    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.base_url = base_url.rstrip("/")
        self.question = page.get_by_test_id("question")
        self.answer = page.get_by_test_id("answer")
        self.progress = page.get_by_test_id("progress")
        self.show_answer_button = page.get_by_role("button", name="Show answer")
        self.next_card_button = page.get_by_role("button", name="Next card")

    def goto(self) -> None:
        self.page.goto(f"{self.base_url}/quiz.html")

    def show_answer(self) -> None:
        self.show_answer_button.click()

    def next_card(self) -> None:
        self.next_card_button.click()

    def current_question(self) -> str:
        return self.question.inner_text()

    def current_answer(self) -> str:
        return self.answer.inner_text()
```

Expose the locators tests need for assertions, and keep methods behavioral. Add a fixture to `conftest.py`:

```python
import pytest

from pages.quiz_page import FlashcardsQuizPage


@pytest.fixture
def quiz_page(page, quiz_base_url: str) -> FlashcardsQuizPage:
    return FlashcardsQuizPage(page, quiz_base_url)
```

A test becomes:

```python
from playwright.sync_api import expect


def test_reveal_with_page_object(quiz_page) -> None:
    quiz_page.goto()
    expect(quiz_page.question).to_have_text("What is confirmation bias?")

    quiz_page.show_answer()
    expect(quiz_page.answer).to_be_visible()
    assert quiz_page.current_answer().startswith("The tendency to notice")

    quiz_page.next_card()
    expect(quiz_page.question).to_have_text("What is the anchoring effect?")
```

POM helps when several tests share page actions and selectors. It is overkill for one small test, a prototype, or a god object with one wrapper per DOM node. Do not hide every assertion inside the page object; tests should state expected behavior.

> **QA takeaway:** A page object should make tests easier to read and selectors cheaper to change. If it makes a test harder to understand, delete it.

---

# Part 5: Network, Offline, and Authentication

## 5.1 Network conditions worth testing

| Condition | What to observe |
|---|---|
| Slow response | Loading state, disabled controls, no duplicate submission |
| HTTP 4xx/5xx | Error message, retry action, data preserved |
| Malformed response | Defensive parsing, no blank screen |
| Aborted request | Offline or DNS-like failure, recovery path |
| Offline after load | Cached/offline behavior, queued actions, clear status |
| Repeated retries | Backoff, duplicate writes, eventual success |

`page.route()` intercepts one page's requests. `context.route()` intercepts every page and popup in a context. Page routes take precedence. Routing disables the HTTP cache, and service-worker requests are not intercepted unless service workers are blocked.

For the underlying network concepts — DNS, TCP, TLS, VPN, proxy, and which layer to blame — see the companion guide `tcp-ip-for-qa.md`.

## 5.2 Continue, fulfill, abort

A route handler must do exactly one of:

- **`route.continue_()`** — send to the network. The trailing underscore avoids the Python keyword. Options can change URL, method, headers, or post data.
- **`route.fulfill(...)`** — return a synthetic response. Useful for mocks, errors, delays, and missing data.
- **`route.abort(error_code="...")`** — fail the request. Codes include `failed`, `connectionrefused`, `namenotresolved`, `timedout`, and `internetdisconnected`.
- **`route.fallback()`** hands to the next matching handler; **`route.fetch()`** performs the real request for modification.

> **These network examples target an API-backed quiz page.** The Part 2 fixture embeds its cards and has no `loading` or `error-state` element, so the static page never calls `/api/cards`. To run the examples, add a small `fetch('/api/cards')` path and those states to the fixture, or route the request your real page makes. The route handlers and assertions are the lesson.

Mocking the smallest external boundary keeps tests focused:

```python
from playwright.sync_api import Page, Route, expect


def test_empty_deck_from_api(page: Page, quiz_base_url: str) -> None:
    def cards_response(route: Route) -> None:
        route.fulfill(status=200, json={"cards": []})

    page.route("**/api/cards", cards_response)
    page.goto(f"{quiz_base_url}/quiz.html")
    expect(page.get_by_test_id("empty-state")).to_be_visible()
    expect(page.get_by_test_id("question")).to_be_hidden()
```

A server error should preserve the real status and shape:

```python
from playwright.sync_api import Page, Route, expect


def test_deck_error_message(page: Page, quiz_base_url: str) -> None:
    def server_error(route: Route) -> None:
        route.fulfill(status=500, json={"error": "cards unavailable"})

    page.route("**/api/cards", server_error)
    page.goto(f"{quiz_base_url}/quiz.html")
    expect(page.get_by_test_id("error-state")).to_contain_text("try again")
```

The endpoint and the empty, loading, and error elements are extensions to the static fixture; the pattern is the lesson. Mock the boundary, then assert a user-visible outcome.

## 5.3 Delay, abort, and offline

These examples use the same API-backed variant described in 5.2. To simulate latency, delay deliberately. This is the one reasonable use of `time.sleep` in a test: you are simulating the network, not waiting for an unknown condition. In the synchronous API, a blocking handler also stalls Playwright's dispatcher, so treat this as a conceptual pattern; for reliable latency tests, use the async API or a proxy/server that delays responses outside Playwright.

```python
import time

from playwright.sync_api import Page, Route, expect


def test_slow_cards_page(page: Page, quiz_base_url: str) -> None:
    def slow_response(route: Route) -> None:
        time.sleep(1.5)
        route.continue_()

    page.route("**/api/cards", slow_response)
    page.goto(f"{quiz_base_url}/quiz.html")
    expect(page.get_by_test_id("loading")).to_be_visible()
    expect(page.get_by_test_id("question")).to_be_visible(timeout=5_000)
```

For a DNS-like failure at the app boundary:

```python
from playwright.sync_api import Page, Route, expect


def test_unresolvable_api_failure(page: Page, quiz_base_url: str) -> None:
    def dns_failure(route: Route) -> None:
        route.abort(error_code="namenotresolved")

    page.route("**/api/cards", dns_failure)
    page.goto(f"{quiz_base_url}/quiz.html")
    expect(page.get_by_test_id("error-state")).to_be_visible()
```

For offline behavior, `context.set_offline(True)` affects navigations, fetch, XHR, and WebSockets; established WebRTC connections are not stopped. Test an already-loaded offline page:

```python
from playwright.sync_api import BrowserContext, Page, expect


def test_quiz_still_works_offline(page: Page, context: BrowserContext, quiz_base_url: str) -> None:
    page.goto(f"{quiz_base_url}/quiz.html")
    context.set_offline(True)

    page.get_by_role("button", name="Show answer").click()
    expect(page.get_by_test_id("answer")).to_be_visible()
    page.get_by_role("button", name="Next card").click()
    expect(page.get_by_test_id("question")).to_have_text("What is the anchoring effect?")
```

The quiz embeds its data, so this should pass. If it fails, the page depends on a request it claims not to need.

> **QA takeaway:** Test the failure mode, not only the error code. A 500 that leaves a blank screen and a 500 with a recoverable message are different quality outcomes.

## 5.4 Authentication and `storage_state`

Logging in through the UI before every test is slow and couples unrelated tests to login. Save a context's state after one real UI login on an authorized staging environment, then seed other contexts:

```python
# Once, after driving the normal login form and asserting the dashboard:
context.storage_state(path="playwright/.auth/user.json")

# In a fixture for tests that do not test login:
context = browser.new_context(storage_state="playwright/.auth/user.json")
page = context.new_page()
```

The file contains cookies and origin storage and may include session tokens. Keep it out of Git, use a dedicated test account, and never reuse a real user's state. Cookies and local storage are included by default; IndexedDB needs `indexed_db=True`, and session storage needs an explicit workaround.

Test login itself separately: invalid credentials, lockout, expired session, logout, and role-based access. Reusing saved state skips the very behavior a login test exists to check.

> **QA takeaway:** Save state to make feature tests faster. Do not save state to avoid testing authentication.

---

# Part 6: Debugging and Evidence

## 6.1 Headed runs, pause, and Inspector

Run one failing test with a visible browser:

```bash
python -m pytest tests/test_quiz.py::test_reveal_answer_then_go_to_next_card --headed --slowmo=500
```

`--headed` shows the browser; `--slowmo=500` delays operations by 500 ms so you can follow them. Slow motion is diagnostic, not a fix. Add `page.pause()` immediately before the step you want to inspect, then run with `python -m pytest --headed -s`; it pauses and opens the Playwright Inspector.

`PWDEBUG=1` opens the Inspector from the start and disables Playwright's default timeout. Use it locally, never in CI:

```powershell
$env:PWDEBUG=1
python -m pytest -s tests/test_quiz.py
$env:PWDEBUG=$null
```

To record a starting point:

```bash
playwright codegen http://127.0.0.1:8000/quiz.html
```

Use **Pick Locator** to test candidates, then copy the generated Python. Generated code is a draft: improve names, remove noise, add meaningful assertions, and account for test data.

## 6.2 Artifacts and traces

| Option | Values | Meaning |
|---|---|---|
| `--screenshot` | `on`, `off`, `only-on-failure` | Default `off`; capture a screenshot |
| `--video` | `on`, `off`, `retain-on-failure` | Default `off`; keep failed runs |
| `--tracing` | `on`, `off`, `retain-on-failure` | Default `off`; keep failed traces |
| `--full-page-screenshot` | flag | Full page instead of viewport; requires `--screenshot` |
| `--output` | directory | Artifact directory; default `test-results` |

Use `python -m pytest --tracing=retain-on-failure --screenshot=only-on-failure --video=retain-on-failure` in CI. A trace is the strongest evidence: actions, before/after DOM snapshots, network, console, and source. Traces can contain sensitive page content and headers.

Inside a test with the `page` and `context` fixtures, record manually when needed:

```python
context.tracing.start(screenshots=True, snapshots=True, sources=True)
page.goto("http://127.0.0.1:8000/quiz.html")
page.get_by_role("button", name="Show answer").click()
context.tracing.stop(path="trace.zip")
```

Open it with `playwright show-trace trace.zip`. Inspect the failed action, the DOM before and after, console, and network. pytest tracing writes trace files under `test-results/`. `pytest --tracing retain-on-failure` keeps only failures.

## 6.3 Reports and triage

Verbose output plus JUnit XML is enough for many CI systems:

```bash
python -m pytest -v --tb=short --junitxml=test-results/junit.xml
```

`--last-failed`, `-x`, `-k`, and `-m smoke` speed focused debugging. `-s` shows prints and is needed for some Inspector workflows. pytest-html can add a human-readable report, but the failing assertion and trace explain the failure.

Triage in this order: server reachable? test alone? fails headed? trace? locator unique? data changed? only parallel/CI? manually reproducible? A human-reproducible failure is a product bug; otherwise keep separating test, data, and environment causes.

> **QA takeaway:** "Flaky" is not a diagnosis. Record the rate, browser, command, and trace, then classify the cause.

---

# Part 7: Browsers, Parallelism, and CI

## 7.1 Cross-browser and devices

```bash
python -m pytest --browser webkit
python -m pytest --browser chromium --browser firefox --browser webkit
python -m pytest --browser webkit --device="iPhone 13"
```

`--browser` is repeatable; the suite runs once per engine. Device profiles set viewport, user agent, touch, and related parameters. Emulation is not a physical device; keep a small real-device smoke test for critical mobile flows. For one test, `@pytest.mark.browser_context_args(viewport={"width": 390, "height": 844})` sets a phone-sized viewport; for custom contexts, `browser.new_context(**playwright.devices["iPhone 13"])` applies a profile. `locale` and `timezone_id` should be deterministic when formatting or dates affect assertions.

## 7.2 Parallelism and retries

Install `pytest-xdist` and run `python -m pytest --numprocesses auto`. Each worker gets its own browser and contexts. Start with a fixed count if `auto` overloads the machine; Playwright recommends 2 up to the CPU count. Parallelism exposes shared rows, accounts, files, and sessions. Fix the coupling; do not make serial execution the default.

For pytest, install `pytest-rerunfailures`:

```bash
python -m pytest --reruns 2 --reruns-delay 1
```

Per-test marker:

```python
import pytest


@pytest.mark.flaky(reruns=2, reruns_delay=1)
def test_known_unstable_flow(page):
    ...
```

Retries are a mitigation and a measurement tool, not a fix. A test that passes on the third try is hiding a race, collision, or bad locator. Track retry counts and open a bug. Playwright Test's Node-based retries do not apply to pytest.

## 7.3 CI and artifacts

```yaml
name: Flashcards E2E

on:
  push:
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-python@v6
        with:
          python-version: "3.13"
      - run: |
          python -m pip install --upgrade pip
          pip install -r requirements-dev.txt
      - run: python -m playwright install --with-deps chromium
      - run: python -m pytest --browser chromium --tracing=retain-on-failure --screenshot=only-on-failure
      - uses: actions/upload-artifact@v5
        if: ${{ !cancelled() }}
        with:
          name: playwright-artifacts
          path: test-results/
```

Keep browser install and Playwright package versions aligned. CI runs headless by default. `--with-deps` installs Linux libraries.

Split large suites with a CI matrix (files, markers, or groups) or `pytest-xdist` within each job. The Playwright Test runner's `--shard` is not a pytest option. The official Playwright Docker image can preinstall browser dependencies; pin its tag to the same Playwright version.

> **QA takeaway:** CI should tell you what failed and give you evidence. A red build with no trace, browser version, or command is half a signal.

---

# Part 8: Test Design for QA

## 8.1 The test pyramid

```
        Manual exploratory testing
          a few E2E journeys
        integration and API checks
     many unit and static checks
```

Use the cheapest test that catches the risk.

| Level | Good for | Flashcards example |
|---|---|---|
| Unit | Parser rules, validation, duplicates | `--check` with malformed cards |
| Integration/API | Data contract, export, errors | CSV contents, status codes |
| E2E | Critical journey across UI, JS, and data | Reveal, next, offline |
| Manual exploratory | Usability, confusing copy, surprises | Does the deck feel understandable? |

E2E is expensive because it renders layouts and depends on the whole stack. A good E2E test has a real user goal, a meaningful assertion, and a failure that would matter. Test these: first card, reveal, next, last card, empty state, offline, API failure, mobile reachability. Leave CSS colors, internal variables, and every validation branch to lower levels.

## 8.2 Flaky causes and fixes

| Cause | Symptom | Fix |
|---|---|---|
| Fixed sleeps | Passes locally, times out in CI | Use a web-first assertion |
| Ambiguous locator | Strict violation or wrong element | Narrow by role, name, or test ID |
| Shared data/account | Fails in parallel | Create per-test data |
| Animation | Click intercepted or element unstable | Wait for the state; handle animation deliberately |
| Network timing | Intermittent loading failures | Assert visible state; control the network |
| Time zone/locale | Dates and formatting differ | Set context options |
| Test order | Passes alone, fails in suite | Remove shared state |
| Real external dependency | Third-party outage | Mock for UI tests; test integration separately |
| Product race | Passes only with retries | Treat as a product bug |

Do not fix flake by increasing timeouts without understanding the cause.

## 8.3 Isolation, data, and mocking

Create the smallest state each test needs and clean it up. Use a dedicated test account, unique names and emails, fixed locale/time zone when relevant, and seeded or mocked data. Do not depend on yesterday's records or on test order.

Mock external services, flaky third parties, rate limits, and conditions you cannot safely create. Do not mock the feature under test so heavily that the test becomes a unit test wearing a browser costume. Keep at least one contract or integration check against the real implementation.

## 8.4 Accessibility and visual checks

Playwright does not replace an accessibility audit, but good habits help: use real buttons, assert roles and accessible names, test keyboard focus and activation, zoom, and reading order. `data-testid` is invisible to users, so an element with a test ID can still be unusable. Run an automated checker as one input and verify manually with a screen reader.

Screenshots are strong evidence but weak oracles. Pixel comparisons vary by fonts, OS, browser, animation, and dynamic data. The Python API captures screenshots but does not provide built-in screenshot assertions. If you add visual regression tooling, use a fixed environment, mask dynamic regions, review diffs, and own the baselines. Semantic and layout assertions remain the first choice for behavior.

## 8.5 E2E checklist

An E2E test should represent a user-visible risk, run alone and in parallel, control its data, use durable locators and web-first assertions, avoid sleeps, leave useful evidence on failure, and fail if the feature is genuinely broken.

---

# Part 9: The Complete Flashcards Suite

## 9.1 Files and configuration

```
flashcards/
├── quiz.html, requirements-dev.txt, pytest.ini
├── pages/__init__.py, pages/quiz_page.py   # POM from Part 4
├── tests/conftest.py                       # server, expected_cards, quiz_page
├── tests/test_quiz.py
└── test-results/
```

`pytest.ini`:

```ini
[pytest]
testpaths = tests
addopts = -ra --strict-markers
markers =
    smoke: critical path checks
    regression: broader regression checks
```

Playwright options can go in `addopts` (for example, `addopts = --browser=firefox`), but keep local-only `--headed` and `--slowmo` on the command line so a debug preference does not silently change CI.

The full `tests/conftest.py` combines the server fixture and POM fixture from Part 4, plus the expected data fixture. These are ordinary pytest fixtures; no Playwright-specific plugin configuration is needed.

## 9.2 Smoke and content tests

`tests/test_quiz.py`:

```python
import re

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.smoke
def test_quiz_loads(page: Page, quiz_base_url: str) -> None:
    response = page.goto(f"{quiz_base_url}/quiz.html")
    assert response is not None
    assert response.status == 200
    expect(page).to_have_url(re.compile(r"/quiz\.html$"))
    expect(page).to_have_title("Flashcards quiz")
    expect(page.get_by_role("heading", name="Flashcards", exact=True)).to_be_visible()


def test_every_card_shows_question_and_answer(
    page: Page,
    quiz_base_url: str,
    expected_cards: list[tuple[str, str]],
) -> None:
    page.goto(f"{quiz_base_url}/quiz.html")
    for number, (question, answer) in enumerate(expected_cards, start=1):
        expect(page.get_by_test_id("progress")).to_have_text(
            f"Card {number} of {len(expected_cards)}"
        )
        expect(page.get_by_test_id("question")).to_have_text(question)
        page.get_by_role("button", name="Show answer").click()
        expect(page.get_by_test_id("answer")).to_have_text(answer)
        if number < len(expected_cards):
            page.get_by_role("button", name="Next card").click()
```

The expected list duplicates the fixture deck on purpose: UI behavior should be checked against an independent expectation, while unit tests verify that the generator creates the right HTML from `cards.md`.

## 9.3 Interaction and edge-case tests

```python
import pytest
from playwright.sync_api import BrowserContext, Error as PlaywrightError, Page, expect


def test_reveal_and_next(page: Page, quiz_base_url: str) -> None:
    page.goto(f"{quiz_base_url}/quiz.html")
    answer = page.get_by_test_id("answer")
    reveal = page.get_by_role("button", name="Show answer")

    expect(answer).to_be_hidden()
    reveal.click()
    expect(answer).to_be_visible()
    expect(reveal).to_be_hidden()

    page.get_by_role("button", name="Next card").click()
    expect(page.get_by_test_id("question")).to_have_text("What is the anchoring effect?")
    expect(answer).to_be_hidden()


def test_last_card_disables_next(
    page: Page,
    quiz_base_url: str,
    expected_cards: list[tuple[str, str]],
) -> None:
    page.goto(f"{quiz_base_url}/quiz.html")
    next_card = page.get_by_role("button", name="Next card")
    for _ in range(len(expected_cards) - 1):
        next_card.click()

    expect(page.get_by_test_id("progress")).to_have_text(
        f"Card {len(expected_cards)} of {len(expected_cards)}"
    )
    expect(next_card).to_be_disabled()
    expect(page.get_by_test_id("question")).to_have_text(expected_cards[-1][0])


def test_empty_deck_shows_empty_state(page: Page, quiz_base_url: str) -> None:
    page.goto(f"{quiz_base_url}/quiz.html?empty=1")
    expect(page.get_by_test_id("empty-state")).to_have_text("No cards available.")
    expect(page.get_by_test_id("quiz")).to_be_hidden()
    expect(page.get_by_test_id("question")).to_be_hidden()


def test_offline_keeps_embedded_deck_usable(
    page: Page,
    context: BrowserContext,
    quiz_base_url: str,
) -> None:
    page.goto(f"{quiz_base_url}/quiz.html")
    context.set_offline(True)
    page.get_by_role("button", name="Show answer").click()
    expect(page.get_by_test_id("answer")).to_be_visible()


def test_failed_document_does_not_leave_half_a_quiz(page: Page, quiz_base_url: str) -> None:
    page.route("**/quiz.html", lambda route: route.abort(error_code="connectionrefused"))
    with pytest.raises(PlaywrightError):
        page.goto(f"{quiz_base_url}/quiz.html")
    expect(page.get_by_test_id("quiz")).to_have_count(0)
```

Malformed cards are rejected by `--check` and covered by parser unit tests; the UI edge cases here are the empty deck and a failed document. The last test proves a failed navigation is surfaced, not that the server's error page is helpful. If the quiz fetches cards from an API, mock that endpoint and assert the user-visible error and recovery path.

## 9.4 POM refactor and mobile viewport

```python
from playwright.sync_api import expect

from pages.quiz_page import FlashcardsQuizPage


def test_pom_reveal_and_next(quiz_page: FlashcardsQuizPage) -> None:
    quiz_page.goto()
    expect(quiz_page.question).to_have_text("What is confirmation bias?")
    quiz_page.show_answer()
    expect(quiz_page.answer).to_be_visible()
    quiz_page.next_card()
    expect(quiz_page.question).to_have_text("What is the anchoring effect?")
```

POM does not replace the edge-case and network tests; it removes repetition from the common journey. Add the mobile check from Part 7:

```python
import pytest
from playwright.sync_api import Page, expect


@pytest.mark.browser_context_args(viewport={"width": 390, "height": 844})
def test_mobile_controls_are_reachable(page: Page, quiz_base_url: str) -> None:
    page.goto(f"{quiz_base_url}/quiz.html")
    expect(page.get_by_role("button", name="Show answer")).to_be_in_viewport()
    expect(page.get_by_role("button", name="Next card")).to_be_in_viewport()
```

This catches basic overflow and off-screen controls, not touch ergonomics or real-device rendering.

## 9.5 Run the suite

```bash
python -m pytest -v
python -m pytest -m smoke
python -m pytest --numprocesses auto
```

The suite should pass without a manually started server, in any order, alone, and in parallel. If you can do all four, the structure is doing its job. The CI workflow from Part 7 is the final piece.

> **QA takeaway:** Grow E2E coverage from user risks, not from a wish to automate every click. A small suite with clear failures beats a large suite nobody trusts.

---

# Part 10: Labs

These labs use the local quiz and your own machine. Do not point interception, authentication tests, or destructive actions at systems you do not own.

## Lab 1 — Read a failure (15 min)

**Goal:** See what a useful failure contains. Change the expected first question to something that does not exist, run `python -m pytest tests/test_quiz.py -k loads -v`, and read the locator, received text, and timeout. Restore it.

**Observe:** Playwright reports the locator, action, elapsed time, and page state. **QA takeaway:** Read evidence before editing. A timeout on the wrong locator is a test bug; a missing card is a product bug.

## Lab 2 — Strict-mode detective (15 min)

**Goal:** Experience strict mode. Add a temporary test running `page.get_by_role("button").click()`, run it, then fix it with the named Show answer button. Try `nth(0)` and explain why the named locator is safer. **Observe:** The broad locator matches two buttons. **QA takeaway:** Ambiguity is information; narrow the locator.

## Lab 3 — Delay without a sleep (20 min)

**Goal:** Separate network simulation from readiness. Route `**/quiz.html` through a handler that sleeps one second, then calls `route.continue_()`. Assert the question text, run the test, then remove the route. **Observe:** The test takes about a second longer but contains no fixed wait for readiness. **QA takeaway:** Latency belongs in simulation; readiness belongs in assertions.

## Lab 4 — Break the document (15 min)

**Goal:** Compare an app error with a navigation failure. Fulfill `**/quiz.html` with status 500 and a body, run a test expecting the heading, then switch to `route.abort(error_code="connectionrefused")`. **Observe:** The 500 body renders; the abort raises a Playwright error before the app exists. **QA takeaway:** Report which layer failed.

## Lab 5 — Offline study (15 min)

**Goal:** Verify the offline promise. Load the quiz, call `context.set_offline(True)`, reveal an answer and go next. **Observe:** The embedded deck continues. **QA takeaway:** Test both loaded-offline and initial-load-offline paths.

## Lab 6 — Cross-browser and mobile (20 min)

**Goal:** Compare engines. Run `python -m pytest --browser webkit --device="iPhone 13"`, then Chromium and Firefox. Take `page.screenshot(path="test-results/mobile.png", full_page=True)` and test keyboard focus. **Observe:** Rendering, user agent, touch, and APIs can differ. **QA takeaway:** Emulation is not a physical device.

## Lab 7 — Trace a failure (20 min)

**Goal:** Use evidence. Break an expectation, run `python -m pytest --tracing=retain-on-failure`, find the trace under `test-results/`, open it with `playwright show-trace <path>`, and inspect the failed action, DOM, console, and network. Fix the test. **Observe:** The trace shows the page at failure time. **QA takeaway:** Attach traces or their essentials to E2E bugs.

## Lab 8 — Prove context isolation (15 min)

**Goal:** See why shared pages are dangerous. In test A, set `localStorage` with `page.evaluate("localStorage.setItem('qa-marker', 'leaked')")`. In test B, navigate and read the key. Run in both orders. **Observe:** Test B gets `None`. **QA takeaway:** Fresh contexts remove a class of order-dependent failures.

## Lab 9 — CI rehearsal (20 min)

**Goal:** Run as CI will. Run with `--tracing=retain-on-failure --screenshot=only-on-failure`, break an assertion, inspect `test-results/`, then fix it and add the workflow from Part 7 in a branch. **Observe:** Headless runs still produce evidence. **QA takeaway:** A suite that needs a visible browser and manual server is not CI-ready.

---

# Appendices

## Appendix A: Cheat sheet

### Setup and run

```bash
python -m venv .venv
# Windows: .\.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install pytest-playwright
python -m playwright install
python -m playwright install chromium firefox webkit
python -m playwright install --with-deps chromium   # Linux CI
python -m pytest
python -m pytest -m smoke
python -m pytest --headed --slowmo=500
python -m pytest --browser webkit --device="iPhone 13"
python -m pytest --numprocesses auto
python -m pytest --tracing=retain-on-failure --screenshot=only-on-failure
playwright codegen http://127.0.0.1:8000/quiz.html
playwright show-trace trace.zip
```

```powershell
$env:PWDEBUG=1
python -m pytest -s tests/test_quiz.py
$env:PWDEBUG=$null
```

### Fixtures

`page` and `context` are function-scoped; `browser`, `browser_name`, and `playwright` are session-scoped; `new_context` is a function-scoped factory for extra contexts.

### Locators and assertions

```python
page.get_by_role("button", name="Show answer")
page.get_by_label("Email")
page.get_by_text("No cards available.")
page.get_by_test_id("answer")
page.get_by_test_id("quiz").get_by_role("button", name="Next card")
locator.filter(has_text="Anchoring")
locator.nth(0)

expect(locator).to_be_visible()
expect(locator).to_be_hidden()
expect(locator).to_be_enabled()
expect(locator).to_be_disabled()
expect(locator).to_have_text("Card 1 of 3")
expect(locator).to_contain_text("confirmation")
expect(locator).to_have_count(2)
expect(page).to_have_url(re.compile(r"/quiz\.html$"))
```

Assertion timeout: 5 s; action/navigation timeout: 30 s.

### Routes

| Call | Meaning |
|---|---|
| `page.route(pattern, handler)` | Intercept this page |
| `context.route(pattern, handler)` | Intercept all context pages |
| `route.continue_()` | Send to network |
| `route.fulfill(status=..., json=...)` | Return fake response |
| `route.abort(error_code="namenotresolved")` | Fail request |
| `route.fallback()` / `route.fetch()` | Next handler / real request |
| `page.unroute(pattern)` | Remove route |

### Markers and common errors

```python
@pytest.mark.smoke
@pytest.mark.skip_browser("firefox")
@pytest.mark.flaky(reruns=2, reruns_delay=1)
def test_resilient_smoke(): pass

@pytest.mark.parametrize("value", ["a", "b"])
def test_values(value): pass

@pytest.mark.browser_context_args(viewport={"width": 390, "height": 844})
def test_mobile(): pass
```

| Symptom | Likely cause | Fix |
|---|---|---|
| `Fixture "page" not found` | Plugin missing | Activate venv; install `pytest-playwright` |
| `Executable doesn't exist` | Browser missing | `python -m playwright install` |
| `ERR_CONNECTION_REFUSED` | Server/port wrong | Start the server; check URL |
| Strict mode violation | Locator matches several | Narrow by role/name/test ID |
| Timeout waiting for locator | Missing, hidden, or wrong | Inspect trace and page state |
| Timeout 5000ms exceeded | Assertion never true | Inspect actual value |
| Passes alone, fails parallel | Shared data | Isolate data |
| Hangs in CI | PWDEBUG or pause | Remove debug settings |

## Appendix B: Glossary

| Term | Definition |
|---|---|
| **Actionability** | Checks before an action: attached, visible, stable, enabled, able to receive events |
| **Auto-waiting** | Built-in waiting for actions and assertions instead of fixed sleeps |
| **Browser context** | Isolated profile with its own cookies, storage, and permissions |
| **E2E test** | Test of a user journey across the real application layers |
| **Flaky test** | Test that passes and fails without a product change |
| **Locator** | Lazy query that finds elements and retries when used |
| **POM** | Page Object Model; class centralizing a page's locators and actions |
| **Route** | Intercepted request that can be continued, fulfilled, or aborted |
| **Sharding** | Splitting a suite across machines/jobs; for pytest, usually a CI matrix |
| **Strict mode** | Single-element action throws when multiple elements match |
| **Test ID** | Stable attribute such as `data-testid` for test targeting |
| **Trace** | Timeline of actions, DOM snapshots, network, and console |
| **Web-first assertion** | Assertion that retries until the UI condition is met |
| **`storage_state`** | Saved cookies and origin storage used to seed a context |

## Appendix C: Quiz

1. Which three engines does Playwright support?
2. What is the difference between a browser and a context?
3. Why a fresh context per test?
4. What does auto-waiting check before a click?
5. Why is `time.sleep` a poor synchronization tool?
6. What happens when a locator matches two buttons and you click?
7. When prefer role over test ID?
8. Default timeout for a web-first assertion?
9. Which flag shows the browser?
10. How do you open a trace?
11. Difference between `continue_`, `fulfill`, and `abort`?
12. What does `storage_state` save and why is it sensitive?
13. When reuse auth state, and when test login?
14. API for offline mode?
15. When is POM useful or overkill?
16. What does `--numprocesses auto` do?
17. Why can retries hide a flaky suite?
18. What should CI upload on failure?
19. Why is a screenshot not a complete visual strategy?
20. Four categories for triaging an E2E flake?

### Answers

1. Chromium, Firefox, WebKit.
2. Browser is the process; context is an isolated profile inside it.
3. Fresh cookies, storage, and data prevent order dependence.
4. Attached, visible, stable, enabled, and able to receive the action.
5. It guesses a duration and does not observe the needed condition.
6. It raises a strict-mode violation.
7. Roles when accessibility semantics are the real contract; test IDs for dynamic content without a stable role/name.
8. Five seconds.
9. `--headed`.
10. `playwright show-trace trace.zip`.
11. Continue sends to network; fulfill returns a synthetic response; abort fails the request.
12. Cookies and origin storage, possibly session tokens; never commit it.
13. Reuse for unrelated feature tests; test login for invalid, expired, locked, and logout flows.
14. `context.set_offline(True)`.
15. Useful with shared actions/selectors; overkill for one test, a prototype, or a wrapper around every node.
16. Runs tests in parallel with pytest-xdist.
17. Retries can turn a race or data collision green without fixing it.
18. Trace, screenshot/video, logs, browser version, command.
19. Pixels vary by environment and dynamic data; baselines need ownership and review.
20. Application, test code, test data, environment/infrastructure.

## Appendix D: Bug report template for E2E and flaky failures

```markdown
## Summary
[Which user journey fails, in which environment, and how often.]

## Environment
- Application version / commit:
- Test repository branch / commit:
- Python / pytest / pytest-playwright / Playwright versions:
- Browser engine and version:
- Device, viewport, headless or headed:
- OS / CI runner:
- Test command:
- Test file and line:

## Preconditions
- Test account:
- Test data:
- Feature flags:
- Network conditions:

## Steps to reproduce
1.
2.
3.

## Expected
[What a user should see or do.]

## Actual
[What happened. Include the exact assertion or locator error.]

## Evidence
- Trace path or attachment:
- Screenshot / video:
- Console error:
- Failed request and status:
- First known failure / last known pass:

## Reproducibility
- Runs alone: yes / no / not tested
- Runs with the full suite: yes / no / not tested
- Headed: yes / no / not tested
- Parallel workers: yes / no / not tested
- Pass rate: X/Y attempts

## Classification
- Application bug / test bug / test data / environment / unknown
- Why:

## Impact
[Which users, flows, or release decisions are affected.]
```

Never write only "flaky test." Include the pass rate, whether it reproduces alone, the trace, and the browser. Separate the product defect from the test defect in the title if both exist.

## Appendix E: Running a knowledge-sharing session

A 75-minute session for beginners. Keep the live demo short and the trace review generous.

| Time | Topic | Activity |
|---|---|---|
| 5 min | Why browser tests matter | Show a failure a unit test cannot see |
| 10 min | What Playwright is | Browser → context → page; compare tools |
| 10 min | First test | Run the quiz smoke test; read output |
| 10 min | Locators and strict mode | Break a broad locator, fix it |
| 10 min | Auto-waiting | Replace a sleep with `expect` |
| 10 min | Network conditions | 500, abort, offline |
| 10 min | Debugging | Step through a pre-recorded trace |
| 5 min | POM and test design | Refactor one test; discuss E2E scope |
| 5 min | CI and Q&A | Show artifacts; assign one lab |

**Demo checklist:** venv activated; quiz fixture available; all engines installed; a pre-recorded failing trace; a redacted auth state or local fake login; a sample bug report.

**Discussion prompts:** Where do you look when a click does nothing? What causes pass-alone/fail-parallel? Would you automate this check? A test passed on retry — is the release ready? What makes this selector durable?

## Appendix F: Resources and what to learn next

**Official references**

- Playwright Python docs: https://playwright.dev/python/docs/intro
- Locators: https://playwright.dev/python/docs/locators
- Assertions: https://playwright.dev/python/docs/test-assertions
- Pytest plugin: https://playwright.dev/python/docs/test-runners
- Network: https://playwright.dev/python/docs/network
- Authentication: https://playwright.dev/python/docs/auth
- Debugging: https://playwright.dev/python/docs/debug
- Trace Viewer: https://playwright.dev/python/docs/trace-viewer
- Emulation: https://playwright.dev/python/docs/emulation
- CI: https://playwright.dev/python/docs/ci
- API reference: https://playwright.dev/python/docs/api/class-playwright

**Supporting references**

- pytest: https://docs.pytest.org/
- pytest-xdist: https://pytest-xdist.readthedocs.io/
- pytest-rerunfailures: https://github.com/pytest-dev/pytest-rerunfailures
- MDN Web Docs: https://developer.mozilla.org/
- W3C WAI: https://www.w3.org/WAI/
- web.dev accessibility: https://web.dev/learn/accessibility/

**What to learn next:** TypeScript/JavaScript Playwright; API testing; accessibility with axe and manual checks; visual regression in a fixed container; Docker and CI sharding; browser performance APIs; security testing with explicit authorization.

---

## A final word

Browser automation is not valuable because it clicks buttons. It is valuable because it turns a user promise into repeatable evidence: the first card appears, the answer is revealed, the next card is different, and the deck survives a lost network.

Install the tools, run one failing test, open its trace, and explain what the user saw. Then make the next test independent, the locator more meaningful, and the failure report easier for someone else to act on. That habit transfers from Python to TypeScript, and from flashcards to whatever product you test next.
