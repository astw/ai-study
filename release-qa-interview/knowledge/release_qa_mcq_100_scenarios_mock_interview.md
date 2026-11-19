# Release QA — Multiple-Choice, Real-World Scenarios & Mock Interview

**Supplement to the 1,000-question Release QA bank**

Contents:
- Part 1: 100 multiple-choice questions with answers and explanations
- Part 2: 100 realistic release scenarios with recommended responses
- Part 3: 25 mock interview questions with sample answers

## Part 1 — Multiple-choice questions

Choose the best answer before reading the explanation. Each question has one best answer.

### MCQ 1. A new build has just been deployed to staging. What should QA execute first?
A. Performance testing
B. Smoke testing
C. Full regression testing
D. Penetration testing
**Answer: B.** Smoke testing checks whether the build's critical paths are basically functional before deeper testing.

### MCQ 2. A login smoke test fails immediately after deployment. What is the best next step?
A. Continue the full regression suite
B. Record it as a low-priority UI defect
C. Stop broader testing and investigate build/environment health
D. Approve the release if other pages load
**Answer: C.** A failed critical smoke test suggests the build may not be testable. Triage the failure before spending time on broad suites.

### MCQ 3. A developer says a defect is fixed. What should QA do?
A. Close it based on the developer's message
B. Retest the original reproduction steps on the identified build
C. Wait for production feedback
D. Run only performance tests
**Answer: B.** Retest the original steps and verify the fix on the correct build; add regression coverage where appropriate.

### MCQ 4. Which best describes regression testing?
A. Testing only newly added features
B. Checking existing functionality after changes
C. Measuring server throughput
D. Checking whether a deployment command completed
**Answer: B.** Regression testing looks for unintended effects of changes on existing behavior.

### MCQ 5. A critical API returns HTTP 500 in staging after deployment. What should happen?
A. Ignore it if the UI loads
B. Treat it as a potential blocker and investigate logs/dependencies
C. Change the expected result to 500
D. Wait until production
**Answer: B.** A server error on a critical path needs triage, impact assessment, and resolution or explicit risk acceptance.

### MCQ 6. Which identifier should appear in release test evidence?
A. Only the tester's name
B. Exact build/version and environment
C. Only the sprint number
D. The production server password
**Answer: B.** Evidence must identify exactly what was tested and where.

### MCQ 7. A test fails only in staging, but passes locally. What should QA compare first?
A. The tester's preferred browser theme
B. Build, configuration, data, dependencies, and environment differences
C. The team's vacation calendar
D. Only source-code formatting
**Answer: B.** Environment drift and configuration differences commonly explain inconsistent results.

### MCQ 8. A release contains a database schema change. Which risk deserves explicit testing?
A. Only button colors
B. Compatibility of old/new application versions with the schema and migration
C. Only spelling in release notes
D. No risk if migration script compiles
**Answer: B.** Schema changes can affect running versions, data integrity, rollback, and deployment sequencing.

### MCQ 9. A test suite has intermittent failures with no product change. What is this called?
A. A deterministic pass
B. A flaky test
C. A code freeze
D. A canary release
**Answer: B.** Flaky tests produce inconsistent outcomes and reduce confidence in the pipeline.

### MCQ 10. Which is the strongest release exit criterion?
A. QA feels comfortable
B. All tests pass, regardless of scope
C. Pre-agreed measurable criteria are met and residual risks are documented
D. No defects were ever found
**Answer: C.** Exit criteria should be objective, agreed in advance, and include risk and defect status.

### MCQ 11. A P1 defect is open in a core payment workflow. What is the appropriate release stance?
A. Ship automatically
B. Assess impact and normally block pending resolution or explicit authorized risk acceptance
C. Hide the defect from the report
D. Downgrade severity to meet the deadline
**Answer: B.** A critical defect in a core flow is normally a release blocker unless an accountable authority explicitly accepts the risk.

### MCQ 12. A product owner asks QA to skip regression to meet a date. Best response?
A. Agree without recording it
B. Explain change impact and risk, propose a risk-based minimum suite, and document the decision
C. Refuse to test anything
D. Run only tests that passed last release
**Answer: B.** Offer an evidence-based risk reduction plan and ensure any residual risk is visible and accepted by the right owner.

### MCQ 13. What does a canary deployment do?
A. Deploys to every user simultaneously
B. Exposes a small portion of traffic to a new version and monitors it
C. Deletes the old version before testing
D. Runs only unit tests
**Answer: B.** Canary releases limit exposure while teams monitor health and business indicators.

### MCQ 14. What is the main purpose of a rollback plan?
A. Guarantee no defects exist
B. Define a controlled way to return to a known-good state
C. Replace test execution
D. Avoid release notes
**Answer: B.** Rollback planning reduces recovery time and clarifies triggers, ownership, and data implications.

### MCQ 15. A release has a known low-severity defect with a documented workaround. What should QA ensure?
A. It is omitted from the release report
B. Impact, workaround, affected versions, and acceptance owner are documented
C. It is automatically fixed by deployment
D. All tests are rerun from scratch
**Answer: B.** Known issues must be transparent so support, product, and release decision-makers understand the residual risk.

### MCQ 16. Which metric best exposes tail latency?
A. Average response time only
B. p95/p99 latency
C. Number of commits
D. Number of test cases written
**Answer: B.** Percentiles reveal slow experiences affecting a subset of requests that averages can hide.

### MCQ 17. A service passes functional tests but fails under expected load. What is the conclusion?
A. The release is fully ready
B. Functional success does not satisfy performance requirements
C. Performance is unrelated to release quality
D. Delete the load test
**Answer: B.** Release readiness includes non-functional requirements where they apply.

### MCQ 18. An API POST request is retried after a timeout. What should QA check?
A. Whether duplicate actions or records are created
B. Only the response font
C. Whether GET requests are faster
D. Only the API hostname
**Answer: A.** Retries can duplicate non-idempotent operations unless idempotency is designed and validated.

### MCQ 19. A user can access another user's record by changing an ID in the URL. What type of issue is this?
A. Cosmetic defect
B. Authorization/access-control vulnerability
C. Performance regression
D. Localization issue
**Answer: B.** Object-level authorization must be enforced server-side for every requested resource.

### MCQ 20. Which test data is preferred for staging when production data is sensitive?
A. Unmasked production export
B. Approved synthetic or properly masked data
C. Personal data copied into spreadsheets
D. Shared administrator credentials
**Answer: B.** Use controlled data that protects privacy while preserving test value.

### MCQ 21. What is the purpose of a quality gate in CI/CD?
A. Make builds slower
B. Prevent progression when required quality checks fail
C. Replace peer review in all cases
D. Automatically accept all defects
**Answer: B.** Quality gates enforce agreed checks before artifacts move to later stages.

### MCQ 22. A feature flag is off for most users but on for a pilot group. What should QA test?
A. Only the default state
B. Enabled/disabled states, targeting rules, transitions, and fallback behavior
C. Only the database backup
D. Only mobile installation
**Answer: B.** Feature flags create multiple behavior paths and need validation across targeting and state changes.

### MCQ 23. A migration reports success. What additional check is valuable?
A. Assume data is correct
B. Reconcile record counts, constraints, relationships, and representative records
C. Delete the backup
D. Skip application testing
**Answer: B.** A successful script exit does not prove data correctness.

### MCQ 24. Which best describes an entry criterion?
A. A condition required before a test phase begins
B. A defect severity
C. A production alert
D. A release note heading
**Answer: A.** Entry criteria ensure the build, environment, data, and prerequisites are ready.

