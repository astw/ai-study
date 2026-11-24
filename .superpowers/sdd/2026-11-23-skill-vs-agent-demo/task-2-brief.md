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

