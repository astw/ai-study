# Design: Leveled Release QA Study Sets (Junior / Mid / Behavior-Leadership)

Date: 2026-11-18
Status: Approved (2026-11-18)

## Goal

Split the existing Release QA interview-prep content (`release_qa_1000_questions_answers.md`, `release_qa_mcq_100_scenarios_mock_interview.md`) into two leveled sets — junior and mid-level — plus a shared behavior/leadership file. Originals stay untouched. Mid-level set includes a new simple "Testing tools" section introducing Playwright, Selenium, Postman, and JMeter (no k6).

## Files (5 new, 2 existing untouched)

| File | Contents |
|---|---|
| `release_qa_junior_questions_answers.md` | Junior Q&A bank, curated + simplified |
| `release_qa_junior_practice.md` | Junior practice: MCQs, scenarios, mock interview |
| `release_qa_mid_questions_answers.md` | Mid-level Q&A bank, deeper answers + Testing tools section |
| `release_qa_mid_practice.md` | Mid-level practice: harder MCQs, deeper scenarios, mock interview |
| `release_qa_behavior_leadership.md` | Shared: behavior (STAR) questions + QA judgment split into junior judgment and leadership parts |

Also update `CLAUDE.md` to describe the new files.

## Format change applied to both levels

Drop the original 5-angle-per-concept repetition (definition / importance / validate / evidence / failure). Each concept becomes a natural 3-part cycle:

1. **What is X?** — plain definition.
2. **Why does it matter in release QA?** — a real consequence, not the canned "reduces release uncertainty" boilerplate.
3. **How would you test / handle it?** — concrete steps.

No contrived questions (e.g., "What evidence would you collect for release calendar?" is out).

## Junior set

### `release_qa_junior_questions_answers.md`

Topics kept: Release fundamentals; test strategy & planning; build & deployment validation (smoke, entry/exit criteria); functional testing (test design techniques: boundary, equivalence, positive/negative); regression basics; defect management (severity vs priority, bug lifecycle, good bug reports); CI/CD basics (what CI/CD is); API basics (HTTP verbs, status codes); web/UI basics; database & migration basics; agile/scrum basics; documentation & evidence; risk troubleshooting basics.

Dropped or trimmed: performance engineering depth, security penetration depth, mobile depth, canary/blue-green (one-line mention max), leadership (moved to file 5).

Target: ~150–180 Q&As. Answers 2–4 sentences, plain language.

### `release_qa_junior_practice.md`

- Part 1: ~50 MCQs (junior difficulty), `**Answer: X.**` + one-sentence explanation.
- Part 2: ~30 scenarios, `**Situation:**` + `**Recommended response:**`.
- Part 3: 15 mock-interview questions with junior-level sample answers.
- Closing: short version of the 7-step answer framework (kept — it is level-appropriate for both).

## Mid-level set

### `release_qa_mid_questions_answers.md`

Same topic skeleton as junior plus mid-level concepts added back: performance testing types + JMeter, security testing basics, DB migration/rollback testing, API testing with Postman, canary/blue-green, risk-based testing, release metrics, incident response.

Answers deepened to 4–7 sentences with specifics, trade-offs, and follow-up-proof detail.

**Testing tools section (simple, per user request):** for each of Playwright, Selenium, Postman, JMeter — what it is, what it is used for, a minimal example of typical use, and a "when to choose which" comparison (Playwright vs Selenium; Postman for API; JMeter for performance). No k6, no deep tutorials.

Target: ~200–250 Q&As including the tool section.

### `release_qa_mid_practice.md`

- Part 1: ~50 MCQs, harder than junior.
- Part 2: ~40 scenarios with more nuanced recommended responses (trade-offs, escalation, risk acceptance).
- Part 3: 15 mock-interview questions with deeper sample answers.

## `release_qa_behavior_leadership.md`

- Part 1: ~30 behavior questions with STAR-format guidance, usable at both levels.
- Part 2: Junior QA judgment (~15 Q&As).
- Part 3: Leadership/judgment (~25 Q&As, reworked from the original's "Leadership and senior QA judgment" topic 951–1000, deeper than the templated originals).

## Conventions

- Markdown Q&A style matching the originals: `#` title, `##` topic, `###` numbered question; continuous numbering per file.
- Plain English, no placeholder text, no boilerplate.
- No git repository in this directory — design doc is not committed; noted for the record.

## Out of scope

- No k6 content anywhere.
- No deep tool tutorials, no code exercises.
- Originals are not modified or deleted.
