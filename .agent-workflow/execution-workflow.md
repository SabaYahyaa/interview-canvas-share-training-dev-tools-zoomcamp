# Task Execution Workflow

## Purpose

Define the standard process for executing project tasks using the Project Manager, Software Engineer, and QA Engineer roles.

## Execution Rules

Follow this workflow whenever the user asks to execute a task.

1. Read the task file and relevant project instructions.
2. Have the Project Manager check that the task is sufficiently defined and within scope.
3. Have the Software Engineer implement the approved task.
4. Have the QA Engineer independently verify every acceptance criterion.
5. If QA finds failures, report them and have the Software Engineer fix issues within the approved scope. Rerun QA afterward.
6. Repeat verification until all criteria pass or a blocker requires the user's decision.
7. Have the Project Manager review the final reports and approve the task only when all workflow requirements are satisfied.

Do not rebuild functionality that is already implemented. Do not change acceptance criteria or expand scope without the user's approval.

## Required Final Summary

Every completed execution must report:

- Implementation status.
- Each acceptance criterion and its verification result.
- QA verdict: PASS, FAIL, or NOT VERIFIED.
- Validation evidence and remaining blockers.
- Project Manager approval status.

Never report PASS without evidence that every acceptance criterion has passed verification. Never claim final approval before the Project Manager has approved the task.