# Junior Release QA — Questions & Answers

**Purpose:** Foundational interview preparation for junior Release QA / QA tester roles.

**How to use:** Read a topic, answer each question aloud in your own words, then compare with the answer. Each concept is asked three ways — what it is, why it matters, and how you would test or handle it.

---

## Release fundamentals

### 1. What is a release candidate?

A release candidate (RC) is a build the team considers feature-complete and ready for final validation. It has a specific version number and comes from a known build pipeline, so everyone knows exactly which code is being tested.

### 2. Why does a release candidate matter in release QA?

All final testing must be done against one exact, identifiable build. If testers validate different builds, results cannot be compared and defects may be reported against code that no longer exists. The RC is the single source of truth for the release decision.

### 3. How would you test or handle a release candidate?

Record the exact version, commit, and build date, and confirm the build came from the official pipeline. Then run the agreed smoke tests and the release test plan against that build. Link every result to that version so your evidence is traceable.

### 4. What is release scope?

Release scope is the list of what a release will and will not contain: the features, fixes, and configuration changes included, and any known exclusions.

### 5. Why does release scope matter in release QA?

Scope tells you exactly what to test and what is out of bounds. If a change is not in scope, you know it should not be in the build — and if you find it there anyway, that is a problem worth flagging. Without a clear scope you cannot know when testing is complete.

### 6. How would you test or handle release scope?

Compare the approved scope (tickets, change requests) with what actually changed in the build. Flag anything that changed but was not approved, and anything approved that is missing. Test the in-scope items first, and record exclusions so the go/no-go meeting has an honest picture.

### 7. What are release criteria?

Release criteria are the pre-agreed, measurable conditions a release must meet before it can ship — for example, all critical tests passed, no open P1 defects, and sign-off from the required owners.

### 8. Why do release criteria matter in release QA?

They turn the release decision from an opinion into a checklist. When a deadline approaches and pressure builds, criteria keep the decision honest: if a condition is not met, the team must either fix it or get explicit approval to accept the risk.

### 9. How would you test or handle release criteria?

Before testing starts, confirm the criteria are written down and measurable. During testing, track your results against each criterion. In the go/no-go meeting, report each criterion as met or not met with evidence — never as a gut feeling.

### 10. What is a code freeze?

A code freeze is a period before a release when changes to the release branch are restricted, usually to fixes for critical defects only. Any change during the freeze must be reviewed and approved.

### 11. Why does a code freeze matter in release QA?

It keeps the build stable while you test it. If developers keep merging changes during validation, yesterday's test results become meaningless. The freeze lets you finish testing a known, stable artifact instead of chasing a moving target.

### 12. How would you test or handle a code freeze?

Treat the freeze start date as a checkpoint: re-test anything that changed after it. If an exception is approved, re-run the affected tests and note the change in your evidence so the release decision accounts for it.

### 13. What is a release branch?

A release branch is a copy of the code created so the team can stabilize a release without blocking ongoing development. Fixes go into the branch for the release, and are also merged back to the main line.

### 14. Why does a release branch matter in release QA?

It isolates what you are testing from day-to-day development noise. You can be confident the build you validated matches the branch that ships — as long as fixes are merged back correctly to the main line too.

### 15. How would you test or handle a release branch?

Confirm the branch contains only approved changes for the release. After the release, verify the fixes that went in are also merged to the main development line, otherwise the next release will reintroduce the same bugs.

### 16. What is a go/no-go decision?

The go/no-go decision is the formal meeting where the team decides, based on test evidence and open risks, whether the release ships, ships with conditions, or is delayed.

### 17. Why does the go/no-go decision matter in release QA?

It is where your testing work turns into a business decision. Your job is not to say yes or no — it is to present honest evidence: what was tested, what passed, what failed, what is untested, and what the risks are. The decision itself belongs to the accountable owner.

### 18. How would you test or handle a go/no-go decision?

Prepare a short, evidence-based summary: build and environment, test results against criteria, open defects with severity, and untested areas. State a recommendation if asked, but make it clear which parts are facts and which are your judgment. Document the decision and who made it.

### 19. What is a rollback plan?

A rollback plan is the prepared procedure for returning to the previous working version if a release goes wrong. It says who triggers it, what triggers it, how long it takes, and what happens to any data changed in the meantime.

### 20. Why does a rollback plan matter in release QA?

Because a release can fail in production even when all tests passed. A tested rollback plan limits how long users are affected and gives the team confidence to release. An untested plan is just a wish.

### 21. How would you test or handle a rollback plan?

If possible, rehearse the rollback in staging: restore the previous version, check that data is consistent, and time how long it takes. In the release checklist, confirm the plan is written, tested, and that the people who would execute it are available during the release window.

## Test strategy and planning

### 22. What is a test strategy?

A test strategy is the high-level approach to testing for a project or release: what will be tested, how deeply, with what techniques and tools, and how risk and time shape those choices.

### 23. Why does a test strategy matter in release QA?

