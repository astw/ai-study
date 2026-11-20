# AI-Assisted Programming and Testing — Topic 5 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add `release-qa-interview/topic-05-ai-assisted-testing/` with a ten-part, Claude Code + MCP-focused guide, 100 Q&A, 150 MCQs, and a README for junior-to-mid release QA interviews.

**Architecture:** Four Markdown deliverables. The guide explains AI-assisted programming and testing in practical QA terms, using the handbook's flashcards project and the repository's verified `mcp-demo/`. The question banks reuse the guide's part titles and terminology. Python 3 structural checkers are the test suite; no AI session, test, or MCP call is executed for this pack.

**Tech Stack:** Markdown, Python 3 standard library, Claude Code/MCP documentation from the repository and current official docs.

**Spec:** `docs/superpowers/specs/2026-11-19-release-qa-interview-topic-05-design.md`

## Global Constraints

- Branch: `release-qa-interview-topic-05`, created from `release-qa-interview-topic-04` at `8e8a981`; topic 4 is pushed but topic 5 stacks locally on it.
- Folder: `release-qa-interview/topic-05-ai-assisted-testing/`.
- Files: `ai-assisted-testing.md`, `qa-100.md`, `mcq-150.md`, `README.md`.
- Primary tools: Claude Code and MCP. The AI handbook (`using-ai-from-zero-to-claude-code.md`) is the deep reference; do not duplicate its full content.
- Q&A counts by part: 8, 9, 12, 10, 10, 9, 9, 10, 10, 13 = 100.
- MCQ counts by part: 12, 15, 17, 15, 15, 14, 14, 15, 15, 18 = 150.
- MCQ format: four options A–D, exactly one `**Correct answer: X.**` line, one `<details>` block per item.
- Q&A format: `#### QN.` plus one `<details><summary>Show answer</summary>` block.
- Answer letters target 37–38 each across the 150 MCQs.
- At least 60 of 150 MCQ stems are scenarios.
- No exact or number-insensitive duplicate stems across both banks.
- Every guide part ends with `### Release QA Use` and `### Watch-outs`.
- Code fences are balanced; use ` ```text ` for prompts/commands that are not shell, and ` ```bash ` for shell commands.
- Use current Claude Code terminology: `CLAUDE.md`, skills (`SKILL.md`), slash commands, subagents (`.claude/agents/`), hooks, MCP servers, tools, resources, prompts.
- Use the MCP demo's exact names: `flashcards-db`, `search_cards(query, limit=5)`, `add_card(question, answer, source="")`, `mcp.server.mcpserver.MCPServer`, `claude mcp add`, `/mcp`.
- Never claim this pack executed an AI session, a test, or an MCP call. The `mcp-demo/` is runnable and was verified in the repository; describe it, do not re-run it as proof.
- No secrets, credentials, real user data, or invented tool flags.
- Commit after each task. End commit messages with the repository's required attribution line.

## Source Contract

Every implementer reads these and uses their terminology verbatim:

- `using-ai-from-zero-to-claude-code.md`:
  - Part 3: Claude Code basics, `CLAUDE.md`, permissions.
  - 4.1–4.2: plan mode, reviewing changes.
  - 4.3: skills, `SKILL.md`, progressive disclosure, slash commands vs skills.
  - 4.4: subagents, agent files, tool restrictions.
  - 4.5: hooks, MCP, the local flashcards demo, plugins.
  - Appendix C: skill and subagent templates.
- `mcp-demo/README.md`, `mcp-demo/server.py`, `mcp-demo/smoke_test.py`:
  - two tools; stdio; SQLite; no credentials; MCP Python SDK 2.x.
- `playwright-for-qa.md` only for the flashcards/quiz contract if an example needs it; do not re-teach Playwright.

The guide uses three running examples:

