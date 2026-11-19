# Leveled Release QA Study Sets — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task (inline execution; content files need one consistent authorial voice, so subagent dispatch is not recommended here). Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce five leveled Release QA interview-prep markdown files (junior Q&A + junior practice + mid Q&A + mid practice + behavior/leadership) and update CLAUDE.md, leaving the two originals untouched.

**Architecture:** Curate + deepen the existing content. Every concept uses a 3-part cycle (What is / Why it matters / How to test or handle). Mid-level adds a simple "Testing tools" section (Playwright, Selenium, Postman, JMeter — no k6).

**Tech Stack:** None — static Markdown content. No git repository (no commit steps; verification is via grep counts and read-throughs instead of tests).

**Spec:** `docs/superpowers/specs/2026-11-18-release-qa-leveled-content-design.md`

---

## Shared format templates (used in every task)

Q&A cycle (all Q&A banks, including tool intros):

```
## <Topic name>

### N. What is <concept>?
<plain definition, 1-2 sentences>

### N+1. Why does <concept> matter in release QA?
<one real consequence; never the boilerplate "reduces release uncertainty">

### N+2. How would you test or handle <concept>?
<concrete steps, 2-3 sentences junior / 3-5 sentences mid>
```

MCQ:

```
### MCQ N. <question>
A. <option>
B. <option>
C. <option>
D. <option>
**Answer: X.** <one-sentence explanation>
```

Scenario:

```
### Scenario N. <title>
**Situation:** <1-2 sentences>
**Recommended response:** <2-4 sentences junior / 4-6 sentences mid>
```

Interview question:

```
### Interview question N. <question>
**Sample answer:** <3-5 sentences junior / 5-8 sentences mid>
```

File header pattern (adapted from originals):

```
# <Title>

**Purpose:** ...
**How to use:** ...
```

Numbering is continuous 1..N within each file. Heading levels: `#` title, `##` topic/part, `###` question. No k6, no TBD/TODO, no placeholder text, no deep tutorials (tool snippets are 5-15 lines max).

---

## Task 1: `release_qa_junior_questions_answers.md`

**Files:**
- Create: `F:\for-qa\release_qa_junior_questions_answers.md`

- [ ] **Step 1: Write header + Release fundamentals (Q1–Q21)**

Header: "Junior Release QA — Questions & Answers", purpose line: "Foundational interview prep for junior Release QA / QA tester roles."

Concepts (3-part cycle each, junior depth 2-4 sentence answers): release candidate; release scope; release criteria; code freeze; release branch; go/no-go decision; rollback plan. (7 concepts = 21 Q&As)

- [ ] **Step 2: Test strategy and planning (next 18 Q&As)**

Concepts: test strategy; test plan; test case; test data; test environment; test coverage. (6 concepts = 18 Q&As)

- [ ] **Step 3: Build and deployment validation (next 12 Q&As)**

Concepts: smoke testing; sanity testing; build verification; staging environment. (4 concepts = 12 Q&As)

- [ ] **Step 4: Functional testing (next 21 Q&As)**

Concepts: functional vs non-functional testing; positive and negative testing; boundary value analysis; equivalence partitioning; exploratory testing; acceptance criteria; user acceptance testing (UAT). (7 concepts = 21 Q&As)

- [ ] **Step 5: Regression and integration (next 15 Q&As)**

Concepts: regression testing; integration testing; retest vs regression; regression suite; flaky test. (5 concepts = 15 Q&As)

- [ ] **Step 6: Defect management (next 15 Q&As)**

Concepts: defect lifecycle; severity vs priority; what goes in a good bug report; defect triage; duplicate and not-a-bug defects. (5 concepts = 15 Q&As)

- [ ] **Step 7: CI/CD basics (next 9 Q&As)**

Concepts: continuous integration; continuous delivery; automated tests in the pipeline. (3 concepts = 9 Q&As)

- [ ] **Step 8: API basics (next 15 Q&As)**

Concepts: what an API is; REST; HTTP verbs; HTTP status codes; basic API testing. (5 concepts = 15 Q&As)

