"""Triage adapters.

Adapters are responsible for producing a schema-valid :class:`~triage_assistant.schema.TriageOutput`.

The workshop encourages using:
- GitHub Models (quick to try with GitHub credentials)
- Microsoft Foundry (Azure AI inference endpoints)

A deterministic offline baseline (DummyAdapter) is included for tests and bootstrapping.
"""

from .chat_completions import ChatCompletionsError
from .dummy import DummyAdapter
from .foundry import FoundryModelInferenceAdapter
from .github_models import GitHubModelsAdapter
from .openai_compatible import OpenAICompatibleAdapter

__all__ = [
    "ChatCompletionsError",
    "DummyAdapter",
    "FoundryModelInferenceAdapter",
    "GitHubModelsAdapter",
    "OpenAICompatibleAdapter",
]
