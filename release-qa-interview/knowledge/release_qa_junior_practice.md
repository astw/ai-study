# Junior Release QA — Practice Set (MCQ, Scenarios, Mock Interview)

**Purpose:** Self-testing and interview drill for junior Release QA / QA tester roles.

**How to use:** Answer each MCQ before reading the explanation. For scenarios, speak your response aloud before comparing. For the mock interview, answer each question in 1–2 minutes.

---

## Part 1 — 50 multiple-choice questions

### MCQ 1. A new build has just been deployed to staging. What should QA run first?

A. Performance testing
B. Smoke testing
C. Full regression testing
D. Cross-browser testing

**Answer: B.** Smoke testing first checks whether the build's critical paths work at all, before any deeper effort.

### MCQ 2. A smoke test fails on the login page right after deployment. What is the best next step?

A. Skip login and test the rest of the application
B. Stop broader testing and report the build as blocked
C. Continue the full regression suite in parallel
D. Approve the release if other pages load

**Answer: B.** A failed critical smoke check means the build may not be testable; continuing wastes effort on an unstable build.

### MCQ 3. Which best describes regression testing?

A. Testing only the newly added feature
B. Checking that existing functionality still works after a change
C. Measuring how fast the server responds
D. Checking whether a deployment command completed

**Answer: B.** Regression testing looks for unintended side effects of changes on existing behavior.

### MCQ 4. A developer says a defect is fixed. What should QA do first?

A. Close the ticket based on the developer's message
B. Retest the original reproduction steps on the identified build
C. Wait for production feedback
D. Run only performance tests

**Answer: B.** Retest the original steps on the correct build; the developer's word is not verification.

### MCQ 5. What is the difference between retesting and regression testing?

A. They are the same thing
B. Retesting verifies a specific fix; regression checks nothing else broke
C. Regression verifies a specific fix; retesting checks nothing else broke
D. Retesting is manual; regression is automated

**Answer: B.** Retesting confirms the fix itself; regression checks the surrounding and existing behavior afterward.

### MCQ 6. A test passes and fails on the same code with no product change. What is this called?

A. A deterministic pass
B. A flaky test
C. A code freeze
D. A canary release

**Answer: B.** Flaky tests produce inconsistent outcomes, usually due to timing or environment instability.

### MCQ 7. A critical API returns HTTP 500 in staging after deployment. What should happen?

A. Ignore it if the UI loads
B. Treat it as a potential blocker and investigate logs and dependencies
C. Change the expected result to 500
D. Wait until production to see if it matters

**Answer: B.** A server error on a critical path needs triage, impact assessment, and resolution or explicit risk acceptance.

### MCQ 8. Which identifier should always appear in release test evidence?

A. Only the tester's name
B. The exact build/version and environment
C. Only the sprint number
D. The production server password

**Answer: B.** Evidence must identify exactly what was tested and where, or results cannot be trusted later.

### MCQ 9. A test fails only in staging but passes locally. What should QA compare first?

A. The tester's preferred browser theme
B. Build, configuration, data, dependencies, and environment differences
C. The team's vacation calendar
D. Only source-code formatting

**Answer: B.** Environment drift and configuration differences are the most common cause of inconsistent results.

### MCQ 10. Which is the strongest release exit criterion?

A. QA feels comfortable
B. All tests pass, regardless of scope
C. Pre-agreed measurable criteria are met and residual risks are documented
D. No defects were ever found

**Answer: C.** Exit criteria must be objective, agreed in advance, and include defect and risk status.

### MCQ 11. What is severity?

A. How urgently a defect should be fixed
B. The technical or business impact of a defect if it occurs
C. Who reported the defect
D. The number of times a defect was reproduced

**Answer: B.** Severity measures impact — data loss and outages are severe regardless of urgency.

### MCQ 12. What is priority?

A. How bad the defect is technically
B. How urgent the fix is from a business perspective
C. The defect's age in days
D. The tester's opinion of the developer

**Answer: B.** Priority is about urgency and business factors: deadlines, workarounds, customer impact.

### MCQ 13. Which of the following belongs in a good bug report?

A. The developer's name only
B. Steps to reproduce, expected vs actual results, build and environment
C. Only a screenshot with no description
D. A severity decided without any evidence