It stops testing from being random. A strategy ties testing effort to the biggest risks first, so when time runs short you have already covered what matters most — and you can explain why you tested what you tested.

### 24. How would you test or handle a test strategy?

Before the release, walk through the strategy and check it against the actual scope: does it cover the changed areas, the critical user journeys, and the known weak spots from past releases? While testing, revisit it when scope changes and re-balance effort.

### 25. What is a test plan?

A test plan is the concrete schedule of testing for a release: scope, environments, data, who tests what, entry and exit criteria, and the test cases to execute. It is the strategy turned into a to-do list.

### 26. Why does a test plan matter in release QA?

It is your contract with the team about what will and will not be tested. When someone asks "did QA test this?", the plan is the answer. It also makes your workload visible so deadlines can be negotiated before testing starts, not after.

### 27. How would you test or handle a test plan?

Write or review the plan against the release scope, flag anything untestable (missing environment, missing data, missing requirements), and keep it updated as scope changes. At the end of the release, report completion against the plan, not just raw test counts.

### 28. What is a test case?

A test case is a written set of steps, expected results, and preconditions that verifies one specific behavior. Good test cases are specific enough that two testers would execute them the same way.

### 29. Why do test cases matter in release QA?

They make testing repeatable and evidence comparable. If a bug escapes to production, the test case is where you check whether it was covered, missed, or executed wrong. They are also the raw material for future automation.

### 30. How would you test or handle a test case?

When executing, follow the steps but stay alert for anything unexpected outside the case — unexpected behavior is often a real bug. If a step or expected result is wrong, fix the case and tell the author instead of silently working around it.

### 31. What is test data?

Test data is the input data you use to run tests — users, orders, files, database rows — prepared to represent realistic scenarios and edge cases.

### 32. Why does test data matter in release QA?

Many bugs only appear with certain data: empty fields, very long values, special characters, or records with unusual state. If your data is too clean, you will miss them. Realistic data also makes test results believable when you present them at go/no-go.

### 33. How would you test or handle test data?

Prepare data for the cases you will run: valid, invalid, boundary, and empty values. Keep it isolated from real customer data, and refresh it when the test environment is reset. If data is missing, raise it early — it is one of the most common reasons testing stalls.

### 34. What is a test environment?

A test environment is the set of servers, databases, services, and configuration where testing happens. It should be as similar as possible to production so results carry over.

### 35. Why does a test environment matter in release QA?

Bugs found in an environment that looks nothing like production may not exist in production — and bugs that will break production may not appear in the wrong environment. Environment differences are the most common cause of "it works on my machine".

### 36. How would you test or handle a test environment?

Before testing, verify the environment: right build deployed, services up, database at the right version, configuration loaded. Record the environment in your evidence. If it drifts from production in an important way, say so — your results only hold for the environment you actually tested.

### 37. What is test coverage?

Test coverage is the measure of how much of the release's scope, requirements, or code is exercised by your tests. It answers the question "did we test the things we needed to test?"

### 38. Why does test coverage matter in release QA?

It shows the gaps. A release can have a thousand passing tests and still ship a broken feature nobody tested. Reporting coverage — requirements covered, critical paths covered, areas not covered — is more honest than reporting pass counts.

### 39. How would you test or handle test coverage?

Map your test cases to the release scope: for each requirement or change, confirm at least one case exists. Flag scope items with no coverage early. In your release summary, report covered and not-covered areas separately so the decision maker sees the holes.

## Build and deployment validation

### 40. What is smoke testing?

Smoke testing is a short check that a freshly deployed build starts and its most critical paths work — login, home page, main workflow. It is the first thing you run after a deployment.

### 41. Why does smoke testing matter in release QA?

It answers one question cheaply: is this build worth testing at all? If the build does not start or login is broken, any deeper testing is wasted time. Smoke is the gate that protects the team from spending hours on an untestable build.

### 42. How would you test or handle smoke testing?

Run the agreed smoke cases immediately after deployment. If any critical check fails, stop broader testing, report it as a blocker, and wait for a fixed build — do not continue the full suite as if nothing happened.

### 43. What is sanity testing?

Sanity testing is a narrow, focused check of a specific fix or change — you verify that the reported bug is fixed and that the immediate area around it still behaves. Some teams use the term loosely, so clarify what yours means.

### 44. Why does sanity testing matter in release QA?

It gives fast feedback on a single change without the cost of a full regression. When a developer says "fixed", a quick sanity check on the right build tells you within minutes whether the fix is worth deeper testing.

### 45. How would you test or handle sanity testing?

Reproduce the original bug steps on the new build, then check the immediate neighboring behavior. If the fix holds, hand the change to regression testing. If not, send it back with exact steps and evidence.

### 46. What is build verification?

Build verification is confirming that the deployed artifact is exactly what it claims to be: correct version, correct commit, correct environment, and the expected features included.

### 47. Why does build verification matter in release QA?

Testing the wrong build wastes the whole release window, and reporting results against a mislabeled build poisons every downstream decision. Two minutes of verification at the start saves hours of confusion later.

