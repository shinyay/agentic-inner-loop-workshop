import json

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


def test_cli_schema_outputs_json_schema() -> None:
    result = runner.invoke(app, ["schema"])
    assert result.exit_code == 0
    data = json.loads(result.stdout)
    assert data.get("type") == "object"
