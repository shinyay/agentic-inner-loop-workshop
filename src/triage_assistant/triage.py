from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Protocol

from .adapters.dummy import DummyAdapter
from .adapters.openai_compatible import OpenAICompatibleAdapter
from .schema import TriageOutput


class TriageAdapter(Protocol):
    """A triage adapter produces a schema-valid triage result."""

    def triage(self, *, title: str, body: str) -> TriageOutput:  # pragma: no cover
        raise NotImplementedError


@dataclass(frozen=True)
class TriageEngine:
    """A thin wrapper around a triage adapter.

    The intent is to make adapters swappable without changing call sites.
    """

    adapter: TriageAdapter

    def triage(self, *, title: str, body: str) -> TriageOutput:
        return self.adapter.triage(title=title, body=body)


def get_default_adapter() -> TriageAdapter:
    """Return the default adapter.

    For workshop purposes:
    - Use the OpenAI-compatible adapter if environment variables are present.
    - Otherwise fall back to the deterministic, offline DummyAdapter.
    """
    base_url = os.getenv("TRIAGE_OPENAI_BASE_URL", "").strip()
    api_key = os.getenv("TRIAGE_OPENAI_API_KEY", "").strip()
    model = os.getenv("TRIAGE_OPENAI_MODEL", "").strip()

    if base_url and api_key and model:
        return OpenAICompatibleAdapter(base_url=base_url, api_key=api_key, model=model)

    return DummyAdapter()


def triage_issue(*, title: str, body: str, adapter: TriageAdapter | None = None) -> TriageOutput:
    """Convenience function for callers that don't need an engine instance."""
    effective_adapter = adapter or get_default_adapter()
    return effective_adapter.triage(title=title, body=body)
