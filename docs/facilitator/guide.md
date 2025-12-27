# Facilitator Guide: Agentic Inner Loop Workshop

This guide is for instructors running the participant scenario in:

- `docs/workshop/09_hands-on-scenario.md`

It contains:
- Suggested timing (60/90/120 minute run options)
- Instructor “talk track” emphasis points
- Common stumbling points and concrete fixes
- Alternative paths for participants without model access

---

## Learning objectives

By the end of the workshop, participants can:

1. Produce and commit **Spec** and **Plan** artifacts that constrain AI-assisted development.
2. Turn a plan into **Issue-sized tasks** with DoD + validation commands.
3. Implement one task using Copilot Chat while keeping the deterministic gate green.
4. Use AI Toolkit to run:
   - Bulk run against a dataset
   - Evaluation with built-in evaluators
   - Versioning + evaluation comparison
5. Convert evaluation failures into new Issues and run a second improvement cycle.

---

## Recommended format

### Group size
- 5–30 participants works well.
- Best experience: pairs (driver/navigator).

### Instructor setup
- Project VS Code and show:
  - Copilot Chat prompts (`/draft-spec`, etc.)
  - GitHub Issues panel + “Start working on issue”
  - AI Toolkit (Agent Builder + Evaluation tab)
  - A sample evaluation comparison (v1 vs v2)

---

## Pre-flight checklist (do this before the workshop)

### Repo health
- [ ] `pytest -q` passes on `main`
- [ ] `.github/prompts/` contains the prompt files referenced in the scenario
- [ ] Templates exist:
  - `docs/templates/eval-report.template.md`
  - `.github/ISSUE_TEMPLATE/*`
- [ ] `datasets/triage_dataset.csv` exists and has enough rows (8–30 is fine)

### Tooling
- [ ] You can sign in to GitHub from VS Code (Copilot + Issues)
- [ ] AI Toolkit appears in the Activity Bar and opens successfully

### Model access plan (choose one)
- [ ] **GitHub Models plan:** you have a PAT with `models:read` and verified inference works
- [ ] **Foundry plan:** you have a resource endpoint and key, and verified inference works
- [ ] **Fallback plan:** you have at least one model usable in AI Toolkit (any catalog), or you will project-run the evaluation steps

### Optional (highly recommended)
- [ ] Prepare a “baseline” v1 evaluation result screenshot or notes to show what failures look like
- [ ] Prepare a tiny improvement “v2” (prompt tweak) that produces an obvious score/failure improvement

---

## Timing options

### Option A: 120 minutes (recommended)
1. Setup + deterministic baseline: 10
2. Spec: 10
3. Plan: 10
4. Issues: 10
5. Implement one Issue + PR: 25
6. AI Toolkit v1 bulk run + evaluation: 20
7. Eval report v1 + feedback → issues: 15
8. v2 improvement + compare + report: 15
9. Retro: 5

### Option B: 90 minutes (standard)
- Reduce implementation scope (smaller issue)
- Use manual rating + 1 evaluator only

### Option C: 60 minutes (fast demo)
- Instructor drives; participants follow along
- Skip PR creation; just commit locally
- AI Toolkit: manual rating only (or 1 evaluator, if time permits)

---

## Run-of-show (120-minute script)

### 0. Opening framing (2–3 min)
Emphasize:
- “Agentic inner loop” means **rapid iteration with memory**:
  - Spec/Plan are the memory artifacts
  - Issues are task memory
  - Eval reports are quality memory
- Two quality gates:
  - deterministic: tests/schema
  - probabilistic: evaluation and version comparison

### 1. Setup (10 min)
Participants follow scenario Step 0–1.

Instructor notes:
- Make sure everyone sees prompt files by typing `/` in Copilot Chat.
- If prompt files don’t appear, fix it early (see troubleshooting).

Stop & check:
- Everyone can run `pytest -q`
- Everyone can run `triage-assistant schema`

### 2. Spec (10 min)
Participants run `/draft-spec` and commit.

Instructor emphasis:
- Spec’s purpose is not length — it’s **constraints**:
  - JSON-only output contract
  - allowed values
  - acceptance criteria that can be tested/evaluated

Stop & check:
- `docs/spec.md` committed

### 3. Plan (10 min)
Participants run `/create-plan` and commit.

