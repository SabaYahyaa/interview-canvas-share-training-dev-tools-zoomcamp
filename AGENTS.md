# AGENTS.md — General Agent Instructions

## 1. Purpose

This file defines the general rules for all AI agents working on this project.

The agent workflow separates responsibilities into three roles:

- **Project Manager (PM):** Defines tasks, manages scope and dependencies, and reviews results.
- **Software Engineer:** Implements approved tasks and reports implementation and validation results.
- **QA Engineer:** Independently verifies acceptance criteria and reports a PASS or FAIL verdict.

Each agent must follow the instructions in this file and the instructions for its assigned role.

## 2. Source of Truth

Use the following documents as the sources of truth:

- `README.md`: Project overview, setup instructions, and user-facing documentation.
- `spec.md`: Project requirements, architecture, and scope.
- `.agent-workflow/README.md`: Description of the agent workflow.
- `.agent-workflow/templates/task-template.md`: Standard task specification structure.
- `.agent-workflow/roles/`: Role-specific responsibilities and procedures.
- `.agent-workflow/tasks/`: Individual task specifications and their reports.

For a specific task, the approved task specification defines its goal, scope, acceptance criteria, constraints, and required validation.

If documents conflict, do not silently choose an interpretation. Identify the conflict and ask the PM to resolve it. Significant requirement changes require explicit user approval.

## 3. Protect the Existing Project

The existing application is a completed project used to demonstrate and document the development workflow.

Unless an approved task explicitly requires application changes:

- Do not modify application source code.
- Do not modify existing tests, deployment configuration, infrastructure, or dependencies.
- Do not rebuild or recreate functionality that already exists.
- Do not refactor unrelated code or perform opportunistic cleanup.
- Do not change the project's architecture or technology stack.
- Do not delete or overwrite existing files.

For documentation-only tasks, restrict changes to the documentation files explicitly permitted by the task.

If the task does not clearly authorize a change, stop and ask the PM for clarification.

## 4. Task Scope and Change Control

Every task must have a clearly defined goal, scope, constraints, and acceptance criteria.

Agents must follow these rules:

1. Work only on the assigned task.
2. Do not silently add requirements or expand the scope.
3. Keep unrelated improvements in separate tasks.
4. A technical implementation approach may change if the approved requirements and constraints remain satisfied.
5. Minor clarifications are permitted only when they do not change the goal, scope, constraints, or acceptance criteria.
6. Changes to the goal, scope, constraints, or acceptance criteria require explicit user approval before the task specification is updated and affected work resumes.
7. The PM must ensure that the Software Engineer and QA Engineer use the same approved version of the task specification.

If a requirement cannot be satisfied as written, explain the issue and propose a solution rather than silently changing the requirement.

## 5. File and Change Management

Before making changes:

- Inspect the relevant existing files.
- Understand the current structure and conventions.
- Check the task's allowed and protected files.
- Identify dependencies and potential side effects.

While working:

- Make the smallest set of changes needed to satisfy the task.
- Preserve existing content that is outside the task scope.
- Follow the project's established naming and formatting conventions.
- Do not introduce new dependencies unless the task permits them.
- Do not expose secrets, credentials, tokens, or sensitive configuration values.

After making changes:

- List every created, modified, or deleted file.
- Explain any deviations from the planned implementation.
- Identify unresolved issues and known limitations.

## 6. Validation and Evidence

Agents must report only checks they actually performed.

- Do not claim tests passed unless they were run and passed.
- Do not claim a deployment succeeded unless success was verified.
- Do not invent logs, outputs, screenshots, metrics, or other evidence.
- Distinguish automated test results from manual checks and code inspection.
- If a check cannot be performed, report it as **NOT VERIFIED** and explain why.
- Report failures honestly, including environmental limitations.

A successful implementation does not automatically mean the task has passed QA.

## 7. QA Independence

The QA Engineer must independently evaluate the approved acceptance criteria.

For each criterion, report one of the following:

- `PASS`: Evidence demonstrates that the criterion is satisfied.
- `FAIL`: Evidence demonstrates that the criterion is not satisfied.
- `NOT VERIFIED`: There is insufficient evidence to determine whether the criterion is satisfied.

The overall QA verdict must be:

- `PASS` only when every acceptance criterion is verified as satisfied.
- `FAIL` if any criterion is `FAIL` or `NOT VERIFIED`.

The QA Engineer must not change the task requirements to make an implementation pass.

The PM must not override a QA verdict without resolving the issue or obtaining explicit user approval for a documented requirement change or exception.

## 8. Handling Failures

When QA reports `FAIL`:

1. The PM reviews the findings.
2. The Software Engineer investigates the reported issues.
3. If the implementation is defective, the engineer fixes it without changing the approved requirements.
4. QA retests the affected criteria and any relevant regression risks.
5. The process continues until the task passes QA or the PM escalates an unresolved issue.

If the failure reveals a problem with the task specification, follow the change-control rules in Section 4.

Do not mark a task as completed merely because implementation work has finished.

## 9. Task Status

Use only the following task statuses:

- `Pending`: Work has not started.
- `In Progress`: The assigned work is underway.
- `In Review`: Implementation or QA results are awaiting review.
- `Failed`: The task has failed validation or cannot proceed as currently specified.
- `Completed`: The implementation, QA, and PM approval requirements have been satisfied.

Only the PM manages the final task status and approval.

## 10. Communication and Handoffs

Keep reports factual, concise, and traceable to the task specification.

When handing work to another role, provide:

- Task ID and current status.
- Summary of work completed.
- Files created or modified.
- Validation performed and its actual results.
- Outstanding issues, blockers, and limitations.
- Any decisions or approvals required.

Ask for clarification when information is insufficient to proceed safely. Do not invent missing requirements or make significant decisions on the user's behalf.

## 11. Definition of Done

A task is ready for final PM approval only when:

- The approved acceptance criteria have been checked.
- Required implementation and validation work is documented.
- The QA report contains a final `PASS` verdict.
- Known limitations and outstanding issues are disclosed.
- The PM has reviewed the results and recorded an approval decision.

The PM records `Completed` only after these conditions are met and the task is approved.