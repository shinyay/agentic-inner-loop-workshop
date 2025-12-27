# Hands-on Scenario: Agentic Inner Loop Workshop

**Audience:** Participants
**Duration:** 90–120 minutes
**Goal:** Start from **Spec** and **Plan**, then experience two iterations of an **Agentic inner loop** using **Copilot Chat × AI Toolkit × GitHub Issues**.

This scenario is designed to be **copy/paste runnable** inside this repository. You’ll produce real artifacts (docs, issues, code, evaluation reports) that prove you can run the loop.

---

## What you will build

A minimal **GitHub Issue Triage Assistant**:

- **Input:** issue `title` + `body`
- **Output:** **JSON only**, validated by the repo schema:
  - `type`: `bug | feature | docs | question`
  - `priority`: `p0 | p1 | p2`
  - `labels`: `string[]`
  - `rationale`: `string`

You’ll improve it with two quality gates:

- **Deterministic gate:** tests + schema validation (must always be green)
- **Probabilistic gate:** AI Toolkit bulk run + evaluation + version comparison (must show “better”)

---

## Outcomes (things you will commit / create)

By the end, you should have:

- ✅ `docs/spec.md` (Spec)
- ✅ `docs/plan.md` (Plan)
- ✅ `docs/issues-draft.md` (Issue draft)
- ✅ 3–6 GitHub Issues created from the plan
- ✅ 1 PR that closes at least one issue via `Fixes #NN`
- ✅ `reports/eval/<timestamp>_v1.md` and `..._v2.md` (evaluation notes)
- ✅ At least one evaluation-driven improvement issue (created from v1 failures)

---

## Prerequisites checklist

### VS Code + extensions
- [ ] VS Code (Stable) installed
- [ ] GitHub Copilot + Copilot Chat installed and enabled
- [ ] GitHub Pull Requests and Issues installed and signed in
- [ ] AI Toolkit installed (Activity Bar shows “AI Toolkit”)

### Workspace
- [ ] You opened this repository folder in VS Code
- [ ] You clicked **Trust** when Workspace Trust prompt appeared
- [ ] In Copilot Chat input, typing `/` shows prompt commands like:
  - `/draft-spec`, `/create-plan`, `/split-to-issues`, `/implement-issue`, `/eval-analyze`, `/feedback-to-issues`

### Runtime
- [ ] Python environment works
- [ ] `pytest -q` passes at least once before you start changing code

---

## Choose your model route

You can do the workshop with either:

### Route A: GitHub Models (recommended)
- You’ll use your GitHub credentials/token for model inference.
- GitHub’s quickstart shows `https://models.github.ai/inference/chat/completions` usage and headers.
  Reference: GitHub Models quickstart and API docs
  - https://docs.github.com/en/github-models/quickstart
  - https://docs.github.com/en/rest/models/inference?apiVersion=2022-11-28

### Route B: Microsoft Foundry (Azure AI inference endpoint)
- Single endpoint typically like: `https://<resource-name>.services.ai.azure.com/models`
- Reference: Foundry endpoints doc
  - https://learn.microsoft.com/en-us/azure/ai-foundry/foundry-models/concepts/endpoints?view=foundry-classic

### Route C: No model access (fallback)
- You can still complete the deterministic loop and still use AI Toolkit if you have *any* model available there (local/other catalog).
- If not, the facilitator can project-run the AI Toolkit evaluation while you follow along.

---

## The inner loop you will run twice

```text
Spec → Plan → Tasks (Issues) → Implement → Run/Evaluate → Feedback → (repeat)
```

- First loop: establish contract + baseline behavior
- Second loop: use AI Toolkit evaluation to drive improvement and re-evaluate

---

# Step-by-step

## 0. Verify the repo is healthy (deterministic gate is green)

### 0.1 Create and activate a virtual environment
From the repo root:

```bash
python -m venv .venv
# Windows:
# .venv\Scripts\activate
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

### 0.2 Run tests
```bash
pytest -q
```

✅ **Checkpoint 0:** Tests pass.

If tests fail:
- Ensure you’re using the repo root
- Ensure `.venv` is activated
- Re-run `pip install -e ".[dev]"`

---

## 1. Configure the provider (GitHub Models or Foundry)

> Do **not** commit `.env`. Use `.env.example` as the tracked template.

### 1.1 Create `.env`
Copy `.env.example` → `.env` and set the provider config.

#### Route A: GitHub Models
```env
TRIAGE_PROVIDER=github
TRIAGE_GITHUB_TOKEN=YOUR_TOKEN_HERE
TRIAGE_GITHUB_MODEL=openai/gpt-4.1
```

#### Route B: Foundry
```env
TRIAGE_PROVIDER=foundry
TRIAGE_FOUNDRY_ENDPOINT=https://<resource-name>.services.ai.azure.com/models
TRIAGE_FOUNDRY_API_KEY=YOUR_KEY_HERE
TRIAGE_FOUNDRY_MODEL=<deployment-name>
TRIAGE_FOUNDRY_API_VERSION=2024-05-01-preview
```

### 1.2 Smoke test the CLI
Run:

```bash
triage-assistant schema
triage-assistant triage --adapter auto --title "Crash on startup" --body "Steps: 1. Install 2. Launch" --pretty
```

✅ **Checkpoint 1:** You get **JSON** output and it matches the schema fields.

If the CLI fails:
- Try `--adapter dummy` to verify the CLI path itself works:
  ```bash
  triage-assistant triage --adapter dummy --title "Crash on startup" --body "Steps..." --pretty
  ```
- If GitHub Models fails with 401/403: check token scope (`models:read`) and that you’re not mixing endpoints/tokens.
- If Foundry fails: ensure the endpoint is the `/models` endpoint and `api-version` is set.

---

## 2. Create the Spec (Spec → committed artifact)

### 2.1 Generate Spec with Copilot prompt file
1. Open **Copilot Chat**
2. Run: `/draft-spec`
3. Ensure `docs/spec.md` is created/updated

### 2.2 Review Spec (human checklist)
Open `docs/spec.md` and ensure it includes:

- Problem statement (what triage decision we are helping with)
- Non-goals (what we explicitly won’t do)
- Output contract (JSON-only, schema-based)
- Acceptance criteria (testable)
- Evaluation plan (dataset + AI Toolkit)

### 2.3 Commit Spec
```bash
git add docs/spec.md
git commit -m "docs: define spec"
```

✅ **Checkpoint 2:** Spec is committed.

---

## 3. Create the Plan (Plan → committed artifact)

### 3.1 Generate Plan with Copilot prompt file
1. Copilot Chat: `/create-plan`
2. Confirm `docs/plan.md` updated

### 3.2 Review Plan quality
Check that each task has:
- A clear Definition of Done (DoD)
- Validation commands (ex: `pytest -q`, `triage-assistant ...`)
- Small enough scope (0.5–2 hours each)

### 3.3 Commit Plan
```bash
git add docs/plan.md
git commit -m "docs: define plan"
```

✅ **Checkpoint 3:** Plan is committed.

---

## 4. Convert Plan into Tasks (Issue drafts → GitHub Issues)

### 4.1 Generate issue drafts
1. Copilot Chat: `/split-to-issues`
2. Confirm `docs/issues-draft.md` is created/updated

### 4.2 Commit issue drafts
```bash
git add docs/issues-draft.md
git commit -m "docs: draft issues from plan"
```

✅ **Checkpoint 4:** Issue draft is committed.

### 4.3 Create 3 starter Issues
Create at least these three issues from `docs/issues-draft.md` (use templates under `.github/ISSUE_TEMPLATE/`):

1. **Deterministic improvement (code + tests)**
   - Example: “Security issues should be labeled `security` and prioritized `p0`”
2. **AI Toolkit baseline evaluation**
   - Example: “Create v1 prompt/agent and run baseline bulk run + evaluation”
3. **Evaluation-driven improvement**
   - Example: “Fix top-3 failure modes from v1 and re-evaluate (v2)”

✅ **Checkpoint 5:** Issues exist in GitHub and are visible in VS Code (GitHub panel).

---

## 5. Implement one Issue (Issue → branch → tests → PR)

### 5.1 Start working on the Issue (creates a branch)
In VS Code:
1. Open GitHub panel (Pull Requests and Issues)
2. Open your “Deterministic improvement” Issue
3. Click **Start working on issue** (or similar action)
4. Confirm you’re now on a new branch

### 5.2 Implement with Copilot prompt file
1. Open Copilot Chat
2. Run `/implement-issue`
3. Paste:
   - Issue title
   - DoD checklist
   - Validation commands
4. Review the edits before accepting

### 5.3 Run deterministic gate
```bash
pytest -q
```

✅ **Checkpoint 6:** Tests pass.

### 5.4 Commit and push (link to Issue)
```bash
git add -A
git commit -m "fix: <short summary> (Fixes #NN)"
git push -u origin HEAD
```

### 5.5 Open a PR (optional but recommended)
From VS Code GitHub panel: **Create Pull Request**.

✅ **Checkpoint 7:** PR exists and references `Fixes #NN`.

