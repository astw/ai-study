# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository overview

This is not a software project: it is a static content set for Release QA / Release Test Engineer interview preparation. There is no source code, no build system, no package manager, no linter, and no tests — nothing to build, run, or install. The directory is not a git repository.

Seven Markdown documents, in three groups:

- **Originals (reference, untouched):**
  - `release_qa_1000_questions_answers.md` — 1,000 Q&As in the legacy 5-angle format.
  - `release_qa_mcq_100_scenarios_mock_interview.md` — legacy practice set (100 MCQ + 100 scenarios + 25 interview questions).
- **Leveled sets (the current study material):**
  - `release_qa_junior_questions_answers.md` — junior Q&A bank (186 Q&As).
  - `release_qa_junior_practice.md` — 50 MCQ + 30 scenarios + 15 interview questions.
  - `release_qa_mid_questions_answers.md` — mid-level Q&A bank (250 Q&As) including the Testing tools section.
  - `release_qa_mid_practice.md` — 50 MCQ + 40 scenarios + 15 interview questions.
  - `release_qa_behavior_leadership.md` — 30 behavior (STAR) questions + 40 judgment Q&As (15 junior, 25 leadership).
- **Process docs:** `docs/superpowers/specs/` and `docs/superpowers/plans/` hold the design spec and implementation plan for the leveled sets.

## Leveled files: shared conventions

The five leveled files use a consistent question cycle — the 3-part format that replaced the originals' 5-angle boilerplate:

1. What is X?
2. Why does X matter in release QA? (a real consequence, never the canned "reduces release uncertainty" line)
3. How would you test or handle X? (concrete steps; 2–4 sentences junior, 4–7 mid)

Format details:
- Heading levels: `#` title, `##` topic/part, `###` numbered question. Numbering is continuous 1..N per file.
- MCQ format: options A–D, then `**Answer: X.**` + explanation. Mid-level explanations must state why the other options lose.
- Scenario format: `**Situation:**` + `**Recommended response:**`. Mid-level responses cover verify / involve / evidence / release decision.
- Behavior format: question + "What they're looking for" + `**Sample answer (STAR):**` with Situation/Task/Action/Result.
- Judgment format: `### Judgment question N. ...` + `**Answer:**`.
- The Testing tools section (mid Q&A file, Q232–250) introduces Playwright, Selenium, Postman, JMeter only — no k6, no deep tutorials (snippets 5–15 lines max).

## Original files (legacy format)

The originals remain for reference and are not edited. Their conventions are documented here for completeness:

`release_qa_1000_questions_answers.md`: 20 topic sections × 50 questions, numbered 1–1000, each concept asked 5 ways (what / why / validate / evidence / failure) with templated boilerplate answers.

`release_qa_mcq_100_scenarios_mock_interview.md`: three parts (MCQ / scenarios / mock interview) plus the 7-step answer framework and interview reminders; the leveled practice files reuse its framework and reminders.

## Editing conventions

When editing the leveled files, preserve the 3-part cycle, the per-file numbering, and the answer-length norms (junior plain and short, mid specific with trade-offs). New Q&As follow the existing templates above. Do not add k6 content, and do not modify the two original files unless the user explicitly asks.
