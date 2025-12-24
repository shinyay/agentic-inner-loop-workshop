"""Triage adapters.

Adapters are responsible for producing a schema-valid `TriageOutput`.
"""

from .dummy import DummyAdapter
from .openai_compatible import OpenAICompatibleAdapter

__all__ = ["DummyAdapter", "OpenAICompatibleAdapter"]
