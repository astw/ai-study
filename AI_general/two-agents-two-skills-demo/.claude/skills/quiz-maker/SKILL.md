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
