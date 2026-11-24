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
Which bullet is the most surprising, and why?
```

Expected: an answer immediately, without re-reading the file. The skill ran in
this conversation, so the article is already in context.

### Step 5 — Clear the conversation

Type:

```text
/clear
```

This removes the article from context so the next experiment starts clean.

### Step 6 — Run the agent

Type:

```text
Use the summarizer agent to summarize article.md.
```

Expected: the main conversation delegates to the `summarizer` subagent. Only
its final report comes back, starting with `[agent report]`, with three
bullets.

### Step 7 — Test the agent's context

Ask the same follow-up:

```text
Which bullet is the most surprising, and why?
```

Expected: the main conversation cannot answer from the agent's memory — the
agent is gone. It must read `article.md` itself or delegate again. That extra
step is the demonstration.

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
| Follow-up questions | Answered from context | Require re-reading or re-delegating |
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
`Use the summarizer agent`, `/clear`, `[agent report]`, and `/exit`.
Expected: all eight present.

---

