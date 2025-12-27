import json
import os
import subprocess
import sys
from pathlib import Path

from typer.testing import CliRunner

from triage_assistant.cli import app
from triage_assistant.schema import validate_output_json

runner = CliRunner()


def test_cli_triage_outputs_valid_json() -> None:
    result = runner.invoke(
        app,
        [
            "triage",
            "--title",
            "Crash when saving file",
            "--body",
            "Steps to reproduce:\n1. Open\n2. Save\nVersion: 1.0",
            "--adapter",
            "dummy",
        ],
    )
    assert result.exit_code == 0, result.stdout
    validate_output_json(result.stdout.strip())


def test_cli_triage_stdout_is_json_object_only() -> None:
    """The triage command must emit a single JSON object to stdout (no logs)."""

    result = runner.invoke(
        app,
        [
            "triage",
            "--title",
            "Crash when saving file",
            "--body",
            "Steps to reproduce:\n1. Open\n2. Save\nVersion: 1.0",
            "--adapter",
            "dummy",
        ],
    )
    assert result.exit_code == 0, result.stdout

    # Strict-ish contract: parse stdout as JSON and ensure it is an object.
    parsed = json.loads(result.stdout)
    assert isinstance(parsed, dict)


def test_cli_schema_outputs_json_schema() -> None:
    result = runner.invoke(app, ["schema"])
    assert result.exit_code == 0
    data = json.loads(result.stdout)
    assert data.get("type") == "object"


def _blank_env() -> dict[str, str]:
    # Ensure tests do not depend on the caller's environment.
    return {
        "TRIAGE_PROVIDER": "",
        "TRIAGE_GITHUB_TOKEN": "",
        "GITHUB_TOKEN": "",
        "TRIAGE_FOUNDRY_ENDPOINT": "",
        "TRIAGE_FOUNDRY_API_KEY": "",
        "AZURE_INFERENCE_CREDENTIAL": "",
        "TRIAGE_FOUNDRY_MODEL": "",
        "TRIAGE_OPENAI_BASE_URL": "",
        "TRIAGE_OPENAI_API_KEY": "",
        "TRIAGE_OPENAI_MODEL": "",
    }


def test_cli_doctor_defaults_to_dummy_when_no_env() -> None:
    result = runner.invoke(app, ["doctor"], env=_blank_env())
    assert result.exit_code == 0
    assert "Selected adapter: dummy" in result.stdout
    assert "GitHub Models: missing TRIAGE_GITHUB_TOKEN (or GITHUB_TOKEN)" in result.stdout
    assert "Foundry: missing TRIAGE_FOUNDRY_ENDPOINT" in result.stdout
    assert "OpenAI-compatible: missing TRIAGE_OPENAI_BASE_URL" in result.stdout


def test_cli_doctor_provider_forces_selection_even_if_missing() -> None:
    env = _blank_env() | {"TRIAGE_PROVIDER": "github"}
    result = runner.invoke(app, ["doctor"], env=env)
    assert result.exit_code == 0
    assert "Selected adapter: github (TRIAGE_PROVIDER=github)" in result.stdout
    assert "GitHub Models: missing TRIAGE_GITHUB_TOKEN (or GITHUB_TOKEN)" in result.stdout


def test_cli_doctor_selects_github_when_token_present() -> None:
    env = _blank_env() | {"TRIAGE_GITHUB_TOKEN": "not-a-real-token"}
    result = runner.invoke(app, ["doctor"], env=env)
    assert result.exit_code == 0
    assert "Selected adapter: github" in result.stdout
    assert "GitHub Models: OK" in result.stdout


def _run_cli_subprocess(
    args: list[str],
    *,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    """Run the Typer app in a subprocess so stdout/stderr are captured separately."""

    code = (
        "import sys; "
        "from triage_assistant.cli import app; "
        "sys.argv = ['triage-assistant'] + sys.argv[1:]; "
        "app()"
    )

    proc_env = os.environ.copy()
    if env is not None:
        proc_env.update(env)

    return subprocess.run(
        [sys.executable, "-c", code, *args],
        env=proc_env,
        text=True,
        capture_output=True,
        check=False,
    )


def test_cli_triage_success_stdout_only_subprocess() -> None:
    """Enforce the strict contract: JSON on stdout, nothing on stderr."""

    proc = _run_cli_subprocess(
        [
            "triage",
            "--title",
            "Crash when saving file",
            "--body",
            "Steps to reproduce:\n1. Open\n2. Save\nVersion: 1.0",
            "--adapter",
            "dummy",
        ],
        env=_blank_env(),
    )

    assert proc.returncode == 0
    assert proc.stderr.strip() == ""
    validate_output_json(proc.stdout.strip())


def test_cli_triage_missing_env_var_error_goes_to_stderr_only_subprocess() -> None:
    """Configuration errors must not pollute stdout (JSON contract)."""

    proc = _run_cli_subprocess(
        [
            "triage",
            "--title",
            "Crash on startup",
            "--body",
            "Steps: 1. Install 2. Launch",
            "--adapter",
            "github",
        ],
        env=_blank_env(),
    )

    assert proc.returncode != 0
    assert proc.stdout.strip() == ""
    assert "Missing environment variable" in proc.stderr
    assert "TRIAGE_GITHUB_TOKEN" in proc.stderr


def test_cli_triage_body_file_read_error_goes_to_stderr_only_subprocess(
    tmp_path: Path,
) -> None:
    missing = tmp_path / "does_not_exist.txt"
    proc = _run_cli_subprocess(
        [
            "triage",
            "--title",
            "Crash on startup",
            "--body-file",
            str(missing),
            "--adapter",
            "dummy",
        ],
        env=_blank_env(),
    )

    assert proc.returncode != 0
    assert proc.stdout.strip() == ""
    assert "Failed to read body file" in proc.stderr


def test_cli_eval_report_contains_key_headings(tmp_path: Path) -> None:
    dataset = Path(__file__).resolve().parents[1] / "datasets" / "triage_dataset.csv"
    report_path = tmp_path / "eval_report.md"

    result = runner.invoke(
        app,
        [
            "eval",
            "--adapter",
            "dummy",
            "--dataset",
            str(dataset),
            "--report",
            str(report_path),
        ],
    )
    assert result.exit_code == 0, result.stdout
    assert report_path.exists()

    report = report_path.read_text(encoding="utf-8")
    assert "# Local Evaluation Report" in report
    assert "## Metrics" in report
    assert "## Top failure patterns" in report
    assert "## Failure examples (first 5)" in report
