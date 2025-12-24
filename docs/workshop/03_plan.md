# 03 — Plan

## Goal

Convert the spec into an implementation plan that can be split into issues.

Primary artifact:

- `docs/plan.md`

## Steps

### Step 1 — Run the plan prompt file

In Copilot Chat, run:

- `/create-plan`

The plan should be sized for the workshop:
- 6–10 tasks
- each task 0.5–2 hours
- each task includes DoD + validation command

### Step 2 — Sanity-check sequencing

Ensure tasks are ordered so that earlier tasks unlock later tasks.

Example sequencing:

1. Schema + contract tests
2. Deterministic baseline adapter
3. CLI wrapper + CLI tests
4. Evaluation dataset + local eval command
5. AI Toolkit baseline evaluation
6. Prompt/agent improvements based on failures

### Step 3 — Add risks

A plan that ignores risks creates thrash.

Examples:
- invalid JSON from models
- non-deterministic rationale text
- label taxonomy ambiguity

### Step 4 — Commit the plan

```bash
git add docs/plan.md
git commit -m "docs: add initial plan"
```

## Outputs for this module

- `docs/plan.md` that is easy to convert into GitHub Issues

Next: `04_issues.md`
