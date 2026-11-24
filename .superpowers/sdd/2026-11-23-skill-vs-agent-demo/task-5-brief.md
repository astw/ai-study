### Task 5: Acceptance walkthrough

**Files:** none — verification only.

- [ ] **Step 1: Verify the file tree**

Run:
```powershell
Get-ChildItem -Recurse -File "C:\Users\wshuhao\AI_Study\AI_general\skill-vs-agent-demo" |
  Select-Object -ExpandProperty FullName
```
Expected exactly four files: `article.md`, `README.md`, `.claude\skills\summarize-inline\SKILL.md`, `.claude\agents\summarizer.md`.

- [ ] **Step 2: Verify both frontmatter blocks**

Run:
```powershell
Get-Content "C:\Users\wshuhao\AI_Study\AI_general\skill-vs-agent-demo\.claude\skills\summarize-inline\SKILL.md" -TotalCount 3
Get-Content "C:\Users\wshuhao\AI_Study\AI_general\skill-vs-agent-demo\.claude\agents\summarizer.md" -TotalCount 4
```
Expected: both start with `---` and contain the exact names `summarize-inline` and `summarizer`.

- [ ] **Step 3: Run the manual experiments**

In a fresh Claude Code session started inside the demo folder, perform the two
experiments in `README.md` in order, including the `/clear` between them.

Expected observations:
1. `/summarize-inline` → three bullets in the main conversation; follow-up answerable from context.
2. The agent experiment → a `[agent report]` with three bullets; the follow-up requires the main Claude to read the file or delegate again.

This step cannot be automated; it needs an interactive Claude Code session.
