# Implementation Plan

Goal:

- Convert `docs/spec.md` into a workshop-sized backlog of issues (0.5–2h each) that are easy to validate.

Steps:

1. Pick one issue → create a branch → implement → open PR.
2. Keep deterministic gates green: `python3 -m pytest -q`.
3. Run probabilistic evaluation (AI Toolkit) periodically and record findings.

Expected outputs:

- 6–10 issue-sized tasks with clear DoD + validation.
- Evaluation findings recorded under `reports/eval/`.

## 1. Milestones

- M0: Spec/plan/issues drafts exist (external memory)
- M1: Deterministic contract stays green (tests + schema discipline)
- M2: Hosted adapter smoke-tests (optional)
- M3: Probabilistic evaluation loop (AI Toolkit dataset runs)
- M4: Feedback closure (eval → new issues)

## 2. Work breakdown

Each task below is designed to be 0.5–2 hours.

### Issue 1: Workshop docs prerequisites + UI drift guardrails

Problem statement:

- Participants get blocked by version/UI differences (VS Code checkpoints, AI Toolkit preview UI).

Definition of Done:

- [ ] Add a short “Versions & prerequisites” note to the relevant workshop doc(s) under `docs/workshop/`.
- [ ] Mention VS Code checkpoints requirement (VS Code 1.103+).
- [ ] Mention AI Toolkit is preview and include at least one fallback navigation path (Command Palette / alternate menu).

Validation:

- `python3 -m pytest -q`

Dependencies:

- None.

### Issue 2: Add `triage-assistant doctor` for configuration diagnosis

Problem statement:

- Hosted adapters fail when env vars are missing; diagnosing “what is auto doing?” is slow.

Definition of Done:

- [ ] Add a `doctor` command that prints which adapter `--adapter auto` would choose.
- [ ] Show missing env vars for GitHub Models / Foundry / OpenAI-compatible (best-effort).
- [ ] Do not break `triage` JSON-only stdout contract.
- [ ] Add unit tests for the doctor output.

Validation:

- `python3 -m pytest -q`

Dependencies:

- None.

### Issue 3: Improve hosted adapter error messages (actionable, safe)

Problem statement:

- HTTP failures are not always actionable; users need “what to check next” without secrets leakage.

Definition of Done:

- [ ] Improve error messages for GitHub Models and Foundry adapters to include status code + safe hint.
- [ ] Ensure tokens/keys are never printed.
- [ ] Add at least one mocked failure test.

Validation:

- `python3 -m pytest -q`

Dependencies:

- None (can be done independently of Issue 2).

### Issue 4: Strengthen CLI contract tests (stdout JSON-only)

Problem statement:

- The most important contract is “`triage` prints JSON-only on stdout”. Regressions break pipelines.

Definition of Done:

- [ ] Add/extend tests that assert `triage` stdout is parseable JSON.
- [ ] Add/extend tests that assert errors go to stderr (not stdout).

Validation:

- `python3 -m pytest -q`

Dependencies:

- None.

### Issue 5: Improve `triage-assistant eval` Markdown report for fast iteration

Problem statement:

- The local eval report is useful, but needs better “what failed” visibility for iteration.

Definition of Done:

- [ ] Improve report readability (expected vs predicted, rationale, failure examples).
- [ ] Add a small “top failure patterns” section (even basic grouping is OK).
- [ ] Add a unit test that asserts key headings exist.

Validation:

- `python3 -m pytest -q`

Dependencies:

- None.

### Issue 6: Document the evaluation loop (AI Toolkit) + where to record results

Problem statement:

- Participants run evals but don’t consistently record findings in a reusable way.

Definition of Done:

- [ ] Add a short “Run/Evaluate” checklist under `docs/workshop/`.
- [ ] Reference dataset: `datasets/triage_dataset.csv`.
- [ ] Specify where to record results: `reports/eval/`.

Validation:

- `python3 -m pytest -q`

Dependencies:

- Issue 1 recommended first (to keep docs consistent), but not required.

### Issue 7: Close the loop (eval findings → new issues)

Problem statement:

- Without turning failures into issues, the loop stalls.

Definition of Done:

- [ ] Document how to create issue drafts from evaluation findings.
- [ ] (Optional) Document how to use `scripts/eval_report_to_issues.py` if appropriate.
- [ ] Ensure the flow produces copy/pasteable issue drafts.

Validation:

- `python3 -m pytest -q`

Dependencies:

- Depends on Issue 6 (evaluation loop docs) for best readability.

### Issue 8: Hosted adapter smoke-test note (optional but practical)

Problem statement:

- Workshop participants often want to confirm hosted adapters work end-to-end, but setup varies.

Definition of Done:

- [ ] Add a short doc note pointing to `docs/providers.md` and showing a minimal smoke-test command.
- [ ] Include a reminder that secrets live in env vars / `.env` and should not be pasted.

Validation:

- `python3 -m pytest -q`

Dependencies:

- None.

## 3. Testing strategy

- Unit tests: `python3 -m pytest -q`
- CLI contract tests: stdout JSON-only for `triage`, errors on stderr
- Schema/contract tests: validate output against `TriageOutput` (`src/triage_assistant/schema.py`)

## 4. Evaluation strategy

- AI Toolkit:
  - dataset: `datasets/triage_dataset.csv`
  - baseline version + compare against later iterations
  - metrics: type accuracy, priority accuracy, label overlap/F1
- Local smoke eval:
  - `triage-assistant eval --adapter dummy --dataset datasets/triage_dataset.csv`
- Record outcomes in `reports/eval/`

## 5. Risks and mitigations

- Provider auth/rate limits: keep dummy baseline; treat hosted runs as best-effort.
- JSON mode differences across models: always validate against schema; keep extraction robust.
- UI drift (preview tooling): document intent + fallbacks, not fragile click paths.

## 6. Timebox

Good enough for one workshop session:

- complete 1–2 issues with tests
- run at least one evaluation (AI Toolkit or local eval)
- record findings under `reports/eval/`