1. **Flashcards project:** `cards.md`, `flashcards.py`, `quiz.html`, `.claude/` skills/agents. Teaching material only; not in this repository.
2. **MCP demo:** the repository's `mcp-demo/` with `flashcards-db`.
3. **Release scenario:** a fictional QA team preparing a flashcards release, using AI for test design, log triage, regression selection, and release notes. No execution claim.

## Review Focus

1. **Tool-feature accuracy:** no invented Claude Code or MCP commands, flags, paths, or methods. Check `claude mcp add`, `SKILL.md`, `.claude/agents/`, `/mcp`, `MCPServer`, tool names, and transports against the handbook and current docs.
2. **Execution evidence:** suggested output is not proof. The pack must distinguish "the assistant proposed" from "the test passed"; no claim that this pack ran an AI session, test, or MCP call.
3. **Security:** prompt injection through files/tools, secrets, data classification, least-privilege MCP tools, trusting a server, and tool permissions.
4. **Capability overclaim:** hallucination, non-determinism, context limits, training cutoff, and the need to reproduce results.
5. **Distinctions:** `CLAUDE.md` vs skill vs slash command vs subagent vs hook vs MCP server; when each is appropriate for QA work.

---

### Task 1: Branch, checkers, and guide Parts 1–2

**Files:**
- Create: `release-qa-interview/topic-05-ai-assisted-testing/ai-assisted-testing.md`
- Create: `.superpowers/sdd/2026-11-19-release-qa-interview-topic-05/check_guide.py`
- Create: `.superpowers/sdd/2026-11-19-release-qa-interview-topic-05/check_qa.py`
- Create: `.superpowers/sdd/2026-11-19-release-qa-interview-topic-05/check_mcq.py`
- Create: `.superpowers/sdd/2026-11-19-release-qa-interview-topic-05/check_content.py`
- Create: `.superpowers/sdd/2026-11-19-release-qa-interview-topic-05/check_all.py`
- Create: `.superpowers/sdd/2026-11-19-release-qa-interview-topic-05/progress.md`

**Interfaces:**
- Consumes: the approved design and this plan.
- Produces: the branch, the checker CLI, and guide Parts 1–2.

- [ ] **Step 1: Create the branch and workspace**

```bash
git switch -c release-qa-interview-topic-05 release-qa-interview-topic-04
mkdir -p .superpowers/sdd/2026-11-19-release-qa-interview-topic-05
```

Write `progress.md` with first line:
`# SDD ledger — plan: docs/superpowers/plans/2026-11-19-release-qa-interview-topic-05.md`

- [ ] **Step 2: Write the failing guide test**

Create `check_guide.py` with:
- `--parts` and `--all`; missing part fails.
- `--toc` slug check.
- Balanced code fences.
- Exact per-part headings from this plan.
- `### Release QA Use` and `### Watch-outs` in every requested part.
- Required terms per part (Part 1: token, context, hallucination; Part 2: prompt, constraint; Part 3: edge case, test data; Part 4: stack trace, diff; Part 5: `CLAUDE.md`, permission; Part 6: `SKILL.md`, description; Part 7: subagent, context; Part 8: MCP, `claude mcp add`, `search_cards`, `add_card`; Part 9: prompt injection, secret; Part 10: flaky, regression).
- No forbidden execution claims: `this pack ran`, `we ran the demo`, `the AI test passed`.

Run:
`python .superpowers/sdd/2026-11-19-release-qa-interview-topic-05/check_guide.py --parts 1 2`
Expected: FAIL with a missing-guide error.

- [ ] **Step 3: Write the guide title, intro, TOC, and Parts 1–2**

Title: `# AI-Assisted Programming and Testing for Release QA`.
Intro: audience, Claude Code + MCP focus, relation to the AI handbook, flashcards and `mcp-demo/` examples, no-execution caveat. TOC links all ten parts.

Part 1 headings exactly:
`## Part 1 — AI and LLM Foundations for QA`, `### What an LLM Does`, `### Tokens and Context`, `### Training Cutoff and Freshness`, `### Non-Determinism and Hallucination`, `### What This Means for QA`, `### Release QA Use`, `### Watch-outs`.

