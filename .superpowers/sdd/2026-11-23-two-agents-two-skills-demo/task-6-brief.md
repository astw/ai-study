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
Do not read article.md or the skill files yourself.
```

Expected: two reports in one turn.

- `[bullet report]` — exactly three bullets, each under 12 words.
- `[quiz report]` — exactly three numbered Q&A pairs, each answer under 20
  words.

The two formats come from the two skills, and each skill was loaded inside its
own agent, not in this conversation.

### Step 4 — Test the main conversation's knowledge of the source

Ask:

```text
Which two pigment names does the article give for yellow and orange?
```

Expected: the main conversation cannot answer from memory. It must read
`article.md` or delegate again. Allow the read when it asks, and notice the
extra step.

### Step 5 — Test the main conversation's knowledge of the skills

Ask:

```text
Without reading files or asking the agents, what procedure did quiz-writer follow?
```

Expected: it cannot say. The skill text never entered the main context.

Then ask:

```text
Ask quiz-writer to report the procedure it was given.
```

Expected: the agent can quote the `quiz-maker` procedure, because the skill was
preloaded into its context.

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
- To change a format, edit that skill only; the agent picks it up at startup.
- The article is the same text as `../skill-vs-agent-demo/article.md`, so the
  two demos can be compared side by side.
````

- [ ] **Step 2: Verify the README covers both agents and all observations**

Run: `Select-String -Path "C:\Users\wshuhao\AI_Study\AI_general\two-agents-two-skills-demo\README.md" -Pattern "claude --version|Start inside this folder|Do not read article.md|bullet-summarizer|quiz-writer|\[bullet report\]|\[quiz report\]|Which two pigment names|Without reading files|Ask quiz-writer"`
Expected: at least ten matching lines, covering every pattern at least once.

---

