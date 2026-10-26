# Task ID: TASK-4-2

## 1. Task ID
`TASK-4-2`

## 2. Title
Automate Image Publishing and Deployment

## 3. Goal
Use GitHub Actions and GitHub Container Registry to build, tag, publish, and deploy application images.

## 4. Context
Module 4 — Production workflow, observability, and incident response. This task is derived from the project development specification. The Interview Canvas application has already been implemented and is the reference implementation. The task is part of the new PM–Software Engineer–QA workflow. Inspect and verify the existing implementation first; do not rebuild functionality just to replay the historical development sequence.

## 5. Dependencies
Complete prerequisite task TASK-4-1, or document why the dependency is not applicable for a verification-only run.

## 6. Status
`In Review`

## 7. Acceptance Criteria
- [ ] The workflow builds and publishes the intended image.
- [ ] Image tags support identifying a specific build.
- [ ] Development deployment follows the documented trigger.
- [ ] Production promotion follows the documented manual process.
- [ ] Secrets are referenced securely rather than committed.

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
- Do not commit or expose secrets in source files, logs, or reports.

## 10. Implementation Steps
1. Inspect the current CI workflow, registry permissions, and deployment hooks.
2. Build and publish images using the project's documented tag convention.
3. Configure development deployment on the intended trigger.
4. Keep production promotion explicit/manual if that is the approved release strategy.
5. Verify workflow conditions and record deployment evidence.

## 11. Deliverables
- Image build/publish workflow
- Development deployment and production-promotion instructions

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
