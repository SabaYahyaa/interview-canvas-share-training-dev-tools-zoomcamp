# Task Specification Template

## 1. Task ID
Unique identifier, such as `TASK-001`.

## 2. Title
Short, action-oriented task title.

## 3. Goal
Describe the result this task should achieve.


## 4. Context
Explain the relevant project/module context and distinguish existing implementation from any new work. The completed Interview Canvas application is a reference implementation; do not rebuild it merely to make this task appear executed.

## 5. Dependencies
List prerequisite tasks or write `None`.

## 6. Status
`Pending`, `In Progress`, `In Review`, `Failed`, `Completed`. A task is not `Completed` until QA passes and the PM approves it.


## 7. Acceptance Criteria
List measurable conditions that must be satisfied.

- [ ] Each criterion is specific and verifiable.
- [ ] Do not mark a criterion passed without evidence.

## 8. Out of Scope
- [ ] Rebuilding the completed application solely to replay historical development.
- [ ] Unrelated refactors or changes to architecture, dependencies, or scope.
- [ ] Claiming unverified work is complete.


## 9. Constraints
- [ ] Follow `AGENTS.md` and `.agent-workflow/README.md`.
- [ ] Inspect the current repository before changes.
- [ ] Preserve existing behavior outside the approved task scope.
- [ ] Request user approval before changing the goal, scope, constraints, or acceptance criteria.
- [ ] Report unavailable checks as `NOT VERIFIED`.

## 10. Implementation Steps
- [ ] Inspect the relevant implementation, configuration, tests, and documentation.
- [ ] Confirm the task scope and dependencies.
- [ ] Implement only the approved changes, if implementation is actually required.
- [ ] Run relevant validation.
- [ ] Report files changed, evidence, and limitations.


## 11. Deliverables
List expected code, configuration, tests, or documentation.

## 12. Validation
Record exact commands/checks and their outcomes. Do not infer success from a feature's existence or a prior report.

## 13. Implementation Report
Completed by the Software Engineer.

- [ ] Summary of changes.
- [ ] Files created, modified, or deleted.
- [ ] Decisions and deviations from the plan.
- [ ] Validation performed and results.
- [ ] Known limitations or unresolved issues.


## 14. QA Report
Completed by the QA Engineer.

- [ ] Acceptance criteria checked, with a result for each criterion.
- [ ] Tests and checks performed, with results and supporting evidence.
- [ ] Defects or unmet criteria.
- [ ] Final verdict: PASS, FAIL, or NOT VERIFIED.
- [ ] Required follow-up task IDs, if applicable.

Overall QA verdict must be PASS only when every acceptance criterion has been verified successfully.

## 15. Approval
Completed by the PM after reviewing the implementation and QA report.

- [ ] Decision: `Approved` or `Changes Required`.
- [ ] Outstanding issues.
- [ ] Follow-up task IDs, if applicable.
The PM may approve the task only when the QA verdict is PASS, the validation evidence is documented, and the work complies with the approved scope. Otherwise, the decision must be Changes Required.