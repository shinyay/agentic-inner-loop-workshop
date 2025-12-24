from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Protocol

from .adapters.dummy import DummyAdapter
from .adapters.foundry import FoundryModelInferenceAdapter
from .adapters.github_models import GitHubModelsAdapter
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

    The workshop is designed to work in both offline and hosted-model environments.

    Resolution order:

    1. If TRIAGE_PROVIDER is set, use it (explicit beats implicit).
    2. If GitHub Models credentials are present, use GitHub Models.
    3. If Microsoft Foundry credentials are present, use Foundry.
    4. If OpenAI-compatible configuration is present, use the OpenAI-compatible adapter.
    5. Otherwise, fall back to the deterministic DummyAdapter.

    Supported TRIAGE_PROVIDER values:
    - github | github-models
    - foundry
    - openai
    - dummy
    """

    provider = os.getenv("TRIAGE_PROVIDER", "").strip().lower()
    if provider:
        return _adapter_from_provider(provider)

    if _has_github_models_config():
        return GitHubModelsAdapter.from_env()

    if _has_foundry_config():
        return FoundryModelInferenceAdapter.from_env()

    if _has_openai_compatible_config():
        return OpenAICompatibleAdapter.from_env()

    return DummyAdapter()


def _adapter_from_provider(provider: str) -> TriageAdapter:
    normalized = provider.replace("_", "-")

    if normalized in {"github", "github-models"}:
        return GitHubModelsAdapter.from_env()

    if normalized in {"foundry", "azure-foundry", "ai-foundry"}:
        return FoundryModelInferenceAdapter.from_env()

    if normalized in {"openai", "openai-compatible"}:
        return OpenAICompatibleAdapter.from_env()

    if normalized in {"dummy", "offline"}:
        return DummyAdapter()

    raise ValueError(
        "Unsupported TRIAGE_PROVIDER. Use one of: github, foundry, openai, dummy. "
        f"Got: {provider!r}"
    )


def _has_github_models_config() -> bool:
    token = (os.getenv("TRIAGE_GITHUB_TOKEN") or os.getenv("GITHUB_TOKEN") or "").strip()
    return bool(token)


def _has_foundry_config() -> bool:
    endpoint = os.getenv("TRIAGE_FOUNDRY_ENDPOINT", "").strip()
    api_key = (
        os.getenv("TRIAGE_FOUNDRY_API_KEY") or os.getenv("AZURE_INFERENCE_CREDENTIAL") or ""
    ).strip()
    model = os.getenv("TRIAGE_FOUNDRY_MODEL", "").strip()
    return bool(endpoint and api_key and model)


def _has_openai_compatible_config() -> bool:
    base_url = os.getenv("TRIAGE_OPENAI_BASE_URL", "").strip()
    api_key = os.getenv("TRIAGE_OPENAI_API_KEY", "").strip()
    model = os.getenv("TRIAGE_OPENAI_MODEL", "").strip()
    return bool(base_url and api_key and model)


def triage_issue(*, title: str, body: str, adapter: TriageAdapter | None = None) -> TriageOutput:
    """Convenience function for callers that don't need an engine instance."""
    effective_adapter = adapter or get_default_adapter()
    return effective_adapter.triage(title=title, body=body)
