#!/usr/bin/env bash
set -euo pipefail

# Dev Container post-create hook.
#
# Goal: make repo-local `.env` variables available to:
# - VS Code tasks (often non-interactive shells)
# - interactive terminals
# - fish users (optional)

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# 1) Interactive bash terminals: source the same env loader from ~/.bashrc
BASHRC="${HOME}/.bashrc"
SNIPPET_MARKER="# triage-assistant: auto-load repo-local .env"

if [[ -f "${BASHRC}" ]] && ! grep -qF "${SNIPPET_MARKER}" "${BASHRC}"; then
  {
    printf "\n%s\n" "${SNIPPET_MARKER}"
    printf '%s\n' 'if [ -f /workspace/.devcontainer/bash_env.sh ]; then . /workspace/.devcontainer/bash_env.sh; fi'
  } >>"${BASHRC}"
fi

# 2) fish terminals (if fish is installed / used): parse simple KEY=VALUE assignments from .env
mkdir -p "${HOME}/.config/fish/conf.d"
cat >"${HOME}/.config/fish/conf.d/triage-assistant-env.fish" <<'FISH'
# triage-assistant: auto-load repo-local .env (Dev Container)
#
# fish cannot `source` bash-style KEY=VALUE files directly, so we parse simple assignments.
# Supported:
# - comments (# ...)
# - blank lines
# - NAME=value (best-effort unquoting of single/double quoted values)

set -l env_file /workspace/.env
if test -f $env_file
  for line in (string split "\n" -- (cat $env_file))
    set -l trimmed (string trim -- $line)
    if test -z "$trimmed"
      continue
    end
    if string match -qr '^#' -- $trimmed
      continue
    end
    if not string match -qr '^[A-Za-z_][A-Za-z0-9_]*=' -- $trimmed
      continue
    end

    set -l parts (string split -m1 '=' -- $trimmed)
    set -l key $parts[1]
    set -l val (string trim -- $parts[2])

    # Best-effort unquote
    if string match -qr '^".*"$' -- $val
      set val (string sub -s 2 -l (math (string length -- $val) - 2) -- $val)
    else if string match -qr "^'.*'$" -- $val
      set val (string sub -s 2 -l (math (string length -- $val) - 2) -- $val)
    end

    if test -n "$key"
      set -gx $key $val
    end
  end
end
FISH

echo "triage-assistant: .env auto-load hooks installed (bash + fish)."