---

## 6. AI Toolkit: Build and evaluate v1 (Bulk run → Evaluation → Versioning)

This is the probabilistic gate loop.

### 6.1 Open AI Toolkit and Agent Builder
1. Open **AI Toolkit** from Activity Bar
2. Open **Model Catalog** and ensure you have at least one model available
3. Open **Agent Builder**
   Note: “Agent Builder” used to be called “Prompt Builder” in earlier versions.
   Reference: https://code.visualstudio.com/docs/intelligentapps/agentbuilder

### 6.2 Create v1 prompt/agent
In Agent Builder:
- System instructions should enforce:
  - “Return **JSON only**”
  - Allowed values for `type` and `priority`
  - “No markdown code fences”
- Input variables:
  - `${title}`
  - `${body}`

> Tip: Keep v1 intentionally minimal. We want failures to learn from.

### 6.3 Bulk run with the repo dataset
Bulk run is integrated into **Agent Builder → Evaluation tab** in current VS Code docs.
Reference: https://code.visualstudio.com/docs/intelligentapps/bulkrun

Steps:
1. Switch to **Evaluation** tab
2. Import `datasets/triage_dataset.csv`
3. Map variables to dataset columns:
   - `title` → `title`
   - `body` → `body`
4. Run:
   - “Run All” (or equivalent)

✅ **Checkpoint 8:** The dataset grid shows a column containing model outputs for each row.

### 6.4 Record manual ratings (fast feedback)
In the dataset view:
- Use 👍 / 👎 to mark outputs that are clearly correct/incorrect
- Capture at least 3 failure examples (copy/paste input + output)

### 6.5 Run an evaluation job
In Evaluation tab:
1. Click **New Evaluation**
2. Choose an evaluator:
   - Start with **Coherence** and/or **Relevance** (often works without strict ground truth mapping)
   - Optionally add **Similarity** or **F1 score** if you have a clear ground truth output column
3. Choose a judging model if required
4. Run evaluation

Reference: https://code.visualstudio.com/docs/intelligentapps/evaluation

✅ **Checkpoint 9:** You have at least one evaluation result recorded in AI Toolkit.

### 6.6 Save v1 as a version
- Click **Save as New Version**
- Name it `v1-baseline`

✅ **Checkpoint 10:** Version history includes `v1-baseline`.

---

## 7. Write the evaluation report v1 (turn tool output into repo memory)

### 7.1 Create an eval report file
Create:

- `reports/eval/<YYYYMMDD-HHMM>_v1.md`

Use the template:
- `docs/templates/eval-report.template.md`

Include:
- Model/provider (GitHub Models or Foundry)
- v1 prompt/agent version name
- Evaluation scores (from AI Toolkit)
- 3–5 failure cases (input → output → why wrong)
- Suggested fixes (as issue-sized items)

