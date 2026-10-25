# Task Specification Template

## 1. Task ID

Unique identifier, such as `TASK-001`.

## 2. Title

Short, descriptive task name.

## 3. Goal

One or two sentences describing the expected outcome.

## 4. Context

Relevant project information, existing behavior, and decisions needed to understand the task.

## 5. Dependencies

Tasks or decisions that must be completed first. Use task IDs where applicable.

## 6. Status

`Pending`, `In Progress`, `In Review`, `Failed`, or `Completed`.

## 7. Acceptance Criteria

List measurable conditions that must be satisfied.

- [ ] Each criterion must be independently verifiable.
- [ ] Include normal cases, edge cases, and failure cases where relevant.
- [ ] Define what constitutes a pass.

## 8. Out of Scope

Explicitly list what this task must not do.

If an excluded item belongs to another task, reference its task ID, such as `TASK-002`. Do not automatically expand the current task to include it.

## 9. Constraints

- **Allowed files and directories:** Where changes may be made.
- **Protected files and directories:** What must not be modified.
- **Libraries and tools:** Required, permitted, or prohibited technologies.
- **Project guidelines:** Coding standards, architecture, security, and other relevant rules.
- **Other restrictions:** Any additional limitations.

## 10. Implementation Steps

Ordered steps describing the intended approach. The engineer may propose a different approach when justified, provided it respects the constraints and acceptance criteria.

## 11. Deliverables

Expected outputs, such as code changes, tests, configuration, or documentation.

## 12. Validation

Commands, automated tests, manual checks, and other evidence required to verify the acceptance criteria. Do not claim a check passed unless it was actually performed.

## 13. Implementation Report

Completed by the Software Engineer.

- Summary of changes.
- Files created, modified, or deleted.
- Decisions and deviations from the plan.
- Validation performed and results.
- Known limitations or unresolved issues.

## 14. QA Report

Completed by the QA Engineer.

- Acceptance criteria checked.
- Tests and checks performed, with results.
- Defects or unmet criteria.
- Final verdict: `PASS` or `FAIL`.
- Evidence and any required follow-up task IDs.

## 15. Approval

Completed by the PM after reviewing the implementation and QA report.

- Decision: `Approved` or `Changes Required`.
- Outstanding issues.
- Follow-up task IDs, if applicable.