Part 2 headings exactly:
`## Part 2 — Prompting and Context`, `### A Clear Task`, `### Constraints and Acceptance Criteria`, `### Examples and File References`, `### Iteration and Review`, `### Prompt Injection Basics`, `### Release QA Use`, `### Watch-outs`.

Content requirements:
- Part 1 explains tokens, context, cutoff, non-determinism, hallucination, and why confident output is not evidence.
- Part 2 shows a weak prompt and a strong prompt for a QA task, with task, constraints, examples, file paths, acceptance criteria, and review loop.
- Part 2 introduces prompt injection as untrusted content inside files/tools, not a magic phrase.
- Both parts end with `### Release QA Use` and `### Watch-outs`.

- [ ] **Step 4: Run the guide check**

Run:
`python .superpowers/sdd/2026-11-19-release-qa-interview-topic-05/check_guide.py --parts 1 2`
Expected: `guide checks passed`.

- [ ] **Step 5: Compile the checkers**

Run:
`python -m py_compile .superpowers/sdd/2026-11-19-release-qa-interview-topic-05/check_*.py`
Expected: exit 0.

- [ ] **Step 6: Commit**

```bash
git add docs/superpowers/specs/2026-11-19-release-qa-interview-topic-05-design.md \
        docs/superpowers/plans/2026-11-19-release-qa-interview-topic-05.md \
        release-qa-interview/topic-05-ai-assisted-testing/ai-assisted-testing.md
git commit -m "feat: add AI-assisted testing guide parts 1-2 and checkers"
```

Ledger line: `Task 1: complete (commits <base7>..<head7>, tests: check_guide.py --parts 1 2 → guide checks passed)`.

---

### Task 2: Guide Parts 3–4

**Files:**
- Modify: `release-qa-interview/topic-05-ai-assisted-testing/ai-assisted-testing.md`

**Interfaces:**
- Consumes: Part 1–2 terminology.
- Produces: test-design and debugging sections used by the banks.

- [ ] **Step 1: Add Part 3**

Headings:
`## Part 3 — AI-Assisted Test Design and Test Data`, `### Requirements to Risks`, `### Test Cases and Edge Cases`, `### Equivalence and Boundaries`, `### Exploratory Charters`, `### Synthetic Test Data`, `### Coverage Gaps`, `### Release QA Use`, `### Watch-outs`.

Content:
- Turn a requirement into risks, then cases; ask the model for missing cases, not just confirmation.
- Equivalence partitions and boundary values with a concrete flashcards example.
- Exploratory charters and heuristics.
- Synthetic test data: realistic but not real personal data; label synthetic rows.
- Coverage gaps: what the model cannot know without the product, logs, or users.
- Include a prompt example and a review checklist.

- [ ] **Step 2: Add Part 4**

Headings:
`## Part 4 — AI-Assisted Debugging and Code Review`, `### Stack Traces and Logs`, `### Reproducing a Failure`, `### Reviewing a Diff`, `### Test Suggestions vs Evidence`, `### Regression Checks`, `### Release QA Use`, `### Watch-outs`.

Content:
- Paste the trace, logs, expected/actual, and reproduction steps; ask for hypotheses, not a verdict.
- Reproduce before accepting a fix.
- Review a diff for behavior changes, missing tests, and unrelated edits.
- Distinguish a suggested test from a test that has run and passed.
- Regression checks: same failure, adjacent behavior, and rollback.
- Include a review checklist and a "what evidence would change my mind" prompt.

- [ ] **Step 3: Run the guide check**

Run:
`python .superpowers/sdd/2026-11-19-release-qa-interview-topic-05/check_guide.py --parts 1 2 3 4`
Expected: `guide checks passed`.

- [ ] **Step 4: Commit**

```bash
git add release-qa-interview/topic-05-ai-assisted-testing/ai-assisted-testing.md
git commit -m "feat: add AI-assisted test design and debugging guide"
```

