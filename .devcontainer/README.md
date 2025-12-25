# Dev Container Configuration

This directory contains the Dev Container configuration for the Agentic Inner Loop Workshop.

## User + environment policy (important)

This Dev Container is intentionally configured to **avoid running as root**.

- Default user inside the container is `vscode`
- Workspace is mounted at `/workspace`
- A workspace virtualenv is created at `/workspace/.venv`
- Dependencies are installed into that venv via `pip install -e ".[dev]"`

This prevents `.venv` and other workspace artifacts from being owned by `root`.

## Environment Variables

**Goal:** Configure environment variables for hosted model providers (GitHub Models, Microsoft Foundry).

**Steps:**

The `.env` file is optional. If you need to configure hosted model providers:

1. Copy `.env.example` to `.env` in the repository root
2. Edit `.env` with your credentials (tokens, endpoints, etc.)
	- If you just want an offline local experience, set `TRIAGE_PROVIDER=dummy`.
3. Rebuild the container

Docker Compose automatically loads `.env` if it exists in the parent directory.

**Expected output:** Environment variables are available in the container for model provider configuration.

## Dependencies

Dependencies are installed via `postCreateCommand` into `/workspace/.venv`.

This happens automatically when the container is created or rebuilt.

## Quick verification (README-style)

Run these commands in the container terminal:

1. Confirm default user:
	- `whoami` → `vscode`

2. Confirm workspace + venv ownership:
	- `ls -ld /workspace /workspace/.venv` → owner should be `vscode`

3. Confirm Python interpreter:
	- `python -c "import sys; print(sys.executable)"` → should point to `/workspace/.venv/bin/python`

4. Run tests:
	- `. .venv/bin/activate && pytest -q`

## Notes

Legacy files (`compose.yaml`, `Dockerfile.py311`, `Dockerfile.py312`) may remain in this directory from earlier iterations,
but the current setup is driven by `.devcontainer/devcontainer.json` and the Dev Containers base image.
