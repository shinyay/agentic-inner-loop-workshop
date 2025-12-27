from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any

import httpx

from ..schema import TriageOutput
from .chat_completions import ChatCompletionsError, extract_json_object, get_chat_completion_content


@dataclass(frozen=True)
class GitHubModelsAdapter:
    """Adapter that calls the GitHub Models inference REST API.

    Environment variables supported by ``from_env()``:

    - TRIAGE_GITHUB_TOKEN (fallback: GITHUB_TOKEN)
    - TRIAGE_GITHUB_MODEL (default: openai/gpt-4.1)
    - TRIAGE_GITHUB_ORG (optional; attribute inference to an org)
    - TRIAGE_GITHUB_BASE_URL (default: https://models.github.ai)
    - TRIAGE_GITHUB_API_VERSION (default: 2022-11-28)

    Optional shared knobs:

    - TRIAGE_TEMPERATURE (float)
    - TRIAGE_SEED (int)
    - TRIAGE_JSON_MODE (true/false)

    Notes:
    - This adapter is intentionally thin: it validates the final JSON against
      ``TriageOutput`` so the CLI always emits schema-valid JSON.
    """

    token: str
    model: str = "openai/gpt-4.1"
    org: str | None = None
    base_url: str = "https://models.github.ai"
    api_version: str = "2022-11-28"
    timeout_s: float = 30.0
    temperature: float = 0.2
    json_mode: bool = True
    seed: int | None = None

    @staticmethod
    def from_env() -> GitHubModelsAdapter:
        token = (os.getenv("TRIAGE_GITHUB_TOKEN") or os.getenv("GITHUB_TOKEN") or "").strip()
        if not token:
            raise KeyError("TRIAGE_GITHUB_TOKEN")

        model = os.getenv("TRIAGE_GITHUB_MODEL", "openai/gpt-4.1").strip()
        org = os.getenv("TRIAGE_GITHUB_ORG", "").strip() or None
        base_url = os.getenv("TRIAGE_GITHUB_BASE_URL", "https://models.github.ai").strip()
        api_version = os.getenv("TRIAGE_GITHUB_API_VERSION", "2022-11-28").strip()

        temperature = _get_float_env("TRIAGE_TEMPERATURE", default=0.2)
        seed = _get_int_env("TRIAGE_SEED")
        json_mode = _get_bool_env("TRIAGE_JSON_MODE", default=True)

        return GitHubModelsAdapter(
            token=token,
            model=model,
            org=org,
            base_url=base_url,
            api_version=api_version,
            temperature=temperature,
            seed=seed,
            json_mode=json_mode,
        )

    def triage(self, *, title: str, body: str) -> TriageOutput:
        system_prompt = (
            "You are a GitHub issue triage assistant. "
            "Return ONLY a JSON object that matches the schema. "
            "Do not wrap the JSON in markdown. "
            "The JSON must include: type, priority, labels, rationale. "
            "type is one of: bug, feature, docs, question. "
            "priority is one of: p0, p1, p2. "
            "labels is an array of strings. "
            "rationale is a short string."
        )

        user_prompt = (
            "Triage the following GitHub issue.\n\n"
            f"Title: {title.strip()}\n\n"
            f"Body:\n{body.strip()}\n"
        )

        payload: dict[str, Any] = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": self.temperature,
        }

        if self.seed is not None:
            payload["seed"] = self.seed

        if self.json_mode:
            payload["response_format"] = {"type": "json_object"}

        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {self.token}",
            "X-GitHub-Api-Version": self.api_version,
            "Content-Type": "application/json",
        }

        try:
            with httpx.Client(timeout=self.timeout_s) as client:
                resp = client.post(self._build_url(), headers=headers, json=payload)
                resp.raise_for_status()
                data = resp.json()
        except httpx.HTTPStatusError as e:
            raise ChatCompletionsError(
                _format_github_models_http_status_error(
                    status_code=e.response.status_code,
                    reason=e.response.reason_phrase,
                    model=self.model,
                    org=self.org,
                )
            ) from e
        except httpx.RequestError as e:
            raise ChatCompletionsError(
                _format_github_models_request_error(
                    exc=e,
                    base_url=self.base_url,
                )
            ) from e
        except json.JSONDecodeError as e:
            raise ChatCompletionsError(
                "GitHub Models returned a non-JSON response. "
                "If this persists, verify TRIAGE_GITHUB_BASE_URL and TRIAGE_GITHUB_MODEL."
            ) from e

        content = get_chat_completion_content(data)
        json_text = extract_json_object(content)
        try:
            return TriageOutput.model_validate_json(json_text)
        except Exception as e:  # pragma: no cover
            raise ChatCompletionsError(f"GitHub Models output failed schema validation: {e}") from e

    def _build_url(self) -> str:
        base = self.base_url.rstrip("/")
        if self.org:
            return f"{base}/orgs/{self.org}/inference/chat/completions"
        return f"{base}/inference/chat/completions"


def _format_github_models_http_status_error(
    *,
    status_code: int,
    reason: str | None,
    model: str,
    org: str | None,
) -> str:
    # Keep this message actionable but secret-safe (no headers, no tokens, no response body).
    parts: list[str] = ["GitHub Models request failed", f"HTTP {status_code}"]
    if reason:
        parts[-1] = f"HTTP {status_code} ({reason})"

    hints: list[str] = []
    if status_code in {401, 403}:
        hints.append(
            "Check TRIAGE_GITHUB_TOKEN (or GITHUB_TOKEN). Ensure the token has access to GitHub Models."
        )
        if org:
            hints.append(
                "If TRIAGE_GITHUB_ORG is set, ensure the token can access that organization."
            )
    elif status_code == 404:
        hints.append(
            "Verify TRIAGE_GITHUB_BASE_URL (default: https://models.github.ai) and the inference path."
        )
        hints.append(f"Verify TRIAGE_GITHUB_MODEL is valid (current: {model!r}).")
        if org:
            hints.append(
                "If TRIAGE_GITHUB_ORG is set, verify the org slug is correct and the org supports inference."
            )
    elif status_code == 429:
        hints.append("You may be rate limited. Retry with backoff or reduce request rate.")
    elif 500 <= status_code <= 599:
        hints.append("Provider error. Retry later; if persistent, check provider status.")
    else:
        hints.append("Check TRIAGE_GITHUB_MODEL and request configuration.")

    hint_text = " ".join(hints)
    return f"{': '.join(parts)}. {hint_text}".strip()


def _format_github_models_request_error(*, exc: httpx.RequestError, base_url: str) -> str:
    # Connection / DNS / timeout errors.
    # Avoid embedding raw exception details that might include sensitive config.
    return (
        "GitHub Models request failed due to a network error. "
        f"Verify TRIAGE_GITHUB_BASE_URL ({base_url!r}) is reachable from your environment "
        "and check proxies/firewall settings."
    )


def _get_float_env(name: str, *, default: float) -> float:
    raw = os.getenv(name, "").strip()
    if not raw:
        return default
    try:
        return float(raw)
    except ValueError:
        return default


def _get_int_env(name: str) -> int | None:
    raw = os.getenv(name, "").strip()
    if not raw:
        return None
    try:
        return int(raw)
    except ValueError:
        return None


def _get_bool_env(name: str, *, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}