### 48. How would you test or handle build verification?

Compare the version number, build ID, and deployment time against the release plan, and check a couple of known changes are present (and known-unchanged areas are not broken). Record the exact build details in your test evidence.

### 49. What is a staging environment?

Staging is the environment used for final validation before production. It mirrors production as closely as possible — same infrastructure shape, configuration, and near-production data — and is often the last stop before go-live.

### 50. Why does a staging environment matter in release QA?

It is where the release is rehearsed. Problems found in staging — deployment failures, configuration errors, integration issues — are exactly the problems that would have hit real users, but without the damage.

### 51. How would you test or handle a staging environment?

Treat staging like a dress rehearsal: deploy the exact candidate, run smoke and regression, and test the deployment and rollback procedures themselves, not just the features. Report any difference between staging and production setup as a risk.

## Functional testing

### 52. What is the difference between functional and non-functional testing?

Functional testing checks that the system does what it is supposed to do — the right result for a given input. Non-functional testing checks how it does it — speed, security, reliability, usability under load.

### 53. Why does the functional vs non-functional distinction matter in release QA?

Because a release can pass every functional test and still fail in production by being too slow, insecure, or unstable. Release testing must include both, and the two need different skills, tools, and timing.

### 54. How would you test or handle functional and non-functional testing?

Cover functional behavior first — a feature that is wrong is wrong no matter how fast. Then run the agreed non-functional checks (performance, security, stability) against the same build, because changing the build after either set invalidates the other.

### 55. What is positive and negative testing?

Positive testing checks that valid input produces the expected result. Negative testing checks that invalid input is handled gracefully — rejected with a sensible message, not a crash or corrupted data.

### 56. Why do positive and negative testing matter in release QA?

Users do not follow the happy path: they leave fields blank, paste text where numbers go, double-click submit. Negative testing finds the bugs in those paths, and it is where serious defects — data loss, security holes — tend to hide.

### 57. How would you test or handle positive and negative testing?

For each input, test the valid value first, then the classic invalid ones: empty, too long, wrong type, special characters, past boundaries. For each invalid input, verify the system rejects it cleanly and the state stays consistent afterward.

### 58. What is boundary value analysis?

Boundary value analysis tests the values at the edges of valid ranges — the minimum, the maximum, and just outside each. Bugs cluster at boundaries because conditions are usually written as greater-than or less-than comparisons.

### 59. Why does boundary value analysis matter in release QA?

A tiny testing effort at the edges catches a disproportionate share of real defects — off-by-one errors, range validation mistakes, and rounding bugs. It is one of the highest-value techniques you can learn early.

### 60. How would you test or handle boundary value analysis?

For a field that accepts 1–100, test 0, 1, 2, 99, 100, and 101 — the boundary, just inside, and just outside on each side. Apply the same idea to dates, quantities, prices, and list limits.

### 61. What is equivalence partitioning?

Equivalence partitioning divides inputs into groups where the system should behave the same, and tests one representative from each group. For an age field with adult/child pricing, you do not need to test every age — one valid child age and one valid adult age suffice.

### 62. Why does equivalence partitioning matter in release QA?

It makes testing efficient without much loss of confidence. Instead of hundreds of similar inputs, you test a few well-chosen representatives and cover whole classes of behavior.

### 63. How would you test or handle equivalence partitioning?

For each input, list the valid and invalid groups (valid number, negative number, letters, empty), then pick one representative per group — usually a typical value plus the boundaries from boundary analysis.

### 64. What is exploratory testing?

Exploratory testing is testing in which you design, execute, and learn at the same time — you explore the system with a goal, follow leads, and document what you find, rather than following a fixed script.

### 65. Why does exploratory testing matter in release QA?

Scripts can only check what someone thought of in advance. Exploration finds the bugs nobody predicted — the weird interaction, the unclear flow, the gap between what the spec says and what the product does. It also builds your product knowledge fast.

### 66. How would you test or handle exploratory testing?

Give yourself a short, focused mission ("map the checkout flow and find anything that breaks it"), take notes as you go, and record anything unexpected with exact steps. Limit sessions to stay sharp, and turn repeatable findings into new test cases afterward.

### 67. What are acceptance criteria?

Acceptance criteria are the specific, testable conditions a feature must meet to be considered done — written with the user story, ideally before development starts. Example: "a user with an expired password sees a reset prompt and cannot log in."

### 68. Why do acceptance criteria matter in release QA?

They are the definition of correct. Without them, testers must guess what "working" means and defects become arguments about interpretation. With them, you can test objectively and the team has the same picture of done.

### 69. How would you test or handle acceptance criteria?

Ask for criteria before the feature is built, and check they are testable — if you cannot tell whether a criterion is met, it needs rewriting. Test each criterion explicitly and mark it pass or fail in your results.

### 70. What is user acceptance testing (UAT)?

UAT is the final validation by the business users or product owner, in an environment close to production, to confirm the release actually solves their problem before it goes live.

