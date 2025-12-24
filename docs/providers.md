# Model Providers

This workshop repository is designed to run in two modes:

1. **Offline mode (default)** — Uses the deterministic `DummyAdapter`.
2. **Hosted-model mode** — Uses a real model through either **GitHub Models** or **Microsoft Foundry**.

The recommended path for the workshop is:

- Use `DummyAdapter` to bootstrap deterministic behavior and tests.
- Use AI Toolkit for VS Code to iterate on prompts/agents.
- Optionally, use a hosted provider from the CLI to smoke-test the end-to-end contract.

---

## How adapter selection works

You can select a provider in two ways:

- CLI flag: `triage-assistant triage --adapter <name>`
- Environment variable: `TRIAGE_PROVIDER=<name>` (applies to `--adapter auto`)

### Supported adapter names

- `dummy` — offline deterministic baseline
- `github` / `github-models` — GitHub Models inference API
- `foundry` — Microsoft Foundry (Azure AI inference endpoint)
- `openai` — OpenAI-compatible chat completions (fallback)
- `auto` — choose automatically based on available credentials

### Auto resolution order

If `TRIAGE_PROVIDER` is not set, `auto` chooses the first matching provider:

1. GitHub Models (token present)
2. Foundry (endpoint + credential + model present)
3. OpenAI-compatible (base URL + key + model present)
4. Dummy

---

## Option A: GitHub Models

GitHub Models provides a hosted inference endpoint and a model catalog. This is usually the
fastest way to get started for workshop participants because it uses a GitHub token.

### Required environment variables

- `TRIAGE_GITHUB_TOKEN` (or `GITHUB_TOKEN`)

### Optional environment variables

- `TRIAGE_GITHUB_MODEL` — Model ID in `{publisher}/{model_name}` form.
  - Default: `openai/gpt-4.1`
- `TRIAGE_GITHUB_ORG` — Attribute inference to an organization (`orgs/{org}/...` endpoint).
- `TRIAGE_GITHUB_BASE_URL` — Default: `https://models.github.ai`
- `TRIAGE_GITHUB_API_VERSION` — Default: `2022-11-28`

Shared optional knobs:

- `TRIAGE_TEMPERATURE` — Float (default: `0.2`)
- `TRIAGE_SEED` — Int (optional)
- `TRIAGE_JSON_MODE` — `true|false` (default: `true`)

### Example

```bash
export TRIAGE_PROVIDER=github
export TRIAGE_GITHUB_TOKEN="..."
export TRIAGE_GITHUB_MODEL="openai/gpt-4.1"  # optional

triage-assistant triage \
  --adapter auto \
  --title "Crash on startup" \
  --body "Steps to reproduce: ..." \
  --pretty
```

---

## Option B: Microsoft Foundry

Microsoft Foundry lets you deploy models and access them through an Azure AI inference endpoint.
In requests, the `model` value typically refers to the **deployment name**.

### Required environment variables

- `TRIAGE_FOUNDRY_ENDPOINT`
  - Example: `https://<resource-name>.services.ai.azure.com/models`
- `TRIAGE_FOUNDRY_MODEL`
  - Example: `mistral-large` (deployment name)
- Credential:
  - `TRIAGE_FOUNDRY_API_KEY` **or** `AZURE_INFERENCE_CREDENTIAL`

### Optional environment variables

- `TRIAGE_FOUNDRY_API_VERSION` — Default: `2024-05-01-preview`

Shared optional knobs:

- `TRIAGE_TEMPERATURE` — Float (default: `0.2`)
- `TRIAGE_SEED` — Int (optional)
- `TRIAGE_JSON_MODE` — `true|false` (default: `true`)

### Example

```bash
export TRIAGE_PROVIDER=foundry
export TRIAGE_FOUNDRY_ENDPOINT="https://<resource-name>.services.ai.azure.com/models"
export TRIAGE_FOUNDRY_API_KEY="..."  # or AZURE_INFERENCE_CREDENTIAL
export TRIAGE_FOUNDRY_MODEL="<deployment-name>"

triage-assistant triage \
  --adapter auto \
  --title "Crash on startup" \
  --body "Steps to reproduce: ..." \
  --pretty
```

---

## Notes for AI Toolkit users

AI Toolkit for VS Code can run prompts/agents against hosted models independently of this CLI.
Use the dataset in `datasets/triage_dataset.csv` for bulk runs and evaluations, and record results
under `reports/eval/`.

The CLI adapters exist for two reasons:

1. Provide a deterministic offline baseline (`dummy`).
2. Smoke-test that a hosted model can produce JSON that validates against `src/triage_assistant/schema.py`.