**Answer: B.** Reproduction steps plus expected/actual results and build details let a developer fix it without asking questions.

### MCQ 14. A defect is found that cannot be reproduced after several attempts. What should QA do?

A. Report it as critical and block the release
B. Delete the report
C. Document what was tried, mark it as not reproducible, and keep an eye on it
D. Close it as a duplicate of nothing

**Answer: C.** Non-reproducible defects still get documented and monitored; they may reappear under specific conditions.

### MCQ 15. Two testers report the same underlying defect with different symptoms. What is the correct handling?

A. Keep both open forever
B. Link them as duplicates and keep one canonical ticket
C. Close both and hope it goes away
D. Downgrade both severities

**Answer: B.** Duplicates are linked to one canonical ticket so the defect list reflects reality.

### MCQ 16. Who usually owns the priority decision for a defect?

A. QA alone
B. The triage group, with product input
C. The build server
D. No one — it is random

**Answer: B.** Priority reflects business urgency and is set by triage with product input; QA typically provides severity.

### MCQ 17. A P1 defect is open in the core payment workflow. What is the appropriate release stance?

A. Ship automatically
B. Normally block the release unless an accountable owner explicitly accepts the risk
C. Hide the defect from the report
D. Downgrade severity to meet the deadline

**Answer: B.** A critical defect in a core flow is a release blocker unless risk acceptance is explicit and authorized.

### MCQ 18. A product owner asks QA to skip regression to meet a date. Best response?

A. Agree silently and hope for the best
B. Explain the risk, propose a risk-based minimum suite, and document the decision
C. Refuse to test anything
D. Run only the tests that passed last release

**Answer: B.** Offer an evidence-based risk reduction plan and make any residual risk visible to the decision owner.

### MCQ 19. A known low-severity defect ships with a documented workaround. What should QA ensure?

A. It is omitted from the release report
B. Impact, workaround, affected versions, and acceptance owner are documented
C. It is automatically fixed by deployment
D. All tests are rerun from scratch

**Answer: B.** Known issues must be transparent so support and decision-makers understand the residual risk.

### MCQ 20. What is defect triage?

A. A meeting to review, prioritize, and assign defects
B. A tool for measuring code quality
C. A type of performance testing
D. A ceremony for celebrating fixed bugs

**Answer: A.** Triage reviews validity, severity, priority, ownership, and release impact.

### MCQ 21. A field accepts values 1 to 100. Which set of values uses boundary value analysis?

A. 1, 50, 100
B. 0, 1, 2, 99, 100, 101
C. 10, 20, 30, 40, 50
D. -1000, 1000

**Answer: B.** Boundary analysis tests the boundaries themselves and just inside/outside each edge.

### MCQ 22. What is equivalence partitioning?

A. Testing every possible input value
B. Dividing inputs into groups that should behave the same and testing one per group
C. Splitting the test team into equal groups
D. Testing only the middle of each range

**Answer: B.** One representative per equivalence class covers the whole class's behavior efficiently.

### MCQ 23. Which is an example of negative testing?

A. Entering a valid username and password and logging in
B. Entering letters into a phone-number field and checking the rejection
C. Testing the application on a fast network
D. Running the test suite at midnight

**Answer: B.** Negative testing verifies that invalid input is rejected gracefully.

### MCQ 24. Which is an example of positive testing?

A. Submitting an empty required form
B. Entering valid data and getting the expected successful result
C. Unplugging the network cable mid-request
D. Entering a 500-character name into a 20-character field

**Answer: B.** Positive testing checks the happy path: valid input, expected output.

### MCQ 25. What is exploratory testing?

A. Following a fixed script step by step
B. Designing and executing tests simultaneously while investigating the system
C. Testing without any notes or reporting
D. A synonym for performance testing

**Answer: B.** Exploratory testing is structured investigation with a goal, learning and documenting as you go.

### MCQ 26. What are acceptance criteria?

A. The salary band for the QA role
B. Testable conditions a feature must meet to be considered done
C. The list of people attending the demo
D. The color scheme of the application

**Answer: B.** Acceptance criteria define what "correct" means and are the basis for testing the story.

### MCQ 27. What is UAT?