Instructor emphasis:
- Plan must produce Issue-sized tasks.
- Each task must include:
  - DoD (checkboxes)
  - validation commands

Stop & check:
- `docs/plan.md` committed

### 4. Issues (10 min)
Participants run `/split-to-issues`, commit, and create 3 Issues.

Instructor emphasis:
- “1 issue = 0.5–2 hours”
- Avoid vague tasks like “improve AI accuracy” — require:
  - specific failure mode
  - reproduction steps
  - how to validate

Stop & check:
- 3 issues created

### 5. Implement one Issue (25 min)
Participants:
- Start working on issue → branch
- Use `/implement-issue`
- Run `pytest -q`
- Commit with `Fixes #NN`
- Open PR (optional if time)

Instructor emphasis:
- Keep diffs small, run tests often.
- Demonstrate checkpoint rollback (if enabled) when someone gets a large unwanted edit.

Stop & check:
- At least one PR or at least one branch with a commit that references the issue.

### 6. AI Toolkit v1 evaluation (20 min)
Participants:
- Open AI Toolkit → Agent Builder → Evaluation tab
- Import dataset
- Run All
- Rate outputs 👍/👎
- Run at least 1 evaluator
- Save as `v1-baseline`

Instructor emphasis:
- Bulk run is now in Agent Builder Evaluation tab (people often look for a separate “Bulk Run” tool).
- Evaluation results are meaningless unless we **write them down** in repo memory (`reports/eval/`).

Stop & check:
- Everyone has at least:
  - bulk run outputs visible, and
  - one evaluator executed (or manual ratings recorded)

### 7. Eval report v1 → feedback issues (15 min)
Participants:
- Create `reports/eval/*_v1.md`
- Run `/feedback-to-issues`
- Create 1–2 eval-driven issues

Instructor emphasis:
- This is the “loop closure” moment.
- Make sure issues include validation steps like:
  - “Re-run v2 evaluation in AI Toolkit”
  - “Compare against v1-baseline”

Stop & check:
- `*_v1.md` committed
- At least one eval-driven issue exists

### 8. v2 improvement + compare (15 min)
Participants:
- Make a prompt tweak or a code fix
- Save as `v2-improved`
- Re-run bulk run + evaluation
- Compare v1 vs v2
- Write `*_v2.md`

Instructor emphasis:
- We don’t need perfect accuracy — we need **observable improvement**:
  - a fixed failure case
  - a score that moved in the right direction

Stop & check:
- `*_v2.md` committed
- A v1 vs v2 comparison exists

### 9. Retro (5 min)
Ask:
- What did Spec/Plan prevent?
- What was the smallest unit of progress?
- What belongs to deterministic vs probabilistic gate?
- What will you do differently next time?

---

## Common stumbling points and fixes

### 1) Prompt files don’t show up in Copilot Chat
**Symptoms**
- Typing `/` shows no `/draft-spec`, etc.

**Likely causes**
- Workspace not trusted
- Opened wrong folder (not repo root)
- Old VS Code / Copilot Chat version

**Fixes**
- Ensure Workspace is trusted (Manage → Workspace Trust)
- Ensure `.github/prompts/` exists in the opened folder
- Reload window: Command Palette → “Developer: Reload Window”
- As a fallback, copy prompt text from the prompt files and paste into chat.

### 2) GitHub Issues panel is empty
**Symptoms**
- No issues appear; cannot “Start working on issue”.

**Fixes**
- Ensure GitHub sign-in in VS Code
- Ensure the repo remote is set to GitHub and you opened the correct repo
- Use browser to create issues if VS Code UI fails, then refresh in VS Code.

### 3) AI Toolkit UI labels don’t match
**Symptoms**
- Participants can’t find “Prompt Builder” or “Bulk Run”.

**Notes**
- “Agent Builder” is the current naming (formerly Prompt Builder).
  Reference: https://code.visualstudio.com/docs/intelligentapps/agentbuilder
- Bulk run is integrated into Agent Builder under the Evaluation tab.
  Reference: https://code.visualstudio.com/docs/intelligentapps/bulkrun

**Fix**
- Tell participants: AI Toolkit → Agent Builder → Evaluation tab

### 4) Evaluation is slow or rate-limited
**Symptoms**
- Timeouts, slow runs, errors during evaluation.

