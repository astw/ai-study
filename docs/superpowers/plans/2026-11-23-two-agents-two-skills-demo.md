# Two Agents, Two Skills Demo Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a six-file, runnable Claude Code demo where two subagents run in parallel, each preloaded with one different project skill.

**Architecture:** A self-contained folder with a `.claude/` project config. Two skills define two distinctly different output contracts; two agents bind one skill each through the `skills:` frontmatter field; one shared article; a README that walks through the dispatch and three observations about where the source and the skills live.

**Tech Stack:** Markdown only — Claude Code skill and subagent definitions, no code, no dependencies.

**Spec:** `docs/superpowers/specs/2026-11-23-two-agents-two-skills-demo-design.md`

## Global Constraints

- Everything lives under `C:\Users\wshuhao\AI_Study\AI_general\two-agents-two-skills-demo\`.
- No application code, test suite, build step, or dependency.
- Each output contract appears only in its own `SKILL.md` — never in an agent body or the README run prompt. (The README's expected-output notes may state the shape; they are how the reader checks the result.)
- Agent frontmatter must be `tools: Read` and a `skills:` list containing exactly one name that matches both the skill folder and the skill's `name:` field.
- Skills must not set `disable-model-invocation: true`; preloading skips such skills.
- Do not commit: the user has not asked for this demo to be committed.
- The README must instruct starting Claude Code inside the demo folder, or `.claude/` is not discovered.
- The run prompt must forbid reading the source or skill files and invoking either skill in the main conversation.

## Review Focus

- Starting Claude Code outside the demo folder means `.claude/` is never discovered; README Step 1 starts inside it and Step 2 warns why.
- Leaking an output contract into an agent body or the run prompt makes a correctly shaped report prove nothing; Tasks 4 and 5 verify the contract text is absent from the agents.
- A typo in a `skills:` entry or a skill's `name:` silently skips preloading; Tasks 2–5 verify the exact names.
- The main conversation reading the article or skill files instead of delegating hides the lesson; the run prompt forbids it, and README Steps 4–5 treat the extra read or re-delegation as the observation.
- An agent without `Read` cannot open the article; Tasks 4 and 5 verify `tools: Read` exactly.

---

### Task 1: Create the folder and the article

**Files:**
- Create: `AI_general/two-agents-two-skills-demo/article.md`

**Interfaces:**
- Consumes: nothing.
- Produces: `article.md` — the shared source read by both agents (Tasks 4–5).

- [ ] **Step 1: Create the demo folder**

Run: `New-Item -ItemType Directory -Force "C:\Users\wshuhao\AI_Study\AI_general\two-agents-two-skills-demo"`
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

Run: `(Get-Content "C:\Users\wshuhao\AI_Study\AI_general\two-agents-two-skills-demo\article.md" | Measure-Object -Word).Words`
Expected: a number between 100 and 160.

---

### Task 2: Add the `bullet-summary` skill

**Files:**
- Create: `AI_general/two-agents-two-skills-demo/.claude/skills/bullet-summary/SKILL.md`

**Interfaces:**
- Consumes: `article.md` from Task 1.
- Produces: skill `bullet-summary`, preloadable by name; output contract "exactly three bullet points, each under 12 words".

- [ ] **Step 1: Create the skill directory**

Run: `New-Item -ItemType Directory -Force "C:\Users\wshuhao\AI_Study\AI_general\two-agents-two-skills-demo\.claude\skills\bullet-summary"`
Expected: directory exists.

- [ ] **Step 2: Write `SKILL.md` with this exact content**

```markdown
---
name: bullet-summary
description: Produce a three-bullet summary of article.md. Preloaded into the bullet-summarizer subagent; not used in the main conversation.
---

# Bullet Summary

When used:

1. Read `article.md` in the current project folder.
2. Summarize it as exactly three bullet points.
3. Keep each bullet under 12 words.
4. Output only the bullets — no introduction, no conclusion.
```

- [ ] **Step 3: Verify the skill name matches the folder**

Run: `Get-Content "C:\Users\wshuhao\AI_Study\AI_general\two-agents-two-skills-demo\.claude\skills\bullet-summary\SKILL.md" -TotalCount 3`
Expected: `---`, then `name: bullet-summary`, then the description line.

- [ ] **Step 4: Verify the contract is stated and the skill is preloadable**

Run: `Select-String -Path "C:\Users\wshuhao\AI_Study\AI_general\two-agents-two-skills-demo\.claude\skills\bullet-summary\SKILL.md" -Pattern "exactly three bullet points|under 12 words"`

Then: `Select-String -Path "C:\Users\wshuhao\AI_Study\AI_general\two-agents-two-skills-demo\.claude\skills\bullet-summary\SKILL.md" -Pattern "disable-model-invocation"`
Expected: the first command prints both matching lines; the second prints nothing.

---

### Task 3: Add the `quiz-maker` skill

**Files:**
- Create: `AI_general/two-agents-two-skills-demo/.claude/skills/quiz-maker/SKILL.md`

**Interfaces:**
- Consumes: `article.md` from Task 1.
- Produces: skill `quiz-maker`, preloadable by name; output contract "exactly three question-and-answer pairs in a numbered Q/A layout, each answer under 20 words".

- [ ] **Step 1: Create the skill directory**

Run: `New-Item -ItemType Directory -Force "C:\Users\wshuhao\AI_Study\AI_general\two-agents-two-skills-demo\.claude\skills\quiz-maker"`
Expected: directory exists.

- [ ] **Step 2: Write `SKILL.md` with this exact content**

```markdown
---
name: quiz-maker
description: Write three question-and-answer pairs from article.md. Preloaded into the quiz-writer subagent; not used in the main conversation.
---

# Quiz Maker

When used:

1. Read `article.md` in the current project folder.
2. Write exactly three question-and-answer pairs about its content.
3. Format each pair as two lines: `Q1: <question>` then `A1: <answer>`; number from 1 to 3.
4. Keep each answer under 20 words.
5. Output only the six lines — no introduction, no conclusion.
```

- [ ] **Step 3: Verify the skill name matches the folder**

Run: `Get-Content "C:\Users\wshuhao\AI_Study\AI_general\two-agents-two-skills-demo\.claude\skills\quiz-maker\SKILL.md" -TotalCount 3`
Expected: `---`, then `name: quiz-maker`, then the description line.

- [ ] **Step 4: Verify the contract is stated and the skill is preloadable**

Run: `Select-String -Path "C:\Users\wshuhao\AI_Study\AI_general\two-agents-two-skills-demo\.claude\skills\quiz-maker\SKILL.md" -Pattern "exactly three question-and-answer pairs|under 20 words|Q1:"`

Then: `Select-String -Path "C:\Users\wshuhao\AI_Study\AI_general\two-agents-two-skills-demo\.claude\skills\quiz-maker\SKILL.md" -Pattern "disable-model-invocation"`
Expected: the first command prints the matching lines; the second prints nothing.

---

### Task 4: Add the `bullet-summarizer` agent

**Files:**
- Create: `AI_general/two-agents-two-skills-demo/.claude/agents/bullet-summarizer.md`

**Interfaces:**
- Consumes: skill `bullet-summary` from Task 2; `article.md` from Task 1.
- Produces: subagent `bullet-summarizer`, invoked by description or as `@agent-bullet-summarizer`, replying with a `[bullet report]` prefix.

- [ ] **Step 1: Create the agents directory**

Run: `New-Item -ItemType Directory -Force "C:\Users\wshuhao\AI_Study\AI_general\two-agents-two-skills-demo\.claude\agents"`
Expected: directory exists.

- [ ] **Step 2: Write `bullet-summarizer.md` with this exact content**

```markdown
---
name: bullet-summarizer
description: Summarize article.md with the preloaded bullet-summary skill. Used by the two-agent parallel demo.
tools: Read
skills:
  - bullet-summary
---