### 71. Why does UAT matter in release QA?

QA verifies the software works as specified; UAT verifies it works as needed. UAT catches mismatches between what was requested and what was actually needed — the defects that technical testing can never find.

### 72. How would you test or handle UAT?

Prepare the environment, data, and accounts the users need, and give them a checklist of scenarios tied to the release scope. Track their findings like any other defects, and treat their sign-off as one of the release criteria.

## Regression and integration

### 73. What is regression testing?

Regression testing re-runs existing tests after a change to confirm that previously working functionality still works. It is how you catch unintended side effects of a fix or feature.

### 74. Why does regression testing matter in release QA?

Most production escapes are not in the new feature — they are in something old that the new change broke. Every change risks side effects, and regression is the only systematic way to catch them before users do.

### 75. How would you test or handle regression testing?

After any change, run the regression suite covering the changed area, its dependencies, and the core user journeys. If full regression is impossible in the window, run a risk-based subset first and say what you skipped.

### 76. What is integration testing?

Integration testing verifies that separately built parts work correctly together — modules within the system, or your system with databases, third-party services, and other applications.

### 77. Why does integration testing matter in release QA?

Most release failures happen at the seams: the API contract changed, the database schema moved, the third-party service behaves differently in production. Unit tests cannot see these — only integration testing can.

### 78. How would you test or handle integration testing?

Identify the connections your release touches — services, databases, external systems — and test real calls across each boundary, including failure cases (timeouts, error responses). Pay special attention to version mismatches during a release window.

### 79. What is the difference between retesting and regression testing?

Retesting verifies a specific fix: run the original bug's steps and check it is gone. Regression testing checks that the fix did not break anything else. A fixed bug needs both.

### 80. Why does the retest vs regression distinction matter in release QA?

Conflating them is a classic mistake: a developer fixes a bug, QA retests only that bug, and the release ships with a new defect next to it. Saying "verified the fix" without regression coverage is reporting half the story.

### 81. How would you test or handle retesting and regression?

When a fix arrives, first retest the exact reproduction steps on the right build, then run the regression cases around the changed area and the core flows. Report both results separately in your evidence.

### 82. What is a regression suite?

A regression suite is the maintained collection of test cases that protect existing functionality — the core journeys and previously fixed bugs that must keep passing with every release.

### 83. Why does a regression suite matter in release QA?

It is the team's safety net and its institutional memory. Every bug that escaped to production should add a case to the suite, so the same bug can never silently return.

### 84. How would you test or handle a regression suite?

Keep it alive: add a case for every significant fixed defect, remove or update cases that no longer match the product, and mark which subset to run when time is short. A stale suite fails silently — old cases pass while the product has moved on.

### 85. What is a flaky test?

A flaky test is one that passes and fails on the same code with no product change — caused by timing, environment instability, or test design. It is the test equivalent of an unreliable witness.

### 86. Why do flaky tests matter in release QA?

They destroy trust in the test results. When failures are routinely ignored as flaky, real failures get ignored too, and the team loses its early-warning system. Flakiness is a defect in the test, and it deserves fixing like any other.

### 87. How would you test or handle a flaky test?

If a test fails once, re-run to confirm whether it is consistent. Report persistent flakiness instead of silently re-running until green. Quarantine badly flaky tests from the release gate until fixed, but track them so they are not forgotten.

## Defect management

### 88. What is the defect lifecycle?

The defect lifecycle is the journey of a bug from discovery to closure: reported, triaged, assigned, fixed, retested, verified, closed — with states like rejected or reopened when things do not go smoothly.

### 89. Why does the defect lifecycle matter in release QA?

It is how a bug becomes an outcome. Bugs that sit unowned or unverified are risks you cannot measure. Knowing the lifecycle lets you see the real state of the release: how many defects are open, fixed, verified, or stuck.

### 90. How would you test or handle the defect lifecycle?

Report defects with enough information to fix them, move them honestly between states, retest fixes on the right build, and never close a defect you have not personally verified. A reopened defect is normal — treat it as a new round, not a failure.

### 91. What is the difference between severity and priority?

Severity is how bad the defect is technically — the impact if it occurs: data loss is severe, a typo is not. Priority is how urgently it should be fixed, which depends on business factors: deadlines, workarounds, customer commitments. A cosmetic typo on the login page of a flagship product can be low severity but high priority.

### 92. Why does severity vs priority matter in release QA?

Because they answer different questions and different people own them. QA usually owns severity (impact assessment); product or the triage group owns priority (business urgency). Mixing them up causes both under-fixing critical bugs and over-spending on trivia.

### 93. How would you test or handle severity and priority?

Assign severity based on impact — data loss, security, outage, and broken core flows are severe. Then let priority be decided with the team based on timing and business needs. When the two conflict, say so explicitly in triage.

### 94. What goes into a good bug report?

A good bug report lets a developer reproduce and fix the defect without asking you anything: a short summary, exact steps to reproduce, expected vs actual results, the build/version and environment, screenshots or logs, and severity.

