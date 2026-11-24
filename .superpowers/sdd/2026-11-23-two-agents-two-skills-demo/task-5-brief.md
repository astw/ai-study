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

