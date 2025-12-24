from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from .adapters.dummy import DummyAdapter
from .adapters.openai_compatible import OpenAICompatibleAdapter, OpenAICompatibleError
from .schema import TriageOutput
from .triage import get_default_adapter

app = typer.Typer(add_completion=False, no_args_is_help=True)
console = Console(stderr=True)


def _read_body(body: str | None, body_file: Path | None) -> str:
    if body_file is not None:
        try:
            return body_file.read_text(encoding="utf-8")
        except OSError as e:
            raise typer.BadParameter(f"Failed to read body file: {e}") from e
    return body or ""


def _resolve_adapter(adapter_name: str | None):
    if adapter_name is None or adapter_name == "auto":
        return get_default_adapter()
    if adapter_name == "dummy":
        return DummyAdapter()
    if adapter_name == "openai":
        try:
            return OpenAICompatibleAdapter.from_env()
        except KeyError as e:
            missing = str(e).strip("'")
            raise typer.BadParameter(
                f"Missing environment variable for OpenAI adapter: {missing}"
            ) from e
    raise typer.BadParameter(f"Unknown adapter: {adapter_name}")


@app.command()
def triage(
    title: Annotated[str, typer.Option(help="GitHub Issue title.")],
    body: Annotated[str | None, typer.Option(help="GitHub Issue body text.")] = None,
    body_file: Annotated[
        Path | None, typer.Option(help="Read issue body from a UTF-8 text file.")
    ] = None,
    adapter: Annotated[
        str,
        typer.Option(
            help="Which adapter to use: auto (default), dummy (offline baseline), openai (OpenAI-compatible)."
        ),
    ] = "auto",
    pretty: Annotated[bool, typer.Option(help="Pretty-print JSON output.")] = False,
) -> None:
    """Triage an issue and print schema-valid JSON to stdout."""
    body_text = _read_body(body, body_file)
    triage_adapter = _resolve_adapter(adapter)

    try:
        result = triage_adapter.triage(title=title, body=body_text)
    except OpenAICompatibleError as e:
        console.print(f"[red]OpenAI adapter error:[/red] {e}")
        raise typer.Exit(code=2) from e
    except Exception as e:
        console.print(f"[red]Unexpected error:[/red] {e}")
        raise typer.Exit(code=1) from e

    typer.echo(result.to_json(pretty=pretty))


@app.command()
def schema(pretty: Annotated[bool, typer.Option(help="Pretty-print JSON schema.")] = True) -> None:
    """Print the JSON schema for the triage output contract."""
    schema_dict = TriageOutput.json_schema()
    if pretty:
        typer.echo(json.dumps(schema_dict, indent=2, ensure_ascii=False))
    else:
        typer.echo(json.dumps(schema_dict, ensure_ascii=False))


@app.command()
def eval(
    dataset: Annotated[Path, typer.Option(help="Path to the CSV dataset.")] = Path(
        "datasets/triage_dataset.csv"
    ),
    adapter: Annotated[
        str,
        typer.Option(help="Adapter to use for evaluation: auto, dummy, openai."),
    ] = "dummy",
    report: Annotated[
        Path | None,
        typer.Option(help="Write a Markdown report to this path. If omitted, print summary only."),
    ] = None,
) -> None:
    """Run a simple local evaluation against the dataset.

    This is NOT meant to replace AI Toolkit evaluation. It exists so you can:
    - sanity-check changes locally
    - keep a deterministic baseline
    """
    if not dataset.exists():
        raise typer.BadParameter(f"Dataset not found: {dataset}")

    triage_adapter = _resolve_adapter(adapter)

    rows = _load_dataset(dataset)
    results = []
    for row in rows:
        pred = triage_adapter.triage(title=row["title"], body=row["body"])
        results.append((row, pred))

    metrics = _compute_metrics(results)

    summary = (
        f"type_accuracy={metrics['type_accuracy']:.3f}, "
        f"priority_accuracy={metrics['priority_accuracy']:.3f}, "
        f"label_f1={metrics['label_f1']:.3f} "
        f"(n={metrics['n']})"
    )
    typer.echo(summary)

    if report is not None:
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_text(
            _render_report(dataset=dataset, metrics=metrics, results=results), encoding="utf-8"
        )
        typer.echo(f"Wrote report: {report}")


def _load_dataset(path: Path) -> list[dict[str, str]]:
    import csv

    rows: list[dict[str, str]] = []
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Expect at least: title, body, expected_type, expected_priority, expected_labels
            rows.append({k: (v or "").strip() for k, v in row.items()})
    return rows


def _compute_metrics(results: list[tuple[dict[str, str], TriageOutput]]) -> dict[str, float]:
    def parse_labels(s: str) -> set[str]:
        s = s.strip()
        if not s:
            return set()
        try:
            raw = json.loads(s)
            if isinstance(raw, list):
                return {str(x).strip() for x in raw if str(x).strip()}
        except Exception:
            # tolerate "a,b,c" format
            return {x.strip() for x in s.split(",") if x.strip()}
        return set()

    n = len(results)
    if n == 0:
        return {"n": 0.0, "type_accuracy": 0.0, "priority_accuracy": 0.0, "label_f1": 0.0}

    type_correct = 0
    priority_correct = 0

    tp = 0
    fp = 0
    fn = 0

    for row, pred in results:
        if pred.type.value == row.get("expected_type", ""):
            type_correct += 1
        if pred.priority.value == row.get("expected_priority", ""):
            priority_correct += 1

        expected = parse_labels(row.get("expected_labels", ""))
        predicted = {x.strip() for x in pred.labels if x.strip()}

        tp += len(expected & predicted)
        fp += len(predicted - expected)
        fn += len(expected - predicted)

    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0

    return {
        "n": float(n),
        "type_accuracy": type_correct / n,
        "priority_accuracy": priority_correct / n,
        "label_f1": f1,
    }


def _render_report(
    *,
    dataset: Path,
    metrics: dict[str, float],
    results: list[tuple[dict[str, str], TriageOutput]],
) -> str:
    lines: list[str] = []
    lines.append("# Local Evaluation Report")
    lines.append("")
    lines.append(f"- Dataset: `{dataset.as_posix()}`")
    lines.append(f"- Samples: {int(metrics['n'])}")
    lines.append("")
    lines.append("## Metrics")
    lines.append("")
    lines.append(f"- Type accuracy: {metrics['type_accuracy']:.3f}")
    lines.append(f"- Priority accuracy: {metrics['priority_accuracy']:.3f}")
    lines.append(f"- Label F1: {metrics['label_f1']:.3f}")
    lines.append("")
    lines.append("## Example failures (first 5)")
    lines.append("")
    count = 0
    for row, pred in results:
        exp_type = row.get("expected_type", "")
        exp_pri = row.get("expected_priority", "")
        if pred.type.value == exp_type and pred.priority.value == exp_pri:
            continue
        lines.append(f"### {row.get('id', '(no id)')}: {row.get('title', '').strip()}")
        lines.append("")
        lines.append(
            f"- Expected: type={exp_type}, priority={exp_pri}, labels={row.get('expected_labels', '')}"
        )
        lines.append(
            f"- Predicted: type={pred.type.value}, priority={pred.priority.value}, labels={pred.labels}"
        )
        lines.append(f"- Rationale: {pred.rationale}")
        lines.append("")
        count += 1
        if count >= 5:
            break
    if count == 0:
        lines.append("No failures found.")
        lines.append("")
    return "\n".join(lines)