---

### Task 3: Guide Parts 5–6 — Claude Code and skills

**Files:**
- Modify: `release-qa-interview/topic-05-ai-assisted-testing/ai-assisted-testing.md`

**Interfaces:**
- Consumes: the handbook's Part 3, 4.1–4.3, and Appendix C.
- Produces: the Claude Code and skill sections used by Q&A/MCQ Parts 5–6.

- [ ] **Step 1: Add Part 5**

Headings:
`## Part 5 — Claude Code Essentials`, `### What Claude Code Is`, `### CLAUDE.md`, `### Context Management`, `### Tools and Permissions`, `### Plan Mode`, `### Reviewing Changes`, `### Release QA Use`, `### Watch-outs`.

Content:
- Claude Code as a terminal/editor agent with tools, not an autocomplete.
- `CLAUDE.md` as project instructions and conventions; keep it short and current.
- Context: files, @ references, conversation growth, compaction; why a fresh session helps.
- Permissions: read/write/execute, approval, least privilege.
- Plan mode: research and propose before editing.
- Reviewing changes: diff, tests, and rollback.
- QA use: ask for a test plan or diff review before allowing edits.

- [ ] **Step 2: Add Part 6**

Headings:
`## Part 6 — Skills and Reusable Workflows`, `### What a Skill Is`, `### SKILL.md and Frontmatter`, `### Progressive Disclosure`, `### Explicit and Automatic Invocation`, `### Skills vs Slash Commands`, `### A QA Skill Example`, `### Release QA Use`, `### Watch-outs`.

Content:
- Skill as a reusable instruction package; explicit `/name` and automatic matching by name/description.
- `SKILL.md` frontmatter: `name`, `description`, `argument-hint`, `allowed-tools`, `disable-model-invocation`, `context: fork`, `model`.
- Progressive disclosure: name/description cheap; body on use; references on demand.
- Skills vs slash commands: current docs recommend skills for new work.
- A QA skill example: generate a risk-based test checklist from a requirement, with rules and output format.
- Watch-outs: vague descriptions, overbroad scope, side effects, stale skills.

- [ ] **Step 3: Run and commit**

Run:
`python .superpowers/sdd/2026-11-19-release-qa-interview-topic-05/check_guide.py --parts 1 2 3 4 5 6`
Expected: `guide checks passed`.

```bash
git add release-qa-interview/topic-05-ai-assisted-testing/ai-assisted-testing.md
git commit -m "feat: add Claude Code and skills guide"
```

---

### Task 4: Guide Parts 7–8 — Subagents and MCP

**Files:**
- Modify: `release-qa-interview/topic-05-ai-assisted-testing/ai-assisted-testing.md`

**Interfaces:**
- Consumes: handbook 4.4–4.5 and `mcp-demo/`.
- Produces: the subagent and MCP sections used by Q&A/MCQ Parts 7–8.

- [ ] **Step 1: Add Part 7**

Headings:
`## Part 7 — Subagents and Agent Workflows`, `### What a Subagent Is`, `### Context Isolation`, `### Tool Restrictions`, `### Parallel Review`, `### Implementer and Reviewer`, `### Orchestration Risks`, `### Release QA Use`, `### Watch-outs`.

Content:
- Subagent as a separate Claude instance with its own context and system prompt.
- Context isolation: volume review, no flooding the main session.
- Tool restrictions: read-only reviewer, test runner, researcher.
- Parallelism and the implementer/reviewer pattern.
- Risks: duplicated work, stale context, conflicting edits, cost, no shared memory.
- QA use: reviewer for a test plan or diff, researcher for logs, test runner for a focused suite.

- [ ] **Step 2: Add Part 8**

Headings:
`## Part 8 — MCP and Tool Integration`, `### What MCP Is`, `### Clients, Servers, Tools, Resources, Prompts`, `### Local and Remote Transports`, `### Connecting the Flashcards Demo`, `### Authentication and Least Privilege`, `### Prompt Injection Through Tools`, `### Release QA Use`, `### Watch-outs`.

