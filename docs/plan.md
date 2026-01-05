# Implementation Plan (AI Toolkit scenario)

Goal:

- Run the workshop inner loop **twice**:

  - **v1 baseline**: bulk run + evaluation + report
  - **v2 improved**: apply fixes + re-run + compare + report

- Keep the deterministic gate green throughout (tests + schema discipline).

Steps:

1. Confirm deterministic baseline works (tests + CLI schema).
2. Create a minimal v1 agent/prompt in AI Toolkit and run bulk run + evaluation.
3. Record v1 findings in `reports/eval/` and convert failures into issues.
4. Implement at least one improvement (prompt-only and/or code+tests).
5. Run v2 bulk run + evaluation, compare with v1, and record v2.

Expected outputs:

- 3–6 GitHub Issues created from this plan.
- At least one PR that closes an issue via `Fixes #NN`.
- `reports/eval/<YYYYMMDD-HHMM>_v1.md` and `reports/eval/<YYYYMMDD-HHMM>_v2.md` committed.

## 1. Milestones

- M0: Deterministic gate is green (tests pass; CLI prints schema-valid JSON)
- M1: AI Toolkit v1 baseline created, bulk run executed, evaluation completed
- M2: v1 evaluation report committed and turned into improvement issues
- M3: At least one improvement implemented and validated
- M4: AI Toolkit v2 evaluation completed and compared to v1; v2 report committed

## 2. Work breakdown

Each task below is designed to be 0.5–2 hours.

### Issue 1: Deterministic gate check + CLI contract smoke

Problem statement:

- Before running probabilistic evaluation, the CLI contract must be stable.

Definition of Done:

- [ ] Tests pass.
- [ ] `triage-assistant schema` prints valid JSON.
- [ ] `triage-assistant triage --adapter dummy ...` prints JSON-only on stdout.

Validation:

- `uv run pytest -q`
- `uv run triage-assistant schema | python3 -c "import json,sys; json.loads(sys.stdin.read())"`

Dependencies:

- None.

### Issue 2: AI Toolkit v1 baseline (prompt/agent)

Problem statement:

- We need a minimal baseline to generate failures we can learn from.

Definition of Done:

- [ ] Create a v1 prompt/agent that:

  - returns **JSON only** (no markdown fences)
  - uses the allowed enums for `type` and `priority`
  - produces outputs that match the schema fields (`type`, `priority`, `labels`, `rationale`)

- [ ] Run bulk run using `datasets/triage_dataset.csv` with `title` and `body` variables.
- [ ] Run at least one evaluation (for example, relevance and/or coherence).
- [ ] Save the prompt/agent as a version named `v1-baseline` (or equivalent).

Validation:

- (manual, tool-assisted) confirm the dataset run exists and produces outputs for all rows.

Dependencies:

- None.

### Issue 3: Write and commit v1 evaluation report

Problem statement:

- We need durable “repo memory” of what failed and what we plan to fix.

Definition of Done:

- [ ] Create `reports/eval/<YYYYMMDD-HHMM>_v1.md` using `docs/templates/eval-report.template.md`.
- [ ] Include:

  - model/provider used
  - the v1 version name
  - evaluation metrics (from AI Toolkit)
  - 3–5 representative failures (input → expected → actual → why)
  - 2–4 actionable follow-ups (issue-sized)

- [ ] Commit the report.

Validation:

- `uv run pytest -q`

Dependencies:

- Depends on Issue 2.

### Issue 4: Create improvement issues from v1 failures

Problem statement:

- Without turning failures into issues, the loop stalls.

Definition of Done:

- [ ] Create 2–4 GitHub Issues based on v1 failures.
- [ ] Each issue includes:

  - a crisp DoD
  - validation steps (tests and/or v2 evaluation rerun)
  - a reference to the v1 report section that motivated it

Validation:

- N/A (process step), but keep deterministic gate green when you implement.

Dependencies:

- Depends on Issue 3.

### Issue 5: Implement one deterministic improvement (code + tests)

Problem statement:

- We want at least one improvement that is enforced deterministically.

Suggested scope (pick one):

- Security-like reports get the `security` label and default to `p0`.
- Crashes with reproduction steps present should not be tagged `needs-repro`.
- Normalize labels more strictly (trim, lower-case, de-dup) and add tests.

Definition of Done:

- [ ] Implement the chosen improvement in code.
- [ ] Add or update tests that lock the new behavior.
- [ ] Open a PR that closes the corresponding GitHub Issue (`Fixes #NN`).

Validation:

- `uv run pytest -q`

Dependencies:

- Depends on Issue 4 (choose one of the created issues).

### Issue 6: AI Toolkit v2 improved + compare to v1

Problem statement:

- We need to demonstrate a measurable improvement, not just changes.

Definition of Done:

- [ ] Apply a targeted improvement (prompt-only, code-assisted, or both).
- [ ] Save as a new version named `v2-improved` (or equivalent).
- [ ] Re-run bulk run + evaluation and compare v2 vs v1.
- [ ] Capture at least one “fixed failure case” from v1.

Validation:

- (manual, tool-assisted) compare view shows metric deltas for v1 vs v2.

Dependencies:

- Depends on Issue 5 (or another improvement issue).

### Issue 7: Write and commit v2 evaluation report

Problem statement:

- The workshop requires recording the before/after (v1 → v2) and next steps.

Definition of Done:

- [ ] Create `reports/eval/<YYYYMMDD-HHMM>_v2.md` using the same template.
- [ ] Include:

  - v1 vs v2 metric deltas
  - what changed
  - at least one fixed failure case
  - remaining gaps and next issues

- [ ] Commit the report.

Validation:

- `uv run pytest -q`

Dependencies:

- Depends on Issue 6.

## 3. Testing strategy

- Unit tests: `uv run pytest -q`
- CLI contract tests: stdout JSON-only for `triage`, errors on stderr
- Schema/contract tests: validate output against `TriageOutput` (`src/triage_assistant/schema.py`)

## 4. Evaluation strategy

- AI Toolkit Agent Builder:

  - dataset: `datasets/triage_dataset.csv`
  - bulk run in v1 and v2
  - evaluators: start with relevance/coherence; add custom checks if needed
  - versioning + compare (v1 vs v2)

- Record outcomes in `reports/eval/`.

Notes:

- Rate limits may apply depending on the chosen model/provider; keep the dummy adapter available as a fallback.

## 5. Risks and mitigations

- Provider auth/rate limits: keep dummy baseline; treat hosted runs as best-effort.
- JSON mode differences across models: always validate against schema; keep extraction robust.
- UI drift (preview tooling): document intent + fallbacks, not fragile click paths.

## 6. Timebox

Good enough for one workshop session:

- complete Issue 5 (one deterministic improvement) with tests and a PR
- complete Issue 3 + Issue 7 (v1 + v2 reports)
- show at least one v2 improvement over v1 (metric delta and/or fixed failure case)


