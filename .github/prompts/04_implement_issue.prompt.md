---
name: implement-issue
description: Implement a selected GitHub Issue with minimal changes and validation.
agent: 'agent'
---

## Task

Implement **one** GitHub Issue from this repository.

## Input needed

If the issue is not already in context, ask for:

- issue title (and/or issue number)
- Definition of Done (checkboxes)
- validation commands

## Constraints

- Make the **minimal** change needed to satisfy the DoD.
- Keep CLI output stable: `triage` prints JSON on stdout only.
- Update/add tests when behavior changes.
- Prefer edits over refactors.

## Required validation

Run at least:

- `pytest -q`

If you change formatting/lint rules, also run:

- `ruff check .`
- `ruff format --check .`

## Output

- Apply code changes in the workspace.
- Summarize what changed and how it was validated.