A. Testing by developers after coding
B. Final validation by business users or the product owner before go-live
C. A type of unit test
D. Testing the backup system

**Answer: B.** UAT confirms the release actually solves the business need, beyond technical correctness.

### MCQ 28. A login form has fields for username and password. Which is the most useful additional negative test?

A. Logging in with a correct username and password
B. Logging in with an empty password and checking the message
C. Changing the page background color
D. Testing on a faster machine

**Answer: B.** Empty, invalid, and boundary inputs on each field are core negative cases.

### MCQ 29. What is a code freeze?

A. A period when the release branch accepts only approved critical fixes
B. A bug in the compiler
C. A security tool
D. A type of server failure

**Answer: A.** A code freeze stabilizes the build for final testing; exceptions are reviewed and approved.

### MCQ 30. What is a release candidate?

A. A random daily build
B. A build considered feature-complete, intended for final validation
C. The first build of a project
D. A developer's local workspace

**Answer: B.** An RC is the named, versioned build that final testing and the release decision target.

### MCQ 31. What is a rollback plan?

A. A guarantee that no defects exist
B. A defined procedure to return to the previous working version
C. A replacement for test execution
D. A way to avoid writing release notes

**Answer: B.** Rollback planning reduces recovery time and defines triggers, ownership, and data implications.

### MCQ 32. Who makes the final go/no-go decision?

A. QA alone
B. The accountable release owner, informed by QA's evidence
C. The build server
D. The developer who wrote the most code

**Answer: B.** QA provides evidence and a recommendation; the accountable owner decides and takes the risk.

### MCQ 33. What is release scope?

A. The list of what a release will and will not contain
B. The number of developers on the team
C. The size of the database
D. The sprint calendar

**Answer: A.** Scope defines included and excluded changes, which tells QA what to test and what to flag.

### MCQ 34. A change was merged into the release branch after testing finished. What must happen?

A. Nothing — it is probably fine
B. Re-test the affected areas on the new build before release
C. Delete the change silently
D. Only update the release notes

**Answer: B.** Results apply to the artifact tested; a new artifact needs re-testing of affected areas.

### MCQ 35. Which HTTP method is typically used to read a resource?

A. POST
B. GET
C. DELETE
D. PATCH

**Answer: B.** GET reads; POST creates, PUT/PATCH update, DELETE deletes.

### MCQ 36. Which status code group means "client error"?

A. 2xx
B. 3xx
C. 4xx
D. 5xx

**Answer: C.** 4xx means the request itself is wrong (400 bad input, 401/403 auth, 404 not found); 5xx is a server failure.

### MCQ 37. A request to delete a read-only resource returns 405. What does this mean?

A. The method is not allowed for this resource
B. The server is too slow
C. The request was successful
D. The resource moved permanently

**Answer: A.** 405 Method Not Allowed means the resource exists but does not support that verb.

### MCQ 38. A valid request returns 200 with an error message in the body. What is this?

A. Correct behavior
B. A bug — the status code and body contradict each other
C. A performance problem
D. A redirect

**Answer: B.** Status code and body must agree; a 200 carrying an error is inconsistent and needs investigation.

### MCQ 39. What is idempotency?

A. Repeating an operation changes the result each time
B. Repeating an operation does not change the result beyond the first success
C. A type of database index
D. A browser feature

**Answer: B.** Idempotent operations (like retried PUTs) are safe to repeat; non-idempotent ones (like POST) can duplicate.

### MCQ 40. A POST that creates an order is retried after a timeout and creates two orders. The root problem is that the operation is not:

A. Idempotent
B. Fast enough
C. Documented
D. Written in the right language

**Answer: A.** A non-idempotent create operation duplicated data on retry; the API needs idempotency protection.

### MCQ 41. What is continuous integration?

A. Deploying to production every day
B. Frequently merging code with automated build and test on every merge
C. A tool for UI design
D. Testing only on Fridays

**Answer: B.** CI merges often and runs automated checks per merge so integration problems surface immediately.

### MCQ 42. What is continuous delivery?

A. Keeping software in a releasable state with automated build, test, and release preparation
B. Automatically releasing every change to production with no approval
C. A database migration tool
D. A type of bug

**Answer: A.** CD automates the path to production; the final release step may still be gated by approval.

