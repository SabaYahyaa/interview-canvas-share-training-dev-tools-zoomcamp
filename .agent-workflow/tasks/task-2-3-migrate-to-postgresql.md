# Task ID: TASK-2-3

## 1. Task ID
`TASK-2-3`

## 2. Title
Migrate to PostgreSQL

## 3. Goal
Move the application from SQLite to PostgreSQL for deployment and multi-user persistence.

## 4. Context
Module 2 — Backend development and database integration. This task is derived from the project development specification. The Interview Canvas application has already been implemented and serves as the reference implementation for this task.

Only the frontend was copied from Alexey Grigorev's interview-canvas-share repository. The cloned repository was subsequently deleted, and the backend and database integration were developed separately in this project's own repository.

The application already has a database integration workflow. This task is part of a new PM–Software Engineer–QA workflow intended to inspect and independently verify the existing PostgreSQL implementation rather than rebuild functionality simply to replay the historical development process.

## 5. Dependencies
Complete prerequisite task TASK-2-2, or document why the dependency is not applicable for a verification-only run.

## 6. Status
`In Review`

## 7. Acceptance Criteria
- [ ] PostgreSQL connection settings are configurable through environment variables without hard-coded credentials or secrets.
- [ ] The application connects to PostgreSQL successfully in the intended deployment configuration.
- [ ] Core persistence flows create, retrieve, and update the required application data using PostgreSQL.
- [ ] Persisted data remains available after an application restart.
- [ ] SQLite support and local-development database instructions are documented if SQLite is retained.
- [ ] Database initialization, schema configuration, and validation results are documented.
- [ ] No unrequested architecture changes are introduced.

## 8. Out of Scope
- Rebuilding already implemented functionality solely to replay history.
- Reimplementing SQLAlchemy models already covered by TASK-2-2, unless a correction is required for PostgreSQL compatibility.
- Changes outside the approved scope of this task.
- Unrelated refactoring or architecture changes.
- Claiming QA or PM approval without supporting evidence.

## 9. Constraints
- Follow `AGENTS.md`, `.agent-workflow/README.md`, and `.agent-workflow/execution-workflow.md`.
- Inspect the existing implementation before making changes.
- Treat the existing application as a reference implementation.
- If the task is intended for a future project, adapt project-specific paths and commands only after user approval.
- Mark unavailable checks `NOT VERIFIED`; do not invent results.
- Ask for explicit user approval before changing scope or acceptance criteria.

## 10. Implementation Steps
1. Inspect the existing database URL, SQLAlchemy engine configuration, environment variables, and deployment settings.
2. Verify how PostgreSQL connection settings are supplied without embedding credentials in application code.
3. Inspect database initialization and schema configuration, including any development and production schema separation.
4. Verify that the application connects to PostgreSQL in the intended deployment environment.
5. Verify core persistence flows against PostgreSQL, including creating and retrieving application data.
6. Verify that persisted data remains available after an application restart.
7. Inspect the local-development database configuration and document SQLite usage if it is retained.
8. Run relevant existing database tests and validation commands.
9. Document the connection requirements, schema setup, validation evidence, and known limitations. Make only changes required to satisfy the approved acceptance criteria.

## 11. Deliverables
- PostgreSQL connection and configuration implementation, verified or corrected as necessary.
- Database setup and local-development instructions.
- Documentation of schema configuration and deployment assumptions.
- Validation evidence for PostgreSQL connectivity and core persistence flows.

## 12. Validation
Inspect the repository's database configuration, dependency management, deployment files, test configuration, and available database environment before selecting commands.

Verify the following where applicable:

- PostgreSQL connection configuration and environment-variable handling.
- Successful database connection in the intended environment.
- Database schema initialization and configuration.
- Core database-backed application operations.
- Persistence across application restarts.
- SQLite/local-development behavior, if retained.
- Relevant automated tests and regression checks.

Record the exact commands and checks performed, their results, and supporting evidence. Do not claim that PostgreSQL functionality passed based solely on code inspection when execution against PostgreSQL is required to verify the criterion.

Any check that cannot be performed must be recorded as `NOT VERIFIED`, with the reason documented. A failed check must include its failure evidence and any required follow-up.

## 13. Implementation Report
Complete this section during execution.

- **Summary:** Changes made or existing implementation verified.
- **Files changed:** Files created, modified, or deleted.
- **Implementation decisions:** Decisions made and deviations from the task specification.
- **Validation performed:** Commands, checks, results, and supporting evidence.
- **Limitations/blockers:** Known limitations, unresolved issues, and checks that could not be completed.

## 14. QA Report
Completed independently by the QA Engineer.

- **Acceptance criteria:** Record PASS, FAIL, or NOT VERIFIED for each criterion, with supporting evidence.
- **Tests and checks:** List the tests and checks performed and their results.
- **Defects or unmet criteria:** Document failures and any required corrections.
- **Overall verdict:** PASS only if every required acceptance criterion has been verified successfully; otherwise FAIL.
- **Follow-up tasks:** Record required follow-up task IDs, if applicable.

The QA Engineer must not treat an unverified criterion as passed.


## 15. Approval
PM decision: `Pending`.

The PM may approve only after QA reports `PASS`,  the supporting evidence is documented, compliance with the approved scope is confirmed, and known limitations are disclosed. If these conditions are not met, the PM decision must remain `Pending` or be changed to `Changes Required`, as appropriate.
