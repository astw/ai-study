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
1. Two reports return in one turn: `[bullet report]` with three short bullets and `[quiz report]` with three Q&A pairs, proving each agent followed its own preloaded skill.
2. The source-detail follow-up requires the main Claude to read `article.md` or delegate, because the article never entered its context.
3. The skill-detail follow-up cannot be answered from the main context; asking `quiz-writer` returns the procedure, because the skill lives inside that agent.

This step cannot be automated; it needs an interactive Claude Code session.
