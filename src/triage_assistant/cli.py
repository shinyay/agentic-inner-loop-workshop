from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from .adapters.chat_completions import ChatCompletionsError
from .adapters.dummy import DummyAdapter
from .adapters.foundry import FoundryModelInferenceAdapter
from .adapters.github_models import GitHubModelsAdapter
from .adapters.openai_compatible import OpenAICompatibleAdapter
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
    """Resolve an adapter name into an adapter instance.

    Supported names:
    - auto: choose based on environment (see triage.get_default_adapter)
    - dummy: offline deterministic baseline
    - github: GitHub Models (models.github.ai)
    - foundry: Microsoft Foundry (Azure AI inference endpoint)
    - openai: OpenAI-compatible chat completions (fallback)
    """

    if adapter_name is None or adapter_name == "auto":
        return get_default_adapter()

    normalized = adapter_name.strip().lower().replace("_", "-")

    if normalized == "dummy":
        return DummyAdapter()

    if normalized in {"github", "github-models"}:
        try:
            return GitHubModelsAdapter.from_env()
        except KeyError as e:
            missing = str(e).strip("'")
            raise typer.BadParameter(
                f"Missing environment variable for GitHub Models adapter: {missing}"
            ) from e

    if normalized in {"foundry", "ai-foundry", "azure-foundry"}:
        try:
            return FoundryModelInferenceAdapter.from_env()
        except KeyError as e:
            missing = str(e).strip("'")
            raise typer.BadParameter(
                f"Missing environment variable for Foundry adapter: {missing}"
            ) from e

    if normalized in {"openai", "openai-compatible"}:
        try:
            return OpenAICompatibleAdapter.from_env()
        except KeyError as e:
            missing = str(e).strip("'")
            raise typer.BadParameter(
                f"Missing environment variable for OpenAI-compatible adapter: {missing}"
            ) from e

    raise typer.BadParameter(f"Unknown adapter: {adapter_name}")


def _is_set(name: str) -> bool:
    return bool((os.getenv(name) or "").strip())


def _missing_env_for_github_models() -> list[str]:
    # GitHub Models accepts TRIAGE_GITHUB_TOKEN or (fallback) GITHUB_TOKEN.
    if _is_set("TRIAGE_GITHUB_TOKEN") or _is_set("GITHUB_TOKEN"):
        return []
    return ["TRIAGE_GITHUB_TOKEN (or GITHUB_TOKEN)"]


def _missing_env_for_foundry() -> list[str]:
    missing: list[str] = []
    if not _is_set("TRIAGE_FOUNDRY_ENDPOINT"):
        missing.append("TRIAGE_FOUNDRY_ENDPOINT")

    if not (_is_set("TRIAGE_FOUNDRY_API_KEY") or _is_set("AZURE_INFERENCE_CREDENTIAL")):
        missing.append("TRIAGE_FOUNDRY_API_KEY (or AZURE_INFERENCE_CREDENTIAL)")

    if not _is_set("TRIAGE_FOUNDRY_MODEL"):
        missing.append("TRIAGE_FOUNDRY_MODEL")
    return missing


def _missing_env_for_openai_compatible() -> list[str]:
    missing: list[str] = []
    if not _is_set("TRIAGE_OPENAI_BASE_URL"):
        missing.append("TRIAGE_OPENAI_BASE_URL")
    if not _is_set("TRIAGE_OPENAI_API_KEY"):
        missing.append("TRIAGE_OPENAI_API_KEY")
    if not _is_set("TRIAGE_OPENAI_MODEL"):
        missing.append("TRIAGE_OPENAI_MODEL")
    return missing


