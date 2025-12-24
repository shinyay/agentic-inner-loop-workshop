# 07 — Feedback Loop Closure

## Goal

Turn evaluation findings into durable work, and run the loop again.

The inner loop is only “agentic” if it closes:

**evaluation → tasks → implementation → re-evaluation**

## Steps

### Step 1 — Read your evaluation report

Open the report you wrote under `reports/eval/`.

Pick 1–3 actions that are:
- small (0.5–2 hours)
- likely to improve the metric
- testable or measurable

### Step 2 — Convert actions into GitHub Issues

Use the issue templates.

For each new issue:
- include a DoD
- include how to validate (AI Toolkit version compare OR unit tests)

If failures are due to unclear requirements, update:
- `docs/spec.md`
- `docs/plan.md`

### Step 3 — Implement one feedback issue

Repeat module `05_implement.md` for one feedback issue.

### Step 4 — Re-evaluate

Run AI Toolkit evaluation again:
- v2: improved prompt/agent

Compare v2 vs v1.

### Step 5 — Record the delta

Append or create a new evaluation note under `reports/eval/`.

## Outputs for this module

- New GitHub Issues derived from evaluation
- A second iteration (v2) in AI Toolkit
- Written record of what improved and why

Next: `08_retro.md`
