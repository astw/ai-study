# Two Agents, Two Skills — Design

Date: 2026-11-23
Status: approved

## Intent

A minimal, runnable Claude Code project in a separate folder that shows two
subagents working in parallel, each preloaded with exactly one different Agent
Skill. It complements `skill-vs-agent-demo/`: that demo contrasts a skill with
an agent; this one shows skills and agents composing, and makes visible that a
preloaded skill's instructions live inside the agent's context, not the
parent's.

## Goals

- A new self-contained folder `AI_general/two-agents-two-skills-demo/`, matching
  the first demo's Markdown-only style.
- Two project skills with distinct output contracts.
- Each output contract appears only in its own `SKILL.md` — never in the agent
  body or the run prompt — so the right-shaped report proves the skill did the
  work.
- Two subagents, one per skill, bound via the `skills:` frontmatter field with
  `tools: Read`.
- One shared article; one prompt dispatches both agents in parallel.
- A README whose observations show three things: the parallel reports, the
  parent lacking the source, and the parent lacking either skill's procedure.
- No application code, tests, or dependencies.

## Non-goals

- No simulation of Claude Code behavior.
- No build step or package.
- No changes to `skill-vs-agent-demo/`.
- No sequential pipeline.
- Not part of the published guides.

## Constraints

- Must be opened in Claude Code from inside the new folder so `.claude/` is
  discovered.
- `skills:` preloading verified against the official docs on 2026-11-23: YAML
  list syntax; every tool the skill body uses must be in the agent's `tools`;
  skills must not set `disable-model-invocation: true`; up to 32 preloaded names.
- Agents use only `Read`.
- Do not commit unless the user asks.

## Approaches considered

1. **Same article, two output styles** (chosen) — isolates the skill as the only
   variable; the two report formats are unmistakably different.
2. **Two articles, one per agent** — changes two variables at once and muddies
   what the demo proves; rejected.
3. **Sequential pipeline** — shows agents cannot share context, but adds
   orchestration steps to a demo meant to be minimal; rejected.

## Design

Folder: `AI_general/two-agents-two-skills-demo/`

- `.claude/skills/bullet-summary/SKILL.md` — read `article.md`; produce exactly
  three bullet points, each under 12 words; no introduction or conclusion.
- `.claude/skills/quiz-maker/SKILL.md` — read `article.md`; produce exactly
  three question-and-answer pairs in a fixed `Q1:` / `A1:` layout, each answer
  under 20 words; no introduction or conclusion.
- `.claude/agents/bullet-summarizer.md` — frontmatter `skills: [bullet-summary]`
  and `tools: Read`; body tells the agent to follow the preloaded skill,
  prefix its reply `[bullet report]`, and not ask questions. It does not restate
  the output contract.
- `.claude/agents/quiz-writer.md` — frontmatter `skills: [quiz-maker]` and
  `tools: Read`; body tells the agent to follow the preloaded skill, prefix its
  reply `[quiz report]`, and not ask questions. It does not restate the output
  contract.
- `article.md` — the 121-word autumn article from the first demo, copied so this
  folder is self-contained.
- `README.md` — prerequisites, run steps, expected observations, concept table,
  and file tree.

### Run contract

Prompt:

```text
Use the bullet-summarizer and quiz-writer agents in parallel on article.md.
Do not read article.md yourself.
```

Expected: two reports, one `[bullet report]` with three bullets and one
`[quiz report]` with three Q&A pairs.

### Observations the README teaches

1. **Parallel dispatch** — both reports return in one turn.
2. **Parent lacks the source** — a source-detail follow-up ("Which two pigment
   names does the article give for yellow and orange?") cannot be answered from
   the parent's context; it must read the file or delegate again.
3. **Parent lacks the skills** — asking what procedure `quiz-writer` followed
   cannot be answered from the parent's context; it requires re-delegating to
   that agent.

## Left to the builder

- Exact skill wording, agent wording, README phrasing.
- Exact wording of the follow-up prompts.
- Whether the article is copied verbatim or lightly reformatted.
