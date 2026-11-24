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

