#!/usr/bin/env python3
"""Convert the workshop triage CSV dataset to JSONL.

Why this exists:
- Some evaluation tools prefer JSONL.
- It is easier to diff JSONL outputs for versioning.

Usage:
    python scripts/csv_to_jsonl.py \
      --input datasets/triage_dataset.csv \
      --output datasets/triage_dataset.jsonl
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    if not args.input.exists():
        raise SystemExit(f"Input not found: {args.input}")

    args.output.parent.mkdir(parents=True, exist_ok=True)

    with (
        args.input.open("r", encoding="utf-8", newline="") as f_in,
        args.output.open("w", encoding="utf-8") as f_out,
    ):
        reader = csv.DictReader(f_in)
        for row in reader:
            obj = {
                "id": (row.get("id") or "").strip(),
                "title": (row.get("title") or "").strip(),
                "body": (row.get("body") or "").strip(),
                "expected_type": (row.get("expected_type") or "").strip(),
                "expected_priority": (row.get("expected_priority") or "").strip(),
                "expected_labels": row.get("expected_labels") or "[]",
            }
            f_out.write(json.dumps(obj, ensure_ascii=False) + "\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
