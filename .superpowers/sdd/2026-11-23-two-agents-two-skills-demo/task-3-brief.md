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

