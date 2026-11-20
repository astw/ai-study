# Release QA Interview Topic 5 — AI-Assisted Programming and Testing Design

**Date:** 2026-11-19
**Status:** Proposed
**Audience:** Junior-to-mid release QA candidates, including new graduates who have used an AI assistant but have not built workflows around one.

## Intent

Add a fifth interview pack for release QA: how AI assistants help with programming and testing, with Claude Code and MCP as the primary tools. The pack should leave a candidate able to:

- explain what an LLM can and cannot do for test work;
- write a prompt that produces a reviewable test artifact;
- use Claude Code for test design, test data, debugging, and code review;
- explain the difference between `CLAUDE.md`, a skill, a slash command, a subagent, a hook, and an MCP server;
- recognize when AI output must be verified, and what evidence to demand;
- describe the security, privacy, and correctness risks of connecting an AI to a codebase or test system.

The existing AI handbook (`using-ai-from-zero-to-claude-code.md`) remains the deep reference. Topic 5 is the interview-focused, QA-specific pack: shorter explanations, release scenarios, 100 Q&A, and 150 MCQs. It reuses the handbook's terminology and the verified `mcp-demo/`; it does not replace the handbook or re-teach its full eight parts.

## Goals

- Explain LLM foundations in QA terms: tokens, context windows, training cutoffs, non-determinism, hallucination, and why a confident answer is not evidence.
- Teach prompting for test work: clear task, constraints, examples, file references, acceptance criteria, and iterative review.
- Show AI-assisted test design, test data generation, exploratory testing, regression selection, debugging, and code review on the flashcards project.
- Explain Claude Code's working model: `CLAUDE.md`, context, tools, permissions, plan mode, skills, subagents, hooks, and MCP.
- Explain skills as reusable instruction packages: `SKILL.md`, frontmatter, progressive disclosure, explicit and automatic invocation, and when a skill is better than a one-off prompt.
- Explain subagents as isolated-context specialists: delegation, tool restrictions, parallelism, and the review/implementer pattern.
- Explain MCP: client/server, tools/resources/prompts, local stdio versus remote servers, the `flashcards-db` demo, authentication, least privilege, and prompt injection through tools.
- Make verification a first-class topic: reproduce the result, inspect the diff, run the test, check the source, and never treat generated code or test results as proof until observed.
- Give release QA interview practice: 100 Q&A and 150 MCQs with the same reveal format as topics 1–4.

## Non-goals

- No model training, fine-tuning, embeddings, or RAG implementation.
- No building a production agent framework or a production MCP server; the local demo is explained, not extended.
- No vendor comparison beyond the concepts needed to explain Claude Code's choices.
- No claims that any AI session, test, or MCP call was executed for this pack. The `mcp-demo/` is the only runnable artifact and is documented as already verified in the repository.
- No prompt-engineering tricks that only work on one model version.
- No replacement for the AI handbook or the Playwright guide.

## Anti-goals

- Treating AI as an oracle: questions that imply generated tests are correct because they look plausible.
- Teaching prompt "magic words" instead of clear task framing and verification.
- Presenting a skill, subagent, or MCP server as automatically safe or production-ready.
- Re-teaching the entire AI handbook inside the question bank.
- Duplicating stems or using prose options that echo the question.
- Claiming a tool feature or command without checking current Claude Code or MCP documentation.

## Approaches considered

1. **QA-focused full pack — chosen.** A ten-part guide, 100 Q&A, 150 MCQs, and a README. Claude Code and MCP are primary; the AI handbook is the deep reference. Best fit for the existing bank and the interview goal.
2. **Condensed handbook summary.** Reuse the handbook's structure and shorten it. Cheaper, but duplicates material and does not build QA-specific interview practice.
3. **Build-an-agent lab.** Write a skill, a subagent, and an MCP server end to end. Strong engineering practice, but beyond the practical QA core the user chose and too dependent on a working local environment.
4. **Vendor-neutral AI testing pack.** Broad concepts across assistants. Useful, but the user chose Claude Code + MCP, and the repository already has those verified artifacts.

## Pack structure

Folder: `release-qa-interview/topic-05-ai-assisted-testing/`

| File | Role |
|---|---|
| `ai-assisted-testing.md` | Ten-part knowledge guide with plain-English explanations, prompt examples, Claude Code configuration examples, MCP commands, and release-QA scenarios. |
| `qa-100.md` | 100 open questions, numbered `Q1`–`Q100`, hidden answers. |
| `mcq-150.md` | 150 four-option questions, numbered `MCQ 1`–`MCQ 150`, one answer and explanation each. |
| `README.md` | Study order, coverage table, counts, relation to the AI handbook, and a note that examples are illustrative. |

### Guide parts