### 7.2 Use Copilot to help summarize the evaluation
Copilot Chat:
1. Run `/eval-analyze`
2. Paste the raw notes you captured (scores, failures)
3. Paste the generated summary into the report file

### 7.3 Commit the report
```bash
git add reports/eval
git commit -m "docs: add eval report v1"
```

✅ **Checkpoint 11:** v1 evaluation is committed.

---

## 8. Feedback → Issues (close the loop)

### 8.1 Turn v1 report into new Issues
Copilot Chat:
1. Run `/feedback-to-issues`
2. Provide the contents of your v1 report
3. Ask for 2–4 issues with:
   - DoD
   - Validation steps (including “re-run v2 evaluation”)

### 8.2 Create at least one evaluation-driven Issue
Create an issue (use Eval regression template if available).

✅ **Checkpoint 12:** You have at least one Issue whose origin is evaluation failures.

---

## 9. Improve and re-evaluate (v2)

### 9.1 Choose one improvement path
Pick **one**:

- **Prompt-only improvement** (fastest)
  - Tighten system instructions
  - Add examples / edge-case guidance
  - Improve JSON constraints
- **Code-assisted improvement**
  - Improve parsing/validation fallback
  - Improve deterministic adapter baseline logic
  - Add a regression test for a failure pattern

### 9.2 Save v2 in AI Toolkit
- Save as New Version: `v2-improved`

### 9.3 Bulk run + evaluation again
Repeat Step 6.3–6.5 for v2.

### 9.4 Compare v1 vs v2
In Evaluation tab:
- Click **Compare**
- Select `v1-baseline`

Note: Compare is easier in full screen mode per VS Code docs.
Reference: https://code.visualstudio.com/docs/intelligentapps/evaluation

✅ **Checkpoint 13:** You can point to a score change and at least one fixed failure case.

### 9.5 Write and commit v2 eval report
Create:
- `reports/eval/<YYYYMMDD-HHMM>_v2.md`

Include:
- v1 vs v2 deltas
- What improved
- What still fails
- Next issues (optional)

Commit:
```bash
git add reports/eval
git commit -m "docs: add eval report v2"
```

---

## 10. Retro: prove you understand the loop

Answer these as a group (or add to your notes):

1. What did **Spec** prevent you from doing (scope control)?
2. What did **Plan** prevent you from doing (random work)?
3. What was the smallest “unit of progress” you used (Issue DoD + validation)?
4. What belongs to the deterministic gate vs probabilistic gate?
5. How did evaluation become **action** (feedback → issues)?

---

## Cheat sheet

### Local commands
```bash
pytest -q
triage-assistant schema
triage-assistant triage --adapter auto --title "..." --body "..." --pretty
triage-assistant triage --adapter dummy --title "..." --body "..." --pretty
```

### Copilot Chat prompt files
- `/draft-spec`
- `/create-plan`
- `/split-to-issues`
- `/implement-issue`
- `/eval-analyze`
- `/feedback-to-issues`

---

## Further reading
- AI Toolkit overview: https://code.visualstudio.com/docs/intelligentapps/overview
- Agent Builder: https://code.visualstudio.com/docs/intelligentapps/agentbuilder
- Bulk run: https://code.visualstudio.com/docs/intelligentapps/bulkrun
- Evaluation + version comparison: https://code.visualstudio.com/docs/intelligentapps/evaluation
- GitHub Models quickstart: https://docs.github.com/en/github-models/quickstart
- GitHub Models inference REST API: https://docs.github.com/en/rest/models/inference?apiVersion=2022-11-28
- Foundry endpoints: https://learn.microsoft.com/en-us/azure/ai-foundry/foundry-models/concepts/endpoints?view=foundry-classic
- Foundry chat completions REST API: https://learn.microsoft.com/en-us/rest/api/aifoundry/model-inference/get-chat-completions/get-chat-completions?view=rest-aifoundry-model-inference-2024-05-01-preview
