from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from typing import Any

import httpx

from ..schema import TriageOutput


class OpenAICompatibleError(RuntimeError):
    """Raised when the OpenAI-compatible adapter cannot produce a valid result."""


def _extract_json_object(text: str) -> str:
    """Extract the first JSON object from a string.

    Many model providers wrap JSON in code fences or add commentary.
    This function tries to recover the first {...} block.

    Raises:
        OpenAICompatibleError: if extraction fails.
    """
    # Remove code fences if present.
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, flags=re.DOTALL | re.IGNORECASE)
    if fenced:
        return fenced.group(1)

    # Fallback: pick the first '{' ... last '}'.
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise OpenAICompatibleError("Model response did not contain a JSON object.")
    return text[start : end + 1]


@dataclass(frozen=True)
class OpenAICompatibleAdapter:
    """Adapter that calls an OpenAI-compatible Chat Completions API.

    This adapter is *optional* for the workshop. The repository defaults to the
    deterministic DummyAdapter unless the required environment variables are set.

    Environment variables (supported by `from_env()`):
    - TRIAGE_OPENAI_BASE_URL   (example: https://api.openai.com)
    - TRIAGE_OPENAI_API_KEY
    - TRIAGE_OPENAI_MODEL      (example: gpt-4o-mini)

    Notes:
    - Many providers are "OpenAI-compatible" but differ slightly.
    - This adapter aims to be defensive and validate output strictly.
    """

    base_url: str
    api_key: str
    model: str
    timeout_s: float = 30.0
    temperature: float = 0.2
    json_mode: bool = True

    @staticmethod
    def from_env() -> OpenAICompatibleAdapter:
        base_url = os.environ["TRIAGE_OPENAI_BASE_URL"].strip()
        api_key = os.environ["TRIAGE_OPENAI_API_KEY"].strip()
        model = os.environ["TRIAGE_OPENAI_MODEL"].strip()
        return OpenAICompatibleAdapter(base_url=base_url, api_key=api_key, model=model)

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

        # Some providers support json_mode via response_format. If unsupported, it is ignored.
        if self.json_mode:
            payload["response_format"] = {"type": "json_object"}

        headers = {"Authorization": f"Bearer {self.api_key}"}

        url = self.base_url.rstrip("/") + "/v1/chat/completions"

        try:
            with httpx.Client(timeout=self.timeout_s) as client:
                resp = client.post(url, headers=headers, json=payload)
                resp.raise_for_status()
                data = resp.json()
        except httpx.HTTPError as e:
            raise OpenAICompatibleError(f"HTTP error calling provider: {e}") from e
        except json.JSONDecodeError as e:
            raise OpenAICompatibleError(f"Provider returned non-JSON response: {e}") from e

        content = _get_chat_completion_content(data)
        json_text = _extract_json_object(content)
        try:
            return TriageOutput.model_validate_json(json_text)
        except Exception as e:  # pragma: no cover
            raise OpenAICompatibleError(f"Model output failed schema validation: {e}") from e


def _get_chat_completion_content(data: dict[str, Any]) -> str:
    """Extract the assistant message content from a chat completions response."""
    try:
        choices = data["choices"]
        message = choices[0]["message"]
        content = message["content"]
    except Exception as e:  # pragma: no cover
        raise OpenAICompatibleError(f"Unexpected response structure: {e}") from e

    if not isinstance(content, str) or not content.strip():
        raise OpenAICompatibleError("Provider returned empty content.")
    return content
