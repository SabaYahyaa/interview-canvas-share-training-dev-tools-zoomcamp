# Task ID: TASK-4-4

## 1. Task ID
`TASK-4-4`

## 2. Title
Instrument FastAPI with OpenTelemetry

## 3. Goal
Instrument the FastAPI service to export traces, metrics, and logs to the configured Grafana Cloud OTLP endpoints.

## 4. Context
Module 4 —  Production workflow, observability, and incident response. This task is derived from the project development specification. The Interview Canvas application has already been implemented and is the reference implementation. The task is part of the new PM–Software Engineer–QA workflow. Inspect and verify the existing implementation first; do not rebuild functionality just to replay the historical development sequence.

## 5. Dependencies
Complete prerequisite task TASK-4-3, or document why the dependency is not applicable for a verification-only run.

## 6. Status
`In Review`

## 7. Acceptance Criteria
- [ ] The application emits the configured telemetry signals.
- [ ] OTLP endpoints and authentication headers are configured through environment variables.
- [ ] Service names distinguish environments.
- [ ] Telemetry behavior and any unavailable checks are documented.

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
- Do not expose telemetry credentials in source files, logs, or reports.

## 10. Implementation Steps
1. Inspect existing telemetry code and environment variable configuration.
2. Instrument relevant FastAPI requests and logging.
3. Configure OTLP exporters for traces, metrics, and logs.
4. Ensure service identity distinguishes the relevant environment.
5. Verify telemetry ingestion and trace/log correlation where supported.

## 11. Deliverables
- OpenTelemetry instrumentation/configuration
- Telemetry validation evidence

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
