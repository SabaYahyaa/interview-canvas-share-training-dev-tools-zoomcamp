# Task ID: TASK-3-4

## 1. Task ID
`TASK-3-4`

## 2. Title
Integrate Automated Checks into CI/CD

## 3. Goal
Integrate code-quality checks and automated tests into the repository's CI pipeline.

## 4. Context
Module 3 — Containerization and automated testing. This task is derived from the project development specification. The Interview Canvas application has already been implemented and is the reference implementation. The task is part of the new PM–Software Engineer–QA workflow. Inspect and verify the existing implementation first; do not rebuild functionality just to replay the historical development sequence.

## 5. Dependencies
Complete prerequisite task TASK-3-3, or document why the dependency is not applicable for a verification-only run.

## 6. Status
`In Review`

## 7. Acceptance Criteria
- [ ] The workflow runs the intended quality checks and tests.
- [ ] Failures prevent later pipeline stages where configured.
- [ ] Workflow steps use real project commands and paths.
- [ ] Validation evidence and any GitHub-only checks not executed locally are recorded.

## 8. Out of Scope
- Rebuilding already implemented functionality solely to replay history.
- Changes outside this task's scope.
- Unrelated refactoring or architecture changes.
- Claiming QA or PM approval without evidence.

## 9. Constraints
- Follow `AGENTS.md`, `.agent-workflow/README.md`, and `.agent-workflow/execution-workflow.md`.
- Inspect the existing implementation before making changes.
- Treat the existing application as a reference implementation.
- If the task is intended for a future project, adapt project-specific paths and commands only after user approval.
- Mark unavailable checks `NOT VERIFIED`; do not invent results.
- Ask for explicit user approval before changing scope or acceptance criteria.

## 10. Implementation Steps
1. Inspect existing GitHub Actions workflows and project commands.
2. Configure lint/format checks and backend tests.
3. Integrate E2E tests if the existing CI architecture supports them.
4. Ensure image publishing/deployment steps depend on the required checks.
5. Validate workflow syntax and record what can be tested locally or in CI.

## 11. Deliverables
- GitHub Actions workflow files
- CI validation evidence

## 12. Validation
Use the commands and checks appropriate to the current repository state. First inspect its scripts, test configuration, and deployment files; do not assume that example commands are valid. Record exact checks, results, and evidence. Any check not actually performed must be marked `NOT VERIFIED`.

## 13. Implementation Report
Complete this section during execution:
- Files changed:
- Changes made or existing implementation verified:
- Validation performed and results:
- Limitations/blockers:

## 14. QA Report
QA must independently verify every acceptance criterion and cite concrete evidence.
- Criterion-by-criterion result: `PASS`, `FAIL`, or `NOT VERIFIED`.
- Overall result: `PASS` only if every criterion is verified; otherwise `FAIL`.
- Defects and required follow-up:

## 15. Approval
PM decision: `Pending`.

The PM may approve only after QA reports `PASS`, the evidence is documented, scope compliance is confirmed, and limitations are disclosed.