You are the bullet-summary worker. Follow the preloaded bullet-summary skill
exactly. Read `article.md` in the current project folder, apply the skill's
procedure, and return the skill's output. Do not ask questions. Prefix your
reply with `[bullet report]`.
```

- [ ] **Step 3: Verify the frontmatter**

Run: `Get-Content "C:\Users\wshuhao\AI_Study\AI_general\two-agents-two-skills-demo\.claude\agents\bullet-summarizer.md" -TotalCount 7`
Expected: `---`, `name: bullet-summarizer`, a description, `tools: Read`, `skills:`, `  - bullet-summary`, `---`.

- [ ] **Step 4: Verify the output contract is not restated in the agent**

Run: `Select-String -Path "C:\Users\wshuhao\AI_Study\AI_general\two-agents-two-skills-demo\.claude\agents\bullet-summarizer.md" -Pattern "exactly three|12 words|bullet point"`
Expected: no output. The contract must exist only in `SKILL.md`.

---

### Task 5: Add the `quiz-writer` agent

**Files:**
- Create: `AI_general/two-agents-two-skills-demo/.claude/agents/quiz-writer.md`

**Interfaces:**
- Consumes: skill `quiz-maker` from Task 3; `article.md` from Task 1.
- Produces: subagent `quiz-writer`, invoked by description or as `@agent-quiz-writer`, replying with a `[quiz report]` prefix.

- [ ] **Step 1: Write `quiz-writer.md` with this exact content** (the agents directory already exists)

```markdown
---
name: quiz-writer
description: Write quiz questions from article.md with the preloaded quiz-maker skill. Used by the two-agent parallel demo.
tools: Read
skills:
  - quiz-maker
---

You are the quiz-maker worker. Follow the preloaded quiz-maker skill exactly.
Read `article.md` in the current project folder, apply the skill's procedure,
and return the skill's output. Do not ask questions. Prefix your reply with
`[quiz report]`.
```

- [ ] **Step 2: Verify the frontmatter**

Run: `Get-Content "C:\Users\wshuhao\AI_Study\AI_general\two-agents-two-skills-demo\.claude\agents\quiz-writer.md" -TotalCount 7`
Expected: `---`, `name: quiz-writer`, a description, `tools: Read`, `skills:`, `  - quiz-maker`, `---`.

- [ ] **Step 3: Verify the output contract is not restated in the agent**

Run: `Select-String -Path "C:\Users\wshuhao\AI_Study\AI_general\two-agents-two-skills-demo\.claude\agents\quiz-writer.md" -Pattern "exactly three|under 20 words|Q1:|A1:"`
Expected: no output. The contract must exist only in `SKILL.md`.

---

### Task 6: Write the README walkthrough

**Files:**
- Create: `AI_general/two-agents-two-skills-demo/README.md`

**Interfaces:**
- Consumes: `bullet-summarizer` from Task 4 and `quiz-writer` from Task 5.
- Produces: the instructions a reader follows to run the parallel experiment and observe the three context facts.

- [ ] **Step 1: Write `README.md` with this exact content**

````markdown
# Two Agents, Two Skills — A Parallel Demo

One folder, one article, two workers. Each subagent is preloaded with a
different skill; both run at the same time and report back.

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
cd C:\Users\wshuhao\AI_Study\AI_general\two-agents-two-skills-demo
```

Use your own path if you copied the folder somewhere else.

### Step 2 — Start Claude Code

```powershell
claude
```

Start inside this folder so `.claude/` is discovered. Starting elsewhere means
neither agent nor either skill is found.

### Step 3 — Dispatch both agents in parallel

Type this at the Claude Code prompt and press Enter:

```text
Use the bullet-summarizer and quiz-writer agents in parallel on article.md.
Do not read article.md or the skill files yourself, and do not invoke either
skill in this conversation; only the agents should use them.
```

Expected: both agents start from this one prompt and run concurrently. Each
report arrives when it finishes, as a completion notification — wait for both
before Step 4.

- `[bullet report]` — exactly three bullets, each under 12 words.
- `[quiz report]` — exactly three numbered Q&A pairs, each answer under 20
  words.

The two formats come from the two skills, and each skill was loaded inside its
own agent, not in this conversation.

### Step 4 — Test the main conversation's knowledge of the source

Ask:

```text
Quote the first sentence of article.md exactly, word for word.
```

Expected: the main conversation cannot quote it from memory; the article's
text never entered its context. It must read `article.md` or delegate again.
Allow the read when it asks, and notice the extra step.

### Step 5 — Test the main conversation's knowledge of the skills

Ask:

```text
Without reading files or asking the agents, list the exact five numbered steps the quiz-maker skill gave quiz-writer.
```

Expected: it can name the skill and its description, but not the steps. The
skill body never entered the main context.

