from __future__ import annotations

import re
from dataclasses import dataclass

from ..schema import IssueType, Priority, TriageOutput

_BUG_HINTS = [
    "bug",
    "crash",
    "crashes",
    "exception",
    "traceback",
    "stack trace",
    "segfault",
    "panic",
    "error",
    "fails",
    "failure",
    "broken",
    "doesn't work",
    "does not work",
    "regression",
]

_DOCS_HINTS = [
    "docs",
    "documentation",
    "readme",
    "typo",
    "spelling",
    "grammar",
    "example is wrong",
]

_QUESTION_HINTS = [
    "how do i",
    "how to",
    "is it possible",
    "can i",
    "question",
    "help",
]

_SEVERITY_HINTS_P0 = [
    "security",
    "vulnerability",
    "data loss",
    "lost data",
    "rce",
    "remote code execution",
    "crash on startup",
    "cannot start",
    "unusable",
    "blocks",
    "blocking",
    "urgent",
    "p0",
]

_REPRO_MARKERS = [
    "steps to reproduce",
    "reproduce",
    "repro",
    "minimal reproduction",
    "mre",
]


def _contains_any(text: str, needles: list[str]) -> bool:
    return any(n in text for n in needles)


def _has_repro(body_lower: str) -> bool:
    if _contains_any(body_lower, _REPRO_MARKERS):
        return True
    # A tiny heuristic: numbered steps are often reproduction steps.
    return bool(re.search(r"\n\s*\d+\.", body_lower))


@dataclass(frozen=True)
class DummyAdapter:
    """A deterministic, rule-based triage adapter.

    This adapter exists to provide:
    - an offline baseline (no model calls required)
    - stable behavior for tests and for workshop bootstrapping

    It is intentionally *simple* and therefore imperfect.
    """

    def triage(self, *, title: str, body: str) -> TriageOutput:
        title = title.strip()
        body = body.strip()

        combined_lower = f"{title}\n{body}".casefold()
        title_lower = title.casefold()
        body_lower = body.casefold()

        issue_type = self._classify_type(title_lower=title_lower, body_lower=body_lower)
        priority = self._classify_priority(issue_type=issue_type, combined_lower=combined_lower)

        labels = self._suggest_labels(
            issue_type=issue_type,
            priority=priority,
            title_lower=title_lower,
            body_lower=body_lower,
        )

        rationale = self._build_rationale(
            issue_type=issue_type,
            priority=priority,
            title=title,
            body=body,
        )

        return TriageOutput(type=issue_type, priority=priority, labels=labels, rationale=rationale)

    def _classify_type(self, *, title_lower: str, body_lower: str) -> IssueType:
        # Docs first: docs issues often include "README", "docs", etc.
        if _contains_any(title_lower, _DOCS_HINTS) or _contains_any(body_lower, _DOCS_HINTS):
            return IssueType.docs

        # Explicit questions: prefer "question" when the user is asking how/what.
        if _contains_any(title_lower, _QUESTION_HINTS) or _contains_any(
            body_lower, _QUESTION_HINTS
        ):
            # If the text also clearly signals a bug, treat it as a bug.
            if _contains_any(title_lower, _BUG_HINTS) or _contains_any(body_lower, _BUG_HINTS):
                return IssueType.bug
            return IssueType.question

        # Bug signals
        if _contains_any(title_lower, _BUG_HINTS) or _contains_any(body_lower, _BUG_HINTS):
            return IssueType.bug

        # Default
        return IssueType.feature

    def _classify_priority(self, *, issue_type: IssueType, combined_lower: str) -> Priority:
        if _contains_any(combined_lower, _SEVERITY_HINTS_P0):
            return Priority.p0

        if issue_type == IssueType.bug:
            return Priority.p1

        # Docs and questions are usually not urgent by default.
        return Priority.p2

    def _suggest_labels(
        self,
        *,
        issue_type: IssueType,
        priority: Priority,
        title_lower: str,
        body_lower: str,
    ) -> list[str]:
        labels: list[str] = []
        labels.append(issue_type.value)
        labels.append(priority.value)

        if issue_type == IssueType.bug:
            if not _has_repro(body_lower):
                labels.append("needs-repro")
            if "version" not in body_lower and "commit" not in body_lower:
                labels.append("needs-env-info")

        if issue_type == IssueType.question:
            if len(body_lower) < 120:
                labels.append("needs-info")

        if issue_type == IssueType.docs:
            if _contains_any(body_lower, ["typo", "spelling", "grammar"]):
                labels.append("good-first-issue")

        if issue_type == IssueType.feature:
            if (
                _contains_any(title_lower, ["support", "add", "implement"])
                and priority == Priority.p2
            ):
                labels.append("enhancement")

        return labels

    def _build_rationale(
        self,
        *,
        issue_type: IssueType,
        priority: Priority,
        title: str,
        body: str,
    ) -> str:
        # Keep it short and stable.
        parts: list[str] = []
        parts.append(f"Classified as '{issue_type.value}' based on the title/body wording.")
        if priority == Priority.p0:
            parts.append("Marked p0 due to severe/urgent keywords.")
        elif priority == Priority.p1:
            parts.append("Marked p1 because bug reports are typically high priority.")
        else:
            parts.append("Marked p2 as default for non-urgent items.")
        if issue_type == IssueType.bug and not _has_repro(body.casefold()):
            parts.append("No clear reproduction steps were detected.")
        return " ".join(parts)
