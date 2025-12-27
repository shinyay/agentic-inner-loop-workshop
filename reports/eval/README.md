# Evaluation reports

Put evaluation notes here.

Why this exists:

- AI Toolkit evaluation results are great in the UI, but workshop learning improves when you
  *write down what changed* and *what to do next*.
- The inner loop only closes when evaluation findings become **actionable tasks**.

Suggested naming:

- `YYYYMMDD_HHMM_baseline.md`
- `YYYYMMDD_HHMM_prompt-v2.md`

Template:

- See `docs/templates/eval-report.template.md`

## Turn findings into issues (close the loop)

To keep the workshop loop moving, convert your evaluation report into actionable tasks:

1. In your report, write 3–10 bullets under `## 4. Actions`.
2. Convert those actions into GitHub Issues with a clear DoD + validation.

Optional helper:

- `scripts/eval_report_to_issues.py` can generate copy/pasteable issue draft skeletons from the bullets under `## 4. Actions`.

Suggested place to save generated drafts:

- `reports/eval/issues-from-eval.md`

See also: `docs/workshop/07_feedback.md`.

