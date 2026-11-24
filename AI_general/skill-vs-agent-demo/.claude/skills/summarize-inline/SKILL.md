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
