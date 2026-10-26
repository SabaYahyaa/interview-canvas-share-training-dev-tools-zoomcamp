# Task ID: TASK-4-7

## 1. Task ID
`TASK-4-7`

## 2. Title
Implement the Incident Responder Service

## 3. Goal
Provide a separate FastAPI webhook service that receives Grafana alert payloads and stores JSON evidence for investigation.

## 4. Context
Module 4 — Production workflow, observability, and incident response. This task is derived from the project development specification. The Interview Canvas application has already been implemented and is the reference implementation. The task is to verify the existing implementation through the new PM–Software Engineer–QA workflow. Inspect and verify the existing implementation first; do not rebuild functionality just to replay the historical development sequence.

## 5. Dependencies
Complete prerequisite task TASK-4-6, or document why the dependency is not applicable for a verification-only run.

## 6. Status
`In Review`

## 7. Acceptance Criteria
- [ ] The responder starts as a separate FastAPI service.
- [ ] The health endpoint responds successfully.
- [ ] The /alerts endpoint accepts expected webhook requests.
- [ ] Alert payloads are processed and saved as JSON evidence.
- [ ] The Grafana webhook integration is validated or marked NOT VERIFIED.
- [ ] Documentation does not claim autonomous AI remediation.

## 8. Out of Scope
- Rebuilding already implemented functionality solely to replay history.
- Changes outside this task's scope.
- Unrelated refactoring or architecture changes.
- Claiming QA or PM approval without evidence.
- Implementing autonomous AI-driven remediation.

## 9. Constraints
- Follow `AGENTS.md`, `.agent-workflow/README.md`, and `.agent-workflow/execution-workflow.md`.
- Inspect the existing implementation before making changes.
- Treat the existing application as a reference implementation.
- If the task is intended for a future project, adapt project-specific paths and commands only after user approval.
- Mark unavailable checks `NOT VERIFIED`; do not invent results.
- Ask for explicit user approval before changing scope or acceptance criteria.
- Do not expose secrets or sensitive webhook payload data in documentation, logs, or reports.
- Document whether JSON evidence is stored on persistent storage or whether it may be lost when the service restarts or redeploys.

## 10. Implementation Steps
1. Inspect the existing incident responder and its health endpoint.
2. Verify the /alerts webhook contract and expected Grafana payload shape.
3. Verify background processing and JSON evidence creation.
4. Inspect the Render deployment and Grafana webhook configuration.
5. Document storage persistence limitations and the fact that AI-agent execution/remediation is not implemented.
6. Record the commands, results, and evidence for each check. Identify any defects or checks that could not be performed.

## 11. Deliverables
- Incident responder service
- Webhook/evidence validation notes
- Explicit limitation statement
- Validation evidence and any outstanding blockers.

## 12. Validation
Use commands and checks appropriate to the current repository state. First inspect its scripts, test configuration, and deployment files; do not assume that example commands are valid. Record the exact checks performed, their results, and supporting evidence.

Verify the service startup, health endpoint, /alerts behavior, JSON evidence creation, and Grafana webhook delivery where possible. A successful response from /alerts alone does not prove that the payload was stored successfully or that Grafana delivery works end to end.

Any check not actually performed must be marked NOT VERIFIED. Do not claim persistent storage unless it has been verified.

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
