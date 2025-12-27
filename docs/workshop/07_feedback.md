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

To keep the loop repeatable, start from the **Actions** section of your evaluation report.
If you used `docs/templates/eval-report.template.md`, your report already has:

- `## 4. Actions`

Under that header, write each action as a bullet point. Keep actions small (0.5–2 hours).
Example:

- Fix label normalization edge-cases (dedupe case-insensitively)
- Add a regression test for stdout JSON-only on `triage`

For each new issue:
- include a DoD
- include how to validate (AI Toolkit version compare OR unit tests)

If failures are due to unclear requirements, update:
- `docs/spec.md`
- `docs/plan.md`

#### Optional: generate copy/pasteable issue drafts from the eval report

If you want a faster path from “Actions” to “Issues”, use the helper script:

- `scripts/eval_report_to_issues.py`

It extracts bullet points under `## 4. Actions` and generates Markdown issue skeletons you can copy/paste into GitHub.

Steps:

1. Ensure your evaluation report has a `## 4. Actions` section with bullet points.
2. Run the script and write drafts to a Markdown file you can keep in the repo.

Suggested output locations (pick one convention and stick to it):

- `reports/eval/issues-from-eval.md` (keeps “findings → tasks” together)
- `docs/issues-from-eval.md` (keeps drafts near other workshop docs)

Expected output:

- A Markdown file containing “Draft 1…N” sections with Problem/DoD/Validation headings, ready to copy/paste into GitHub Issues.

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