Content:
- MCP as a protocol connecting Claude Code to external tools/data.
- Client/server; tools/resources/prompts; stdio versus HTTP/SSE.
- The local demo: `flashcards-db`, `search_cards`, `add_card`, SQLite, no credentials, MCP Python SDK 2.x `MCPServer`.
- Exact commands: `claude mcp add flashcards-db -- "<python>" "<server.py>"`, `/mcp`, `claude mcp remove flashcards-db`.
- Authentication, least privilege, read/write tool risk, trusting a server.
- Prompt injection through tool results; tool output is data, not instructions.
- QA use: query a test database, read an issue tracker, attach evidence; do not connect production data without approval.

- [ ] **Step 3: Run and commit**

Run:
`python .superpowers/sdd/2026-11-19-release-qa-interview-topic-05/check_guide.py --parts 1 2 3 4 5 6 7 8`
Expected: `guide checks passed`.

```bash
git add release-qa-interview/topic-05-ai-assisted-testing/ai-assisted-testing.md
git commit -m "feat: add subagents and MCP guide"
```

---

### Task 5: Guide Parts 9–10 and README

**Files:**
- Modify: `release-qa-interview/topic-05-ai-assisted-testing/ai-assisted-testing.md`
- Create: `release-qa-interview/topic-05-ai-assisted-testing/README.md`

**Interfaces:**
- Consumes: all guide parts.
- Produces: the completed guide and reader entry point.

- [ ] **Step 1: Add Part 9**

Headings:
`## Part 9 — Safety, Security, and Verification`, `### Secrets and Data Classification`, `### Licensing and Provenance`, `### Hallucinated APIs and False Evidence`, `### Reproducibility`, `### Human Review`, `### The Evidence Checklist`, `### Release QA Use`, `### Watch-outs`.

Content:
- Never paste secrets, tokens, customer data, or production logs without approval.
- License/provenance of generated code and copied snippets.
- Hallucinated APIs, imports, commands, and test output.
- Reproduce: run the test, inspect the diff, check the source, capture the command and result.
- Human review and sign-off; AI is not the release authority.
- Evidence checklist: command, environment, expected/actual, artifact, reviewer.

- [ ] **Step 2: Add Part 10**

Headings:
`## Part 10 — Release QA Workflows and Interview Scenarios`, `### AI in CI`, `### Flaky Test Triage`, `### Regression Selection`, `### Release Notes`, `### Bug Reports`, `### Test Data Cleanup`, `### End-to-End Scenarios`, `### Release QA Use`, `### Watch-outs`.

Content:
- AI in CI: summarize failures, suggest likely causes, draft a triage note; never auto-approve a release.
- Flaky test triage: separate product failure from test infrastructure; require reproduction.
- Regression selection: risk-based, not "run everything" or blind AI selection.
- Release notes and bug reports: factual, evidence-linked, no invented tickets.
- Test data cleanup: synthetic data, no production copies, rollback.
- End-to-end interview scenarios: a failing test, a suspicious diff, an MCP tool returning untrusted text, a release decision.

- [ ] **Step 3: Write README**

Include: folder contents, audience, Claude Code + MCP focus, relation to the AI handbook, study order (guide → Q&A → MCQs), counts 100/150, 10-part coverage table, running examples, and a note that no AI session/test/MCP call was executed for this pack. Point to `mcp-demo/` for the runnable demo.

- [ ] **Step 4: Run and commit**

Run:
`python .superpowers/sdd/2026-11-19-release-qa-interview-topic-05/check_guide.py --all --toc`
Expected: `guide checks passed`.

Run:
`python .superpowers/sdd/2026-11-19-release-qa-interview-topic-05/check_content.py`
Expected: guide coverage passes; bank files missing are expected at this stage.

