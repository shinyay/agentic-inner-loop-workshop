#!/usr/bin/env bash
# shellcheck disable=SC1090

# Auto-load repo-local `.env` into the current shell environment.
#
# - Non-interactive bash reads the file pointed to by $BASH_ENV.
# - Interactive shells can source this from ~/.bashrc.
#
# This script is safe to source even when `.env` is missing.

_triage_repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
_triage_env_file="${_triage_repo_root}/.env"

if [[ -f "${_triage_env_file}" ]]; then
  # Export all variables defined in the file.
  set -a
  . "${_triage_env_file}"
  set +a
fi

unset _triage_repo_root _triage_env_file
