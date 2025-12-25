# Dev Container Configuration

This directory contains the Dev Container configuration for the Agentic Inner Loop Workshop.

## Services

Two Python versions are available:

- **py312** (default): Python 3.12
- **py311**: Python 3.11

## Switching Python Versions

**Goal:** Change the container to use a different Python version (3.11 or 3.12).

**Steps:**

1. Edit `.devcontainer/devcontainer.json`
2. Change the `"service"` field from `"py312"` to `"py311"` (or vice versa)
3. Save the file
4. Open the Command Palette (`Ctrl/Cmd+Shift+P`)
5. Run `Dev Containers: Rebuild Container`

**Expected output:** The container rebuilds with the selected Python version.

## Environment Variables

**Goal:** Configure environment variables for hosted model providers (GitHub Models, Microsoft Foundry).

**Steps:**

The `.env` file is optional. If you need to configure hosted model providers:

1. Copy `.env.example` to `.env` in the repository root
2. Edit `.env` with your credentials (tokens, endpoints, etc.)
3. Rebuild the container

Docker Compose automatically loads `.env` if it exists in the parent directory.

**Expected output:** Environment variables are available in the container for model provider configuration.

## Dependencies

Dependencies are installed via `postCreateCommand` using direct pip installation to the system Python (no workspace .venv).

This happens automatically when the container is created or rebuilt.