### 95. Why do good bug reports matter in release QA?

The bug report is QA's main deliverable to developers. Vague reports ("it's broken") bounce back, waste cycles, and breed frustration. A precise report with reproduction steps gets fixed fast and earns respect for QA's work.

### 96. How would you test or handle writing bug reports?

Reproduce the bug at least twice before reporting, write the steps as if for someone who has never seen the screen, attach evidence (screenshot, video, log), and state expected vs actual plainly. Check for duplicates first.

### 97. What is defect triage?

Defect triage is the regular meeting where the team reviews new and open defects, confirms they are valid, sets severity and priority, assigns owners, and decides which ones block the release.

### 98. Why does defect triage matter in release QA?

It prevents defect chaos: duplicates, mislabeled severities, orphaned bugs, and last-minute surprises at go/no-go. A well-run triage keeps the defect list honest and the release decision informed.

### 99. How would you test or handle defect triage?

Come prepared with your defects reproduced and evidence ready. Present facts — impact, steps, workaround — and let the group decide priority and ownership. After triage, track that decisions are recorded on the ticket, not just in the room.

### 100. What are duplicate and not-a-bug defects?

A duplicate is the same underlying defect reported more than once, often with different symptoms. A not-a-bug is a report that, on investigation, matches the intended behavior, a configuration error, or an environment issue.

### 101. Why do duplicates and not-a-bugs matter in release QA?

They distort the release picture: a list full of duplicates looks worse than reality, and wrongly-closed real defects look better. Clean defect hygiene keeps the go/no-go numbers meaningful.

### 102. How would you test or handle duplicates and not-a-bugs?

Search existing tickets before reporting, and when closing as duplicate or not-a-bug, write why in the ticket and agree with the reporter. Be careful: many "not-a-bug" closings are real bugs with a different root cause — investigate before closing.

## CI/CD basics

### 103. What is continuous integration (CI)?

Continuous integration means developers merge code frequently — at least daily — and every merge triggers an automated build and test run, so integration problems are found in minutes instead of at release time.

### 104. Why does CI matter in release QA?

It moves defect detection to the cheapest possible moment. Instead of discovering at release time that two developers' changes conflict, the team learns within minutes of the merge. For QA, CI means the candidate build arrives already carrying automated test results.

### 105. How would you test or handle CI?

Check that the pipeline actually runs meaningful tests on every merge — not just compilation — and that failures are visible and acted on. For a release, review the CI history of the candidate branch: a green final run means little if it was preceded by a string of ignored failures.

### 106. What is continuous delivery (CD)?

Continuous delivery keeps the software in a releasable state at all times: after CI, the build passes automated tests and is packaged and deployed to an environment automatically, though the final production release may still need approval.

### 107. Why does CD matter in release QA?

It changes QA's job from "validate this one big release" to "keep the flow of small releases safe". Releases become routine, small, and low-risk instead of rare, large, and terrifying — and each one is easier to test and to roll back.

### 108. How would you test or handle CD?

Verify that every change flows through the same automated checks on the way to production, and that manual gates exist where they are agreed. When a deploy is automated, test the deployment itself — configuration, secrets, startup — not just the features.

### 109. What role do automated tests play in a CI/CD pipeline?

Automated tests are the pipeline's quality gates: unit tests run on every merge, then integration and UI tests on the candidate build, and the pipeline blocks promotion when a gate fails.

### 110. Why do tests in the pipeline matter in release QA?

They give every release a floor of verified quality before a human ever looks at it. Your manual effort is then spent on what automation cannot judge — new behaviors, usability, exploration — instead of re-checking old ground.

### 111. How would you test or handle tests in the pipeline?

Review which tests run at which stage and whether they cover the release's critical paths. When a pipeline failure appears, treat it as a product failure until proven otherwise — investigate before re-running or bypassing.

## API basics

### 112. What is an API?

An API (Application Programming Interface) is a defined way for software to talk to other software. For testers, it usually means the HTTP endpoints a backend exposes: a URL, a method, and a structured response.

### 113. Why do APIs matter in release QA?

APIs are the plumbing behind most modern applications — the mobile app, the website, and partners all talk through them. Bugs in an API affect every client at once, and many can be caught faster and more precisely by testing the API directly than through the UI.

### 114. How would you test or handle an API?

Send requests to the endpoint with a tool like Postman or curl, using valid and invalid inputs, and check the response body, status code, and side effects (database rows, downstream calls). Test both success and error paths, not just the happy case.

### 115. What is REST?

REST is a common style for designing APIs: resources identified by URLs, manipulated with standard HTTP methods (GET, POST, PUT, DELETE), and returning structured data, usually JSON, in responses.

### 116. Why does REST matter in release QA?

Because most APIs you will test are REST-style, and the style gives you a predictable structure: the same method on the same resource should behave consistently. Once you understand the conventions, you can test unfamiliar endpoints quickly.

### 117. How would you test or handle a REST API?

