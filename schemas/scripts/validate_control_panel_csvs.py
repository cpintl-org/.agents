#!/usr/bin/env python3
"""Validate the Google Sheets control panel CSVs against their JSON Schemas.

Each CSV in ``templates/agent-control-panel`` has a matching row schema in
``schemas/csv``. This checker confirms that:

* every expected CSV has a schema, and every schema has a CSV;
* the CSV header contains exactly the columns the schema requires, in order;
* no row is ragged (too few or too many cells compared to the header);
* every row validates against its schema, after coercing the columns the
  schema declares as integers.

Template rows may use ``{placeholder}`` values; schemas permit this explicitly.

Usage:  python3 schemas/scripts/validate_control_panel_csvs.py
"""
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

try:
    import jsonschema
except ImportError:  # pragma: no cover - handled by the caller
    print("ERROR: jsonschema is required (pip install jsonschema)", file=sys.stderr)
    raise SystemExit(1)

REPO_ROOT = Path(__file__).resolve().parents[2]
CSV_DIR = REPO_ROOT / "templates" / "agent-control-panel"
SCHEMA_DIR = REPO_ROOT / "schemas" / "csv"
PLACEHOLDER = re.compile(r"^\{[^{}]+\}$")


def load_schema(stem: str) -> Dict[str, Any]:
    path = SCHEMA_DIR / f"{stem}.schema.json"
    if not path.is_file():
        raise FileNotFoundError(f"no schema for {stem}.csv (expected {path.name})")
    return json.loads(path.read_text(encoding="utf-8"))


def integer_columns(schema: Dict[str, Any]) -> List[str]:
    props = schema.get("properties", {})
    return [
        name
        for name, spec in props.items()
        if isinstance(spec, dict) and spec.get("type") == "integer"
    ]


def coerce(value: str, columns: List[str], name: str) -> Any:
    """Convert a decimal CSV cell to int when the schema wants an integer."""
    if name in columns and re.fullmatch(r"[+-]?\d+", value or ""):
        return int(value)
    return value


def validate_csv(csv_path: Path) -> List[str]:
    errors: List[str] = []
    try:
        schema = load_schema(csv_path.stem)
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        return [f"{csv_path.name}: {exc}"]

    try:
        jsonschema.Draft202012Validator.check_schema(schema)
    except Exception as exc:  # noqa: BLE001 - want the reason on one line
        return [f"{csv_path.name}: schema is not valid: {exc}"]

    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.reader(handle))

    if not rows:
        return [f"{csv_path.name}: file is empty (expected a header row)"]

    header, body = rows[0], rows[1:]

    required = list(schema.get("required", []))
    declared = set(schema.get("properties", {}))
    if header != required:
        missing = [c for c in required if c not in header]
        extra = [c for c in header if c not in declared]
        if missing:
            errors.append(f"{csv_path.name}: missing column(s) {missing}")
        if extra:
            errors.append(f"{csv_path.name}: unexpected column(s) {extra}")
        if not missing and not extra:
            errors.append(
                f"{csv_path.name}: column order differs from the schema "
                f"(expected {required}, found {header})"
            )
        return errors

    ints = integer_columns(schema)
    validator = jsonschema.Draft202012Validator(schema)

    for offset, raw in enumerate(body, start=2):
        if not any(cell.strip() for cell in raw):
            continue  # tolerate a blank line
        if len(raw) != len(header):
            errors.append(
                f"{csv_path.name}:{offset}: has {len(raw)} cell(s), "
                f"expected {len(header)}"
            )
            continue
        record = {
            name: coerce(raw[index], ints, name) for index, name in enumerate(header)
        }
        for err in sorted(validator.iter_errors(record), key=lambda e: list(e.path)):
            where = "/".join(str(p) for p in err.path) or "<row>"
            errors.append(f"{csv_path.name}:{offset}: {where}: {err.message}")

    return errors


def main() -> int:
    if not CSV_DIR.is_dir():
        print(f"ERROR: control panel directory not found: {CSV_DIR}", file=sys.stderr)
        return 1

    csv_paths = sorted(CSV_DIR.glob("*.csv"))
    if not csv_paths:
        print(f"ERROR: no CSV files found in {CSV_DIR}", file=sys.stderr)
        return 1

    problems: List[str] = []
    for csv_path in csv_paths:
        problems.extend(validate_csv(csv_path))

    # A schema with no CSV means the panel and the schemas have drifted apart.
    for schema_path in sorted(SCHEMA_DIR.glob("*-*.schema.json")):
        if schema_path.name == "control-panel-csv.schema.json":
            continue
        if not (CSV_DIR / f"{schema_path.stem.removesuffix('.schema')}.csv").is_file():
            problems.append(f"{schema_path.name}: no matching CSV in {CSV_DIR.name}")

    if problems:
        for problem in problems:
            print(f"ERROR: {problem}", file=sys.stderr)
        return 1

    print(f"OK: {len(csv_paths)} control panel CSV(s) match schemas/csv/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