def _auto_adapter_choice() -> tuple[str, str]:
    """Return (adapter_name, reason) for what `--adapter auto` would choose.

    This mirrors the intent of `triage_assistant.triage.get_default_adapter()` but does
    not instantiate adapters or make network calls.
    """

    provider = (os.getenv("TRIAGE_PROVIDER") or "").strip()
    if provider:
        normalized = provider.lower().replace("_", "-")
        if normalized in {"github", "github-models"}:
            return "github", f"TRIAGE_PROVIDER={provider}"
        if normalized in {"foundry", "azure-foundry", "ai-foundry"}:
            return "foundry", f"TRIAGE_PROVIDER={provider}"
        if normalized in {"openai", "openai-compatible"}:
            return "openai", f"TRIAGE_PROVIDER={provider}"
        if normalized in {"dummy", "offline"}:
            return "dummy", f"TRIAGE_PROVIDER={provider}"
        return "(invalid)", f"TRIAGE_PROVIDER={provider} (unsupported)"

    if not _missing_env_for_github_models():
        return "github", "GitHub Models credentials detected"

    if not _missing_env_for_foundry():
        return "foundry", "Foundry credentials detected"

    if not _missing_env_for_openai_compatible():
        return "openai", "OpenAI-compatible configuration detected"

    return "dummy", "No hosted adapter credentials detected"


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
            help=(
                "Which adapter to use: auto (default), dummy (offline baseline), "
                "github (GitHub Models), foundry (Microsoft Foundry), openai (OpenAI-compatible)."
            )
        ),
    ] = "auto",
    pretty: Annotated[bool, typer.Option(help="Pretty-print JSON output.")] = False,
) -> None:
    """Triage an issue and print schema-valid JSON to stdout."""
    body_text = _read_body(body, body_file)
    triage_adapter = _resolve_adapter(adapter)

    try:
        result = triage_adapter.triage(title=title, body=body_text)
    except ChatCompletionsError as e:
        console.print(f"[red]Model adapter error:[/red] {e}")
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
def doctor() -> None:
    """Diagnose configuration and explain what `--adapter auto` would do.

    This command is intentionally best-effort and never prints secret values.
    """

    chosen, reason = _auto_adapter_choice()
    provider = (os.getenv("TRIAGE_PROVIDER") or "").strip() or None

    gh_missing = _missing_env_for_github_models()
    foundry_missing = _missing_env_for_foundry()
    openai_missing = _missing_env_for_openai_compatible()

    lines: list[str] = []
    lines.append("triage-assistant doctor")
    lines.append("")
    lines.append("Auto adapter resolution")
    lines.append(f"- TRIAGE_PROVIDER: {provider if provider is not None else '(not set)'}")
    lines.append(f"- Selected adapter: {chosen} ({reason})")

    if chosen == "(invalid)":
        lines.append("")
        lines.append(
            "NOTE: TRIAGE_PROVIDER is set to an unsupported value. `--adapter auto` will fail."
        )

    lines.append("")
    lines.append("Environment checks (missing only)")

    def _fmt_missing(provider_name: str, missing: list[str]) -> str:
        if not missing:
            return f"- {provider_name}: OK"
        return f"- {provider_name}: missing {', '.join(missing)}"

    lines.append(_fmt_missing("GitHub Models", gh_missing))
    lines.append(_fmt_missing("Foundry", foundry_missing))
    lines.append(_fmt_missing("OpenAI-compatible", openai_missing))

    typer.echo("\n".join(lines))


