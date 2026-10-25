# AI-Assisted Development Workflow

## 1. Purpose

This directory contains the reusable workflow for coordinating AI-assisted software development through three specialized roles:

- **Project Manager (PM):** Plans tasks, defines requirements, and reviews results.
- **Software Engineer:** Implements approved tasks and corrects implementation defects.
- **QA Engineer:** Independently verifies the implementation against the approved acceptance criteria.

The workflow aims to make development more structured, traceable, testable, and reusable across projects.

## 2. Directory Structure

```text
.agent-workflow/
├── README.md
├── templates/
│   └── task-template.md
├── roles/
│   ├── pm.md
│   ├── software-engineer.md
│   └── qa-engineer.md
└── tasks/
    ├── task-001-frontend-mock-backend.md
    └── ...
```

- `templates/`: Reusable templates for defining tasks.
- `roles/`: Responsibilities, workflows, constraints, and outputs for each agent role.
- `tasks/`: Individual task specifications, implementation reports, and QA results.

The root `AGENTS.md` contains general instructions that apply to agents working in the repository. Project-specific requirements are documented in `spec.md` and the relevant task specifications.

## 3. Roles and Responsibilities

### Project Manager

The PM translates project goals into clear tasks with explicit goals, scope, out-of-scope items, constraints, dependencies, acceptance criteria, and validation requirements.

The PM coordinates implementation and QA, reviews the evidence, and makes the final task acceptance decision.

### Software Engineer

The Software Engineer implements the approved task within its defined scope and constraints.

The engineer runs relevant checks, documents changes and limitations, and corrects implementation defects reported by QA.

### QA Engineer

The QA Engineer independently verifies the implementation against the approved task specification.

The QA Engineer records evidence for each acceptance criterion and issues an overall `PASS` or `FAIL` verdict.

The QA Engineer does not implement fixes or change approved requirements.

## 4. Standard Workflow

### Step 1: Define the task

The PM reviews the project context and creates a task using `templates/task-template.md`.

The task must specify the goal, dependencies, scope, out-of-scope items, constraints, acceptance criteria, deliverables, and validation requirements.

Important ambiguities must be resolved before the affected work begins.

### Step 2: Implement the task

The Software Engineer receives the approved task specification and inspects the relevant project files.

The engineer implements the task within the approved scope and prepares an implementation report.

### Step 3: Validate the implementation

The QA Engineer reviews the approved requirements and the implementation evidence.

The QA Engineer evaluates each acceptance criterion and reports `PASS` or `FAIL`, documenting test results and any unverified conditions.

### Step 4: Correct failures

If QA reports `FAIL` because of an implementation defect, the Software Engineer corrects the defect without changing the approved requirements.

The corrected implementation is submitted for QA retesting.

This feedback loop continues until the required criteria pass or further clarification or authorization is needed.

### Step 5: Review and accept

When QA reports `PASS`, the PM reviews the evidence and determines whether the task satisfies all required acceptance and approval conditions.

The PM records the decision and marks the task `Completed` only after the required validation and approval are complete.

## 5. Requirement and Scope Changes

Agents must not silently change approved requirements.

- **Minor clarification:** The PM may clarify existing requirements when the clarification does not change the goal, scope, constraints, or acceptance criteria.
- **Implementation approach:** The Software Engineer may use a different technical approach if it satisfies all approved requirements and constraints.
- **Requirement change:** Changes to the approved goal, scope, constraints, or acceptance criteria require explicit user approval before the revised requirements are used.
- **Unrelated work:** Create a separate task and reference its task ID.
- **Specification problems:** Report ambiguous, contradictory, or incomplete requirements to the PM for investigation.

After an approved requirement change, the PM updates the task specification and ensures that the Software Engineer and QA Engineer use the same approved version.

## 6. Task Status

Use the following status values in task specifications:

| Status | Meaning |
|---|---|
| `Pending` | The task has been defined but implementation has not started. |
| `In Progress` | The task is actively being implemented. |
| `In Review` | The implementation is awaiting QA, PM review, or a required approval. |
| `Failed` | The task has failed validation or cannot proceed under its current requirements. |
| `Completed` | Required validation and PM approval are complete. |

Update the status to reflect the actual task state. A Software Engineer's report that implementation is finished does not, by itself, mean the task is `Completed`.

## 7. QA and Acceptance Rules

- Every acceptance criterion must be verifiable.
- QA must record evidence rather than rely solely on the implementation report.
- A criterion that fails or cannot be verified prevents an overall `PASS`.
- The QA Engineer owns the QA verdict; the PM owns the final acceptance decision.
- A `FAIL` verdict triggers correction or investigation, not an automatic change to the task requirements.
- The task specification must remain consistent with the requirements approved by the user.

## 8. Task Records and Traceability

Each task specification should provide a record of:

- The approved requirements and constraints.
- The implementation summary and changed files.
- Validation commands and actual results.
- QA findings, evidence, and verdict.
- Corrections and retest results.
- PM approval or outstanding issues.

Record material changes to approved requirements so that the team can determine which specification version was used for implementation and testing.

## 9. Using the Workflow for Another Project

To reuse this workflow in another repository:

1. Copy the `.agent-workflow/` directory and adapt the project-specific paths as necessary.
2. Review and update the root `AGENTS.md` to establish the general agent instructions.
3. Create or adapt `spec.md` to describe the new project's goals, architecture, constraints, and relevant decisions.
4. Use `templates/task-template.md` to define the first task.
5. Adapt the role instructions to the project's tools, testing methods, and approval requirements.
6. Begin implementation only after the task has been clearly defined and approved.

Keep the workflow conventions reusable while ensuring that each task reflects the actual project rather than assumptions carried over from another repository.

## 10. Related Documentation

- [Project specification](../spec.md)
- [General agent instructions](../AGENTS.md)
- [Task template](templates/task