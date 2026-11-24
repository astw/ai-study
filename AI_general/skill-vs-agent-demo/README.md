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