### MCQ 43. A pipeline is "green" but a critical path is broken in staging. What does this show?

A. The pipeline tests do not cover that critical path
B. The pipeline is lying
C. Staging is always broken
D. Testing is unnecessary

**Answer: A.** A green pipeline only proves what it tested; uncovered critical paths are a coverage gap.

### MCQ 44. What should QA do when an automated test fails in the pipeline?

A. Immediately bypass it to keep the build moving
B. Investigate the failure before deciding whether it is product or test related
C. Delete the failing test
D. Run the whole suite again until it passes

**Answer: B.** Treat failures as product failures until proven otherwise; investigate before re-running or bypassing.

### MCQ 45. In scrum, when should QA ideally start testing a user story?

A. After the release is deployed
B. As soon as the story is testable in the sprint
C. During the next sprint
D. Only at the retrospective

**Answer: B.** Continuous in-sprint testing finds defects when they are cheapest to fix.

### MCQ 46. What is the definition of done?

A. The developer stopped working on the story
B. The team's shared checklist for when work is complete, including testing
C. The date the sprint ends
D. The product owner's mood

**Answer: B.** Done includes testable outcomes agreed by the team; it feeds release criteria.

### MCQ 47. A user story says "make the login page better" with no criteria. What should QA do?

A. Guess what to test and hope for the best
B. Ask for testable acceptance criteria before or early in testing
C. Skip testing the story
D. Mark it done immediately

**Answer: B.** Untestable stories need criteria; raise the gap early, ideally before development.

### MCQ 48. What is the best thing to bring to a daily standup as QA?

A. A detailed list of every test executed
B. What you tested yesterday, what you will test today, and any blockers
C. Silence
D. A code review of the database schema

**Answer: B.** The standup is for status and blockers; QA's blockers are as important as developers'.

### MCQ 49. A release has unclear scope and no written criteria. What is QA's best early move?

A. Start random testing
B. Raise the gaps and ask for scope and criteria before deep testing
C. Wait for production feedback
D. Write the release notes early

**Answer: B.** Without scope and criteria, testing cannot be planned or judged; surface the gap immediately.

### MCQ 50. What is the most honest way to report a test that could not be run?

A. Report it as passed to save time
B. Report it as blocked/not run with the reason
C. Delete it from the plan
D. Report it as failed

**Answer: B.** Blocked and not-run tests must be visible; hiding them falsifies the release picture.

## Part 2 — 30 realistic release scenarios

### Scenario 1. Smoke test fails on staging

**Situation:** The login endpoint returns 503 immediately after deployment.

**Recommended response:** Pause the broader suite. Verify the deployed artifact, service readiness, dependencies, and configuration, and raise a blocker if the critical path stays down. Resume only after the environment and build are stable.

### Scenario 2. Smoke passes but one key workflow fails

**Situation:** The dashboard loads, but users cannot create a new project.

**Recommended response:** Treat smoke as an initial gate, not proof of quality. Triage the failed workflow, determine the impact, and block or document risk according to the release criteria.

### Scenario 3. Late code change after regression

**Situation:** A developer merges a small fix after the full regression run completed.

**Recommended response:** Identify the new artifact and the changed components. Run retest plus targeted regression around the change and its dependencies; do not reuse results from the previous build as if nothing changed.

### Scenario 4. Staging and production configuration differ

**Situation:** A feature works in staging, but production uses a different authentication provider.

**Recommended response:** Document the parity gap, validate the production-specific configuration as safely as possible, test the authentication behavior specifically, and make the residual risk explicit before approval.

### Scenario 5. Database migration partially completes

**Situation:** A schema migration stops halfway through, leaving some tables changed and others not.

**Recommended response:** Stop the release path immediately. Have the DBA or data team assess the state, restore from backup or complete the migration, then re-verify data integrity before any further testing or promotion.

### Scenario 6. Test data is missing

**Situation:** The test environment has no users with the right states to test the new billing feature.

**Recommended response:** Raise the blocker early with specific needs (e.g., "a user with an expired card and a pending order"). Work with developers or the data team to create or generate the data, and record the gap in test status.

### Scenario 7. Staging is down before the test window

**Situation:** QA arrives to test, and the staging environment is completely unavailable.