- [ ] **Step 9: Web and UI testing (next 12 Q&As)**

Concepts: cross-browser testing; responsive design testing; form validation; browser dev tools. (4 concepts = 12 Q&As)

- [ ] **Step 10: Database and data migration (next 12 Q&As)**

Concepts: database testing basics; data migration; data integrity; test data management. (4 concepts = 12 Q&As)

- [ ] **Step 11: Agile and collaboration (next 12 Q&As)**

Concepts: scrum; user story; definition of done; the QA role in a sprint. (4 concepts = 12 Q&As)

- [ ] **Step 12: Documentation and evidence (next 12 Q&As)**

Concepts: test evidence; release notes; test summary report; sign-off. (4 concepts = 12 Q&As)

- [ ] **Step 13: Risk and troubleshooting (next 12 Q&As)**

Concepts: risk (basic); escalation; blocking issue; post-release validation. (4 concepts = 12 Q&As)

- [ ] **Step 14: Verify**

Run: `grep -c '^### ' F:/for-qa/release_qa_junior_questions_answers.md`
Expected: 186 (62 concepts × 3). Read through the file once; fix numbering gaps, boilerplate remnants ("It matters because it reduces release uncertainty"), or placeholder text.

---

## Task 2: `release_qa_junior_practice.md`

**Files:**
- Create: `F:\for-qa\release_qa_junior_practice.md`

- [ ] **Step 1: Write header + Part 1 — 50 junior MCQs**

Header: "Junior Release QA — Practice Set (MCQ, Scenarios, Mock Interview)". Topic mix: smoke/regression basics (10), defect management (10), test design techniques (8), release process basics (8), API/status codes (6), CI/CD basics (4), agile basics (4). One best answer each; distractors must be plausible but clearly wrong.

- [ ] **Step 2: Part 2 — 30 junior scenarios**

Titles: Smoke test fails on staging; Smoke passes but one key workflow fails; Late code change after regression; Staging and production config differ; Database migration partially completes; Test data is missing; Staging environment is down before the test window; A developer says a defect is fixed; P1 defect open in a core workflow; Product owner asks to skip regression; Release notes are incomplete; A test fails only in staging; Test case expected result is wrong; A defect cannot be reproduced; Two defects are duplicates; A build is deployed with the wrong version number; Sign-off is requested but exit criteria are not met; A login form change breaks password reset; A flaky test fails in the pipeline; A required mobile device is unavailable; A stakeholder asks for a release date commitment; A hotfix is needed during code freeze; A tester is asked to approve a release they did not test; A new feature has no acceptance criteria; A critical API returns 500 in staging; A UI text change causes a layout break; A test environment runs out of disk space; A developer disagrees a defect is valid; A release is deployed but monitoring shows errors; A junior tester must report daily status.

- [ ] **Step 3: Part 3 — 15 junior mock interview questions**

Titles: Tell me about yourself as a QA tester; What is the difference between smoke, sanity, and regression testing?; How do you write a test case?; What is in a good bug report?; What is severity vs priority?; How do you test a login page?; What would you do first after a build is deployed to staging?; How do you decide what to test when time is short?; What is boundary value analysis?; How do you handle a developer who says your defect is invalid?; What is a test plan and what goes in it?; How do you test an API with Postman? (basic level); What is regression testing and when do you run it?; How do you keep test evidence?; What questions would you ask before starting testing a new feature?

- [ ] **Step 4: Closing sections**

"Practical answer framework for scenario questions" — the 7-step sequence (Clarify → Contain → Investigate → Assess impact → Communicate → Decide → Prevent recurrence), one line each. "Important interview reminders" — 6 bullets from the original file 2 (`:1440-1447`), kept verbatim.

- [ ] **Step 5: Verify**

Run: `grep -c '^### MCQ' F:/for-qa/release_qa_junior_practice.md` → 50; `grep -c '^### Scenario'` → 30; `grep -c '^### Interview'` → 15. Read through once; every MCQ must have exactly one `**Answer: X.**` line.

---