### MCQ 25. A deployment succeeds but the service is not ready to accept traffic. What should QA distinguish?
A. Liveness and readiness health checks
B. Severity and priority
C. Unit and mutation testing
D. Version and branch names
**Answer: A.** A process can be alive while not ready to serve requests because dependencies or initialization are incomplete.

### MCQ 26. Which is the best defect report?
A. 'It doesn't work'
B. Exact build/environment, steps, expected/actual results, frequency, and evidence
C. A screenshot without context
D. A verbal complaint only
**Answer: B.** A reproducible, evidence-rich report speeds triage and avoids ambiguity.

### MCQ 27. A defect is severe but affects a rarely used admin function. How should priority be set?
A. Severity alone determines priority
B. Consider impact, likelihood, exposure, workaround, and business commitments
C. Always set priority to low
D. Let the tester choose privately
**Answer: B.** Severity and priority are related but distinct; priority is a decision about urgency.

### MCQ 28. What is the safest way to handle a failed deployment?
A. Make undocumented manual changes
B. Follow the deployment runbook, assess state, and escalate to the owner
C. Immediately delete logs
D. Continue as though it succeeded
**Answer: B.** Controlled recovery protects environment integrity and preserves evidence.

### MCQ 29. What does idempotency mean?
A. Every retry creates a new result
B. Repeating an operation has no additional unintended effect
C. A request has no authentication
D. An API never times out
**Answer: B.** Idempotency is important for safe retries and duplicate request handling.

### MCQ 30. Which is an example of negative testing?
A. Submit a valid email address
B. Submit malformed input and verify safe validation
C. Check the page title
D. Measure normal throughput
**Answer: B.** Negative tests check invalid and unexpected inputs and safe error handling.

### MCQ 31. What is boundary value analysis?
A. Testing random values only
B. Testing values at and around input limits
C. Testing every possible value
D. Testing only valid workflows
**Answer: B.** Boundary values often expose off-by-one and validation defects.

### MCQ 32. A critical test is blocked by unavailable test data. How should it be reported?
A. As passed
B. As blocked, with dependency, owner, impact, and next action
C. As failed product behavior
D. Remove it from scope without comment
**Answer: B.** Blocked is distinct from failed and must remain visible in release reporting.

### MCQ 33. A release changes an API response field from optional to required. What is the main concern?
A. Backward compatibility for existing clients
B. Screen brightness
C. Database backup naming
D. Test case numbering
**Answer: A.** Existing consumers may not send the new required field, causing integration failures.

### MCQ 34. What should a post-release validation focus on?
A. Every possible test case
B. Critical user journeys and production health indicators
C. Only code style
D. Only developer workstation status
**Answer: B.** Post-release checks should be fast, targeted, and aligned to the most important risks.

### MCQ 35. What is the purpose of a code freeze?
A. Stop all testing
B. Limit changes during stabilization and control exceptions
C. Prevent release notes
D. Guarantee zero defects
**Answer: B.** A freeze reduces late change risk; approved exceptions still require impact analysis and testing.

### MCQ 36. A security scanner reports a vulnerable library. What should QA/release team do?
A. Ignore all scanner findings
B. Assess affected version, exploitability, exposure, and approved remediation
C. Publish the scanner log with secrets
D. Assume no risk if tests pass
**Answer: B.** Scanner results need triage and risk assessment rather than blind acceptance or dismissal.

### MCQ 37. What is least privilege?
A. Everyone has admin rights
B. Each identity receives only the access needed for its task
C. No user can log in
D. Permissions are inherited without review
**Answer: B.** Least privilege limits damage from mistakes or compromised accounts.

### MCQ 38. Which approach is best for flaky automated tests?
A. Rerun until green and hide failures
B. Investigate timing, state, dependencies, data collisions, and environment instability
C. Delete the whole suite
D. Mark all failures as product defects
**Answer: B.** Find and fix the source of nondeterminism; do not conceal unreliable results.

### MCQ 39. A release changes a shared authentication component. Which regression scope is sensible?
A. Only the changed page
B. All important authentication consumers and critical login/session journeys
C. Only performance tests
D. No regression because the component is shared
**Answer: B.** Shared components have broad blast radius; test dependent applications and workflows.

### MCQ 40. What is a release readiness review?
A. A code review only
B. A structured review of scope, test evidence, defects, operations, approvals, and recovery readiness
C. A customer survey
D. A performance benchmark only
**Answer: B.** It combines technical and operational evidence before the release decision.

### MCQ 41. A production alert fires after rollout and error rate rises above the agreed threshold. What should happen?
A. Wait for complaints
B. Follow incident process, assess impact, and apply rollback/mitigation criteria
C. Disable monitoring
D. Close the release ticket
**Answer: B.** Use predefined thresholds and incident ownership to respond quickly.

### MCQ 42. What does test traceability connect?
A. Only testers to managers
B. Requirements/risks to test cases, results, and defects
C. Only build numbers to servers
D. Only code style to pull requests
**Answer: B.** Traceability exposes coverage gaps and supports impact analysis.

### MCQ 43. Which is the strongest evidence that a rollback works?
A. A written statement that it should work
B. A controlled rehearsal or verified procedure with measured outcome
C. A green unit test
D. A screenshot of the release calendar
**Answer: B.** Recovery procedures should be exercised and validated, not merely documented.

### MCQ 44. A new build has a different commit than the build previously tested. What should QA do?
A. Assume it is equivalent
B. Verify the artifact and assess/repeat impacted tests on the exact candidate
C. Reuse old results without checking
D. Approve based on version label only
**Answer: B.** Test evidence must map to the exact artifact being considered for release.

### MCQ 45. What is the purpose of a soak test?
A. Test sudden spikes only
B. Run sustained load to reveal gradual degradation or resource leaks
C. Test keyboard navigation
D. Validate translations
**Answer: B.** Long-duration testing can expose leaks and cumulative resource problems.

### MCQ 46. What is a dead-letter queue used for?
A. Store successful web pages
B. Hold messages that could not be processed after configured handling
C. Replace application logs
D. Encrypt database backups
**Answer: B.** Dead-letter handling preserves failed messages for investigation and controlled reprocessing.

### MCQ 47. Which action best supports accessibility validation?
A. Mouse-only testing
B. Keyboard navigation, focus order, labels, contrast, and assistive-technology checks
C. Only test on a large monitor
D. Disable semantic markup
**Answer: B.** Accessibility needs multiple checks; automated scans alone are not sufficient.

### MCQ 48. A team wants to deploy without QA sign-off. What is the best response?
A. Block forever without discussion
B. Clarify governance, provide evidence and risks, and ensure an authorized owner accepts any exception
C. Silently approve
D. Delete test results
**Answer: B.** QA should make risk transparent and follow agreed release authority rather than silently bypassing controls.

### MCQ 49. What should release notes be checked against?
A. Only marketing wording
B. Approved scope, actual shipped changes, known issues, and compatibility impact
C. Only the previous release date
D. Only the developer's branch name
**Answer: B.** Release notes must accurately represent the shipped artifact.

### MCQ 50. What is environment drift?
A. A test case moving between folders
B. Unexpected differences in software/configuration between environments
C. A user changing browser tabs
D. A release meeting being delayed
**Answer: B.** Drift can make staging results unreliable and production behavior surprising.

### MCQ 51. Why measure p95 response time?
A. It is always equal to the average
B. It shows the response time within which 95% of measured requests complete
C. It counts 95% of test cases
D. It measures server disk size
**Answer: B.** Percentiles help understand user experience beyond average latency.

