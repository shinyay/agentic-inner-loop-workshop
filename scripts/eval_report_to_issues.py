#!/usr/bin/env python3
"""Generate issue draft skeletons from an evaluation report.

This script is intentionally simple:
- it looks for a section header "## 4. Actions"
- it collects bullet points under that header
- it emits Markdown skeletons that you can copy into GitHub Issues

Usage:
    python scripts/eval_report_to_issues.py \
      --report reports/eval/20250101_1200_prompt-v2.md \
      --output docs/issues-from-eval.md
"""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    if not args.report.exists():
        raise SystemExit(f"Report not found: {args.report}")

    text = args.report.read_text(encoding="utf-8").splitlines()

    actions = _extract_actions(text)
    if not actions:
        raise SystemExit("No actions found under '## 4. Actions'.")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(_render(actions, source=args.report.as_posix()), encoding="utf-8")
    print(f"Wrote: {args.output}")
    return 0


def _extract_actions(lines: list[str]) -> list[str]:
    in_actions = False
    items: list[str] = []

    for line in lines:
        if line.strip() == "## 4. Actions":
            in_actions = True
            continue
        if in_actions and line.startswith("## "):
            break
        if in_actions:
            stripped = line.strip()
            if stripped.startswith("- "):
                items.append(stripped.removeprefix("- ").strip())
            elif stripped.startswith("* "):
                items.append(stripped.removeprefix("* ").strip())

    return [x for x in items if x]


def _render(actions: list[str], *, source: str) -> str:
    out: list[str] = []
    out.append("# Issue drafts from evaluation")
    out.append("")
    out.append(f"Source report: `{source}`")
    out.append("")
    for i, action in enumerate(actions, start=1):
        out.append(f"## Draft {i}: {action}")
        out.append("")
        out.append("### Problem")
        out.append("")
        out.append("Describe the failure or opportunity identified by evaluation.")
        out.append("")
        out.append("### Definition of Done")
        out.append("")
        out.append("- [ ] ...")
        out.append("")
        out.append("### Validation")
        out.append("")
        out.append("- AI Toolkit: compare vN vs v(N-1)")
        out.append("- or: `pytest -q`")
        out.append("")
    return "\n".join(out)


if __name__ == "__main__":
    raise SystemExit(main())
