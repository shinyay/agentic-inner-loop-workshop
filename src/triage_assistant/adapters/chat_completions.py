from __future__ import annotations

import re
from typing import Any


class ChatCompletionsError(RuntimeError):
    """Raised when a chat-completions based adapter cannot produce a valid result."""


def extract_json_object(text: str) -> str:
    """Extract the first JSON object from a string.

    Many model providers wrap JSON in code fences or add commentary.
    This helper tries to recover the first ``{...}`` block.

    Raises:
        ChatCompletionsError: If extraction fails.
    """
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, flags=re.DOTALL | re.IGNORECASE)
    if fenced:
        return fenced.group(1)

    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ChatCompletionsError("Model response did not contain a JSON object.")
    return text[start : end + 1]


def get_chat_completion_content(data: dict[str, Any]) -> str:
    """Extract assistant text from a chat completions response.

    The repository intentionally keeps adapters lightweight and uses the
    common ``choices[0].message.content`` structure shared by several providers
    (GitHub Models, Azure AI Foundry, OpenAI-compatible endpoints).

    Raises:
        ChatCompletionsError: If the response structure is unexpected or empty.
    """
    try:
        choices = data["choices"]
        message = choices[0]["message"]
        content = message["content"]
    except Exception as e:  # pragma: no cover
        raise ChatCompletionsError(f"Unexpected response structure: {e}") from e

    # Some APIs may return content as a list of parts; attempt a best-effort
    # flattening into a single string.
    if isinstance(content, list):
        parts: list[str] = []
        for part in content:
            if isinstance(part, str):
                parts.append(part)
                continue
            if isinstance(part, dict):
                # Common shapes: {"type":"text","text":"..."}, {"text":"..."}
                text_part = part.get("text")
                if isinstance(text_part, str):
                    parts.append(text_part)
        content = "\n".join(p for p in parts if p.strip())

    if not isinstance(content, str) or not content.strip():
        raise ChatCompletionsError("Provider returned empty content.")
    return content