```bash
git add release-qa-interview/topic-05-ai-assisted-testing/
git commit -m "feat: complete AI-assisted testing guide and README"
```

---

### Task 6: Q&A Parts 1–4

**Files:**
- Create: `release-qa-interview/topic-05-ai-assisted-testing/qa-100.md`

**Interfaces:**
- Consumes: guide Parts 1–4.
- Produces: Q1–Q39 with hidden answers and Contents links for all ten parts.

- [ ] **Step 1: Add the Q&A shell and Parts 1–4**

Headings/counts:
`## Part 1 — AI and LLM Foundations for QA (8 questions)`, `## Part 2 — Prompting and Context (9 questions)`, `## Part 3 — AI-Assisted Test Design and Test Data (12 questions)`, `## Part 4 — AI-Assisted Debugging and Code Review (10 questions)`.

Topics:
- Part 1: tokens, context, training cutoff, non-determinism, hallucination, confidence vs evidence, LLM vs search, why QA must verify.
- Part 2: task, constraints, examples, file references, acceptance criteria, iteration, weak vs strong prompt, prompt injection.
- Part 3: requirements→risks, edge cases, equivalence/boundaries, exploratory charters, synthetic data, coverage gaps, test-data privacy.
- Part 4: stack traces, logs, reproduction, diff review, suggested vs verified test, regression checks, evidence.

Answers 2–5 sentences, concrete prompts/examples. No execution claim.

- [ ] **Step 2: Run and commit**

Run:
`python .superpowers/sdd/2026-11-19-release-qa-interview-topic-05/check_qa.py --parts 1:8 2:9 3:12 4:10 --total 39`
Expected: 39 questions, sequential, 39 balanced reveals.

```bash
git add release-qa-interview/topic-05-ai-assisted-testing/qa-100.md
git commit -m "feat: add AI-assisted testing Q&A parts 1-4"
```

---

### Task 7: Q&A Parts 5–7

**Files:**
- Modify: `release-qa-interview/topic-05-ai-assisted-testing/qa-100.md`

**Interfaces:**
- Consumes: guide Parts 5–7; Q1–Q39.
- Produces: Q40–Q67.

- [ ] **Step 1: Add Parts 5–7**

Headings/counts:
`## Part 5 — Claude Code Essentials (10 questions)`, `## Part 6 — Skills and Reusable Workflows (9 questions)`, `## Part 7 — Subagents and Agent Workflows (9 questions)`.

Topics:
- Part 5: Claude Code vs autocomplete, `CLAUDE.md`, context/@/compaction, permissions, plan mode, diff review, terminal/editor.
- Part 6: skill definition, `SKILL.md`, frontmatter fields, progressive disclosure, explicit/automatic invocation, skills vs commands, QA skill example, side effects.
- Part 7: subagent definition, context isolation, tool allowlists, parallelism, implementer/reviewer, orchestration risks, when not to use one.

- [ ] **Step 2: Run and commit**

Run:
`python .superpowers/sdd/2026-11-19-release-qa-interview-topic-05/check_qa.py --parts 1:8 2:9 3:12 4:10 5:10 6:9 7:9 --total 67`
Expected: 67 questions, sequential, 67 balanced reveals.

```bash
git add release-qa-interview/topic-05-ai-assisted-testing/qa-100.md
git commit -m "feat: add AI-assisted testing Q&A parts 5-7"
```

---

### Task 8: Q&A Parts 8–10

**Files:**
- Modify: `release-qa-interview/topic-05-ai-assisted-testing/qa-100.md`

**Interfaces:**
- Consumes: guide Parts 8–10; Q1–Q67.
- Produces: Q68–Q100 and the complete Q&A bank.

- [ ] **Step 1: Add Parts 8–10**

Headings/counts:
`## Part 8 — MCP and Tool Integration (10 questions)`, `## Part 9 — Safety, Security, and Verification (10 questions)`, `## Part 10 — Release QA Workflows and Interview Scenarios (13 questions)`.

