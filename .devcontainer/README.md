# Dev Container Configuration

This directory contains the Dev Container configuration for the Agentic Inner Loop Workshop.

## Services

Two Python versions are available:

- **py312** (default): Python 3.12
- **py311**: Python 3.11

## Switching Python Versions

To switch between Python versions:

1. Open the Command Palette (`Ctrl/Cmd+Shift+P`)
2. Run `Dev Containers: Rebuild Container`
3. Before rebuilding, edit `.devcontainer/devcontainer.json`
4. Change the `"service"` field from `"py312"` to `"py311"` (or vice versa)
5. Save and rebuild

## Environment Variables

The `.env` file is optional. If you need to configure hosted model providers:

1. Copy `.env.example` to `.env` in the repository root
2. Edit `.env` with your credentials (tokens, endpoints, etc.)
3. Rebuild the container

Docker Compose automatically loads `.env` if it exists in the parent directory.

## Dependencies

Dependencies are installed via `postCreateCommand` using direct pip installation to the system Python (no workspace .venv).

This happens automatically when the container is created or rebuilt.
