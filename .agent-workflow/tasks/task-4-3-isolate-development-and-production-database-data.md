# Task ID: TASK-4-3

## 1. Task ID
`TASK-4-3`

## 2. Title
Isolate Development and Production Database Data

## 3. Goal
Keep development and production database data isolated when the environments share a PostgreSQL instance.

## 4. Context
Module 4 — Production workflow, observability, and incident response. This task is derived from the project development specification. The Interview Canvas application has already been implemented and is the reference implementation. The task is part of the new PM–Software Engineer–QA workflow. Inspect and verify the existing implementation first; do not rebuild functionality just to replay the historical development sequence.

## 5. Dependencies
Complete prerequisite task TASK-4-2, or document why the dependency is not applicable for a verification-only run.

## 6. Status
`In Review`

## 7. Acceptance Criteria
- [ ] Development and production use distinct database schemas.
- [ ] Connection settings select the intended schema.
- [ ] Validation demonstrates the environments do not unintentionally share application tables/data.
- [ ] No credentials are committed to the repository.

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
- Do not expose database credentials in source files, logs, or reports.

## 10. Implementation Steps
1. Inspect the deployed database configuration and schema strategy.
2. Configure the production schema/search path.
3. Configure the development schema/search path independently.
4. Verify that each environment reads and writes only to its intended schema.
5. Document the isolation model and its limitations.

## 11. Deliverables
- Database schema isolation configuration
- Isolation verification notes

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
- Defects and required follow-up task IDs, if applicable.

## 15. Approval
PM decision: `Pending`.

The PM may approve only after QA reports `PASS`, the evidence is documented, scope compliance is confirmed, and limitations are disclosed.
