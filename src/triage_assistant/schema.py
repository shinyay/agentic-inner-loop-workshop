from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator


class IssueType(str, Enum):
    """High-level classification of an issue."""

    bug = "bug"
    feature = "feature"
    docs = "docs"
    question = "question"


class Priority(str, Enum):
    """Triage priority.

    The workshop uses a simple three-tier system:
    - p0: urgent / blocking / severe
    - p1: important but not immediately blocking
    - p2: nice-to-have / backlog
    """

    p0 = "p0"
    p1 = "p1"
    p2 = "p2"


class TriageOutput(BaseModel):
    """The schema contract for triage results.

    This is the *single source of truth* for the triage output contract. Any adapter
    (rule-based or model-based) must return an instance of this model.

    Notes:
    - The CLI prints a JSON representation of this model.
    - Tests rely on this contract.
    """

    type: IssueType = Field(..., description="Primary classification.")
    priority: Priority = Field(..., description="Triage priority.")
    labels: list[str] = Field(
        default_factory=list,
        description="Recommended GitHub labels. Must be stable and human-readable.",
    )
    rationale: str = Field(
        ...,
        min_length=1,
        description="Short explanation for why the issue was classified this way.",
    )

    @field_validator("labels")
    @classmethod
    def normalize_labels(cls, labels: list[str]) -> list[str]:
        """Normalize labels for stability.

        - trims whitespace
        - removes empties
        - de-duplicates case-insensitively while preserving order
        """
        cleaned: list[str] = []
        for label in labels:
            if not isinstance(label, str):
                continue
            normalized = label.strip()
            if not normalized:
                continue
            cleaned.append(normalized)

        deduped: list[str] = []
        seen: set[str] = set()
        for label in cleaned:
            key = label.casefold()
            if key in seen:
                continue
            seen.add(key)
            deduped.append(label)

        return deduped

    def to_json(self, *, pretty: bool = False) -> str:
        """Serialize output as JSON text."""
        if pretty:
            return self.model_dump_json(indent=2, by_alias=True)
        return self.model_dump_json(by_alias=True)

    @staticmethod
    def json_schema() -> dict[str, Any]:
        """Return the JSON schema for the output contract."""
        return TriageOutput.model_json_schema()


def validate_output_json(text: str) -> TriageOutput:
    """Validate JSON text against the triage output schema."""
    return TriageOutput.model_validate_json(text)
