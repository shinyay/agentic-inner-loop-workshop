# Issue drafts (AI Toolkit scenario)

Goal:

- Convert `docs/plan.md` into **copy/paste-ready GitHub Issue drafts** that match the hands-on scenario.

How to use:

1. Copy one draft below into a new GitHub Issue.
2. Use VS Code GitHub panel → “Start working on issue” to create a branch.
3. Implement (if needed) → run validation → open a PR that closes the issue.

Notes:

- Validation commands in this repo should prefer `uv run ...` (the system Python may not have `pip/ensurepip`).
- Never paste tokens/keys into issues or commit them.

---

## Issue 1: Deterministic improvement (code + tests)

Labels (suggested):

- `bug`
- `p1`

Problem statement:

- We need at least one improvement that is enforced **deterministically** (tests), not only via prompt tuning.

Proposed change (pick one scope; smallest wins):

- A) Security-like reports get the `security` label and default to `p0`.
- B) Crashes with reproduction steps present should not be labeled `needs-repro`.
- C) Normalize labels more strictly (trim, lowercase, de-dup) and add tests.

Definition of Done:

- [ ] Implement the chosen improvement in code.
- [ ] Add/adjust unit tests that lock the new behavior.
- [ ] Keep `triage` stdout JSON-only (no extra logging).

Validation command(s):

- `uv run pytest -q`

PR instructions:

- Commit message includes `Fixes #NN`.

Notes / dependencies:

- None.

---

## Issue 2: AI Toolkit v1 baseline (prompt/agent) + bulk run + evaluation

Labels (suggested):

- `feature`
- `p2`

Problem statement:

- We need a v1 baseline to discover failure modes from real model outputs.

Definition of Done:

- [ ] Create a minimal Agent Builder prompt/agent that:

	- returns **JSON only** (no markdown code fences)
	- respects the allowed enums for `type` and `priority`
	- outputs the schema fields: `type`, `priority`, `labels`, `rationale`

- [ ] Bulk run with `datasets/triage_dataset.csv` mapping:

	- `title` → `title`
	- `body` → `body`

- [ ] Run at least one evaluation (e.g., coherence and/or relevance).
- [ ] Save version as `v1-baseline`.

Validation command(s):

- (manual) confirm the dataset grid shows outputs for all rows and an evaluation result exists.

Notes / dependencies:

- None.

---

## Issue 3: Write and commit evaluation report v1

Labels (suggested):

- `docs`
- `p2`

Problem statement:

- Evaluation results must become “repo memory” so we can turn them into issues.

Definition of Done:

- [ ] Create `reports/eval/<YYYYMMDD-HHMM>_v1.md` using `docs/templates/eval-report.template.md`.
- [ ] Include:

	- provider/model used
	- v1 version name (`v1-baseline`)
	- evaluation scores (from AI Toolkit)
	- 3–5 representative failures (input → output → why wrong)
	- 2–4 follow-up items (issue-sized)

- [ ] Commit the report.

Validation command(s):

- `uv run pytest -q`

Notes / dependencies:

- Depends on Issue 2.

---

## Issue 4: Feedback-to-issues (create improvement issues from v1 failures)

Labels (suggested):

- `docs`
- `p2`

Problem statement:

- Without converting failures into issues, the loop stalls.

Definition of Done:

- [ ] Create 2–4 GitHub Issues derived from `..._v1.md`.
- [ ] Each issue includes:

	- a crisp DoD
	- validation steps (tests and/or “re-run v2 evaluation”)
	- a link/reference to the v1 report section that motivated it

- [ ] At least one issue is explicitly “evaluation-driven” (i.e., it cites a failure case).

Validation command(s):

- N/A (process step).

Notes / dependencies:

- Depends on Issue 3.

---

## Issue 5: AI Toolkit v2 improved + compare vs v1

Labels (suggested):

- `feature`
- `p2`

Problem statement:

- We need to show measurable improvement (v2 vs v1), not just changes.

Definition of Done:

- [ ] Apply a targeted improvement (prompt-only, code-assisted, or both).
- [ ] Save version as `v2-improved`.
- [ ] Re-run bulk run + evaluation.
- [ ] Use compare view to compare `v2-improved` vs `v1-baseline`.
- [ ] Capture at least one “fixed failure case” from v1.

Validation command(s):

- (manual) compare view shows metric deltas and you can point to at least one fixed case.

Notes / dependencies:

- Depends on Issue 4 (so you know what to improve).

---

## Issue 6: Write and commit evaluation report v2 (v1 → v2 deltas)

Labels (suggested):

- `docs`
- `p2`

Problem statement:

- The workshop requires a written record of the improvement (deltas + what changed).

Definition of Done:

- [ ] Create `reports/eval/<YYYYMMDD-HHMM>_v2.md` using the same template.
- [ ] Include:

	- v1 vs v2 metric deltas
	- what changed (prompt and/or code)
	- at least one fixed failure case
	- remaining gaps and next issues

- [ ] Commit the report.

Validation command(s):

- `uv run pytest -q`

Notes / dependencies:

- Depends on Issue 5.



