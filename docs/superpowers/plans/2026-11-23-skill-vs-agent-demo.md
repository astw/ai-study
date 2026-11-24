# Skill vs Agent Demo Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a four-file, runnable Claude Code project that demonstrates a skill and a subagent doing the same summarization task.

**Architecture:** A self-contained folder with a `.claude/` project config. The skill loads instructions into the main conversation; the agent is a separate worker. Both summarize the same `article.md` into three bullets, so the execution model is the only variable.

**Tech Stack:** Markdown only — Claude Code skill and subagent definitions, no code, no dependencies.

**Spec:** `docs/superpowers/specs/2026-11-23-skill-vs-agent-demo-design.md`

## Global Constraints

- Everything lives under `C:\Users\wshuhao\AI_Study\AI_general\skill-vs-agent-demo\`.
- No application code, test suite, build step, or dependency.
- Skill and agent must produce the same output shape: exactly three bullets, each under 12 words.
- Do not commit: the user has not asked for this demo to be committed.

## Review Focus

- Starting Claude Code outside the demo folder means `.claude/` is not discovered; the README must say to start inside it.
- Running the agent experiment right after the skill experiment leaves the article in main context; the README must require `/clear` first.
- A frontmatter typo silently prevents discovery; each task verifies the exact name, description, and tools fields.
- Without a marker, the agent's report is indistinguishable from a normal answer; the agent must prefix `[agent report]`.
- If the two paths produce different formats, the comparison is invalid; both tasks pin the same three-bullet, under-12-words contract.

---

### Task 1: Create the folder and the article

**Files:**
- Create: `AI_general/skill-vs-agent-demo/article.md`

**Interfaces:**
- Consumes: nothing.
- Produces: `article.md` — the shared input read by the skill (Task 2) and the agent (Task 3).

- [ ] **Step 1: Create the demo folder**

Run: `New-Item -ItemType Directory -Force "C:\Users\wshuhao\AI_Study\AI_general\skill-vs-agent-demo"`
Expected: directory exists.

- [ ] **Step 2: Write `article.md` with this exact content**

```markdown
# Why Leaves Change Color in Autumn

In spring and summer, leaves are green because they contain large amounts of
chlorophyll, the pigment that captures sunlight for photosynthesis. As days
shorten and temperatures fall, trees stop producing chlorophyll. The green
fades, and pigments that were hidden underneath — yellow carotenoids and
orange xanthophylls — become visible.

Some trees also make red anthocyanins in autumn, especially when sunny days
are followed by cool nights. These pigments may help protect the leaf while
it sends nutrients back into the tree.

Eventually the tree seals off each leaf at the stem, and the leaf falls. The
colors are not new: they were there all along, or appear briefly as the leaf
finishes its work.
```

- [ ] **Step 3: Verify the article**

Run: `(Get-Content "C:\Users\wshuhao\AI_Study\AI_general\skill-vs-agent-demo\article.md" | Measure-Object -Word).Words`
Expected: a number between 100 and 160.

---

### Task 2: Add the skill

**Files:**
- Create: `AI_general/skill-vs-agent-demo/.claude/skills/summarize-inline/SKILL.md`

**Interfaces:**
- Consumes: `article.md` from Task 1.
- Produces: user-invocable skill `/summarize-inline`, output format "exactly three bullets, each under 12 words".

- [ ] **Step 1: Create the skill directory**

Run: `New-Item -ItemType Directory -Force "C:\Users\wshuhao\AI_Study\AI_general\skill-vs-agent-demo\.claude\skills\summarize-inline"`
Expected: directory exists.

- [ ] **Step 2: Write `SKILL.md` with this exact content**

```markdown
---
name: summarize-inline
description: Summarize article.md in exactly three short bullets in the main conversation. Use when the user asks to summarize the demo article inline or invokes /summarize-inline.
---

# Summarize Inline

When invoked:

1. Read `article.md` from the current project folder.
2. Summarize it in exactly three bullet points.
3. Keep each bullet under 12 words.
4. Do not add an introduction or conclusion.

Because this runs in the main conversation, the article is now in context and
follow-up questions can be answered directly.
```

- [ ] **Step 3: Verify the skill definition**

Run:
```powershell
Get-Content "C:\Users\wshuhao\AI_Study\AI_general\skill-vs-agent-demo\.claude\skills\summarize-inline\SKILL.md" -TotalCount 4
```
Expected: the first line is `---`, then `name: summarize-inline`, then the description line, then `---`. The `name` must match the folder name exactly.

- [ ] **Step 4: Verify the output contract is stated**

Search the file for `exactly three bullet points` and `under 12 words`.
Expected: both present.

---

### Task 3: Add the agent

**Files:**
- Create: `AI_general/skill-vs-agent-demo/.claude/agents/summarizer.md`

**Interfaces:**
- Consumes: `article.md` from Task 1; same output format as the skill from Task 2.
- Produces: subagent `summarizer`, invoked by description or as `@agent-summarizer`, returning a report prefixed `[agent report]`.

- [ ] **Step 1: Create the agent directory**

Run: `New-Item -ItemType Directory -Force "C:\Users\wshuhao\AI_Study\AI_general\skill-vs-agent-demo\.claude\agents"`
Expected: directory exists.

- [ ] **Step 2: Write `summarizer.md` with this exact content**

```markdown
---
name: summarizer
description: Read and summarize article.md into exactly three short bullets in a separate context. Use when the user asks to delegate the demo article summary to the summarizer agent.
tools: Read
---