## Task 3: `release_qa_mid_questions_answers.md`

**Files:**
- Create: `F:\for-qa\release_qa_mid_questions_answers.md`

- [ ] **Step 1: Write header + Release fundamentals & strategy (first 2 topics)**

Header: "Mid-Level Release QA — Questions & Answers". Depth: 4-7 sentence answers with specifics and trade-offs; assume the reader knows junior concepts.

Release fundamentals concepts: release candidate; release scope and exclusions; release criteria and exit criteria; code freeze and exceptions; release branch strategy; canary and blue-green releases; release calendar; go/no-go decision ownership; rollback strategy. (9 concepts)
Test strategy concepts: risk-based testing; test strategy vs test plan; test coverage and traceability; test data strategy; test environment strategy; release metrics (defect escape rate, test completion). (6 concepts)

- [ ] **Step 2: Build/deploy + functional + regression**

Build and deployment validation: pipeline gates and quality gates; feature flags; deployment verification; environment parity and drift. (4 concepts)
Functional testing: test design techniques at depth (boundary, equivalence, state transition, decision tables); exploratory testing with charters; acceptance criteria and BDD basics. (3 concepts)
Regression and integration: change impact analysis; regression suite maintenance; flaky test management; integration testing strategies; retest vs regression discipline. (5 concepts)

- [ ] **Step 3: Defect management + automation/CI-CD**

Defect management: severity and priority calibration; triage leadership; defect metrics and trends; root cause analysis basics; known issues and risk acceptance. (5 concepts)
Automation and CI/CD: test pyramid; automation strategy and what to automate; pipeline design for quality gates; test environment automation; shift-left testing. (5 concepts)

- [ ] **Step 4: Performance + security + environment/config**

Performance and reliability: load testing; stress and soak testing; performance metrics (p95/p99, throughput, error rate); performance test environment realism. (4 concepts)
Security and privacy: OWASP basics; authentication and authorization testing; session and token handling; vulnerability scanning basics; privacy and data handling. (5 concepts)
Environment and configuration: configuration drift; secrets management; feature config validation; parity between staging and production. (4 concepts)

- [ ] **Step 5: Database + API + web/UI + mobile**

Database and migration: migration and rollback testing; schema compatibility (old/new versions); data integrity and anonymization; migration runbooks. (4 concepts)
API and microservices: contract testing; authentication flows; pagination, filtering, rate limiting; idempotency. (4 concepts)
Web and UI: cross-browser strategy; accessibility basics (WCAG); visual regression; UI automation basics (pointer to Testing tools). (4 concepts)
Mobile: device fragmentation; app release process and store review. (2 concepts)

- [ ] **Step 6: Monitoring + agile + governance + docs + risk**

Monitoring and incident response: synthetic monitoring; alerting basics; incident response during release; post-mortems. (4 concepts)
Agile and collaboration: QA in cross-functional teams; definition of ready vs done; communicating risk to stakeholders. (3 concepts)
Release governance: change management; compliance and audit basics; documentation and evidence standards. (3 concepts)
Risk scenarios: risk matrix; contingency planning; release decision under pressure. (3 concepts)

- [ ] **Step 7: Testing tools section (simple introductions)**

Four tools, each with a 4-question cycle: What is it / What is it used for in release QA / How does a typical use look (Playwright and Selenium: a 5-15 line code snippet; Postman: a 4-6 step workflow; JMeter: a short setup description) / When to choose it. (4 tools × 4 = 16 questions)

Tools: Playwright; Selenium; Postman; JMeter.

Then a final comparison concept, 3-part cycle (What is the comparison / Why does choosing the right tool matter / How do you decide): "Playwright vs Selenium vs Postman vs JMeter — when to choose which" (UI automation vs API vs performance; simple, per user request; no k6).

- [ ] **Step 8: Verify**

Run: `grep -c '^### ' F:/for-qa/release_qa_mid_questions_answers.md`
Expected: 250 (77 core concepts × 3 = 231 + 16 tool questions + 3 comparison questions). Read through once; confirm no k6 mentions (`grep -i k6` → no matches), no boilerplate remnants, snippet blocks are short and correct.