### MCQ 52. Which statement about QA and quality is most accurate?
A. QA alone owns all quality
B. Quality is shared; QA provides independent evidence and risk visibility
C. Developers do not test
D. Operations has no role
**Answer: B.** Quality is a team responsibility across the lifecycle.

### MCQ 53. A bug fix is merged after the regression suite ran. Can the old regression result approve the new build?
A. Yes, because the ticket is fixed
B. No; identify the new artifact and run appropriate retesting/regression
C. Yes, if the build number is similar
D. Only if no one noticed
**Answer: B.** Evidence from a previous artifact does not automatically apply to a changed candidate.

### MCQ 54. Which is the best way to prioritize tests when time is limited?
A. Run alphabetically
B. Prioritize critical business flows, changed components, dependencies, and high-risk failure modes
C. Run only easy tests
D. Skip tests with historical failures
**Answer: B.** Risk-based prioritization maximizes useful coverage under time constraints.

### MCQ 55. A new deployment changes a feature flag default. What should be verified?
A. Only the flag name
B. Default value, targeting, existing customer behavior, and rollback/disable path
C. Only the deployment duration
D. Only the source branch
**Answer: B.** A changed default can expose functionality to unintended users or alter existing behavior.

### MCQ 56. A service uses eventual consistency. Which assertion is most appropriate?
A. Data must be instantly identical in every system
B. Validate the documented convergence window and user-visible behavior during propagation
C. Ignore missing updates forever
D. Disable retries
**Answer: B.** Tests should reflect the consistency model and its service-level expectations.

### MCQ 57. What is the main goal of root cause analysis?
A. Assign blame
B. Identify underlying causes and prevention actions
C. Close the incident quickly without evidence
D. Rewrite the test plan
**Answer: B.** Root cause analysis should lead to durable corrective actions.

### MCQ 58. Which deployment pattern keeps two production-like environments and switches traffic?
A. Blue-green
B. Pairwise
C. Boundary-value
D. Waterfall
**Answer: A.** Blue-green deployment validates one environment before shifting traffic from the other.

### MCQ 59. What is a useful first step when a staging environment is unstable?
A. Run all tests repeatedly
B. Check deployment health, dependencies, capacity, configuration, and recent environment changes
C. Change product expectations
D. Close every defect
**Answer: B.** Stabilize and diagnose the environment before interpreting test outcomes.

### MCQ 60. A test passes when run alone but fails in the suite. Likely areas to inspect?
A. Test order, shared state, data collision, cleanup, and concurrency
B. Only CSS colors
C. Release notes
D. Customer billing plan
**Answer: A.** Suite-only failures often indicate hidden coupling or shared resources.

### MCQ 61. Which should be included in a Go/No-Go summary?
A. Only a pass percentage
B. Build identity, scope, test status, critical defects, residual risks, approvals, and recommendation
C. Only team attendance
D. Only number of commits
**Answer: B.** Decision-makers need concise, traceable evidence and explicit risk.

### MCQ 62. What is a safe handling practice for secrets in logs?
A. Print tokens for debugging
B. Redact secrets and restrict log access
C. Email credentials to the team
D. Store passwords in screenshots
**Answer: B.** Logs must support diagnosis without becoming a source of credential exposure.

### MCQ 63. A rollback restores application code but not the database schema. What concern remains?
A. None
B. The old application may be incompatible with the changed schema or data
C. Only the UI theme
D. Only browser cache
**Answer: B.** Application rollback and database rollback are separate concerns; compatibility must be planned.

### MCQ 64. Which is an example of a useful SLO?
A. The system should be good
B. 99.9% of eligible requests complete successfully over the defined measurement window
C. No bugs ever
D. Deploy every Friday
**Answer: B.** An SLO should specify an indicator, target, and measurement window.

### MCQ 65. A defect appears only for one customer tenant. What should QA capture?
A. Tenant identifier in a public report
B. Sanitized tenant context, configuration, data shape, timestamps, and correlation IDs
C. Only a generic screenshot
D. The customer's password
**Answer: B.** Tenant-specific configuration or data may matter, but evidence must protect customer secrets and personal data.

### MCQ 66. What is the purpose of a feature rollback/kill switch?
A. Replace test coverage
B. Disable a problematic feature quickly without necessarily reverting the entire deployment
C. Delete user data
D. Turn off monitoring
**Answer: B.** A kill switch can reduce impact while a broader fix is prepared.

### MCQ 67. Which is the best response to a flaky smoke test?
A. Treat every failure as harmless
B. Make the smoke test deterministic and investigate; critical smoke failures should remain visible
C. Remove all smoke tests
D. Approve after three retries
**Answer: B.** Smoke tests are a release gate; reliability and transparent failure handling matter.

### MCQ 68. What should be tested for session expiry?
A. Only login success
B. Expiry behavior, refresh, logout, revoked sessions, and protected-resource access
C. Only password length
D. Only page loading
**Answer: B.** Session lifecycle controls are essential to security and usability.

### MCQ 69. Which test type evaluates behavior beyond normal capacity to find limits?
A. Stress testing
B. Smoke testing
C. Localization testing
D. Snapshot testing
**Answer: A.** Stress testing explores capacity limits and failure behavior under excessive load.

### MCQ 70. What is the key distinction between severity and priority?
A. They are identical
B. Severity is impact; priority is urgency/order for fixing
C. Severity is assigned by users only
D. Priority measures latency
**Answer: B.** A serious issue may have different urgency depending on exposure, workaround, and business context.

### MCQ 71. A release has no open critical defects, but a critical test is not executed. What is true?
A. Release is automatically safe
B. There is a coverage/evidence gap that must be assessed against exit criteria
C. Not executed means passed
D. The test should be deleted
**Answer: B.** Absence of known defects is not proof of correctness when important tests were not run.

### MCQ 72. What is the purpose of a deployment runbook?
A. Marketing release description
B. Repeatable operational steps for deployment, validation, troubleshooting, and recovery
C. A list of employee birthdays
D. A replacement for monitoring
**Answer: B.** A runbook reduces ambiguity and supports consistent execution.

### MCQ 73. Which is the best practice for production-like staging data?
A. Use unrestricted production copies
B. Use synthetic or masked data with controlled access and documented refresh
C. Share database dumps publicly
D. Use personal data in screenshots
**Answer: B.** Data controls protect privacy and reduce accidental exposure.

### MCQ 74. A downstream service is unavailable during testing. What should QA do?
A. Assume integration passes
B. Record the dependency blocker and validate fallback/timeout behavior where possible
C. Change expected response to success
D. Skip it from the release report
**Answer: B.** Separate dependency availability from product behavior and preserve visibility of untested paths.

### MCQ 75. What does change impact analysis help determine?
A. Which office is hosting the release party
B. Affected components, workflows, integrations, data, and regression tests
C. Only who wrote the code
D. Only the color of the UI
**Answer: B.** Impact analysis guides efficient regression selection.

### MCQ 76. What is a good reason to run tests in parallel?
A. To hide failures
B. To reduce duration for independent tests while controlling shared-resource conflicts
C. To avoid collecting logs
D. To make results nondeterministic
**Answer: B.** Parallelism improves speed only when tests are isolated and results remain diagnosable.

### MCQ 77. What should happen when a release exception is approved?
A. No record is needed
B. Record approver, rationale, scope, residual risk, mitigation, and expiry/follow-up
C. Delete the failed test
D. Change the result to pass
**Answer: B.** Exceptions must be auditable and must not falsify test evidence.

### MCQ 78. Which statement best describes post-release monitoring?
A. Testing ends at deployment
B. Monitor technical and business indicators against baselines and agreed triggers
C. Only watch social media
D. Disable alerts after launch
**Answer: B.** Monitoring validates real-world behavior and detects issues not exposed in staging.

