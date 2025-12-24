---
name: draft-spec
description: Draft or refresh docs/spec.md using the repository template.
argument-hint: "goal=... (optional)"
agent: 'agent'
---

You are working in the repository **agentic-inner-loop-workshop**.

## Task

Create or update `docs/spec.md` by using the template in:

- `docs/templates/spec.template.md`

## Requirements

1. Keep the spec readable in **~5 minutes**.
2. The spec must explicitly define:
   - the output contract (type/priority/labels/rationale)
   - allowed values for `type` and `priority`
   - the label taxonomy used in this repo
3. Reference `src/triage_assistant/schema.py` as the single source of truth.
4. Acceptance criteria must be **testable** and include validation commands.
5. Include an evaluation plan that mentions:
   - deterministic gates (pytest, schema validation)
   - probabilistic evaluation (AI Toolkit + `datasets/triage_dataset.csv`)
6. Ask up to **3 clarifying questions** only if necessary. Otherwise, make reasonable assumptions.

## Output

- Edit `docs/spec.md` only.
- Do not change code in this task.