**Recommended response:** Escalate immediately with details (what is down, since when, what you tried). Do not burn the test window waiting silently — track the lost time and re-plan the window with the release owner.

### Scenario 8. A developer says a defect is fixed

**Situation:** A developer messages: "That bug you filed is fixed now."

**Recommended response:** Thank them, then verify: retest the original reproduction steps on the build they specify. Only after the retest passes and targeted regression is done should the ticket move toward closure.

### Scenario 9. P1 defect in a core workflow

**Situation:** A critical defect is open in the payment flow two days before release.

**Recommended response:** Make the impact visible: what breaks, who is affected, is there a workaround. Recommend blocking the release unless a fix is verified or an accountable owner explicitly accepts the risk in writing.

### Scenario 10. Product owner asks to skip regression

**Situation:** "We don't have time for regression. Let's just test the new feature and ship."

**Recommended response:** Explain the risk of side effects, propose a risk-based minimum suite covering the changed area and critical paths, and document what is skipped and who accepted that risk. Do not agree silently.

### Scenario 11. Release notes are incomplete

**Situation:** The release notes list only one of the five shipped changes.

**Recommended response:** Compare the notes against scope and the defect list, and send the gaps back to the owner before release. Users and support act on release notes — missing entries become confusion and tickets later.

### Scenario 12. A test fails only in staging

**Situation:** A workflow fails in staging but passes on the developer's machine.

**Recommended response:** Compare build, configuration, data, dependencies, and environment differences between the two. Capture the failing request or screen as evidence, and report with environment details — do not dismiss it as "environment issue" without checking.

### Scenario 13. A test case's expected result is wrong

**Situation:** A test case says to expect result X, but the product spec clearly says result Y.

**Recommended response:** Do not silently change your testing to match the case. Confirm against the spec, test the correct expectation, and fix the test case — reporting the mismatch to the case owner so the suite stays trustworthy.

### Scenario 14. A defect cannot be reproduced

**Situation:** A bug you found last week will not reproduce today.

**Recommended response:** Document exactly what you tried (build, data, steps, attempts), mark the ticket as not reproducible, and monitor. Note the original evidence. Do not close it as "fixed" and do not delete it.

### Scenario 15. Two defects are duplicates

**Situation:** You filed a bug, and a colleague filed the same issue with different symptoms.

**Recommended response:** Link the tickets as duplicates, keep one canonical ticket with the clearest reproduction, and reference the duplicate. This keeps the defect count honest for the release decision.

### Scenario 16. A build is deployed with the wrong version number

**Situation:** The version reported by the application does not match the release candidate number.

**Recommended response:** Stop and treat it as a blocker. Wrong version means either the wrong artifact was deployed or the labeling is broken — either way, results against it are meaningless until the correct build is confirmed.

### Scenario 17. Sign-off is requested but exit criteria are not met

**Situation:** The release owner asks QA to sign off even though two exit criteria are unmet.

**Recommended response:** Do not sign. State plainly which criteria are unmet, what the risks are, and what would resolve them (fix, retest, or documented risk acceptance). Sign-off records accountability — keep it honest.

### Scenario 18. A login form change breaks password reset

**Situation:** The new login form works, but users who click "forgot password" hit a blank page.

**Recommended response:** Report as a regression in a critical journey: reproduce with exact steps, note that it worked in the previous release, and treat it as a potential blocker since account access is a core flow.

### Scenario 19. A flaky test fails in the pipeline

**Situation:** A UI test failed in the pipeline, but it passed locally and passed on re-run.

**Recommended response:** Do not just re-run until green. Note the failure, check whether a real product issue could explain it, and report the flakiness as a test defect to be fixed — flaky tests erode trust in the whole pipeline.

### Scenario 20. A required mobile device is unavailable

**Situation:** The release plan requires testing on a specific tablet, which nobody can find.

**Recommended response:** Raise it early, propose the closest available substitute or emulator, and document the gap so the release decision includes "this device class was not physically tested."

### Scenario 21. A stakeholder asks for a release date commitment

**Situation:** A manager asks QA: "Can we absolutely ship on Friday?"

**Recommended response:** Answer with facts, not a promise: current test status, open defects, remaining effort, and risks. Give a realistic assessment and let the accountable owner make the commitment with full information.