Map the resources and their methods from the API documentation, test each method's success and error responses, and verify the resource state actually changes correctly — for example, after a DELETE, a GET should return 404.

### 118. What are the main HTTP verbs?

The main HTTP verbs are GET (read), POST (create), PUT or PATCH (update), and DELETE (delete). Each verb is a different instruction to the server about what to do with the resource.

### 119. Why do HTTP verbs matter in release QA?

Because using the wrong verb is a classic bug: a GET that changes data, a POST that duplicates records when retried, a DELETE with no protection. Testing each verb against each resource catches dangerous mistakes that the UI may hide.

### 120. How would you test or handle HTTP verbs?

For each resource, test the verbs it should support and confirm the ones it should not support are rejected (for example, DELETE on a read-only resource returns 405). Check idempotency for repeated POSTs where duplicates would be harmful.

### 121. What are HTTP status codes?

Status codes are the three-digit numbers a server returns with every response, grouped by meaning: 2xx success, 3xx redirect, 4xx client error (your request is wrong), 5xx server error (the server failed).

### 122. Why do status codes matter in release QA?

They are the API's first answer to every question you ask it. A 200 with a wrong body is a bug; a 500 on a valid request is a possible blocker. Checking status codes is the fastest way to scan an API's health during a release.

### 123. How would you test or handle status codes?

For each endpoint, test the expected success code, then the expected errors: 400 for malformed input, 401/403 for authentication problems, 404 for missing resources, 500 for induced server failures. Verify the body and behavior match the code — a 200 that returns an error message is still a bug.

### 124. What is basic API testing?

Basic API testing is sending requests to endpoints and verifying responses and side effects: correct status code, correct data structure and values, correct handling of errors, and correct changes to stored data.

### 125. Why does basic API testing matter in release QA?

It finds defects below the surface that UI testing cannot pinpoint, and it finds them earlier, because APIs can be tested as soon as the backend deploys — before any UI exists. It is also the foundation every automation tool builds on.

### 126. How would you test or handle basic API testing?

Start from the API documentation, build a request collection (for example in Postman), and cover: valid requests, invalid data, missing fields, wrong auth, and boundary values. Record status code, response body, and any database changes in your evidence.

## Web and UI testing

### 127. What is cross-browser testing?

Cross-browser testing verifies that a web application behaves correctly in the browsers your users actually use — typically Chrome, Edge, Safari, and Firefox — on the relevant operating systems and viewports.

### 128. Why does cross-browser testing matter in release QA?

Browsers render the same code differently, especially older Safari or specific mobile browsers. A release can work perfectly in Chrome and break in the browser a third of your users use. The browser matrix is part of the release's risk surface.

### 129. How would you test or handle cross-browser testing?

Agree with the team which browsers and versions to support based on usage data. Test the critical user journeys in each, not just the home page, and report any browser-specific defect with the exact browser and version in the report.

### 130. What is responsive design testing?

Responsive design testing checks that the layout adapts correctly to different screen sizes — desktop, tablet, phone — without broken layouts, hidden controls, or unusable touch targets.

### 131. Why does responsive design testing matter in release QA?

Most traffic today is mobile, and a release that breaks the mobile layout breaks the product for most users. Layout bugs also ship silently — they rarely show in backend tests or desktop-only checks.

### 132. How would you test or handle responsive design testing?

Test the main journeys at the viewport sizes in your supported range, using browser dev tools or real devices. Check that nothing overlaps, no button becomes unreachable, and content does not require horizontal scrolling where it should not.

### 133. What is form validation testing?

Form validation testing checks that forms accept valid input, reject invalid input with clear messages, and never lose or corrupt data on submission — including after a server error.

### 134. Why does form validation matter in release QA?

Forms are where users and the system exchange data, and where data quality is born or lost. A form that accepts garbage silently creates support tickets and corrupt reports for months. A form that rejects valid input blocks real users.

### 135. How would you test or handle form validation?

For every field: valid value, empty, boundary values, invalid types, and special characters. Then the whole form: required fields missing, duplicate submission (double click), long input, and submission when the server returns an error. Confirm the user's entered data survives a failed submit.

### 136. What are browser developer tools?

Browser developer tools (DevTools) are the built-in panel in every browser for inspecting pages: viewing network requests, console errors, element inspection, storage, and simulating devices and slow networks.

### 137. Why do browser developer tools matter in release QA?

They let you see what the browser actually received and did — failed requests, JavaScript errors, missing files — which turns "the page looks wrong" into a precise, reportable defect. DevTools are the tester's microscope.

### 138. How would you test or handle using browser developer tools?

When something looks wrong, open DevTools and check the console for errors and the network tab for failed or slow requests. Capture the failing request details in your bug report — a screenshot of the console or network entry is worth a paragraph of description.

## Database and data migration

### 139. What is database testing?

Database testing verifies that the application stores, retrieves, and changes data correctly: correct tables and columns, correct data types and constraints, and correct data after every operation.

### 140. Why does database testing matter in release QA?