You are a summarization worker. Read `article.md` in the current project folder
and return exactly three bullet points, each under 12 words. Do not add an
introduction or conclusion. Do not ask questions. Prefix your reply with
`[agent report]` so the caller can tell it came from a subagent.
```

- [ ] **Step 3: Verify the agent definition**

Run:
```powershell
Get-Content "C:\Users\wshuhao\AI_Study\AI_general\skill-vs-agent-demo\.claude\agents\summarizer.md" -TotalCount 5
```
Expected: `---`, `name: summarizer`, a description, `tools: Read`, `---`. The `tools` field must be exactly `Read`.

- [ ] **Step 4: Verify the output contract is stated**

Search the file for `exactly three bullet points`, `under 12 words`, and `[agent report]`.
Expected: all three present.

---

### Task 4: Write the README walkthrough

**Files:**
- Create: `AI_general/skill-vs-agent-demo/README.md`

**Interfaces:**
- Consumes: `/summarize-inline` from Task 2 and `summarizer` from Task 3.
- Produces: the instructions a reader follows to run both experiments.

- [ ] **Step 1: Write `README.md` with this exact content**

````markdown
# Skill vs Agent — A Minimal Demo

One folder, one task, two ways to run it. The task: summarize `article.md` in
three bullets.

## What You Need

- Claude Code installed and signed in. Check it with:

  ```powershell
  claude --version
  ```

  If the command is not found, install Claude Code first:
  https://code.claude.com/docs/en/overview

## How to Run It, Step by Step

### Step 1 — Open a terminal in this folder

```powershell
cd C:\Users\wshuhao\AI_Study\AI_general\skill-vs-agent-demo
```

Use your own path if you copied the folder somewhere else.

### Step 2 — Start Claude Code

```powershell
claude
```

Wait for the prompt. `.claude/` is discovered from the folder where the
session starts, so starting here matters.

### Step 3 — Run the skill

Type this at the Claude Code prompt and press Enter:

```text
/summarize-inline
```

Expected: Claude reads `article.md` and replies with exactly three bullets,
each under 12 words.

### Step 4 — Test the skill's context

Ask this follow-up:

```text
Which two pigment names does the article give for yellow and orange?
```

Expected: an answer from the article that is already in this conversation. The
skill ran here, so Claude can answer without another tool call.

### Step 5 — Clear the conversation

Type:

```text
/clear
```

This removes the article from context so the next experiment starts clean.

### Step 6 — Run the agent

Type:

```text
Use the summarizer agent to summarize article.md. Do not read the file
yourself; delegate the reading.
```

Expected: the main conversation delegates to the `summarizer` subagent. Only
its final report comes back, starting with `[agent report]`, with three
bullets.

### Step 7 — Test the agent's context

Ask the same source-detail follow-up:

```text
Which two pigment names does the article give for yellow and orange?
```

Expected: the main conversation has only the agent's three bullets, and they do
not name both pigments. It must read `article.md` itself or delegate again. That
extra step is the demonstration.

### Step 8 — Exit

Type:

```text
/exit
```

(or press Ctrl+C twice).

## The Difference in One Table

| | Skill (`/summarize-inline`) | Agent (`summarizer`) |
|---|---|---|
| What runs | Instructions in the main conversation | A separate worker with its own context |
| What you see | The whole process and the source text | Only the final report |
| Follow-up about the source | Answered from context | Requires reading the file or re-delegating |
| Can it ask you questions? | Yes, it is the main conversation | No |
| Good for | Procedures, checklists, reusable knowledge | Delegated work you want summarized back |

## Files

```text
skill-vs-agent-demo/
├── .claude/
│   ├── skills/summarize-inline/SKILL.md   # the skill: HOW to do it
│   └── agents/summarizer.md               # the agent: WHO does it
├── article.md                             # the input for both experiments
└── README.md                              # this file
```

## Notes

- Both paths produce the same three-bullet shape on purpose; only the
  execution model differs.
- The skill and agent definitions are ordinary Markdown files. Open them —
  there is nothing hidden.
````

- [ ] **Step 2: Verify the README covers both paths and the run steps**

Search for `claude --version`, `Step 1`, `Step 8`, `/summarize-inline`,
`Use the summarizer agent`, `/clear`, `[agent report]`, `/exit`, and
`Which two pigment names`.
Expected: all nine present.

---

### Task 5: Acceptance walkthrough

**Files:** none — verification only.

- [ ] **Step 1: Verify the file tree**

Run:
```powershell
Get-ChildItem -Recurse -File "C:\Users\wshuhao\AI_Study\AI_general\skill-vs-agent-demo" |
  Select-Object -ExpandProperty FullName
```
Expected exactly four files: `article.md`, `README.md`, `.claude\skills\summarize-inline\SKILL.md`, `.claude\agents\summarizer.md`.

- [ ] **Step 2: Verify both frontmatter blocks**

Run:
```powershell
Get-Content "C:\Users\wshuhao\AI_Study\AI_general\skill-vs-agent-demo\.claude\skills\summarize-inline\SKILL.md" -TotalCount 3
Get-Content "C:\Users\wshuhao\AI_Study\AI_general\skill-vs-agent-demo\.claude\agents\summarizer.md" -TotalCount 4
```
Expected: both start with `---` and contain the exact names `summarize-inline` and `summarizer`.

- [ ] **Step 3: Run the manual experiments**

In a fresh Claude Code session started inside the demo folder, perform the two
experiments in `README.md` in order, including the `/clear` between them.

Expected observations:
1. `/summarize-inline` → three bullets in the main conversation; the source-detail follow-up is answerable from context.
2. The agent experiment → a `[agent report]` with three bullets; the source-detail follow-up requires the main Claude to read the file or delegate again, because the bullets do not name both pigments.

This step cannot be automated; it needs an interactive Claude Code session.
