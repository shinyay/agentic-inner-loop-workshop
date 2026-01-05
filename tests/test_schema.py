import json

from triage_assistant.schema import IssueType, Priority, TriageOutput, validate_output_json


def test_labels_normalization_dedup_and_trim() -> None:
    out = TriageOutput(
        type=IssueType.bug,
        priority=Priority.p1,
        labels=[" bug ", "BUG", "", "needs-repro", "Needs-Repro"],
        rationale="Because.",
    )
    assert out.labels == ["bug", "needs-repro"]


def test_labels_normalization_lowercases_first_occurrence() -> None:
    out = TriageOutput(
        type=IssueType.bug,
        priority=Priority.p1,
        labels=["Needs-Repro", "needs-repro", "P1", "bug"],
        rationale="Because.",
    )
    assert out.labels == ["needs-repro", "p1", "bug"]


def test_to_json_roundtrip() -> None:
    out = TriageOutput(
        type=IssueType.feature,
        priority=Priority.p2,
        labels=["feature", "p2"],
        rationale="A new capability request.",
    )
    text = out.to_json(pretty=False)
    parsed = validate_output_json(text)
    assert parsed == out


def test_json_schema_contains_required_fields() -> None:
    schema = TriageOutput.json_schema()
    schema_json = json.dumps(schema)
    assert "type" in schema_json
    assert "priority" in schema_json
    assert "labels" in schema_json
    assert "rationale" in schema_json
