from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any

import httpx

from ..schema import TriageOutput
from .chat_completions import ChatCompletionsError, extract_json_object, get_chat_completion_content


@dataclass(frozen=True)
class FoundryModelInferenceAdapter:
    """Adapter that calls the Azure AI Model Inference API via a Microsoft Foundry endpoint.

    This adapter targets the **Azure AI inference endpoint** described in Microsoft Foundry
    documentation. The endpoint typically looks like:

        https://<resource-name>.services.ai.azure.com/models

    Environment variables supported by ``from_env()``:

    - TRIAGE_FOUNDRY_ENDPOINT (required)
    - TRIAGE_FOUNDRY_API_KEY (fallback: AZURE_INFERENCE_CREDENTIAL)
    - TRIAGE_FOUNDRY_MODEL (required; deployment name)
    - TRIAGE_FOUNDRY_API_VERSION (default: 2024-05-01-preview)

    Optional shared knobs:

    - TRIAGE_TEMPERATURE (float)
    - TRIAGE_SEED (int)
    - TRIAGE_JSON_MODE (true/false)

    Notes:
    - A "model" in requests usually refers to the **deployment name** in your Foundry resource.
    - This adapter validates the model output against ``TriageOutput``.
    """

    endpoint: str
    api_key: str
    model: str
    api_version: str = "2024-05-01-preview"
    timeout_s: float = 30.0
    temperature: float = 0.2
    json_mode: bool = True
    seed: int | None = None

    @staticmethod
    def from_env() -> FoundryModelInferenceAdapter:
        endpoint = os.getenv("TRIAGE_FOUNDRY_ENDPOINT", "").strip()
        if not endpoint:
            raise KeyError("TRIAGE_FOUNDRY_ENDPOINT")

        api_key = (
            os.getenv("TRIAGE_FOUNDRY_API_KEY") or os.getenv("AZURE_INFERENCE_CREDENTIAL") or ""
        ).strip()
        if not api_key:
            raise KeyError("TRIAGE_FOUNDRY_API_KEY")

        model = os.getenv("TRIAGE_FOUNDRY_MODEL", "").strip()
        if not model:
            raise KeyError("TRIAGE_FOUNDRY_MODEL")

        api_version = os.getenv("TRIAGE_FOUNDRY_API_VERSION", "2024-05-01-preview").strip()

        temperature = _get_float_env("TRIAGE_TEMPERATURE", default=0.2)
        seed = _get_int_env("TRIAGE_SEED")
        json_mode = _get_bool_env("TRIAGE_JSON_MODE", default=True)

        return FoundryModelInferenceAdapter(
            endpoint=endpoint,
            api_key=api_key,
            model=model,
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
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "model": self.model,
            "temperature": self.temperature,
        }

        if self.seed is not None:
            payload["seed"] = self.seed

        if self.json_mode:
            payload["response_format"] = {"type": "json_object"}

        headers = {
            "api-key": self.api_key,
            "Content-Type": "application/json",
        }

        url = self._build_url()
        params = {"api-version": self.api_version}

        try:
            with httpx.Client(timeout=self.timeout_s) as client:
                resp = client.post(url, headers=headers, params=params, json=payload)
                resp.raise_for_status()
                data = resp.json()
        except httpx.HTTPStatusError as e:
            raise ChatCompletionsError(
                _format_foundry_http_status_error(
                    status_code=e.response.status_code,
                    reason=e.response.reason_phrase,
                    endpoint=self.endpoint,
                    model=self.model,
                    api_version=self.api_version,
                )
            ) from e
        except httpx.RequestError as e:
            raise ChatCompletionsError(
                _format_foundry_request_error(exc=e, endpoint=self.endpoint)
            ) from e
        except json.JSONDecodeError as e:
            raise ChatCompletionsError(
                "Foundry returned a non-JSON response. "
                "Verify TRIAGE_FOUNDRY_ENDPOINT, TRIAGE_FOUNDRY_MODEL, and TRIAGE_FOUNDRY_API_VERSION."
            ) from e

        content = get_chat_completion_content(data)
        json_text = extract_json_object(content)
        try:
            return TriageOutput.model_validate_json(json_text)
        except Exception as e:  # pragma: no cover
            raise ChatCompletionsError(f"Foundry output failed schema validation: {e}") from e

    def _build_url(self) -> str:
        base = self.endpoint.rstrip("/")
        return f"{base}/chat/completions"


def _format_foundry_http_status_error(
    *,
    status_code: int,
    reason: str | None,
    endpoint: str,
    model: str,
    api_version: str,
) -> str:
    parts: list[str] = ["Foundry request failed", f"HTTP {status_code}"]
    if reason:
        parts[-1] = f"HTTP {status_code} ({reason})"

    hints: list[str] = []
    if status_code in {401, 403}:
        hints.append(
            "Check TRIAGE_FOUNDRY_API_KEY (or AZURE_INFERENCE_CREDENTIAL). Ensure the key has access to the endpoint."
        )
    elif status_code == 404:
        hints.append(
            "Verify TRIAGE_FOUNDRY_ENDPOINT points to your Azure AI inference endpoint (typically ...services.ai.azure.com/models)."
        )
        hints.append(
            f"Verify TRIAGE_FOUNDRY_MODEL is a valid deployment name (current: {model!r})."
        )
    elif status_code == 429:
        hints.append("You may be rate limited. Retry with backoff or reduce request rate.")
    elif 500 <= status_code <= 599:
        hints.append("Provider error. Retry later; if persistent, check service health.")
    else:
        hints.append("Check endpoint, model deployment name, and API version.")

    hints.append(f"Endpoint: {endpoint!r} | api-version: {api_version!r}")
    return f"{': '.join(parts)}. {' '.join(hints)}".strip()


def _format_foundry_request_error(*, exc: httpx.RequestError, endpoint: str) -> str:
    return (
        "Foundry request failed due to a network error. "
        f"Verify TRIAGE_FOUNDRY_ENDPOINT ({endpoint!r}) is reachable from your environment "
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