### MCQ 79. A production issue is reported after release. What should QA contribute?
A. Blame the tester
B. Help reproduce, assess escaped coverage, identify detection gaps, and add prevention tests
C. Delete the test suite
D. Ignore it as an operations issue
**Answer: B.** QA supports containment and learning, then improves future detection.

### MCQ 80. What is contract testing particularly useful for?
A. Checking UI spacing
B. Verifying API provider/consumer expectations and compatibility
C. Measuring CPU temperature
D. Testing backup restore
**Answer: B.** Contract tests detect interface mismatches without always requiring full end-to-end environments.

### MCQ 81. A browser upgrade is part of the release support matrix. What is needed?
A. Assume compatibility
B. Run targeted compatibility tests on supported browser/version combinations
C. Test only on the developer's machine
D. Skip UI tests
**Answer: B.** Supported platform combinations should be validated according to risk and support commitments.

### MCQ 82. What does a test charter provide for exploratory testing?
A. A fixed script with no learning
B. A mission, scope, and focus for structured exploration
C. A production password
D. A deployment artifact
**Answer: B.** A charter keeps exploration purposeful and helps capture useful findings.

### MCQ 83. Which action is best if release notes omit a shipped breaking API change?
A. Ignore the omission
B. Correct the notes and notify affected stakeholders before release
C. Wait for support tickets
D. Change the API back without review
**Answer: B.** Breaking changes must be communicated accurately so consumers can prepare.

### MCQ 84. What is the best way to validate alerting for a new service?
A. Assume dashboards are enough
B. Verify telemetry, thresholds, routing, and alert response using an approved test
C. Trigger an uncontrolled production outage
D. Disable paging
**Answer: B.** An alert is useful only if it detects the condition and reaches the right responders.

### MCQ 85. What is a useful check for a message consumer after deployment?
A. Only whether the process starts
B. Queue lag, processing success, duplicate handling, retries, and dead-letter behavior
C. Only the page title
D. Only branch protection
**Answer: B.** Asynchronous processing can fail after startup; operational indicators matter.

### MCQ 86. Which is the best way to handle a test that is not applicable?
A. Mark it passed
B. Mark not applicable with rationale and authorized scope decision
C. Delete evidence
D. Mark it failed
**Answer: B.** Not applicable should be transparent and justified, not confused with a pass.

### MCQ 87. A hotfix is proposed during a release freeze. What is required?
A. Merge directly with no tests
B. Assess urgency and impact, approve exception, run focused tests and regression, document it
C. Wait for next year
D. Skip build identification
**Answer: B.** Freeze exceptions need controlled review and evidence.

### MCQ 88. What does MTTD measure?
A. Average time to detect an incident
B. Average time to deploy a feature
C. Number of defects per sprint
D. Time to compile
**Answer: A.** MTTD tracks detection speed and can guide monitoring improvements.

### MCQ 89. What is the best use of defect trend data?
A. Rank individual testers
B. Identify recurring product/process risks and prevention opportunities
C. Hide older defects
D. Replace release criteria
**Answer: B.** Trends are useful for systemic improvement when interpreted in context.

### MCQ 90. A test requires a third-party payment sandbox. The sandbox is down. What should QA report?
A. Payment flow passed
B. Integration test blocked by external dependency; record attempted checks and remaining risk
C. Product defect confirmed
D. No impact because it is staging
**Answer: B.** Be precise about what was and was not validated and escalate dependency risk.

### MCQ 91. Which approach best protects against accidental production deployment from a staging pipeline?
A. Rely on operator memory
B. Use environment-scoped permissions, approvals, artifact promotion controls, and clear pipeline safeguards
C. Share one admin account
D. Disable audit logs
**Answer: B.** Preventive controls reduce human error and provide traceability.

### MCQ 92. What should be verified after a configuration-only release?
A. No tests are needed
B. Effective values, secret references, feature behavior, connectivity, and critical smoke paths
C. Only source formatting
D. Only the commit message
**Answer: B.** Configuration changes can alter behavior even when application code is unchanged.

### MCQ 93. A test passes but its expected result was changed to match the actual result without approval. What is the issue?
A. This is good test maintenance
B. The oracle may have been weakened; confirm requirement and obtain approval before changing expectation
C. The test is now stronger
D. No issue if green
**Answer: B.** Expected results must reflect approved requirements, not be changed simply to turn failures green.

### MCQ 94. What is the main purpose of a release branch?
A. Store production passwords
B. Stabilize a release while controlling which fixes enter it
C. Replace version control
D. Avoid integration testing
**Answer: B.** A release branch isolates stabilization and supports controlled change.

### MCQ 95. A new version changes default permissions. What is the highest-value testing focus?
A. Only page load speed
B. Role/permission matrix, least privilege, existing users, and privilege escalation paths
C. Only spelling
D. Only mobile layout
**Answer: B.** Permission defaults can create serious security and customer-impact risks.

### MCQ 96. What should QA do if the exact artifact deployed to production differs from the tested candidate?
A. Accept if the version string matches
B. Raise an artifact integrity/release-control issue and establish what was deployed
C. Reuse all results
D. Ignore the checksum
**Answer: B.** Release evidence must map to the actual deployed artifact.

### MCQ 97. Which is the best description of a release blocker?
A. Any defect a tester dislikes
B. An issue that violates agreed release criteria or creates unacceptable risk
C. Every cosmetic issue
D. A test that takes over five minutes
**Answer: B.** Blocker status should be based on agreed criteria and risk, with an accountable decision process.

### MCQ 98. What is the purpose of a rollback rehearsal?
A. Practice hiding a failure
B. Prove the recovery steps, ownership, timing, and data implications are understood
C. Replace smoke testing
D. Test marketing copy
**Answer: B.** A rehearsal reveals gaps before a real incident.

### MCQ 99. A key workflow passes in isolation but fails end-to-end. What should QA investigate?
A. Cross-component contracts, identity/context propagation, state, timing, and data consistency
B. Only the isolated component's color
C. Only test naming
D. No investigation because unit test passed
**Answer: A.** End-to-end failures often occur at integration boundaries that isolated tests do not cover.

### MCQ 100. Which is the best principle for release test evidence?
A. Evidence should be reproducible, attributable, and tied to the exact build/environment
B. Evidence can be reconstructed from memory
C. Only pass counts matter
D. Store credentials with screenshots
**Answer: A.** Traceable evidence supports audits, triage, and release decisions.

---

## Part 2 — 100 realistic release scenarios

For each scenario, explain what you would verify, who you would involve, what evidence you would capture, and how it affects the release decision.

### Scenario 1. Smoke test fails on staging

**Situation:** The login endpoint returns 503 immediately after deployment.

**Recommended response:** Pause the broader suite; verify the deployed artifact, service readiness, dependencies, configuration, and logs. Raise a blocker if the critical path remains unavailable. Resume only after the environment/build is stable.

### Scenario 2. Smoke test passes but one key workflow fails

**Situation:** The dashboard loads, but users cannot create a new project.

**Recommended response:** Treat smoke as an initial gate, not proof of release quality. Triage the failed business workflow, determine change impact, and block or document risk according to exit criteria.

### Scenario 3. Late code change after regression

**Situation:** A developer merges a small fix after the full regression run.

**Recommended response:** Identify the new artifact and changed components. Run retest plus targeted regression around dependencies and critical paths; do not reuse results as if the artifact were unchanged.

### Scenario 4. Staging and production configuration differ

