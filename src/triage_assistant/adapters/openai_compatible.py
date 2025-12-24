from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any

import httpx

from ..schema import TriageOutput
from .chat_completions import ChatCompletionsError, extract_json_object, get_chat_completion_content


class OpenAICompatibleError(ChatCompletionsError):
    """Raised when the OpenAI-compatible adapter cannot produce a valid result."""


@dataclass(frozen=True)
class OpenAICompatibleAdapter:
    """Adapter that calls an OpenAI-compatible Chat Completions API.

    This repository's workshop materials focus on GitHub Models and Microsoft Foundry.
    The OpenAI-compatible adapter remains available as a fallback for environments that
    already standardize on an OpenAI-style endpoint.

    Environment variables (supported by ``from_env()``):

    - TRIAGE_OPENAI_BASE_URL (example: https://api.openai.com)
    - TRIAGE_OPENAI_API_KEY
    - TRIAGE_OPENAI_MODEL (example: gpt-4o-mini)

    Notes:
    - Many providers are "OpenAI-compatible" but differ slightly.
    - This adapter validates output strictly against ``TriageOutput``.
    """

    base_url: str
    api_key: str
    model: str
    timeout_s: float = 30.0
    temperature: float = 0.2
    json_mode: bool = True

    @staticmethod
    def from_env() -> "OpenAICompatibleAdapter":
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

        content = get_chat_completion_content(data)
        json_text = extract_json_object(content)
        try:
            return TriageOutput.model_validate_json(json_text)
        except Exception as e:  # pragma: no cover
            raise OpenAICompatibleError(f"Model output failed schema validation: {e}") from e
