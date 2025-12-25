# 01 — Setup

## Goal

Get your VS Code workspace into a state where you can run the full loop:

- Copilot Chat (Ask/Edit/Agent/Plan)
- AI Toolkit (Agent Builder, Bulk Run, Evaluation)
- GitHub Issues (create issues, start work on issues)
- Python environment (run tests and CLI)

## Setup Options

You can set up this workshop in two ways:

- **Option A: Dev Container** (recommended) — Docker-based environment with Python pre-configured
- **Option B: Local Python** — Install Python and dependencies on your local machine

Choose the option that best fits your environment and preferences.

---

## Option A: Dev Container Setup

### 1. Open the repository

**Goal:** Get the workshop repository ready in VS Code.

**Steps:**

1. Clone the repository.
2. Open it in VS Code.
3. If prompted, mark the workspace as **Trusted**.

**Expected output:** The repository is open in VS Code and trusted.

### 2. Install Dev Containers extension

**Goal:** Enable VS Code to work with Dev Containers.

**Steps:**

Install the **Dev Containers** extension from the VS Code marketplace.

**Expected output:** The Dev Containers extension is installed and active.

### 3. Open in Dev Container

**Goal:** Launch the development environment in a Docker container.

**Steps:**

1. When prompted, click **Reopen in Container**
   - Or use Command Palette (`Ctrl/Cmd+Shift+P`): `Dev Containers: Reopen in Container`
2. Wait for VS Code to build the container (this may take a few minutes the first time)
3. Dependencies are installed automatically via `postCreateCommand`

**Expected output:** Container is built with Python 3.12, dependencies installed, and VS Code is connected to the containerized environment.

### 4. Switch Python version (optional)

**Goal:** Change the container to use Python 3.11 instead of Python 3.12.

**Steps:**

1. Open `.devcontainer/devcontainer.json`
2. Change `"service": "py312"` to `"service": "py311"`
3. Save the file
4. Open Command Palette and run: `Dev Containers: Rebuild Container`

**Expected output:** Container is rebuilt with Python 3.11.

### 5. Configure environment variables (optional)

**Goal:** Set up credentials for hosted model providers (GitHub Models, Microsoft Foundry).

**Steps:**

1. Copy `.env.example` to `.env` in the repository root
2. Edit `.env` with your credentials
3. Rebuild the container if already running

**Expected output:** Environment variables are available in the container for model provider configuration.

### 6. Verify prompt files are discoverable

**Goal:** Confirm that Copilot Chat can discover the workshop's custom prompts.

**Steps:**

1. Open Copilot Chat (Chat view).
2. Type `/` in the input box.

**Expected output:**

You should see prompts such as:
- `draft-spec`
- `create-plan`
- `split-to-issues`

If you do not see them, confirm they exist under `.github/prompts/` and that the workspace is trusted.

### 7. Run the baseline tests

**Goal:** Verify that the development environment is correctly configured by running the test suite.

**Steps:**

Open a terminal in VS Code:

```bash
pytest -q
```

**Expected output:** You should see passing tests.

### Outputs for this option

- Dev Container is running with Python 3.11 or 3.12
- VS Code extensions installed automatically
- Prompt files discoverable via `/`
- `pytest -q` passes

---

## Option B: Local Python Setup

### 1. Open the repository

1. Clone the repository.
2. Open it in VS Code.
3. If prompted, mark the workspace as **Trusted**.

### 2. Install / verify extensions

Recommended extensions are listed in `.vscode/extensions.json`.

Install:

- GitHub Copilot
- GitHub Copilot Chat
- AI Toolkit for VS Code
- GitHub Pull Requests and Issues
- Python + Pylance

### 3. Sign in

1. Open the Accounts menu (bottom left in VS Code).
2. Sign in to GitHub for:
   - GitHub Pull Requests and Issues
   - GitHub Copilot

If Copilot is disabled for the workspace, enable it.

### 4. Connect AI Toolkit to a model provider (optional)

AI Toolkit can run prompts/agents against hosted models.
For this workshop, you can choose either:

- **GitHub Models** (recommended for most participants)
- **Microsoft Foundry** (recommended for enterprise / Azure environments)

In VS Code:

1. Open **AI Toolkit**.
2. Open the **Model Catalog**.
3. When prompted, authorize / sign in for the provider you want to use.

If you skip this step, you can still complete the workshop using the offline `dummy` adapter.

### 5. Enable chat checkpoints

This repo recommends enabling chat checkpoints so you can "rewind" edits after big agent changes.

Check `.vscode/settings.json` includes:

- `chat.checkpoints.enabled: true`

Optional:
- `chat.checkpoints.showFileChanges: true`

### 6. Verify prompt files are discoverable

1. Open Copilot Chat (Chat view).
2. Type `/` in the input box.
3. You should see prompts such as:
   - `draft-spec`
   - `create-plan`
   - `split-to-issues`

If you do not see them, confirm they exist under `.github/prompts/` and that the workspace is trusted.

### 7. Create a Python environment

From a terminal in VS Code:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -e ".[dev]"
```

### 8. Run the baseline tests

**Goal:** Verify that the development environment is correctly configured by running the test suite.

**Steps:**

```bash
pytest -q
```

**Expected output:** You should see passing tests.

### Outputs for this option

- VS Code is ready (extensions installed, signed in)
- Prompt files are discoverable via `/`
- `pytest -q` passes

---

## Next Steps

Regardless of which setup option you chose, you're now ready to start the workshop!

Next: `02_spec.md`