---

## Task 4: `release_qa_mid_practice.md`

**Files:**
- Create: `F:\for-qa\release_qa_mid_practice.md`

- [ ] **Step 1: Header + Part 1 — 50 mid MCQs**

Header: "Mid-Level Release QA — Practice Set (MCQ, Scenarios, Mock Interview)". Topic mix: risk-based testing and release decisions (12), automation/CI-CD (10), performance and reliability (8), API testing (8), security basics (6), migration and rollback (6). Questions require choosing between trade-offs, not recalling definitions; explanations must state why the other options lose.

- [ ] **Step 2: Part 2 — 40 mid scenarios**

Each recommended response 4-6 sentences covering: what to verify, who to involve, what evidence to capture, effect on the release decision. Titles: Canary shows elevated error rate after 10% rollout; Database migration must roll back mid-release; Flaky suite blocks the quality gate; Security scan reports a high finding the day before release; A critical defect is found in production on the previous release; Two teams release into shared services the same day; Feature flag is left off in production config; Performance test shows p99 regression of 40%; Contract test fails against a new API version; Rollback plan is untested and vague; A stakeholder pushes to bypass code freeze; Test environment does not match production (data shape); Automation suite coverage dropped after a refactor; A hotfix is needed but the release branch is frozen; Post-deploy smoke passes but business metrics drop; Release evidence is incomplete for audit; A P1 defect has a workaround — release decision time; QA lead is asked to sign off without testing a vendor component; A third-party outage affects staging tests; A/B experiment contaminates release metrics; Load test was run on undersized environment; A developer deploys directly to production during a release; Escalation policy is unclear during an incident; A release is deployed with an untested config change; Two defects: one data-loss rare, one UI cosmetic common — how to prioritize; Regression suite takes 8 hours but release window is 4; QA disagrees with product on severity of a defect; A security fix is late and untested; API rate limiting breaks a critical batch job; A test flake is masking a real product bug; Release calendar conflicts with a blackout period; A data migration silently drops a column used by a dashboard; QA is asked to reduce test cycle time by 50%; Incident post-mortem reveals missing synthetic checks; A canary is rolled back but data was partially migrated; The build pipeline passes while tests were skipped; A vendor update breaks integration tests late; A new QA hire is assigned release sign-off (delegation/judgment); A release decision must be made with 60% test completion; Post-release, a regression defect escapes and customers report it.

- [ ] **Step 3: Part 3 — 15 mid mock interview questions**

Titles: Walk me through your last release cycle end to end; How do you build a risk-based test plan for a release?; How would you design quality gates in a CI/CD pipeline?; When would you block a release, and how do you communicate it?; How do you handle a flaky test suite before a release?; Describe a time a release went wrong and what you changed; How do you test a database migration and its rollback?; What would you automate first and why?; How do you measure release quality?; How do you test an API with Postman at scale?; How would you introduce UI automation with Playwright to a team?; What is the difference between load, stress, and soak testing, and when do you run each?; How do you handle a security finding discovered late in a release?; How do you work with developers and product to reach a go/no-go decision?; How do you keep release evidence audit-ready?

- [ ] **Step 4: Verify**

Run: `grep -c '^### MCQ' F:/for-qa/release_qa_mid_practice.md` → 50; `grep -c '^### Scenario'` → 40; `grep -c '^### Interview'` → 15. Read through once; every MCQ has one `**Answer:**` line; scenario responses all touch verify/involve/evidence/decision.

---

## Task 5: `release_qa_behavior_leadership.md`

**Files:**
- Create: `F:\for-qa\release_qa_behavior_leadership.md`

- [ ] **Step 1: Header + Part 1 — 30 behavior questions (STAR)**

