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
