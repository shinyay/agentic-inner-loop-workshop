---
name: split-to-issues
description: Convert docs/plan.md into issue drafts and write docs/issues-draft.md.
agent: 'agent'
---

## Task

Read `docs/plan.md` and produce GitHub Issue drafts.

## Output format

Write a new file:

- `docs/issues-draft.md`

For each issue draft, include:

- Title
- Labels (suggested)
- Problem statement
- Definition of Done (checkboxes)
- Validation command(s)
- Notes / dependencies

## Constraints

- Prefer **small** issues.
- Ensure at least one issue covers:
  - deterministic baseline (tests, schema, CLI stability)
  - probabilistic evaluation (AI Toolkit dataset run + versioning)
  - feedback loop closure (turn eval failures into new issues)

## Output

- Create or update `docs/issues-draft.md` only.
- Do not create GitHub Issues automatically.