**Situation:** A feature works in staging but production uses a different authentication provider.

**Recommended response:** Document the parity gap, validate the production-specific configuration safely, test integration/authentication behavior, and make the residual risk explicit before approval.

### Scenario 5. Database migration partially completes

**Situation:** The migration updates some tables but times out before finishing.

**Recommended response:** Stop further rollout, preserve logs and database state, involve the database owner, assess transaction/partial-write safety, and execute the approved recovery procedure. Reconcile data before retrying.

### Scenario 6. Rollback may be incompatible

**Situation:** The new version writes a field the previous version does not understand.

**Recommended response:** Do not assume application rollback is safe. Assess schema/data compatibility, use backward-compatible migration strategy where possible, and choose a tested forward fix or recovery plan.

### Scenario 7. Critical defect with workaround

**Situation:** A rare admin action fails, but a documented manual workaround exists.

**Recommended response:** Assess severity, exposure, frequency, workaround reliability, and customer impact. Record the issue and obtain explicit acceptance from the authorized owner if release proceeds.

### Scenario 8. Performance regression

**Situation:** p95 latency rises from 300 ms to 1.8 seconds under expected load.

**Recommended response:** Compare with baseline under equivalent conditions; inspect resource use, traces, and changed dependencies. Treat unmet SLOs as release risk and require remediation or formal acceptance.

### Scenario 9. High throughput with many errors

**Situation:** The load test reports higher requests per second but 8% of requests time out.

**Recommended response:** Do not call this a pass. Analyze throughput, latency, and error rate together; identify saturation and confirm agreed performance thresholds.

### Scenario 10. Canary error spike

**Situation:** After 5% traffic is shifted, HTTP 500s exceed the agreed threshold.

**Recommended response:** Pause rollout expansion, notify the release/on-call owner, inspect cohort-specific telemetry, and follow the canary rollback or mitigation criteria.

### Scenario 11. Feature flag accidentally enabled

**Situation:** A feature intended for internal users is visible to all tenants.

**Recommended response:** Disable or correct the flag using the approved control, verify targeting and exposure, assess data/customer impact, and add tests for default and targeting rules.

### Scenario 12. Authorization regression

**Situation:** A user with a read-only role can edit another user's record.

**Recommended response:** Treat as a security blocker. Reproduce safely with test accounts, capture sanitized evidence, verify server-side authorization, retest role/object boundaries, and escalate.

### Scenario 13. Secrets appear in logs

**Situation:** A failed authentication request logs an access token.

**Recommended response:** Restrict access to affected logs, follow security incident procedures, remove or redact secrets through approved processes, assess exposure, and add regression checks for log redaction.

### Scenario 14. Vulnerable dependency found

**Situation:** A scanner flags a critical CVE in a transitive library.

**Recommended response:** Confirm dependency version and reachability, assess exploitability and exposure, consult security owners, upgrade/mitigate, rerun scans and relevant tests, and document any accepted risk.

### Scenario 15. API breaking change

**Situation:** A response field used by older clients is renamed.

**Recommended response:** Identify consumers and supported versions, validate compatibility, coordinate versioning or transition, and ensure release notes and contract tests cover the change.

### Scenario 16. Duplicate transaction after retry

**Situation:** A timeout causes the client to submit the same order twice.

**Recommended response:** Check idempotency keys and server-side deduplication. Verify safe retry semantics and ensure no duplicate business effect occurs.

### Scenario 17. Queue backlog after deployment

**Situation:** The worker starts, but queue depth grows continuously.

**Recommended response:** Check consumer health, throughput, errors, resource limits, poison messages, and downstream dependencies. Confirm alerting and recovery behavior before release approval.

### Scenario 18. Messages processed out of order

**Situation:** A new parallel consumer changes message ordering.

**Recommended response:** Clarify ordering guarantees and business requirements. Test concurrency, partitioning, retries, duplicates, and downstream state consistency.

### Scenario 19. Intermittent test failure

**Situation:** A test fails roughly one run in twenty.

**Recommended response:** Capture failure timing and logs; investigate shared state, test data collisions, race conditions, network dependency, and timeouts. Do not mask it with unlimited retries.

### Scenario 20. Suite-only test failure

**Situation:** A test passes alone but fails after another test runs.

**Recommended response:** Inspect test order, shared fixtures, cleanup, static state, and data reuse. Make tests independent and rerun in parallel and sequential modes.

### Scenario 21. Environment unavailable

**Situation:** Staging becomes unreachable during a planned regression window.

**Recommended response:** Mark affected tests blocked, notify environment ownership, preserve completed evidence, estimate schedule impact, and avoid recording unexecuted tests as passed.

### Scenario 22. Third-party sandbox outage

**Situation:** The payment provider's test sandbox is down.

**Recommended response:** Record the integration as blocked by an external dependency. Validate local error handling and mocks where useful, but clearly state that real integration behavior remains unverified.

### Scenario 23. Test data contains personal information

**Situation:** A tester finds real customer names and emails in staging.

**Recommended response:** Stop unnecessary access and sharing, notify the privacy/data owner, follow approved containment, confirm masking/authorization, and use synthetic or masked data going forward.

### Scenario 24. Release notes omit breaking change

**Situation:** An API behavior change is absent from the release notes.

**Recommended response:** Correct the notes and notify consumers before release. Include migration guidance, affected versions, compatibility impact, and support contact.

### Scenario 25. Build artifact mismatch

**Situation:** The artifact deployed to staging has a different checksum from the pipeline artifact.

**Recommended response:** Stop validation and deployment progression. Verify provenance, storage, pipeline records, and artifact integrity; redeploy the trusted artifact and retest.

### Scenario 26. Wrong build deployed

**Situation:** Staging shows build 2.4.8, while the test plan targets 2.4.9.

**Recommended response:** Do not execute against the wrong candidate. Confirm deployment identity, deploy the intended artifact, and restart or invalidate test evidence as appropriate.

### Scenario 27. Unreviewed emergency change

**Situation:** A hotfix is pushed directly to the release branch.

**Recommended response:** Pause promotion; obtain review and change authorization, assess scope and dependencies, run focused tests and regression, and preserve an audit trail.

### Scenario 28. Code freeze exception

**Situation:** A customer-impacting defect needs a fix during code freeze.

**Recommended response:** Use the exception process: document urgency, scope, risk, approver, targeted test plan, regression impact, and rollback/mitigation.

### Scenario 29. Go/no-go disagreement

**Situation:** Product wants to ship, while QA recommends no-go due to a failed critical test.

**Recommended response:** Present reproducible evidence, user impact, unmet criterion, and options. Escalate to the authorized decision-maker; record the decision and risk acceptance without changing test results.

### Scenario 30. Test coverage gap

**Situation:** A requirement was added late and has no linked test.

**Recommended response:** Clarify acceptance criteria, assess criticality, create focused coverage, and report any remaining untested risk. Update traceability.

### Scenario 31. Requirement ambiguity

**Situation:** The requirement says a session should expire 'soon'.

**Recommended response:** Ask the product/security owner for a measurable timeout and expected behavior. Document examples and avoid inventing an acceptance threshold.

### Scenario 32. Defect cannot be reproduced

**Situation:** Support reports a failure but QA cannot reproduce it.

**Recommended response:** Request sanitized timestamp, timezone, build, tenant/config context, workflow, client details, and correlation ID. Search telemetry and preserve uncertainty rather than closing prematurely.

### Scenario 33. Defect severity dispute

**Situation:** Development calls a data exposure issue medium severity.

**Recommended response:** Use the severity definitions and evidence: data sensitivity, affected users, exploitability, and scope. Bring the issue to triage and escalate unresolved risk.