Topics:
- Part 8: MCP client/server, tools/resources/prompts, stdio/remote, `claude mcp add`, `flashcards-db`, least privilege, auth, prompt injection through tools, when MCP is overkill.
- Part 9: secrets, data classification, licensing, hallucinated APIs, reproducibility, human review, evidence checklist.
- Part 10: AI in CI, flaky triage, regression selection, release notes, bug reports, test-data cleanup, end-to-end scenarios, limitations, release authority.

- [ ] **Step 2: Run and commit**

Run:
`python .superpowers/sdd/2026-11-19-release-qa-interview-topic-05/check_qa.py --parts 1:8 2:9 3:12 4:10 5:10 6:9 7:9 8:10 9:10 10:13 --total 100 --toc`
Expected: 100 questions, sequential, 100 balanced reveals, TOC resolves.

```bash
git add release-qa-interview/topic-05-ai-assisted-testing/qa-100.md
git commit -m "feat: complete AI-assisted testing Q&A bank"
```

---

### Task 9: MCQ Parts 1–4

**Files:**
- Create: `release-qa-interview/topic-05-ai-assisted-testing/mcq-150.md`

**Interfaces:**
- Consumes: guide Parts 1–4.
- Produces: MCQ 1–59.

- [ ] **Step 1: Add the MCQ shell and Parts 1–4**

Headings/counts:
`## Part 1 — AI and LLM Foundations for QA (12 questions)`, `## Part 2 — Prompting and Context (15 questions)`, `## Part 3 — AI-Assisted Test Design and Test Data (17 questions)`, `## Part 4 — AI-Assisted Debugging and Code Review (15 questions)`.

Topics follow Q&A Parts 1–4, with scenario items for test design, debugging, and evidence. At least 24 of these 59 stems are scenarios. Four options, one answer line. Track letters; full 150 must land 37–38 each.

- [ ] **Step 2: Run and commit**

Run:
`python .superpowers/sdd/2026-11-19-release-qa-interview-topic-05/check_mcq.py --parts 1:12 2:15 3:17 4:15 --total 59`
Expected: 59 questions, four options each, 59 answer lines, balanced reveals.

```bash
git add release-qa-interview/topic-05-ai-assisted-testing/mcq-150.md
git commit -m "feat: add AI-assisted testing MCQs parts 1-4"
```

---

### Task 10: MCQ Parts 5–7

**Files:**
- Modify: `release-qa-interview/topic-05-ai-assisted-testing/mcq-150.md`

**Interfaces:**
- Consumes: guide Parts 5–7; MCQ 1–59.
- Produces: MCQ 60–102.

- [ ] **Step 1: Add Parts 5–7**

Headings/counts:
`## Part 5 — Claude Code Essentials (15 questions)`, `## Part 6 — Skills and Reusable Workflows (14 questions)`, `## Part 7 — Subagents and Agent Workflows (14 questions)`.

Topics follow Q&A Parts 5–7, with scenarios for permissions, skill authoring, delegation, and tool restrictions. At least 20 of these 43 stems are scenarios.

- [ ] **Step 2: Run and commit**

Run:
`python .superpowers/sdd/2026-11-19-release-qa-interview-topic-05/check_mcq.py --parts 1:12 2:15 3:17 4:15 5:15 6:14 7:14 --total 102`
Expected: 102 questions, four options each, 102 answer lines, balanced reveals.

```bash
git add release-qa-interview/topic-05-ai-assisted-testing/mcq-150.md
git commit -m "feat: add AI-assisted testing MCQs parts 5-7"
```

---

### Task 11: MCQ Parts 8–10

**Files:**
- Modify: `release-qa-interview/topic-05-ai-assisted-testing/mcq-150.md`

**Interfaces:**
- Consumes: guide Parts 8–10; MCQ 1–102.
- Produces: MCQ 103–150 and the complete MCQ bank.

- [ ] **Step 1: Add Parts 8–10**