### Scenario 22. A hotfix is needed during code freeze

**Situation:** A critical production issue needs an urgent fix, but the release is in code freeze.

**Recommended response:** Follow the exception process: risk assessment, review, approval, targeted testing of the fix plus affected areas, and documentation. A freeze exception is possible — it just has to be deliberate and visible.

### Scenario 23. A tester is asked to approve a release they did not test

**Situation:** A colleague asks you to "just sign off" on a release you were not involved in.

**Recommended response:** Decline politely. You can only report on testing you did. Offer to review the evidence and, with the right handover and time, either test the critical paths yourself or document that sign-off reflects evidence review only.

### Scenario 24. A new feature has no acceptance criteria

**Situation:** A feature is in the release with no criteria and a vague description.

**Recommended response:** Raise it immediately — before testing starts. Work with product to write testable criteria; without them, you cannot judge pass or fail, and the release decision loses its basis.

### Scenario 25. A critical API returns 500 in staging

**Situation:** The core search API returns 500 errors on valid requests.

**Recommended response:** Reproduce with the exact request, capture logs and response, and report as a potential blocker. Work with developers to identify the root cause (code, config, dependency) before broader testing continues.

### Scenario 26. A UI text change causes a layout break

**Situation:** A harmless copy change ("Sign in" to "Log in") breaks the button layout on mobile.

**Recommended response:** Report as a real defect with device/viewport details and a screenshot. Small changes breaking layouts is exactly what regression and responsive checks exist to catch.

### Scenario 27. A test environment runs out of disk space

**Situation:** Mid-testing, the environment's disk fills up and services start failing.

**Recommended response:** Stop testing and report the environment failure with evidence. Confirm the failures are environment-caused, not product-caused, then resume once it is fixed. Log the lost time against the test window.

### Scenario 28. A developer disagrees a defect is valid

**Situation:** "That's not a bug, it's by design," says the developer.

**Recommended response:** Bring evidence: expected behavior per the spec or acceptance criteria, actual behavior, and impact. Discuss respectfully; if disagreement persists, escalate to triage or the product owner — the spec owner decides, not the loudest voice.

### Scenario 29. A release is deployed but monitoring shows errors

**Situation:** The release went live, and the error rate dashboard starts climbing.

**Recommended response:** Treat it as a live incident: alert the release channel, check whether the errors correlate with the new version, run a quick post-release smoke, and be ready to trigger the rollback plan if the release is the cause.

### Scenario 30. A junior tester must report daily status

**Situation:** Your lead asks for a daily testing status update during release week.

**Recommended response:** Keep it structured: what was tested, what passed, what failed or blocked, defects found, and what is next. Include environment and build info. Honest status beats impressive status — surprises at go/no-go are what hurt releases.

## Part 3 — 15 mock interview questions

### Interview question 1. Tell me about yourself as a QA tester.

**Sample answer:** I focus on release testing — validating builds against acceptance criteria and release criteria. I have experience writing and executing test cases, reporting defects with clear reproduction steps, smoke and regression testing, and basic API testing with Postman. I like finding the bug that everyone else missed, and I document everything so release decisions are based on evidence.

### Interview question 2. What is the difference between smoke, sanity, and regression testing?

**Sample answer:** Smoke is a short check that a new build's critical paths work after deployment. Sanity is a narrow check of a specific change or fix. Regression re-runs existing tests to make sure changes did not break existing behavior. Smoke asks "is the build worth testing?", regression asks "did anything break?"

### Interview question 3. How do you write a test case?

**Sample answer:** I start from the requirement or acceptance criteria and define the preconditions, steps, expected result, and priority. I make steps specific enough that another tester would run it the same way, and I include negative and boundary cases, not just the happy path. I also link the case to the requirement so coverage is traceable.

### Interview question 4. What goes into a good bug report?

**Sample answer:** A clear title, the build/version and environment, exact steps to reproduce, expected vs actual results, severity, and evidence like screenshots, logs, or a video. The test is whether a developer can reproduce and fix it without asking me anything.

### Interview question 5. What is the difference between severity and priority?