### Scenario 34. Many low-priority defects

**Situation:** The release has 40 cosmetic defects and no known critical defects.

**Recommended response:** Review clustering, user impact, accessibility, and acceptance thresholds. Summarize trends and obtain the appropriate product decision for accepted items.

### Scenario 35. Production smoke fails

**Situation:** After deployment, the health endpoint passes but login fails.

**Recommended response:** Treat the release as potentially unhealthy; halt further rollout, check real user journey telemetry and dependencies, and execute incident/rollback criteria.

### Scenario 36. Production metric anomaly

**Situation:** Error rate is normal but support tickets double after release.

**Recommended response:** Investigate business-level symptoms, segment by user/workflow, compare before/after behavior, and review whether monitoring lacks a customer-impact signal.

### Scenario 37. Alert not triggered

**Situation:** A known staging fault does not generate the expected alert.

**Recommended response:** Validate metric emission, threshold, evaluation window, routing, and notification integration. Treat alert coverage as an operational readiness gap.

### Scenario 38. Certificate rotation failure

**Situation:** A service cannot connect after a TLS certificate change.

**Recommended response:** Check certificate chain, hostname, expiry, trust store, reload behavior, and dependent clients. Restore via approved process and add rotation validation.

### Scenario 39. Clock/timezone defect

**Situation:** A scheduled release task runs several hours early for one region.

**Recommended response:** Check timezone assumptions, UTC storage, daylight-saving transitions, scheduler configuration, and regional tests. Confirm the expected business time explicitly.

### Scenario 40. Localization overflow

**Situation:** A translated button label is truncated in German.

**Recommended response:** Test supported locales and viewport sizes, fix layout constraints, and include longer-string and date/number formats in localization regression.

### Scenario 41. Accessibility regression

**Situation:** A new modal traps keyboard focus outside the dialog.

**Recommended response:** Treat it as an accessibility defect; validate keyboard order, focus containment/restoration, labels, and screen-reader behavior against requirements.

### Scenario 42. Browser-specific issue

**Situation:** The new UI works in Chrome but fails in Safari.

**Recommended response:** Confirm support matrix and versions, collect console/network evidence, isolate browser-specific APIs/CSS, and run targeted cross-browser regression.

### Scenario 43. Mobile upgrade loses settings

**Situation:** Users upgrading the app lose saved preferences.

**Recommended response:** Reproduce upgrade paths from supported prior versions, inspect migration/storage logic, assess user impact, and verify data-preserving upgrade behavior.

### Scenario 44. Offline sync conflict

**Situation:** A user edits a record offline while another user updates it online.

**Recommended response:** Verify conflict-resolution rules, user feedback, retry behavior, and data integrity. Test reconnect and duplicate synchronization scenarios.

### Scenario 45. Push notification duplicates

**Situation:** Users receive two notifications for one event.

**Recommended response:** Trace event generation, queue retries, provider callbacks, and deduplication keys. Validate exactly-once business effect even if delivery is at-least-once.

### Scenario 46. File upload validation gap

**Situation:** The UI blocks a file type but the API accepts it directly.

**Recommended response:** Treat server-side validation as authoritative. Test direct API requests, size/type limits, storage permissions, and safe error responses.

### Scenario 47. Large file download fails

**Situation:** Downloads over 500 MB terminate midway.

**Recommended response:** Test streaming, timeouts, range requests, proxy limits, and resume behavior under realistic network conditions.

### Scenario 48. Session remains active after logout

**Situation:** A previously issued token still accesses protected APIs.

**Recommended response:** Verify token/session invalidation and revocation semantics; treat unauthorized access as a security issue and test all relevant clients.

### Scenario 49. Password reset token reuse

**Situation:** A reset link can be used more than once.

**Recommended response:** Validate one-time use, expiry, invalidation after success, rate limits, and audit behavior. Escalate if it violates security requirements.

### Scenario 50. Rate limit regression

**Situation:** A credential endpoint no longer throttles repeated attempts.

**Recommended response:** Treat as security-sensitive; validate thresholds, identity/IP strategy, distributed behavior, response headers, and false-positive handling.

### Scenario 51. Database index slows writes

**Situation:** A new index improves reads but increases write latency.

**Recommended response:** Benchmark representative read/write workloads, compare plans and resource use, and assess whether the trade-off meets SLOs.

### Scenario 52. Data migration count mismatch

**Situation:** Source has 1,000,000 rows and target has 998,500.

**Recommended response:** Reconcile by key and category, inspect rejected/duplicate records and filters, define acceptable exceptions, and obtain data-owner sign-off.

### Scenario 53. Backup restore untested

**Situation:** The team says backups run nightly but has never restored one.

**Recommended response:** Request a controlled restore validation and recovery-time evidence. Do not treat backup existence as proven recoverability.

### Scenario 54. Partial outage in one region

**Situation:** Only users in one geography see elevated failures.

**Recommended response:** Segment monitoring by region, inspect regional configuration/dependencies/routing, validate failover, and communicate affected scope.

### Scenario 55. Capacity exhaustion

**Situation:** Memory grows steadily during a 12-hour soak test.

**Recommended response:** Investigate leaks, caches, resource cleanup, and workload patterns. Compare baseline and thresholds; do not approve if capacity risk is unacceptable.

### Scenario 56. Autoscaling does not trigger

**Situation:** CPU rises under load but instance count remains unchanged.

**Recommended response:** Validate metrics, scaling policy, permissions, cooldowns, quotas, and thresholds; repeat controlled load tests and verify scale-in recovery.

### Scenario 57. Circuit breaker stuck open

**Situation:** A dependency recovers but calls remain blocked.

**Recommended response:** Inspect state transitions, half-open probes, reset policy, and dependency health. Test recovery without causing uncontrolled traffic.

### Scenario 58. Retry storm

**Situation:** A downstream outage causes thousands of retries per second.

**Recommended response:** Validate backoff, jitter, retry budgets, circuit breakers, and idempotency. Ensure retries do not amplify outages.

### Scenario 59. API pagination skips records

**Situation:** Records are missing when users move between pages during updates.

**Recommended response:** Check stable sort keys/cursors and concurrent data changes. Define consistency expectations and test insert/delete scenarios between pages.

### Scenario 60. API rate limit blocks valid users

**Situation:** A shared NAT causes unrelated customers to hit one IP-based quota.

**Recommended response:** Assess rate-limit identity dimensions and fairness. Test tenant/user-aware policies, headers, recovery, and abuse protection.

### Scenario 61. Backward compatibility issue

**Situation:** An older mobile app crashes when it receives a new enum value.

**Recommended response:** Test older supported clients against new server responses; use tolerant contract design, versioning, or coordinated minimum-client policy.

### Scenario 62. Feature default changes behavior

**Situation:** A config default turns on a new workflow for existing tenants.

**Recommended response:** Test existing and new tenant defaults, migration behavior, targeting, and opt-out/rollback. Assess customer impact before rollout.

### Scenario 63. Secret rotation breaks service

**Situation:** A service continues using an expired credential after rotation.

**Recommended response:** Validate secret refresh, restart/reload, dual-key overlap, dependent services, and alerting. Ensure the rotation procedure is repeatable.

### Scenario 64. Release approval missing

**Situation:** The deployment ticket has no production approval.

**Recommended response:** Do not infer approval from chat. Follow governance, obtain the authorized approval, and ensure it references the exact artifact and risk.

### Scenario 65. Rollback owner unavailable

**Situation:** The planned deployment has no named person able to execute rollback.