The database is where most of the product's actual value lives. A UI that displays wrong data or a process that silently drops records can pass every screen-level test. Release QA must look beneath the screens at the data itself.

### 141. How would you test or handle database testing?

For each data-changing operation, check the rows before and after: correct values, correct rows affected, no orphans, constraints enforced. Use direct queries as a second pair of eyes on what the UI claims happened.

### 142. What is a data migration?

A data migration is the process of moving or transforming data when the system changes — for example, when a release changes the database schema, merges tables, or moves data to a new structure.

### 143. Why do data migrations matter in release QA?

Migrations are among the riskiest parts of any release: they touch every row of existing customer data, they are hard to roll back, and a mistake may not be visible until days later. Many of the worst production incidents in history were migration failures.

### 144. How would you test or handle a data migration?

Run the migration on a copy of production-like data, then verify counts and content before and after — no data lost, no data corrupted, every transform correct. Test the rollback path too, and confirm the old and new application versions both work with the migrated data if there is a transition period.

### 145. What is data integrity?

Data integrity means the data is accurate and consistent: values are valid, relationships are intact (a child record's parent exists), and constraints are enforced. Broken integrity shows up as orphaned records, duplicate rows, or impossible values.

### 146. Why does data integrity matter in release QA?

Integrity problems compound silently — one broken relationship today becomes wrong reports, failed processes, and angry customers in the months after the release. They are the most expensive class of bugs to fix later, because the bad data must be repaired by hand.

### 147. How would you test or handle data integrity?

After any data-changing operation, run integrity checks: record counts before and after, foreign key validity, unique constraints, and spot-check content. Include integrity checks in every migration test, not just functional flows.

### 148. What is test data management?

Test data management is preparing and maintaining the data your tests need: realistic datasets, specific edge-case records, and procedures to reset data between test runs.

### 149. Why does test data management matter in release QA?

Without it, testers waste hours hunting for "a user who has an expired card and a pending order", tests fail for data reasons instead of product reasons, and environments become polluted. With it, tests are repeatable and failures are trustworthy.

### 150. How would you test or handle test data management?

Build reusable datasets for common scenarios, keep them versioned and refreshable, and isolate them from each other (each test creates and cleans up its own records where possible). Never use real customer data in test environments without approval and protection.

## Agile and collaboration

### 151. What is scrum?

Scrum is a framework for organizing work in short fixed cycles (sprints, usually 1–2 weeks) with defined roles and ceremonies: planning, daily standup, review, and retrospective. The goal is frequent, inspectable progress.

### 152. Why does scrum matter in release QA?

It defines when and how QA participates: testing happens inside the sprint, not after it. For release QA it means a steady stream of small, tested increments instead of one giant untested release at the end.

### 153. How would you test or handle working in scrum?

Get involved in planning so testing effort is visible and included in estimates. Test continuously during the sprint rather than at the end, and use the retrospective to raise process problems like unclear criteria or late handoffs.

### 154. What is a user story?

A user story is a short description of a feature from the user's perspective: "As a customer, I want to reset my password so that I can regain access to my account." It carries acceptance criteria that define when the story is done.

### 155. Why do user stories matter in release QA?

They are the unit of scope for testing: each story's acceptance criteria are your test oracle. Stories without criteria are untestable — you end up guessing what "working" means, and arguing about it later.

### 156. How would you test or handle user stories?

For each story in the release, test the acceptance criteria explicitly and explore around them for edge cases. If a story arrives without criteria, raise it at the earliest possible moment — preferably before development starts.

### 157. What is the definition of done?

The definition of done is the team's shared checklist of what must be true before work counts as complete: code reviewed, tested, criteria met, documentation updated, no open critical defects.

### 158. Why does the definition of done matter in release QA?

It is the team's quality contract. Without it, "done" means "the developer stopped working on it", and QA inherits unfinished work at release time. With it, quality is built in rather than inspected in at the end.

### 159. How would you test or handle the definition of done?

Help define it so it includes testable outcomes, and hold it during the sprint: work that does not meet the definition is not done, regardless of the deadline. In the release context, the definition of done feeds directly into your release criteria.

### 160. What is the QA role in a sprint?

QA in a sprint tests early and continuously: reviewing stories and criteria before development, testing as soon as builds arrive, pairing with developers on tricky areas, and giving fast feedback instead of waiting for the end.

### 161. Why does the QA role in a sprint matter in release QA?

When QA only tests at the end of a release, every defect found there is expensive and schedule-threatening. QA embedded in the sprint finds problems when they are cheap to fix — which is what makes the final release window calm instead of chaotic.

### 162. How would you test or handle your role in a sprint?

Attend planning and standups, keep a testing task board visible, and test incrementally as stories complete. Communicate risk early and often — a one-line update that a story is not testable today beats a surprise at the release boundary.

## Documentation and evidence

### 163. What is test evidence?

Test evidence is the record that proves testing happened and what the result was: exact build and environment, test case executed, steps, expected vs actual result, timestamps, screenshots, and logs.

### 164. Why does test evidence matter in release QA?

Because after the release, the only thing left of your testing is what you recorded. Evidence answers the questions that always come: was this tested? Against which build? What exactly happened? It is also what protects the team in audits and post-incident reviews.

### 165. How would you test or handle test evidence?

Record evidence as you test, not from memory afterward. Capture the build number, environment, date, and result for every executed case, and store it somewhere the whole team can find. A blocked or not-run test must be recorded as such — never as passed.

### 166. What are release notes?

Release notes are the user- and team-facing summary of what a release contains: new features, fixed defects, known issues, and any actions users need to take.

### 167. Why do release notes matter in release QA?

They are part of the release deliverable and a communication channel to users and support. A defect that ships with a documented workaround is a managed risk; the same defect undocumented is a support storm. QA often verifies that the notes match what actually shipped.

### 168. How would you test or handle release notes?

Review the notes against the release scope and defect list: features included, fixes included, known issues disclosed, version correct. Flag anything in the notes that is not in the release, and anything in the release that is missing from the notes.

### 169. What is a test summary report?

The test summary report is the end-of-release document that answers "how did testing go?": scope tested, build and environment, results against criteria, defect summary, untested areas, and the QA recommendation.

### 170. Why does a test summary report matter in release QA?

It is the artifact the go/no-go decision is actually made from. Stakeholders cannot read your spreadsheets; they read the summary. A clear, honest summary — including what was not tested — is QA's core contribution to the release decision.

### 171. How would you test or handle a test summary report?

Write it as the release closes: one page, build details, results against each release criterion, open defects with severity, and explicit untested areas. State a go/no-go recommendation only if asked, and separate facts from judgment.

### 172. What is sign-off?

Sign-off is the formal approval by the accountable parties — QA, product, engineering, sometimes security or operations — that a release may proceed. Each signer takes responsibility for their area of the release.

### 173. Why does sign-off matter in release QA?

It makes accountability explicit. When the release later goes wrong, the record shows who approved what on what evidence. Sign-off also forces the last honest look: no one signs a release they are uncomfortable with without thinking twice.

### 174. How would you test or handle sign-off?

Sign only on written evidence: the build you tested, the results you recorded, and the criteria you evaluated. If something is untested or unresolved, say so in writing with your sign-off or refusal. Never sign off on work you did not test.

## Risk and troubleshooting

### 175. What is risk in release QA?

Risk is the combination of how likely something is to go wrong and how much damage it would do. Release QA constantly weighs risk: which areas to test first, which defects block, what is acceptable to ship.

### 176. Why does risk matter in release QA?

Because you can never test everything. Risk is the basis for every prioritization decision — test effort, defect severity, go/no-go. Testers who think in terms of risk spend their time where it protects the most value.

### 177. How would you test or handle risk?

Rank the release's areas by likelihood of failure and business impact, and test in that order. When time runs out, the untested remainder is the least risky part — and you can say so with evidence instead of apology.

### 178. What is escalation?

Escalation is raising a problem to the people with authority to resolve it, when you cannot resolve it yourself — a blocking defect, a missing environment, a decision nobody is making. It is not complaining; it is routing a problem to its owner in time to matter.

### 179. Why does escalation matter in release QA?

Because quiet blockers kill releases. A problem raised on day one is a decision; the same problem raised the day before release is a crisis. Escalation is how QA keeps the release honest and on schedule.

### 180. How would you test or handle escalation?

Escalate with facts, not frustration: what is blocked, since when, what you tried, what you need, and by when. Escalate to the right owner first, keep a record, and follow up if there is no response. Escalating late is the only wrong way to escalate.

### 181. What is a blocking issue?

A blocking issue is a defect or problem that prevents testing or shipping from proceeding: the build does not deploy, a critical flow is down, the test environment is unusable, or an exit criterion cannot be met.

### 182. Why do blocking issues matter in release QA?

They are the highest-priority items in the release, and how they are handled defines the release. A blocker that is ignored while testing "continues around it" produces results that look productive but prove nothing about the release.

### 183. How would you test or handle a blocking issue?

When you hit a blocker, stop dependent testing rather than working around it silently. Report it with evidence, agree with the team on who fixes it and when, and resume only after the block is cleared. Track blockers separately in your summary — they tell the true story of the release.

### 184. What is post-release validation?

Post-release validation is checking the release in production after it goes live: the new version is actually deployed, key journeys work with real data and real traffic, and monitoring shows no unusual errors.

### 185. Why does post-release validation matter in release QA?

Because production is the only fully real environment. Some problems only appear there — real data, real scale, real integrations. A short, targeted check after go-live catches a broken release while rollback is still cheap.

### 186. How would you test or handle post-release validation?

Immediately after go-live, verify the deployed version, run a quick smoke of the critical journeys against production, and watch the dashboards for errors and business metrics for an agreed period. Report findings back to the release channel, and be ready to trigger the rollback plan if something is wrong.
