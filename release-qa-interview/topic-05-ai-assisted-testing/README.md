# AI-Assisted Programming and Testing — Topic 5

Interview-prep pack for junior-to-mid release QA engineers who need to explain
and use AI assistance without over-trusting it. The focus is Claude Code and the
Model Context Protocol (MCP), with the concepts kept practical.

## What is here

| File | Contents |
|---|---|
| `ai-assisted-testing.md` | Ten-part knowledge guide: LLM limits, prompting, test design and data, debugging and review, Claude Code, skills, subagents, MCP, safety/verification, and release workflows. |
| `qa-100.md` | 100 open questions with hidden answers. |
| `mcq-150.md` | 150 multiple-choice questions with answers and explanations. |
| `README.md` | This file. |

## Who it is for

New graduates and junior-to-mid release QA candidates. It assumes no AI
engineering background. The goal is to be able to:

- explain what an LLM can and cannot do for test work;
- write a prompt that produces a reviewable test artifact;
- use Claude Code for test design, debugging, and code review;
- explain `CLAUDE.md`, skills, slash commands, subagents, hooks, and MCP;
- demand and check evidence before reporting a result;
- describe the security and privacy risks of connecting AI to a codebase.

## How it relates to the AI handbook

`using-ai-from-zero-to-claude-code.md` is the deep reference. This pack is the
interview-focused, QA-specific summary and question bank. It reuses the
handbook's terminology, its flashcards project, and the repository's
`mcp-demo/`. It does not replace the handbook or re-teach its full eight parts.

## Study order

1. Read `ai-assisted-testing.md` part by part.
2. Answer `qa-100.md` with the answers hidden; explain each answer aloud.
3. Take `mcq-150.md`; review every explanation, not just the score.
4. Re-read the weak parts and retry the missed questions.

## Coverage

| Part | Guide section | Q&A | MCQs |
|---|---|---:|---:|
| 1 | AI and LLM foundations for QA | 8 | 12 |
| 2 | Prompting and context | 9 | 15 |
| 3 | AI-assisted test design and test data | 12 | 17 |
| 4 | AI-assisted debugging and code review | 10 | 15 |
| 5 | Claude Code essentials | 10 | 15 |
| 6 | Skills and reusable workflows | 9 | 14 |
| 7 | Subagents and agent workflows | 9 | 14 |
| 8 | MCP and tool integration | 10 | 15 |
| 9 | Safety, security, and verification | 10 | 15 |
| 10 | Release QA workflows and interview scenarios | 13 | 18 |
| **Total** | | **100** | **150** |

## Running examples

- **Flashcards project:** Maya's `cards.md`, `flashcards.py`, `quiz.html`, and
  `.claude/` skills/agents from the AI handbook. It is teaching material and is
  not in this repository.
- **MCP demo:** the repository's `mcp-demo/` exposes `search_cards` and
  `add_card` over SQLite with the MCP Python SDK 2.x. See `mcp-demo/README.md`
  for the runnable setup. The demo is the only runnable artifact in this pack.
- **Release scenario:** a fictional QA team preparing a flashcards release. It
  is a narrative, not a recorded session.

## Practice note

No AI session, test, or MCP call was executed for this pack. The `mcp-demo/`
is documented as runnable in its own README; this guide describes it and does
not claim to have run it. The expected results and artifacts are teaching
examples, not observed output.

## A note on trust

The interview skill this pack teaches is not “use AI more.” It is “use AI where
it widens the search, and demand evidence where the answer affects a release.”
A confident answer is a hypothesis. A passing test with a command and output is
evidence.