**Recommended response:** Treat operational ownership as a readiness gap. Assign and confirm an available owner and rehearse/verify the procedure before proceeding.

### Scenario 66. Deployment window too short

**Situation:** The migration and validation may exceed the approved window.

**Recommended response:** Estimate duration from evidence, include validation and rollback buffer, and reschedule or split the deployment if safe completion is unlikely.

### Scenario 67. Monitoring dashboard stale

**Situation:** The release dashboard is still showing metrics from the previous cluster.

**Recommended response:** Verify data source, labels, cluster identity, and timestamps. Do not use stale dashboards as release evidence.

### Scenario 68. Log correlation missing

**Situation:** A request spans four services but logs cannot be joined.

**Recommended response:** Check trace/correlation propagation across HTTP and messaging boundaries; improve instrumentation before relying on logs for incident triage.

### Scenario 69. Customer-specific config issue

**Situation:** Only one tenant with a custom domain fails after release.

**Recommended response:** Compare sanitized tenant configuration, certificate/DNS, feature flags, and routing; protect customer data and add a tenant-configuration test.

### Scenario 70. Unexpected dependency upgrade

**Situation:** A transitive package changes during a rebuild without source changes.

**Recommended response:** Compare lockfiles/SBOM and artifact provenance, pin or control dependencies, assess vulnerability/behavior changes, and rerun impacted tests.

### Scenario 71. Security scan false positive

**Situation:** A scanner flags code that is not reachable in the deployed feature.

**Recommended response:** Document evidence, confirm with security owner, record a justified disposition, and retain traceability; do not silently suppress.

### Scenario 72. Test automation credential expired

**Situation:** The pipeline's service account cannot authenticate.

**Recommended response:** Mark affected tests blocked, rotate credentials through the secret manager, verify least privilege, and rerun the impacted pipeline stages.

### Scenario 73. Parallel tests corrupt shared data

**Situation:** Two test workers update the same account.

**Recommended response:** Isolate data per worker or use unique fixtures, transactional cleanup, and concurrency-safe setup. Rerun to verify deterministic behavior.

### Scenario 74. Production data leak in screenshot

**Situation:** A bug report screenshot contains customer email addresses.

**Recommended response:** Restrict sharing, replace/redact the evidence according to policy, notify the privacy owner if exposed, and use sanitized examples in future reports.

### Scenario 75. A/B test contamination

**Situation:** Users in the control group receive the new feature.

**Recommended response:** Check assignment persistence, targeting rules, cache/session behavior, and exposure logging. Validate cohort isolation before interpreting results.

### Scenario 76. Billing calculation regression

**Situation:** A discount is applied twice for some renewal paths.

**Recommended response:** Test decision tables across plan, renewal, coupon, currency, and timing combinations; reconcile calculations and treat financial impact as high risk.

### Scenario 77. Time-sensitive batch missed

**Situation:** A nightly job does not run after deployment.

**Recommended response:** Check scheduler registration, timezone, permissions, worker health, and missed-run recovery. Validate idempotent replay and downstream reconciliation.

### Scenario 78. Data retention job deletes too early

**Situation:** Records are removed before the configured retention period.

**Recommended response:** Stop or disable the affected job through approved controls, preserve evidence, assess recoverability and compliance impact, and test boundary dates.

### Scenario 79. Search index stale

**Situation:** New records save successfully but do not appear in search.

**Recommended response:** Validate event publishing, indexing lag, retries, dead-letter handling, and reindex strategy; define acceptable consistency delay.

### Scenario 80. Cache serves stale permissions

**Situation:** A user's revoked role remains effective for several minutes.

**Recommended response:** Check cache invalidation/TTL and authorization source of truth. Treat excessive privilege persistence as a security risk.

### Scenario 81. Service starts but background jobs fail

**Situation:** Kubernetes readiness passes, but scheduled tasks never execute.

**Recommended response:** Add business-level checks for scheduler/worker operation, inspect queue and permissions, and validate job execution after deployment.

### Scenario 82. Release artifact not reproducible

**Situation:** The same source commit produces different package contents.

**Recommended response:** Inspect build inputs, dependency resolution, timestamps, environment variables, and pipeline provenance. Improve deterministic builds and artifact signing.

### Scenario 83. Customer asks for immediate deployment

**Situation:** A customer requests a release before mandatory tests finish.

**Recommended response:** Explain unmet criteria and risk, offer a scoped alternative or staged rollout, and require authorized risk acceptance for any exception.

### Scenario 84. QA capacity shortage

**Situation:** One tester must validate a large release in one day.

**Recommended response:** Risk-rank changed components and critical journeys, automate/reuse stable checks, seek cross-team support, and clearly report untested areas.

### Scenario 85. Release has no clear owner

**Situation:** Development, QA, and operations each assume another team owns deployment.

**Recommended response:** Clarify a single accountable release coordinator and named owners for build, approval, deployment, validation, communications, and rollback.

### Scenario 86. Defect reopened repeatedly

**Situation:** A fix passes once but the defect returns in later builds.

**Recommended response:** Compare code paths and environment, investigate root cause, add durable regression coverage, and verify the fix on the release candidate.

### Scenario 87. Acceptance criteria changed mid-test

**Situation:** Product updates expected behavior after QA reports a failure.

**Recommended response:** Record the requirement change, obtain approval, assess affected tests and scope, and distinguish product change from defect resolution.

### Scenario 88. Release dashboard reports 98% pass

**Situation:** The remaining 2% includes all security and payment tests.

**Recommended response:** Look beyond aggregate percentage. Report critical-path status and blocked/failed risk; release readiness depends on risk-weighted criteria.

### Scenario 89. Test case marked pass with no evidence

**Situation:** A test execution record says pass but contains no result details.

**Recommended response:** Request or recreate valid evidence on the exact build. Do not rely on unsupported status for critical release gates.

### Scenario 90. Multiple versions coexist

**Situation:** Old and new application instances run during rolling deployment.

**Recommended response:** Test mixed-version compatibility, shared schema, session behavior, message formats, and deployment ordering.

### Scenario 91. Long-running request interrupted

**Situation:** A deployment restarts a service while a long export is running.

**Recommended response:** Validate graceful shutdown, request draining, resumability, job persistence, and user-visible recovery.

### Scenario 92. Regional data residency concern

**Situation:** A new analytics service copies records to another region.

**Recommended response:** Pause approval pending privacy/compliance review; verify data flows, residency requirements, access, retention, and approved architecture.

### Scenario 93. Release causes elevated database connections

**Situation:** Connection pools exhaust after rollout.

**Recommended response:** Compare connection metrics, pool configuration, concurrency, leaks, and query behavior; validate under load and monitor saturation.

### Scenario 94. A critical test is not automatable

**Situation:** A hardware-dependent workflow requires manual validation.

**Recommended response:** Define a repeatable manual procedure, qualified tester, evidence requirements, and schedule; do not omit it solely because automation is unavailable.

### Scenario 95. Release branch diverges from main

**Situation:** A fix is applied only to the release branch.

**Recommended response:** Confirm cherry-pick/back-merge policy and ensure the fix is integrated into the ongoing development line to prevent regression.

### Scenario 96. A customer-facing toggle is exposed

**Situation:** An internal feature flag appears in the public UI.

**Recommended response:** Disable exposure, verify access controls and targeting, assess whether users changed state, and add UI/API authorization checks.

### Scenario 97. A test is flaky due to clock assumptions

**Situation:** A test fails around midnight and daylight-saving changes.

**Recommended response:** Use controlled clocks/time zones where possible, avoid timing assumptions, and cover date boundaries and daylight-saving transitions.

