# Task ID: TASK-4-5

## 1. Task ID
`TASK-4-5`

## 2. Title
Build Grafana Dashboards

## 3. Goal
Create Grafana Cloud dashboards for application metrics, logs, and traces.

## 4. Context
Module 4 — Production workflow, observability, and incident response. This task is derived from the project development specification. The Interview Canvas application has already been implemented and is the reference implementation. The task is part of the new PM–Software Engineer–QA workflow. Inspect and verify the existing implementation first; do not rebuild functionality just to replay the historical development sequence.

## 5. Dependencies
Complete prerequisite task TASK-4-4, or document why the dependency is not applicable for a verification-only run.

## 6. Status
`In Review`

## 7. Acceptance Criteria
- [ ] Dashboard panels query the intended data sources.
- [ ] Metrics, logs, and traces are represented where data is available.
- [ ] Queries use the correct environment/service labels.
- [ ] The dashboard is checked against live or test telemetry.

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
1. Inspect configured Prometheus, Loki, and Tempo data sources.
2. Create panels for request rate, HTTP status distribution, and latency percentiles where data is available.
3. Add log panels using the correct service labels.
4. Add trace panels and log-to-trace navigation where configured.
5. Verify panels against actual telemetry and document data limitations.

## 11. Deliverables
- Grafana dashboard
- Panel/query validation notes

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
