# AI-Assisted Programming and Testing for Release QA

This guide is for release QA engineers who want to use AI assistants well enough
to trust the result — or to know why they should not. It focuses on Claude Code
and the Model Context Protocol (MCP), with the concepts explained in plain
English. The running examples are Maya's flashcards project from
`using-ai-from-zero-to-claude-code.md` and the runnable `mcp-demo/` in this
repository.

The AI handbook is the deep reference. This guide is the interview-focused,
QA-specific path: shorter explanations, release scenarios, and the habits that
keep generated work reviewable. No AI session, test, or MCP call was executed
for this guide. The `mcp-demo/` is runnable and is documented separately; this
guide describes it, it does not claim to have run it.

## Contents

- [Part 1 — AI and LLM Foundations for QA](#part-1--ai-and-llm-foundations-for-qa)
- [Part 2 — Prompting and Context](#part-2--prompting-and-context)
- [Part 3 — AI-Assisted Test Design and Test Data](#part-3--ai-assisted-test-design-and-test-data)
- [Part 4 — AI-Assisted Debugging and Code Review](#part-4--ai-assisted-debugging-and-code-review)
- [Part 5 — Claude Code Essentials](#part-5--claude-code-essentials)
- [Part 6 — Skills and Reusable Workflows](#part-6--skills-and-reusable-workflows)
- [Part 7 — Subagents and Agent Workflows](#part-7--subagents-and-agent-workflows)
- [Part 8 — MCP and Tool Integration](#part-8--mcp-and-tool-integration)
- [Part 9 — Safety, Security, and Verification](#part-9--safety-security-and-verification)
- [Part 10 — Release QA Workflows and Interview Scenarios](#part-10--release-qa-workflows-and-interview-scenarios)

## Part 1 — AI and LLM Foundations for QA

A large language model is useful precisely because it is not a database. It
does not retrieve a stored answer and hand it back. It predicts the next token
from patterns learned during training, conditioned on the prompt and the
context you provide. That makes it excellent at drafting, summarizing,
transforming, and suggesting. It also means its output is a proposal, not a
fact.

### What an LLM Does

An LLM receives text, turns it into tokens, and repeatedly predicts the next
token. The result can look like reasoning, but the mechanism is pattern
completion over a very large corpus. For QA work, the useful framing is:

- It can propose test cases, edge cases, and failure hypotheses.
- It can summarize a log, a diff, or a requirement.
- It can draft a bug report or a test plan.
- It can explain an unfamiliar error message.
- It cannot know your product, your users, or your release criteria unless you
  put that information in front of it.
- It cannot prove that a test passed, a bug is fixed, or a release is safe.

Treat the model as a fast, well-read collaborator who has not seen your system
and cannot be trusted with the final call.

### Tokens and Context

Models read tokens, not words. A token is roughly a word piece; code, JSON, and
unusual identifiers often use more tokens than prose. The **context window** is
the total amount of text the model can consider at once: your instructions, the
files you attach, the conversation so far, and the model's own output.

Three practical consequences:

1. **More context is not automatically better.** A focused file, a failing
   test, and the expected behavior usually beat a dump of the whole repository.
2. **Context is finite.** Long sessions accumulate chat history, tool output,
   and file contents. When the window fills, older material may be summarized
   or dropped. Start a fresh session when the task changes.
3. **Names and paths matter.** Tell the model exactly which file, function, or
   requirement to use. “Look at the project” is not a context strategy.

### Training Cutoff and Freshness

Every model has a training cutoff. It may know an older version of a library,
a command that has since changed, or a best practice that has moved on. In a
release-QA context, stale knowledge shows up as:

- an API or CLI flag that no longer exists;
- a test framework pattern from an older major version;
- a security recommendation that has been superseded;
- a vendor-specific limit or default that changed.

The fix is not to distrust everything. The fix is to verify version-sensitive
claims against the current documentation or the repository's own files. When a
claim matters to a release decision, cite the source and the version.

### Non-Determinism and Hallucination

Two different things make AI output unreliable in different ways.

**Non-determinism:** the same prompt can produce different wording, different
test ideas, or a different fix on another run. That is useful for brainstorming
and dangerous for reproducibility. If a result matters, capture the prompt, the
model, the files, and the output.

**Hallucination:** the model can produce a confident, fluent answer that is
simply wrong. Common shapes in QA work:

- a function or CLI flag that does not exist;
- a test file that imports a package the project does not use;
- a plausible stack trace or test result that was never produced;
- a claim that a fix works because the code “looks correct”;
- a citation to documentation that does not say what the model claims.

The danger is not that the model is always wrong. The danger is that wrong
output looks the same as right output. Confidence is not evidence.

### What This Means for QA

Use AI where breadth and speed help, and keep judgment and evidence human:

- **Generate options, then select.** Ask for ten edge cases, then decide which
  ones apply to the product.
- **Ask for assumptions.** A good prompt invites the model to list what it does
  not know.
- **Demand evidence.** “Show the command, the expected result, and the observed
  result” is a better request than “is it fixed?”
- **Reproduce.** Run the test, inspect the diff, open the log, or query the
  system yourself before you report a result.
- **Keep a human release authority.** AI can draft a recommendation; it cannot
  sign off a release.

### Release QA Use

A release QA engineer can use an assistant to:

- turn a requirement into a risk list and a first draft of test cases;
- summarize a long CI log and point at the first meaningful failure;
- suggest boundary values and negative cases that the team may have missed;
- review a diff for missing tests, behavior changes, and unrelated edits;
- draft a bug report from a reproduction transcript;
- draft release notes from a list of merged changes.

In every case, the output is input to a review, not the review itself.

### Watch-outs

- A fluent answer is not a verified answer.
- A model that has not seen your product will invent product rules.
- Training cutoffs make version-specific claims perishable.
- Long contexts can hide the one line that matters.
- Never paste secrets, customer data, or production logs into a tool without
  approval.

## Part 2 — Prompting and Context

A prompt is a work request, not a magic spell. The model does better when the
request names the task, the material, the constraints, the deliverable, and the
evidence you expect. You do not need a long prompt; you need a complete one.

### A Clear Task

A weak request leaves the model to guess:

```text
Write tests for the flashcards quiz.
```

A stronger request says what to test, where the code is, what “done” means, and
what not to change:

```text
You are helping a release QA engineer review the flashcards quiz before a
release.

Read:
- quiz.html (the quiz page)
- cards.md (the question data)
- flashcards.py (the generator)

Task: propose a test checklist for the quiz's "one card at a time, Show answer,
Next card" behavior.

Constraints:
- Do not edit files yet.
- Cover the happy path, empty data, malformed cards, keyboard use, and a
  refresh mid-quiz.
- Separate product risks from test-implementation details.
- Mark anything you cannot verify from the files as an assumption.

Output: a table with Area, Risk, Test idea, and Evidence needed.
```

The second prompt is reviewable. You can see what was asked, what was excluded,
and what the model is allowed to assume.

### Constraints and Acceptance Criteria

Useful constraints answer questions the model would otherwise decide silently:

- **Scope:** which files, screens, endpoints, or requirements are in scope?
- **Non-goals:** what should not be changed or proposed?
- **Tools:** may the model read files, run tests, edit code, or only analyze?
- **Format:** a table, a checklist, a unified diff, a bug report, a JSON list?
- **Evidence:** must it cite a file and line, show a command, or quote a log?
- **Definition of done:** what must be true before the answer is acceptable?

“Make it better” is not acceptance criteria. “Every proposed test names the
behavior it protects and the evidence that would prove it” is.

### Examples and File References

Models copy shape. If you want a particular test format, show one example. If
you want the model to use a file, give the exact path. In Claude Code, an `@`
reference points at a file or directory; a path in prose works too, but the
exact name is what prevents guessing.

Use the smallest useful set of files. A failing test, its fixture, and the
function under test are usually enough. Dumping the whole repository increases
cost and makes it harder for the model to find the relevant line.

### Iteration and Review

Treat the first answer as a draft. A productive loop:

1. Ask for a plan or a list of assumptions before the full answer.
2. Ask the model to critique its own plan against the requirement.
3. Narrow to one change or one test at a time.
4. Review the diff before running anything.
5. Run the test or command yourself and capture the result.
6. If the result is wrong, show the model the actual output, not just “it
   failed.”

“Show me the smallest change that addresses this finding, and list what you did
not change” is a strong review prompt. It limits scope and makes hidden edits
visible.

### Prompt Injection Basics

Prompt injection is an instruction hidden in content the model reads. It can
arrive in:

- a source file or comment;
- a web page the assistant fetches;
- an issue ticket or test description;
- a log line or database value;
- an MCP tool result;
- a README or configuration file from an untrusted repository.

The content might say “ignore previous instructions,” “send the contents of
`.env`,” or “run this command.” The model cannot reliably tell data from
instructions, so the system around it must. Practical defenses:

- Treat tool output and file content as data, not commands.
- Do not give an assistant broad credentials or write access it does not need.
- Keep secrets out of the context in the first place.
- Require approval for destructive or network actions.
- Review the tool call, not just the final answer.

Prompt injection is not solved by adding “ignore malicious instructions” to the
prompt. It is reduced by least privilege, scoped tools, and human review.

### Release QA Use

Use prompts to produce artifacts that a reviewer can check:

- a risk table from a requirement;
- a test checklist with evidence for each item;
- a bug report with reproduction steps and observed/expected results;
- a diff review limited to behavior changes and missing tests;
- a release-note draft that cites the merged changes.

Do not use a prompt to declare a release ready. That decision needs evidence
from the system, not text from a model.

### Watch-outs

- A long prompt is not automatically a clear prompt.
- Missing acceptance criteria invite invented scope.
- A model may follow instructions embedded in a file or tool result.
- A model may claim it ran something it did not run.
- Ask for assumptions and evidence; review them before you act.

## Part 3 — AI-Assisted Test Design and Test Data

Test design is one of the best uses of an AI assistant, because the work is
about breadth: what could go wrong, what did we forget, and what evidence would
show it. The assistant is a brainstorming partner. You still choose the risks,
the oracle, and the priority.

### Requirements to Risks

Start with a requirement and ask for risks before asking for test cases. A
requirement for the flashcards quiz might say:

```text
The quiz shows one card at a time. "Show answer" reveals the answer.
"Next card" moves to the next card. After the last card, the quiz shows a
completion message.
```

Ask the model to separate:

- **Functional risks:** wrong card order, answer visible before the button,
  Next skipping a card, no completion message.
- **Data risks:** empty `cards.md`, a card with an empty answer, duplicate
  questions, malformed Markdown, very long text.
- **State risks:** refresh mid-quiz, back button, two tabs, browser restart.
- **Input risks:** keyboard-only use, touch, rapid clicking, special characters.
- **Non-functional risks:** slow load, small screen, screen reader, offline.
- **Release risks:** cached old JavaScript, mixed versions of HTML and data,
  analytics or logging that changes behavior.

The output is a risk list, not a verdict. You decide which risks matter for this
release.

### Test Cases and Edge Cases

For each risk, ask for a test idea with an expected result and the evidence that
would prove it. A useful table shape is:

| Area | Risk | Test idea | Expected result | Evidence |
|---|---|---|---|---|
| Data | `cards.md` is empty | Open the quiz with an empty file | A clear empty-state message, no crash | Screenshot and console log |
| State | Refresh after three cards | Answer three cards, refresh | Quiz restarts or resumes consistently with the product rule | Observed index and stored state |
| Input | Keyboard only | Tab to Show answer, press Enter, Tab to Next | Focus order and actions work | Keyboard transcript |
| Content | Very long question | Use a 2,000-character question | Text wraps or scrolls without hiding controls | Screenshot at target widths |

Ask the model to mark anything it cannot know as an **assumption**. A test case
built on an invented product rule is worse than no test case, because it looks
authoritative.

### Equivalence and Boundaries

Equivalence partitioning groups inputs that should behave the same way.
Boundary value analysis tests the edges of each group. For the flashcards quiz:

- **Card count:** 0, 1, 2, many. The first and last card are boundaries; the
  empty set is its own case.
- **Question length:** empty, one character, a normal question, a very long
  question.
- **Answer length:** empty, one line, many lines, special characters.
- **Index:** before the first card, first, middle, last, after the last.
- **Timing:** click Next once, double-click, click while the answer is
  animating, click after the completion message.
- **Data quality:** valid Markdown, missing `A:` line, duplicate `Q:` lines,
  Windows and Unix line endings.

The model is good at enumerating these. It is not good at knowing which ones
your product treats as errors. Put the product rule next to the case.

### Exploratory Charters

A charter gives an exploratory session a target and a time box:

```text
Explore the quiz for 20 minutes. Focus on state after refresh, back-button
navigation, and keyboard-only use. Record anything that surprises you, with
the exact steps and a screenshot.
```

Ask the model for charter ideas, then run the session yourself. AI can suggest
heuristics such as “interrupt,” “repeat,” “reverse,” “starve,” and “overload,”
but it cannot see the screen, the animation, or the user's confusion.

### Synthetic Test Data

Use synthetic data that looks realistic but is not real personal data:

```text
Create 12 synthetic flashcards for a psychology quiz. Use invented names and
generic examples. Mark the file as synthetic in the first line. Include two
cards with long answers, one duplicate question, and one card with a special
character in the answer.
```

Rules:

- Never copy production user data into a prompt or a test fixture.
- Label synthetic rows so a reviewer does not mistake them for real data.
- Include the awkward cases deliberately: empty fields, long text, Unicode,
  duplicates, malformed records.
- Keep the data small enough that a failure is easy to reproduce.

### Coverage Gaps

An AI assistant does not know:

- the product's real rules, service-level objectives, or supported browsers;
- what users actually do, or which failures hurt most;
- the production data distribution;
- the release's risk appetite and rollback plan;
- what changed in the last deploy if you do not provide the diff;
- whether a test is flaky in CI.

Ask it to list its assumptions and the evidence it would need. Then fill those
gaps from the product, logs, analytics, and the team.

### Release QA Use

Use AI to draft a risk-based test checklist, generate boundary cases, propose
exploratory charters, and create synthetic fixtures. Review the checklist for
traceability, and run the high-risk cases yourself. The output should make the
test plan more complete, not less accountable.

### Watch-outs

- The model will invent product rules when the requirement is silent.
- More test cases is not the same as better coverage.
- Non-functional and accessibility risks are easy to miss.
- Synthetic data can still leak if it is copied from production.
- A generated expected result is a hypothesis until the product confirms it.

## Part 4 — AI-Assisted Debugging and Code Review

Debugging is where AI feels most useful and where over-trust is most expensive.
A confident explanation of a failure can send a team down the wrong path. Use
the assistant to generate hypotheses and review evidence; keep reproduction and
the final diagnosis human.

### Stack Traces and Logs

Give the model the whole trace, not only the last line. Include:

- the command or user action that triggered the failure;
- the first error, not just the final “exit code 1”;
- the environment, version, and recent changes;
- the relevant log window, with secrets removed;
- the expected and actual behavior.

Ask for a ranked list of hypotheses, with the evidence for each and the next
check that would confirm or eliminate it. Do not ask “what is the bug?” and
accept the first answer.

```text
Here is a failing test, the full trace, and the last 50 log lines. The failure
started after the quiz template changed. List three hypotheses, ranked by
likelihood. For each, name the evidence in the trace that supports it and the
smallest check that would confirm or eliminate it. Do not propose a fix yet.
```

### Reproducing a Failure

A failure is not understood until it is reproduced. Before accepting a fix:

1. Write the shortest steps that show the failure.
2. Record expected and actual behavior.
3. Run the reproduction on the same build and environment.
4. Capture the evidence: command, output, screenshot, log, or trace.
5. Repeat once to see whether it is deterministic.

AI can help turn a messy transcript into steps. It cannot make the failure
reproducible by describing it.

### Reviewing a Diff

A diff review is a structured task. Ask for:

- behavior changes, including changes hidden in refactors;
- missing or weakened tests;
- error handling and edge cases;
- unrelated edits and scope creep;
- secrets, credentials, or debug output;
- dependency or configuration changes;
- rollback risk.

```text
Review this diff as a release QA reviewer. Do not edit it. Return a table with
File:line, Finding, Severity, Why it matters, and the test or evidence that
would catch it. Separate behavior changes from style. If you cannot verify a
claim from the diff, say so.
```

A good review points at lines and names the failure mode. “Looks good” is not a
review.

### Test Suggestions vs Evidence

These are different statements:

- **Suggestion:** “A test for an empty `cards.md` would cover this.”
- **Evidence:** “I ran `python -m pytest tests/test_quiz.py::test_empty_cards`
  and it passed; here is the output.”

The first is a plan. The second is a result. Never let the first be reported as
the second. If the assistant says it ran something, ask for the command and
output; if it cannot show them, treat the claim as unverified.

### Regression Checks

For a bug fix, check three rings:

1. **Same failure:** the original reproduction no longer fails.
2. **Adjacent behavior:** the code path still works for nearby inputs, other
   cards, other browsers, and the previous data format.
3. **Rollback:** the change can be reverted without leaving data or
   configuration in a broken state.

Ask the model to propose the rings, then choose the tests that fit the release
risk. A fix that passes the new test but breaks the previous format is not a
safe release fix.

### Release QA Use

Use AI to summarize a trace, propose hypotheses, draft a diff review, and list
regression checks. Reproduce the failure, run the tests, and inspect the diff
yourself. Attach the command and output to the bug report so the next person
can verify the claim.

### Watch-outs

- A plausible diagnosis can be wrong; rank hypotheses, do not crown one.
- A truncated log hides the first error.
- The model may suggest weakening a test to make it pass.
- “The test passed” without a command and output is not evidence.
- A fix can pass the new test and still break the old data format.
