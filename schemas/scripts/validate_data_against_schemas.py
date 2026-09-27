#!/usr/bin/env python3
"""Validate committed data files against their JSON Schemas.

The CI workflow already checks that every schema is *legal* Draft 2020-12. That
only proves the schema parses. This checker proves the committed records
actually *obey* it, so a hand-edited run record or source registration cannot
drift away from its contract unnoticed.

Each pair is declared in ``PAIRS`` below. To add a check, add one tuple.

Usage:  python3 schemas/scripts/validate_data_against_schemas.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import List, Tuple

try:
    import jsonschema
except ImportError:
    print("ERROR: jsonschema is required (pip install jsonschema)", file=sys.stderr)
    raise SystemExit(1)

REPO_ROOT = Path(__file__).resolve().parents[2]

# (data file, schema file) - a data file is validated against a schema.
PAIRS: List[Tuple[str, str]] = [
    ("evaluation/reports/pilot-run-record-001.json", "evaluation/run-record.schema.json"),
    ("evaluation/example-run-record.json", "evaluation/run-record.schema.json"),
    ("memory/pilot-cpi-style-source.json", "memory/source-registration.schema.json"),
]


def load(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON: {exc}") from exc


def main() -> int:
    problems: List[str] = []
    checked = 0

    for data_rel, schema_rel in PAIRS:
        data_path = REPO_ROOT / data_rel
        schema_path = REPO_ROOT / schema_rel

        if not schema_path.is_file():
            problems.append(f"{schema_rel}: schema file is missing")
            continue
        if not data_path.is_file():
            problems.append(f"{data_rel}: data file is missing")
            continue

        try:
            schema = load(schema_path)
            instance = load(data_path)
        except ValueError as exc:
            problems.append(f"{data_rel}: {exc}")
            continue

        try:
            jsonschema.Draft202012Validator.check_schema(schema)
        except Exception as exc:  # noqa: BLE001
            problems.append(f"{schema_rel}: not a valid Draft 2020-12 schema: {exc}")
            continue

        validator = jsonschema.Draft202012Validator(schema)
        errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.path))
        if errors:
            for err in errors:
                where = "/".join(str(p) for p in err.path) or "<root>"
                problems.append(f"{data_rel}: {where}: {err.message}")
        else:
            checked += 1

    if problems:
        for problem in problems:
            print(f"ERROR: {problem}", file=sys.stderr)
        return 1

    print(f"OK: {checked} data file(s) validate against their schemas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
