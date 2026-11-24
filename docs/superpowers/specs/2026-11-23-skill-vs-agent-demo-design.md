# Skill vs Agent Demo — Design

Date: 2026-11-23
Status: approved

## Intent

A minimal, runnable Claude Code project that lets someone see the difference
between an Agent Skill and a subagent by running the same summarization task
both ways.

## Goals

- One folder, four files, no dependencies.
- The same task performed by a skill and by an agent, so the execution model is
  the only variable.
- A README that explains what to observe and maps each observation back to the
  concepts (HOW vs WHO, shared vs separate context, who can ask questions).

## Non-goals

- No simulation of Claude Code behavior.
- No application code, tests, or build step.
- Not part of the published guides.

## Constraints

- Must be opened in Claude Code from inside the demo folder so `.claude/` is
  discovered.
- Uses only built-in tools (`Read`).

## Approaches considered

1. **Runnable Claude Code project** (chosen) — authentic; shows real context
   behavior and real invocation.
2. **A script that simulates both** — cannot show real context isolation or
   skill/agent triggering; rejected as misleading.
3. **Markdown-only walkthrough** — no runnable configuration; rejected.

## Design

Folder: `AI_general/skill-vs-agent-demo/`

- `.claude/skills/summarize-inline/SKILL.md` — user-invocable skill; loads
  instructions into the main conversation to read `article.md` and produce
  exactly three bullets.
- `.claude/agents/summarizer.md` — subagent with `tools: Read`; reads
  `article.md` and returns a three-bullet report, prefixed so it is
  recognizable as subagent output.
- `article.md` — a short neutral article (about 150 words).
- `README.md` — two experiments and what to observe in each.

## Left to the builder

- Exact article text and exact wording of the prompts.
- Exact README wording.
