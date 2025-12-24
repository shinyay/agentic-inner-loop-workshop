---
name: eval-analyze
description: Create a written evaluation report from AI Toolkit results and failures.
agent: 'ask'
---

## Task

Help me write an evaluation report.

## Input I will provide

- Which prompt/agent version I evaluated (v1, v2, ...)
- The evaluation metrics and what changed
- 3–5 representative failure cases (inputs + outputs)

## Output

Generate a report that matches:

- `docs/templates/eval-report.template.md`

I will copy/paste the result into `reports/eval/<timestamp>_vN.md`.

## Constraints

- Be concrete and action-oriented.
- Each failure should propose a plausible fix.
