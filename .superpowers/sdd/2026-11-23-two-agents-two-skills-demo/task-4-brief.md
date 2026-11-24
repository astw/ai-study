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