Then ask:

```text
Ask quiz-writer to quote the exact five numbered steps of the quiz-maker skill it was given. Do not write quiz questions.
```

Expected: the agent can quote the five steps, because the skill was preloaded
into its context.

### Step 6 — Exit

Type:

```text
/exit
```

(or press Ctrl+C twice).

## The Setup in One Table

| | `bullet-summarizer` | `quiz-writer` |
|---|---|---|
| Skill preloaded | `bullet-summary` | `quiz-maker` |
| Output | 3 bullets, each under 12 words | 3 Q&A pairs, answers under 20 words |
| Context | Its own | Its own |
| What the parent sees | `[bullet report]` only | `[quiz report]` only |

## Files

```text
two-agents-two-skills-demo/
├── .claude/
│   ├── skills/
│   │   ├── bullet-summary/SKILL.md   # contract: 3 bullets
│   │   └── quiz-maker/SKILL.md       # contract: 3 Q&A pairs
│   └── agents/
│       ├── bullet-summarizer.md      # preloads bullet-summary
│       └── quiz-writer.md            # preloads quiz-maker
├── article.md                        # the shared source
└── README.md                         # this file
```

## Notes

- The output contracts live only in the `SKILL.md` files. The agents and the
  prompt above do not restate them, so a correctly shaped report shows the
  skill did the work.
- If the main conversation answers a Step 4 or Step 5 probe without reading,
  delegating, or quoting, it used general knowledge or the skill descriptions.
  Ask for the exact quote or the exact list to expose the difference.
- To change a format, edit that skill only; the agent picks it up at startup.
- The article is the same text as `../skill-vs-agent-demo/article.md`, so the
  two demos can be compared side by side.
````

- [ ] **Step 2: Verify the README covers both agents and all observations**

Run: `Select-String -Path "C:\Users\wshuhao\AI_Study\AI_general\two-agents-two-skills-demo\README.md" -Pattern "claude --version|Start inside this folder|Do not read article.md|do not invoke either|bullet-summarizer|quiz-writer|\[bullet report\]|\[quiz report\]|Quote the first sentence|Without reading files|five numbered steps|Ask quiz-writer"`
Expected: at least twelve matching lines, covering every pattern at least once.

---

### Task 7: Acceptance walkthrough

**Files:** none — verification only.

- [ ] **Step 1: Verify the file tree**

Run: `Get-ChildItem -Recurse -File "C:\Users\wshuhao\AI_Study\AI_general\two-agents-two-skills-demo" | Select-Object -ExpandProperty FullName`
Expected exactly six files: `article.md`, `README.md`, `.claude\skills\bullet-summary\SKILL.md`, `.claude\skills\quiz-maker\SKILL.md`, `.claude\agents\bullet-summarizer.md`, `.claude\agents\quiz-writer.md`.

- [ ] **Step 2: Verify the skill bindings**

Run:
```powershell
Select-String -Path "C:\Users\wshuhao\AI_Study\AI_general\two-agents-two-skills-demo\.claude\agents\*.md" -Pattern "^name:|^tools:|^  - "
```
Expected: `name: bullet-summarizer` with `tools: Read` and `- bullet-summary`; `name: quiz-writer` with `tools: Read` and `- quiz-maker`.

- [ ] **Step 3: Verify no contract leaked into the agents**

Run: `Select-String -Path "C:\Users\wshuhao\AI_Study\AI_general\two-agents-two-skills-demo\.claude\agents\*.md" -Pattern "exactly three|under 12 words|under 20 words|Q1:|bullet point"`
Expected: no output.

- [ ] **Step 4: Run the manual experiment**

In a fresh Claude Code session started inside the demo folder, follow
`README.md` Steps 3–5 in order.

Expected observations:
1. Both agents start from the one prompt and run concurrently; the reports arrive as completion notifications: `[bullet report]` with three short bullets and `[quiz report]` with three Q&A pairs, proving each agent followed its own preloaded skill.
2. The exact-quote follow-up requires the main Claude to read `article.md` or delegate, because the article never entered its context.
3. The five-steps follow-up cannot be answered from the main context; asking `quiz-writer` returns the steps, because the skill lives inside that agent.

This step cannot be automated; it needs an interactive Claude Code session.
