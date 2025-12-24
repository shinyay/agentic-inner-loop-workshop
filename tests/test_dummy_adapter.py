from triage_assistant.adapters.dummy import DummyAdapter
from triage_assistant.schema import IssueType, Priority


def test_bug_with_repro_steps_is_bug_p1_without_needs_repro() -> None:
    adapter = DummyAdapter()
    out = adapter.triage(
        title="Crash when saving file",
        body="Steps to reproduce:\n1. Open the app\n2. Click Save\nVersion: 1.2.3",
    )
    assert out.type == IssueType.bug
    assert out.priority == Priority.p1
    assert "bug" in out.labels
    assert "p1" in out.labels
    assert "needs-repro" not in out.labels
    assert "needs-env-info" not in out.labels


def test_bug_without_repro_gets_needs_repro_and_env_info() -> None:
    adapter = DummyAdapter()
    out = adapter.triage(
        title="App fails with KeyError",
        body="It fails with error: KeyError: 'x'.",
    )
    assert out.type == IssueType.bug
    assert out.priority == Priority.p1
    assert "needs-repro" in out.labels
    assert "needs-env-info" in out.labels


def test_docs_issue_is_docs_p2_and_can_be_good_first_issue() -> None:
    adapter = DummyAdapter()
    out = adapter.triage(
        title="README typo in installation section",
        body="There is a typo: 'instal' should be 'install'.",
    )
    assert out.type == IssueType.docs
    assert out.priority == Priority.p2
    assert "docs" in out.labels
    assert "good-first-issue" in out.labels


def test_question_issue_is_question_p2_and_can_need_info() -> None:
    adapter = DummyAdapter()
    out = adapter.triage(
        title="How do I configure the OpenAI adapter?",
        body="How do I set the environment variables?",
    )
    assert out.type == IssueType.question
    assert out.priority == Priority.p2
    assert "needs-info" in out.labels


def test_feature_request_is_feature_p2_and_enhancement() -> None:
    adapter = DummyAdapter()
    out = adapter.triage(
        title="Add export to PDF",
        body="It would be useful to export reports to PDF.",
    )
    assert out.type == IssueType.feature
    assert out.priority == Priority.p2
    assert "enhancement" in out.labels