@app.command()
def eval(
    dataset: Annotated[Path, typer.Option(help="Path to the CSV dataset.")] = Path(
        "datasets/triage_dataset.csv"
    ),
    adapter: Annotated[
        str,
        typer.Option(
            help=(
                "Adapter to use for evaluation: dummy (default), auto, github, foundry, openai. "
                "For remote adapters, configure environment variables first."
            )
        ),
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

    If you configure a hosted adapter (GitHub Models / Foundry), you can also
    run this command to smoke-test end-to-end behavior.
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
    def _parse_expected_labels(s: str) -> set[str]:
        s = (s or "").strip()
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

    def _safe_excerpt(text: str, *, max_chars: int = 240) -> str:
        text = (text or "").strip().replace("\r\n", "\n")
        if len(text) <= max_chars:
            return text
        return text[: max_chars - 1].rstrip() + "…"

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

    # Failure pattern analysis (basic grouping is OK; keep deterministic ordering).
    type_confusions: dict[tuple[str, str], int] = {}
    priority_confusions: dict[tuple[str, str], int] = {}
    missing_label_counts: dict[str, int] = {}
    extra_label_counts: dict[str, int] = {}
    mismatch_kind_counts: dict[str, int] = {}

    total_failures = 0
    for row, pred in results:
        exp_type = (row.get("expected_type", "") or "").strip()
        exp_pri = (row.get("expected_priority", "") or "").strip()
        exp_labels = _parse_expected_labels(row.get("expected_labels", ""))
        pred_labels = {x.strip() for x in pred.labels if x.strip()}

        type_mismatch = pred.type.value != exp_type
        pri_mismatch = pred.priority.value != exp_pri
        label_mismatch = exp_labels != pred_labels

        if not (type_mismatch or pri_mismatch or label_mismatch):
            continue

        total_failures += 1

        mismatch_kinds: list[str] = []
        if type_mismatch:
            mismatch_kinds.append("type")
            key = (exp_type, pred.type.value)
            type_confusions[key] = type_confusions.get(key, 0) + 1
        if pri_mismatch:
            mismatch_kinds.append("priority")
            key = (exp_pri, pred.priority.value)
            priority_confusions[key] = priority_confusions.get(key, 0) + 1
        if label_mismatch:
            mismatch_kinds.append("labels")
            for missing in sorted(exp_labels - pred_labels):
                missing_label_counts[missing] = missing_label_counts.get(missing, 0) + 1
            for extra in sorted(pred_labels - exp_labels):
                extra_label_counts[extra] = extra_label_counts.get(extra, 0) + 1

        kind = "+".join(mismatch_kinds)
        mismatch_kind_counts[kind] = mismatch_kind_counts.get(kind, 0) + 1

    lines.append("## Top failure patterns")
    lines.append("")
    lines.append(f"- Failures: {total_failures} / {int(metrics['n'])}")

    if total_failures == 0:
        lines.append("")
        lines.append("No failures found.")
        lines.append("")
        return "\n".join(lines)

    def _top_items(d: dict[object, int], *, limit: int = 5):
        return sorted(d.items(), key=lambda kv: (-kv[1], str(kv[0])))[:limit]

    lines.append("")
    lines.append("Mismatch breakdown (by fields)")
    for kind, count in _top_items(mismatch_kind_counts, limit=10):
        lines.append(f"- {kind}: {count}")

    top_type = _top_items(type_confusions)
    if top_type:
        lines.append("")
        lines.append("Most common type confusions")
        for (exp, got), count in top_type:
            lines.append(f"- `{exp} → {got}`: {count}")

    top_pri = _top_items(priority_confusions)
    if top_pri:
        lines.append("")
        lines.append("Most common priority confusions")
        for (exp, got), count in top_pri:
            lines.append(f"- `{exp} → {got}`: {count}")

    top_missing = _top_items(missing_label_counts)
    if top_missing:
        lines.append("")
        lines.append("Most commonly missed labels")
        for label, count in top_missing:
            lines.append(f"- `{label}`: {count}")

    top_extra = _top_items(extra_label_counts)
    if top_extra:
        lines.append("")
        lines.append("Most common extra labels")
        for label, count in top_extra:
            lines.append(f"- `{label}`: {count}")

    lines.append("")
    lines.append("## Failure examples (first 5)")
    lines.append("")
    count = 0
    for row, pred in results:
        exp_type = (row.get("expected_type", "") or "").strip()
        exp_pri = (row.get("expected_priority", "") or "").strip()
        exp_labels = _parse_expected_labels(row.get("expected_labels", ""))
        pred_labels = {x.strip() for x in pred.labels if x.strip()}

        if (
            pred.type.value == exp_type
            and pred.priority.value == exp_pri
            and pred_labels == exp_labels
        ):
            continue

        title = (row.get("title", "") or "").strip()
        issue_id = (row.get("id", "") or "").strip() or "(no id)"
        body_excerpt = _safe_excerpt(row.get("body", ""))

        lines.append(f"### {issue_id}: {title}")
        lines.append("")

        if body_excerpt:
            lines.append("**Input (excerpt)**")
            lines.append("")
            lines.append("```text")
            lines.append(body_excerpt)
            lines.append("```")
            lines.append("")

        lines.append("**Expected**")
        lines.append("")
        lines.append(f"- type: `{exp_type}`")
        lines.append(f"- priority: `{exp_pri}`")
        lines.append(f"- labels: `{sorted(exp_labels)}`")
        lines.append("")

        lines.append("**Predicted**")
        lines.append("")
        lines.append(f"- type: `{pred.type.value}`")
        lines.append(f"- priority: `{pred.priority.value}`")
        lines.append(f"- labels: `{sorted(pred_labels)}`")

        missing = sorted(exp_labels - pred_labels)
        extra = sorted(pred_labels - exp_labels)
        if missing:
            lines.append(f"- missing labels: `{missing}`")
        if extra:
            lines.append(f"- extra labels: `{extra}`")
        lines.append(f"- rationale: {pred.rationale}")
        lines.append("")
        count += 1
        if count >= 5:
            break
    return "\n".join(lines)
