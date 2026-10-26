# Task ID: TASK-2-2

## 1. Task ID
`TASK-2-2`

## 2. Title
Introduce SQLAlchemy and SQLite

## 3. Goal
Replace temporary in-memory persistence with SQLAlchemy models and a local SQLite database.

## 4. Context
Module 2 — Backend development and database integration.

The Interview Canvas application has already been implemented and serves as the reference implementation for this task.

Only the frontend was copied from Alexey Grigorev's interview-canvas-share repository. The cloned repository was subsequently deleted, and the backend and database integration were developed separately in this project's own repository.

The SQLAlchemy and SQLite implementation already exists historically. This task is part of a new PM–Software Engineer–QA workflow intended to inspect and independently verify the existing implementation rather than rebuild functionality simply to replay the development process.

## 5. Dependencies
Complete prerequisite task TASK-2-1, or document why the dependency is not applicable for a verification-only run.

## 6. Status
`In Review`

## 7. Acceptance Criteria
- [ ] SQLAlchemy models represent the persisted entities and relationships required by the application.

- [ ] The application can be configured to use SQLite for local development.

- [ ] Relevant application reads and writes use database persistence rather than relying solely on process memory.

- [ ] Persisted session and canvas data can be retrieved after the application is restarted.

- [ ] Database configuration and known persistence limitations are documented.

- [ ] No unrequested architecture changes are introduced.


## 8. Out of Scope
- Rebuilding already implemented functionality solely to replay history.
- Introducing PostgreSQL-specific deployment configuration, which belongs to the relevant subsequent task.
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
1.Inspect the existing database configuration, SQLAlchemy models, and database session management.

2. Identify the persisted entities and relationships required by the application.

3. Verify that the SQLAlchemy models represent the required application data.

4. Inspect how the SQLite database is created, initialized, and configured for local development.

5. Verify that relevant application operations use database reads and writes rather than only in-memory state.

6. Test persistence by creating or updating data, restarting the application, and checking that the data can still be retrieved.

7. Run the relevant existing tests and validation commands.

8. Document the implementation, validation evidence, and known limitations. Make only changes required to satisfy the approved acceptance criteria.

## 11. Deliverables
- SQLAlchemy models and database configuration
- Validation evidence demonstrating persistence across application restarts.
- Implementation report documenting changes, verification results, and known limitations.

## 12. Validation
Inspect the actual repository structure, dependency configuration, database setup, and test configuration before selecting commands.

Verify the following where applicable:

- SQLAlchemy models and their relationships.

- SQLite database initialization and local configuration.

- Database-backed reads and writes for relevant application flows.

- Persistence of stored data across application restarts.

- Existing automated backend tests and relevant regression checks.

Record the exact commands and checks performed, their results, and supporting evidence. Do not assume that a check passed merely because the relevant code exists.

Any check that cannot be performed must be recorded as `NOT VERIFIED`, with the reason documented. A failed check must include its failure evidence and any required follow-up.

## 13. Implementation Report
Complete this section during execution:
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

The PM may approve the task only after QA reports PASS, the supporting evidence is documented, compliance with the approved scope is confirmed, and known limitations are disclosed. If these conditions are not met, the PM decision must remain `Pending` or be changed to `Changes Required`, as appropriate.