Headings/counts:
`## Part 8 — MCP and Tool Integration (15 questions)`, `## Part 9 — Safety, Security, and Verification (15 questions)`, `## Part 10 — Release QA Workflows and Interview Scenarios (18 questions)`.

Topics follow Q&A Parts 8–10, with scenarios for MCP trust, prompt injection, secrets, flaky tests, release decisions, and evidence. At least 16 of these 48 stems are scenarios. Final answer letters 37–38 each; adjust option order without changing content.

- [ ] **Step 2: Run and commit**

Run:
`python .superpowers/sdd/2026-11-19-release-qa-interview-topic-05/check_mcq.py --parts 1:12 2:15 3:17 4:15 5:15 6:14 7:14 8:15 9:15 10:18 --total 150 --toc --letter-bounds`
Expected: 150 questions, four options each, 150 answer lines, TOC resolves, letters 37–38 each.

```bash
git add release-qa-interview/topic-05-ai-assisted-testing/mcq-150.md
git commit -m "feat: complete AI-assisted testing MCQ bank"
```

---

### Task 12: Cross-file checks, final review, and finish

**Files:**
- Test: `.superpowers/sdd/2026-11-19-release-qa-interview-topic-05/check_all.py`
- Modify: guide, Q&A, MCQ, README for review fixes.

**Interfaces:**
- Consumes: all four deliverables and all checkers.
- Produces: a green branch ready for the integration decision.

- [ ] **Step 1: Run the full suite**

Run:
`python .superpowers/sdd/2026-11-19-release-qa-interview-topic-05/check_all.py`
Expected: guide checks pass; Q&A 100; MCQ 150; content checks pass; scenario ≥60/150; zero duplicate stems; letters 37–38 each.

- [ ] **Step 2: Verify tool claims against sources**

Check the guide and banks against `using-ai-from-zero-to-claude-code.md`, `mcp-demo/README.md`, `mcp-demo/server.py`, and current Claude Code/MCP docs. Confirm every command, path, frontmatter field, tool name, and transport claim. Flag anything unverified as a finding rather than guessing.

- [ ] **Step 3: Dispatch the whole-branch reviewer**

Generate the review package for `8e8a981..HEAD` and dispatch one fresh reviewer on the most capable model with the design, plan, Review Focus, and ledger. Ask for Critical/Important/Minor findings.

- [ ] **Step 4: Fix the findings in one wave**

Fix Critical/Important findings in one pass. Add a regression check where the finding is structural; verify prose against the source contract. Run `check_all.py` after the pass. Record each fix in the ledger.

- [ ] **Step 5: Record deferred minors and rulings**

Append every `Final: minor (deferred):` and `Final: Ruling:` line to the ledger. The final message must list them.

- [ ] **Step 6: Commit the fix wave**

```bash
git add release-qa-interview/topic-05-ai-assisted-testing/
git commit -m "docs: apply AI-assisted testing final review fixes"
```

- [ ] **Step 7: Delete the workspace and finish**

After the review is clean and the fixes are committed, delete `.superpowers/sdd/2026-11-19-release-qa-interview-topic-05/` and invoke `superpowers:finishing-a-development-branch`. The base branch is `release-qa-interview-topic-04`. Present the three integration options and wait for the user's choice.

## Self-Review

- **Spec coverage:** every design part maps to Tasks 1–5; the Q&A and MCQ distributions map to Tasks 6–11; source verification and review map to Task 12.
- **Step scan:** each task names exact files, headings, counts, and a check command with an expected result.
- **Type consistency:** part titles, counts, and checker CLI match; Q&A 100 and MCQ 150.
- **Review Focus:** each failure mode has a task and a check: tool accuracy (Tasks 3–5, 12), execution evidence (Tasks 1–5, 12), security (Tasks 4–5, bank tasks), capability overclaim (Tasks 1–5), distinctions (Tasks 3–4, bank tasks).
- **Proportion:** the plan carries the source contract and exact checks; it does not write the prose or the questions.
