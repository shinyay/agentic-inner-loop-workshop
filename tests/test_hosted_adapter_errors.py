from __future__ import annotations

import httpx
import pytest

from triage_assistant.adapters.chat_completions import ChatCompletionsError
from triage_assistant.adapters.github_models import GitHubModelsAdapter


def test_github_models_http_401_error_is_actionable_and_does_not_leak_token(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    token = "ghp_SUPER_SECRET_TOKEN"

    adapter = GitHubModelsAdapter(token=token)

    request = httpx.Request(
        "POST",
        "https://models.github.ai/inference/chat/completions",
    )
    response = httpx.Response(401, request=request, json={"error": "unauthorized"})

    class FakeClient:
        def __init__(self, *, timeout: float) -> None:  # noqa: ARG002
            pass

        def __enter__(self) -> FakeClient:
            return self

        def __exit__(self, exc_type, exc, tb) -> None:  # noqa: ANN001
            return None

        def post(self, url: str, *, headers: dict[str, str], json: dict) -> httpx.Response:  # noqa: ANN001
            return response

    monkeypatch.setattr("triage_assistant.adapters.github_models.httpx.Client", FakeClient)

    with pytest.raises(ChatCompletionsError) as excinfo:
        adapter.triage(title="Crash on startup", body="Steps: 1. Run 2. Crash")

    msg = str(excinfo.value)
    assert "GitHub Models" in msg
    assert "HTTP 401" in msg
    assert "TRIAGE_GITHUB_TOKEN" in msg

    # Ensure secrets are not echoed.
    assert token not in msg
    assert "Bearer" not in msg
