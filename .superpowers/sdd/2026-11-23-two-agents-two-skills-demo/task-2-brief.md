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