**Sample answer:** Severity is how bad the defect is — its impact if it happens: data loss and outages are severe. Priority is how urgent the fix is from a business view — deadlines, workarounds, and customer impact. A cosmetic typo on the login page of a flagship product can be low severity but high priority.

### Interview question 6. How would you test a login page?

**Sample answer:** Positive cases: valid credentials log in, session starts. Negative: wrong password, wrong username, empty fields, locked account, expired password. Boundaries: maximum length passwords, special characters. Cross-checks: password reset link, "remember me", error messages not revealing whether the username exists, and behavior after multiple failed attempts.

### Interview question 7. What would you do first after a build is deployed to staging?

**Sample answer:** Verify the deployment — correct version, correct environment, services up — then run the smoke suite on the critical paths. If smoke fails, I stop and report a blocker. If it passes, I move to the planned functional and regression testing for the release scope.

### Interview question 8. How do you decide what to test when time is short?

**Sample answer:** Risk first: the changed areas, their dependencies, and the critical user journeys. I use the test plan's priorities and the release criteria. I test the highest-risk items first so that when time runs out, the untested remainder is the least risky part — and I report what was not tested honestly.

### Interview question 9. What is boundary value analysis?

**Sample answer:** Testing the edges of valid ranges where bugs cluster. For a field accepting 1–100, I test 0, 1, 2, 99, 100, and 101 — the boundary, just inside, and just outside on each side. Off-by-one errors and wrong comparison operators in the code are caught this way.

### Interview question 10. How do you handle a developer who says your defect is invalid?

**Sample answer:** I come with evidence: the expected behavior from the spec or acceptance criteria, the actual behavior, and the impact. If we still disagree, I take it to triage or the product owner — the spec owner makes the call. My job is to present facts clearly, not to win an argument.

### Interview question 11. What is a test plan and what goes in it?

**Sample answer:** A test plan is the concrete testing schedule for a release: scope, environments, test data, who tests what, entry and exit criteria, and the cases to run. It is the contract of what will be tested, and the basis for reporting completion against the release decision.

### Interview question 12. How do you test an API with Postman?

**Sample answer:** I build a request with the endpoint, method, headers, and body, send it, and check the status code, response body, and side effects. I cover valid input, invalid data, missing fields, wrong authentication, and boundary values, and I keep a collection so the checks are repeatable for regression.

### Interview question 13. What is regression testing and when do you run it?

**Sample answer:** Regression re-runs existing tests to confirm changes did not break existing behavior. I run it after every significant change — a fix, a merge, a configuration update — and always as part of the release cycle before go/no-go, prioritizing the changed areas and critical journeys when full regression is not possible.

### Interview question 14. How do you keep test evidence?

**Sample answer:** I record as I test: exact build and environment, test case executed, steps, expected vs actual result, and screenshots or logs where relevant. Blocked and not-run tests are recorded as such, never as passed. Evidence is stored where the team can find it, so the release decision and any later audit can see what actually happened.

### Interview question 15. What questions would you ask before testing a new feature?

**Sample answer:** What are the acceptance criteria? Which build and environment should I test? What is the expected behavior, including error cases? Are there dependencies or other teams involved? What data do I need? Who is the developer and product owner? Getting these answered first prevents testing the wrong thing or discovering gaps at the end.

---

## Practical answer framework for scenario questions

Use this sequence when answering under interview pressure:

1. **Clarify** — exact build, scope, environment, expected behavior, and severity.
2. **Contain** — pause rollout or broader testing when a critical gate fails.
3. **Investigate** — compare logs, metrics, configuration, data, dependencies, and recent changes.
4. **Assess impact** — affected users, workflows, data, security, availability, and workaround.
5. **Communicate** — identify owner, evidence, status, and decision required.
6. **Decide** — fix and retest, mitigate, defer, rollback, or seek documented risk acceptance.
7. **Prevent recurrence** — add regression coverage, monitoring, automation, or process improvements.

## Important interview reminders

- Never report a blocked or not-run test as passed.
- Test evidence must identify the exact artifact and environment.
- A green pipeline or successful deployment does not by itself prove release readiness.
- Smoke testing is an initial stability gate, not a replacement for regression testing.
- QA recommends based on evidence; release authority and risk acceptance should be explicit.
- Be honest about untested areas and residual risk.