1. **AI and LLM foundations for QA** — tokens, context, training cutoff, non-determinism, hallucination, and why output needs evidence.
2. **Prompting and context** — task, constraints, examples, file references, acceptance criteria, iteration, and prompt injection basics.
3. **AI-assisted test design and test data** — requirements to risks to cases, edge cases, equivalence partitions, boundary values, exploratory charters, synthetic data, and coverage gaps.
4. **AI-assisted debugging and code review** — stack traces, logs, failing tests, reproduction steps, diff review, and the difference between a suggestion and a verified fix.
5. **Claude Code essentials** — `CLAUDE.md`, context management, tools, permissions, plan mode, reviewing changes, and when to use the terminal versus the editor.
6. **Skills and reusable workflows** — `SKILL.md`, frontmatter, progressive disclosure, explicit/automatic invocation, skills versus slash commands, and QA skill examples.
7. **Subagents and agent workflows** — isolated context, tool allowlists, delegation, parallel review, implementer/reviewer separation, and orchestration risks.
8. **MCP and tool integration** — client/server, tools/resources/prompts, stdio versus remote transport, `claude mcp add`, the `flashcards-db` demo, authentication, least privilege, and prompt injection through tools.
9. **Safety, security, and verification** — secrets, data classification, licensing, hallucinated APIs, unreproducible results, human review, and the evidence checklist.
10. **Release QA workflows and interview scenarios** — AI in CI, flaky-test triage, regression selection, release notes, bug reports, test-data cleanup, and end-to-end interview scenarios.

Each part ends with `### Release QA Use` and `### Watch-outs`. Configuration examples are labeled as teaching examples; the only runnable MCP artifact is `mcp-demo/`.

### Running examples

- **Flashcards project:** Maya's `flashcards/` folder from the AI handbook, with `cards.md`, `flashcards.py`, `quiz.html`, `.claude/` commands, skills, and agents. It is teaching material and is not in this repository. Do not present a generated file as the real project.
- **MCP demo:** `mcp-demo/server.py`, `smoke_test.py`, `requirements.txt`, and `README.md` in this repository. Tools: `search_cards(query, limit=5)` and `add_card(question, answer, source="")`. SDK: `mcp.server.mcpserver.MCPServer`, MCP Python SDK 2.x.
- **Release scenario:** a fictional release QA team preparing a flashcards app release, using AI for test design, regression selection, log triage, and release notes. No claim that the scenario was executed.

## Question bank design

### Q&A distribution (100)

| Part | Count |
|---|---:|
| 1 AI and LLM foundations | 8 |
| 2 Prompting and context | 9 |
| 3 Test design and test data | 12 |
| 4 Debugging and code review | 10 |
| 5 Claude Code essentials | 10 |
| 6 Skills and reusable workflows | 9 |
| 7 Subagents and agents | 9 |
| 8 MCP and tool integration | 10 |
| 9 Safety, security, verification | 10 |
| 10 Release QA workflows | 13 |
| **Total** | **100** |

### MCQ distribution (150)

| Part | Count |
|---|---:|
| 1 AI and LLM foundations | 12 |
| 2 Prompting and context | 15 |
| 3 Test design and test data | 17 |
| 4 Debugging and code review | 15 |
| 5 Claude Code essentials | 15 |
| 6 Skills and reusable workflows | 14 |
| 7 Subagents and agents | 14 |
| 8 MCP and tool integration | 15 |
| 9 Safety, security, verification | 15 |
| 10 Release QA workflows | 18 |
| **Total** | **150** |

### Style rules

- At least 60 of 150 MCQ stems are scenarios.
- Four options per MCQ, exactly one correct answer, and a `**Correct answer: X.**` explanation that names the trap.
- Answer letters roughly balanced (target 37–38 each).
- No exact or number-insensitive duplicate stems across both banks.
- Q&A answers 2–5 sentences, with a concrete prompt, command, or artifact where useful.
- Use current Claude Code terminology: `CLAUDE.md`, skills, subagents, hooks, MCP servers, tools, resources, prompts.
- Distinguish "the assistant suggested" from "the test passed"; never imply execution without evidence.
- Use the handbook's `mcp-demo` tool names and commands exactly.

## Verification

- Counts, sequential numbering, per-part totals, reveal balance, four options, one answer line, answer distribution, TOC anchors, scenario share, and duplicate stems.
- Terminology check against the AI handbook and current Claude Code/MCP documentation. Verify commands and config paths, especially `claude mcp add`, `SKILL.md`, `.claude/agents/`, and `/mcp`.
- No invented tool names, flags, or MCP methods. The `mcp-demo` description must match `server.py`, `smoke_test.py`, and `mcp-demo/README.md`.
- No execution claim. The guide may say the demo is runnable and was verified in the repository; it must not claim this pack ran it.
- No secrets, credentials, or real user data in examples.

## What is left to the builder

- Write the exact explanations, examples, questions, options, and explanations.
- Keep the flashcards and MCP examples consistent with the handbook and `mcp-demo/`.
- Check each Claude Code and MCP claim against current documentation before committing it.
- Run the structural checks and a fresh-context review before finishing the branch.
