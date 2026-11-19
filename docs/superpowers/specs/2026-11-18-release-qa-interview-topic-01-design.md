# Release QA Interview Topic 1 — Design

**Date:** 2026-11-18
**Status:** Approved by the user in conversation.

## Intent

A self-test question bank for a mid-level release QA interview, covering test
methodologies, the software development life cycle, and testing types. The
reader studies alone: question first, answer hidden until revealed.

## Goals

- 100 interview-style Q&A with answers of 2–5 sentences.
- 150 four-option MCQs with an answer and an explanation each.
- Answers hidden in `<details>` blocks so the bank works for self-testing.
- A short README so later topics can sit beside this one.
- Plain language matching the existing guides; scenario-heavy, release-QA
  oriented.

## Non-goals

- Kanban content (explicitly excluded by the user).
- Tool-specific automation (Selenium, Playwright, JMeter, and similar).
- Certification trivia or exam-dump style questions.
- Topic 2 and later topics.
- A mock interview schedule or scoring system.

## Constraints

- Markdown only; no build step.
- Folder: `release-qa-interview/topic-01-test-methodologies-and-sdlc/`.
- Files: `README.md`, `qa-100.md`, `mcq-150.md`.
- Exact counts: Q&A 25/40/20/15 by part; MCQ 30/60/40/20 by part.
- Continuous numbering Q1–Q100 and MCQ 1–150.
- Four options A–D per MCQ; one correct; the explanation names the trap.
- No near-duplicate stems within or across the two files.
- Correct-answer letters spread roughly evenly (30–45 per letter).
- Mid-level depth (roughly 2–5 years of QA experience).

## Approaches considered

1. **Two files, hidden answers (chosen).** `qa-100.md` and `mcq-150.md`,
   part-level table of contents, answers in `<details>`. Best for self-testing;
   renders on GitHub and VS Code preview.
2. **Two files, inline answers.** Simpler Markdown, but it spoils self-testing.
3. **Split by subtopic into about ten files.** Easier to navigate one area, but
   more files and more index maintenance for the same content.

## Coverage

| Part | Q&A | MCQ | Contents |
|---|---|---|---|
| 1. SDLC fundamentals and models | 25 | 30 | phases, Waterfall, V-model, iterative/incremental, spiral, Agile/Scrum, SDLC vs STLC, shift-left/right, DevOps, release vs deploy |
| 2. Test levels and testing types | 40 | 60 | unit, integration, system, acceptance/UAT, alpha/beta; smoke, sanity, regression, retest, build verification; performance, load, stress, spike, soak, volume, scalability; security, usability, compatibility, accessibility, localization, recovery; black/gray/white box, static/dynamic |
| 3. Design techniques and methodologies | 20 | 40 | equivalence partitioning, boundary values, decision tables, state transition, pairwise, use case, error guessing, exploratory, risk-based, TDD/BDD/ATDD, test pyramid, strategy vs plan |
| 4. Release QA in practice | 15 | 20 | entry/exit criteria, test plan vs strategy, traceability, severity vs priority, regression scope, go/no-go, test summary report, metrics, hotfix verification, sign-off |

## Question rules

- Q&A: one concept per question; answer 2–5 sentences; an example where it
  clarifies.
- MCQ: stem, four options, one correct, plausible distractors; explanation
  1–3 sentences; about 40% workplace scenarios; no "all of the above".
- Part headings carry their counts; table-of-contents anchors match.
- Plain English; define jargon on first use in an answer.

## Verification

Inline Python checks after each build task: per-part counts, continuous
numbering, `<details>` balance, MCQ option sets and one answer line, TOC
anchors, duplicate normalized stems, and answer-letter distribution. A final
read checks tone, duplicate ideas, and that every explanation eliminates the
nearest distractor.
