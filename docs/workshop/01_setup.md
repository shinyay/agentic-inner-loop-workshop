# 01 — Setup

## Goal

Get your VS Code workspace into a state where you can run the full loop:

- Copilot Chat (Ask/Edit/Agent/Plan)
- AI Toolkit (Agent Builder, Bulk Run, Evaluation)
- GitHub Issues (create issues, start work on issues)
- Python environment (run tests and CLI)

## 1. Open the repository

1. Clone the repository.
2. Open it in VS Code.
3. If prompted, mark the workspace as **Trusted**.

## 2. Install / verify extensions

Recommended extensions are listed in `.vscode/extensions.json`.

Install:

- GitHub Copilot
- GitHub Copilot Chat
- AI Toolkit for VS Code
- GitHub Pull Requests and Issues
- Python + Pylance

## 3. Sign in

1. Open the Accounts menu (bottom left in VS Code).
2. Sign in to GitHub for:
   - GitHub Pull Requests and Issues
   - GitHub Copilot

If Copilot is disabled for the workspace, enable it.

## 4. Enable chat checkpoints

This repo recommends enabling chat checkpoints so you can “rewind” edits after big agent changes.

Check `.vscode/settings.json` includes:

- `chat.checkpoints.enabled: true`

Optional:
- `chat.checkpoints.showFileChanges: true`

## 5. Verify prompt files are discoverable

1. Open Copilot Chat (Chat view).
2. Type `/` in the input box.
3. You should see prompts such as:
   - `draft-spec`
   - `create-plan`
   - `split-to-issues`

If you do not see them, confirm they exist under `.github/prompts/` and that the workspace is trusted.

## 6. Create a Python environment

From a terminal in VS Code:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -e ".[dev]"
```

## 7. Run the baseline tests

```bash
pytest -q
```

You should see passing tests.

## Outputs for this module

- VS Code is ready (extensions installed, signed in)
- Prompt files are discoverable via `/`
- `pytest -q` passes

Next: `02_spec.md`