### Scenario 98. The release has a failed accessibility check

**Situation:** Keyboard users cannot reach the save action.

**Recommended response:** Assess against accessibility requirements, fix focus/navigation semantics, retest with keyboard and assistive technology, and document any exception.

### Scenario 99. A deployment changes DNS

**Situation:** Some clients resolve the old endpoint for hours.

**Recommended response:** Validate TTL, propagation, certificate coverage, routing, and backward-compatible overlap. Monitor clients during the transition.

### Scenario 100. Production rollback restores service but loses new records

**Situation:** The old database snapshot predates transactions accepted after deployment.

**Recommended response:** Treat data loss as a critical recovery issue. Reconcile transactions from durable logs/queues, involve data owners, and redesign recovery to preserve post-deploy writes.

---

## Part 3 — Release QA mock interview

Use these as a structured practice interview. Answer each in 1–2 minutes, then compare your answer with the sample.

### Interview question 1. Tell me about your approach to validating a release.

**Sample answer:** I start with scope and risk: identify the exact candidate artifact, changes, dependencies, acceptance criteria, and release risks. I confirm environment and data readiness, run smoke tests, then risk-based functional, integration, regression, non-functional, and security checks. I track defects and blocked tests, report evidence against exit criteria, and provide a go/no-go recommendation with residual risks.

### Interview question 2. A new build is deployed to staging. What do you do first?

**Sample answer:** Verify deployment identity and environment health, then run the agreed smoke suite on critical paths. If smoke fails, pause broader testing and triage. If it passes, continue with change-focused tests and regression based on impact.

### Interview question 3. How do you decide what regression tests to run?

**Sample answer:** Use change impact analysis: changed code and configuration, dependent services, shared components, customer-critical workflows, prior defects, and risk. Run the highest-risk paths first, then expand coverage based on time and release criteria.

### Interview question 4. How do you handle a release with open defects?

**Sample answer:** Classify severity and priority using agreed definitions, assess affected users and workflows, workaround and exposure, and compare with exit criteria. Recommend fix, defer, or no-go based on risk. Any accepted risk must be documented and approved by the accountable owner.

### Interview question 5. What is the difference between smoke, sanity, and regression testing?

**Sample answer:** Smoke is a small critical check of build stability after deployment. Sanity is focused validation of a particular change or fix; terminology varies by organization. Regression checks that existing behavior has not been unintentionally broken.

### Interview question 6. How would you test a database migration?

**Sample answer:** Review migration design and compatibility, take/verify backups, test on representative data, validate schema and constraints, reconcile records and relationships, measure duration and locks, test application compatibility during mixed versions, and verify recovery/forward-fix strategy.

### Interview question 7. How do you manage a late code change?

**Sample answer:** Identify the exact new artifact, require review and authorization, perform impact analysis, run focused retesting and regression, and update evidence. If time does not allow adequate validation, make the residual risk explicit and escalate the decision.

### Interview question 8. What do you include in a release test report?

**Sample answer:** Build and environment, scope, execution totals by pass/fail/blocked/not-run, coverage, critical defects and known issues, performance/security status, dependencies, evidence links, risks, exit-criteria status, and recommendation.

### Interview question 9. What would make you recommend no-go?

**Sample answer:** An unmet mandatory exit criterion, unresolved critical security/data-integrity/customer-impact issue, failed critical workflow, unverified artifact, inadequate recovery readiness, or insufficient evidence for an unacceptable risk. I explain the evidence and actions needed.

### Interview question 10. How do you work with developers who disagree with a defect?

**Sample answer:** Keep the discussion evidence-based. Share exact build, environment, steps, expected and actual results, logs, and impact. Reproduce together, clarify the requirement with product if needed, and use triage or escalation for unresolved risk.

### Interview question 11. How do you test APIs in a release?

**Sample answer:** Validate contract, authentication and authorization, input validation, status codes, schema, error handling, pagination, rate limits, idempotency, retries/timeouts, version compatibility, and integration with consumers. Automate stable contract and critical-path checks.

### Interview question 12. How do you approach performance testing?

**Sample answer:** Agree workload model and SLOs, establish a comparable baseline, run load/stress/spike/soak tests as appropriate, and analyze throughput, p95/p99 latency, errors, and resource headroom together. Report bottlenecks and production capacity risk.

### Interview question 13. How do you validate a rollback plan?

**Sample answer:** Confirm triggers, decision authority, owner, artifact, database/data implications, configuration and traffic reversal, customer communication, and recovery time. Prefer a rehearsal or controlled validation and ensure post-rollback smoke checks are defined.

### Interview question 14. What is your approach to production deployment validation?

**Sample answer:** Use a controlled deployment plan, verify artifact and configuration, monitor health and business indicators, execute targeted smoke checks, observe error/latency/resource trends, and keep rollback or mitigation available during the agreed observation window.

### Interview question 15. How do you deal with flaky automation?

**Sample answer:** Measure and isolate the flake, inspect timing, shared state, data collisions, dependencies, concurrency, and environment. Fix the root cause, improve diagnostics, and keep flaky tests visible rather than silently retrying until green.

### Interview question 16. How do you prioritize when the test window is short?

**Sample answer:** Prioritize by business impact, likelihood, change blast radius, security/data sensitivity, usage frequency, and failure detectability. Run smoke and critical end-to-end paths first, then high-risk changes and integrations. Report what remains untested.

### Interview question 17. What would you do if staging differs from production?

**Sample answer:** Document each difference and decide whether it affects behavior, scale, security, data, or integrations. Validate production-specific configuration safely, improve parity where practical, and state the remaining uncertainty in the release decision.

### Interview question 18. How do you ensure test data is safe?

**Sample answer:** Use synthetic or approved masked data, restrict access, avoid secrets in screenshots/logs, define refresh and cleanup, and confirm that test data does not expose real customer information.

### Interview question 19. Describe a good defect report.

**Sample answer:** A concise title, exact build and environment, preconditions, steps, expected and actual results, frequency, impact, sanitized data, logs/screenshots, timestamp and correlation ID, plus any workaround.

### Interview question 20. What is the role of QA in a Go/No-Go meeting?

**Sample answer:** Present independent, objective evidence against agreed criteria, explain critical defects and untested areas, quantify impact and mitigation, and recommend a path. The authorized business/release owner makes and records the decision.

### Interview question 21. How do you test feature flags?

**Sample answer:** Test default state, enabled/disabled behavior, targeting rules, user/tenant cohorts, transitions, stale cache, rollback/kill switch, and interactions with permissions and data migration.

### Interview question 22. How would you validate a security-sensitive authentication release?

**Sample answer:** Test login, MFA, recovery, token/session expiry, revocation, rate limiting, lockout, authorization, audit logging, secret handling, and backward compatibility for supported clients. Coordinate with security and avoid real customer credentials.

### Interview question 23. What would you do after a production escape?

**Sample answer:** Help contain and reproduce the issue, assess affected scope, preserve evidence, and support incident response. Then analyze why detection failed, add or improve tests/monitoring, and track prevention actions without blame.

### Interview question 24. How do you measure QA effectiveness?

**Sample answer:** Use a balanced set such as escaped defects, critical-path coverage, test cycle time, flaky-test rate, automation reliability, incident trends, and risk closure. Avoid optimizing a single metric or using metrics to blame individuals.

### Interview question 25. Why should we hire you for Release QA?

**Sample answer:** I bring a risk-based mindset, disciplined validation, clear defect evidence, and strong coordination across development, product, and operations. I focus not just on executing tests but on giving decision-makers a reliable view of release readiness and residual risk.

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