Header: "Behavior & Leadership Questions for Release QA". For each: the question, one line on what interviewers are looking for, and a STAR sample answer (Situation, Task, Action, Result) written for a Release QA context. Questions: Tell me about a time you blocked a release; ...a time you missed a bug that reached production; ...a time you disagreed with a developer; ...a time you disagreed with a product owner about scope; ...a time you had to test under a tight deadline; ...a time you automated something repetitive; ...a time you had to learn a new tool quickly; ...a time you handled a production incident; ...a time you improved a process; ...a time you received difficult feedback; ...a time you gave difficult feedback; ...a time you dealt with a flaky environment; ...a time you said no to a stakeholder; ...a time you had to prioritize with limited time; ...a time you worked with a difficult teammate; ...a time you found a critical bug late; ...a time you made a mistake in testing; ...a time you had to explain technical risk to non-technical people; ...a time you improved test coverage; ...a time you handled conflicting priorities; ...a time you onboarded someone; ...a time you worked with remote teams across time zones; ...a time you had to test without a specification; ...a time you prevented a bad release; ...a time you recovered from a rollback; ...a time you influenced a decision with data; ...a time you challenged an estimate; ...a time you managed a vendor or third-party dependency; ...a time you delivered bad news to leadership; ...a time you went beyond your job description.

- [ ] **Step 2: Part 2 — 15 junior QA judgment Q&As**

Format: `### Judgment question N. <question>` + `**Answer:**`. Topics: how do you know a release is ready to test; when is a defect "done"; how to handle unclear acceptance criteria; how to prioritize your own testing day; what to do when you disagree with a severity; when to ask for help; how to handle testing a feature you don't understand; what "tested enough" means to you; how to stay organized across releases; how to respond when a build is untestable; how to handle repeated environment failures; when to push back on a deadline; how to give a status update honestly; how to handle being asked to skip steps; what to do after a release goes live.

- [ ] **Step 3: Part 3 — 25 leadership/judgment Q&As**

Format: same as Part 2 (`### Judgment question N. <question>` + `**Answer:**`), answers 5-8 sentences at leadership depth. Rework the original's "Leadership and senior QA judgment" topic (original file 1, Q951-1000) — drop the 5-angle boilerplate: quality ownership; quality culture; QA as a coach; building a test strategy for an organization; hiring and growing QA engineers; test automation ROI; deciding when not to automate; release governance design; risk communication to executives; balancing speed and quality; metrics that matter vs vanity metrics; handling a culture of blame; introducing shift-left; managing vendor QA; test environment strategy at scale; dealing with conflicting stakeholder demands; when to overrule a go decision; when to accept a risk; building release decision frameworks; mentoring junior QA; dealing with burnout and pressure; audit and compliance readiness; continuous improvement programs; negotiating test scope with delivery pressure; defining quality gates with engineering leadership.

- [ ] **Step 4: Verify**

Run: `grep -c '^### Behavior' F:/for-qa/release_qa_behavior_leadership.md` → 30; `grep -c '^### Judgment'` → 40 (15 junior + 25 leadership). Read through once; STAR samples all have Situation/Task/Action/Result structure.

---

## Task 6: Update CLAUDE.md + final verification

**Files:**
- Modify: `F:\for-qa\CLAUDE.md`

- [ ] **Step 1: Update CLAUDE.md**

Rewrite the "Repository overview" to describe all 7 files (2 originals + 5 new), add the 3-part Q&A convention for the new files (replacing the 5-angle description), note the junior/mid/behavior split, and that the Testing tools section covers Playwright/Selenium/Postman/JMeter only (no k6).

- [ ] **Step 2: Final cross-file verification**

Run: `grep -c '^### ' F:/for-qa/release_qa_*.md` — confirm counts match each file's plan target. Run: `grep -in 'k6\|TBD\|TODO\|reduces release uncertainty' F:/for-qa/release_qa_junior_*.md F:/for-qa/release_qa_mid_*.md F:/for-qa/release_qa_behavior_leadership.md` — expected: no matches. Run: `ls -la F:/for-qa` — confirm the two original files are byte-identical in timestamp/content (untouched).

---

## Execution order

Tasks run in order 1 → 6. No task depends on another's output except Task 6 (verification), so ordering exists only to keep numbering conventions consistent across files.