**Likely causes**
- Rate limits when using GitHub-hosted models as judges
- Too many dataset rows
- Using a heavyweight judge model

**Fixes**
- Reduce dataset rows to 5–10 for the workshop
- Run manual ratings only (👍/👎) for first pass
- Use a cheaper/smaller judge model if possible
- If evaluation can’t run, still write `reports/eval/*` with manual failure analysis.

### 5) JSON output is invalid (code fences, extra prose)
**Symptoms**
- Output contains markdown fences or non-JSON text.

**Fixes**
- Prompt changes:
  - “Return JSON only. No markdown. No code fences.”
  - Provide a strict JSON schema excerpt or field constraints
- Code changes:
  - Improve extraction/validation fallback
  - Add tests that assert valid JSON-only output

### 6) GitHub Models auth errors (401/403)
**Symptoms**
- 403 “No access to model…” or 401 unauthorized.

**Likely causes**
- Token missing `models:read`
- Using the wrong endpoint/token pairing

**Fixes**
- Verify PAT scope includes `models:read`
- Confirm endpoint is `https://models.github.ai/inference/chat/completions`
- Confirm request headers include `Authorization: Bearer ...` and recommended API version header

References:
- GitHub Models quickstart: https://docs.github.com/en/github-models/quickstart
- GitHub Models inference API: https://docs.github.com/en/rest/models/inference?apiVersion=2022-11-28

### 7) Foundry endpoint errors
**Symptoms**
- 404 on chat completions, or auth failures.

**Fixes**
- Ensure endpoint ends with `/models`
- Ensure query `api-version` is set (example: `2024-05-01-preview`)
- Ensure header is correct (`api-key` for key auth)
- Confirm deployment name matches `model`/`name` parameter usage in your adapter

References:
- Foundry endpoint concept: https://learn.microsoft.com/en-us/azure/ai-foundry/foundry-models/concepts/endpoints?view=foundry-classic
- Chat completions REST: https://learn.microsoft.com/en-us/rest/api/aifoundry/model-inference/get-chat-completions/get-chat-completions?view=rest-aifoundry-model-inference-2024-05-01-preview

---

## Alternative paths (when things go wrong)

### A) No one can access any model
Run the workshop as:
- Spec → Plan → Issues → Implement (deterministic only)
- Instructor demonstrates AI Toolkit evaluation on projector
- Participants still write eval reports from the demonstration output

### B) Time is running out
Minimal viable loop completion:
- Generate Spec + Plan + Issues (commit)
- Implement only one tiny Issue (commit)
- AI Toolkit: bulk run only + manual rating (no evaluators)
- Write v1 report + create one feedback issue

### C) Mixed audience (some have Foundry, some GitHub Models)
Encourage:
- Same dataset
- Same output contract
- Compare results in retro (“provider differences are part of the learning”)

---

## Suggested “starter issue” you can seed (optional)

If you want faster startup, seed this issue before the workshop:

**Title:** “Treat security-related issues as bug + p0 + security label (dummy adapter)”
**DoD**
- [ ] Add/update logic in deterministic adapter
- [ ] Add tests
- [ ] `pytest -q` passes
**Validation**
- `pytest -q`
- `triage-assistant triage --adapter dummy --title "...security..." --body "..." --pretty`

---

## Reference docs (for instructors)
- AI Toolkit overview: https://code.visualstudio.com/docs/intelligentapps/overview
- Agent Builder: https://code.visualstudio.com/docs/intelligentapps/agentbuilder
- Bulk run: https://code.visualstudio.com/docs/intelligentapps/bulkrun
- Evaluation: https://code.visualstudio.com/docs/intelligentapps/evaluation
- GitHub Models quickstart: https://docs.github.com/en/github-models/quickstart
- GitHub Models inference API: https://docs.github.com/en/rest/models/inference?apiVersion=2022-11-28
- Foundry endpoints: https://learn.microsoft.com/en-us/azure/ai-foundry/foundry-models/concepts/endpoints?view=foundry-classic
- Foundry chat completions REST: https://learn.microsoft.com/en-us/rest/api/aifoundry/model-inference/get-chat-completions/get-chat-completions?view=rest-aifoundry-model-inference-2024-05-01-preview
