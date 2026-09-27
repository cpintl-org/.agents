#!/usr/bin/env python3
"""Repository hygiene sweeps shared by local checks and CI.

Groups five checks that used to be separate inline shell snippets:

1. every ``*.json`` that looks like a schema is valid Draft 2020-12
2. every tracked ``*.json`` parses, and every ``*.yaml``/``*.yml`` loads
3. no file matches a known credential format
4. no tracked path uses traversal, an absolute prefix, or a doubled dot
5. the Workspace bridge still declares its safe defaults

Usage:  python3 schemas/scripts/validate_repo_hygiene.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import List

try:
    import jsonschema
except ImportError:
    print("ERROR: jsonschema is required (pip install jsonschema)", file=sys.stderr)
    raise SystemExit(1)

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required (pip install PyYAML)", file=sys.stderr)
    raise SystemExit(1)

REPO_ROOT = Path(__file__).resolve().parents[2]
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", "build"}

# Credential shapes only. Ordinary words such as "secret" or "token" are fine:
# this repository documents configuration key names on purpose.
CREDENTIAL_PATTERNS = (
    ("AWS access key id", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("private key block", re.compile(r"BEGIN (?:RSA|OPENSSH|EC|DSA) PRIVATE KEY")),
    ("GitHub classic/legacy token", re.compile(r"ghp_[A-Za-z0-9]{20,}")),
    ("OpenAI-style key", re.compile(r"sk-[A-Za-z0-9]{20,}")),
    ("Google API key", re.compile(r"AIza[0-9A-Za-z_-]{20,}")),
    ("Google OAuth client secret", re.compile(r"GOCSPX-[A-Za-z0-9_-]{20,}")),
    ("Slack token", re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}")),
)

SCHEMA_DIRS = ("schemas", "memory", "evaluation", "prompts", "templates", "guardrails")

# Asserted so a future edit cannot quietly relax the safe operating mode.
BRIDGE_DEFAULTS = (
    ("workspace-bridge/README.md", r"DRY_RUN.*true", "README states DRY_RUN true"),
    ("config/mcp-bridge-mapping.yaml", r"defaultMode: read-only", "bridge defaultMode is read-only"),
    ("config/mcp-bridge-mapping.yaml", r"allowWrite: false", "bridge allowWrite is false"),
)


def tracked_files() -> List[Path]:
    """All repository files, skipping build and cache directories."""
    files: List[Path] = []
    for path in REPO_ROOT.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file():
            files.append(path)
    return files


def check_schemas() -> List[str]:
    problems: List[str] = []
    count = 0
    for directory in SCHEMA_DIRS:
        base = REPO_ROOT / directory
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*.json")):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except Exception as exc:  # noqa: BLE001
                problems.append(f"{path.relative_to(REPO_ROOT)}: invalid JSON: {exc}")
                continue
            # Everything under schemas/ is a schema by definition. Elsewhere only
            # treat a file as a schema if it advertises itself as one, so plain
            # data files are not misread.
            rel = path.relative_to(REPO_ROOT)
            looks_like_schema = rel.parts[0] == "schemas" or (
                isinstance(data, dict)
                and (
                    "$schema" in data
                    or "properties" in data
                    or data.get("type") == "object"
                )
            )
            if not looks_like_schema:
                continue
            try:
                jsonschema.Draft202012Validator.check_schema(data)
                count += 1
            except Exception as exc:  # noqa: BLE001
                problems.append(
                    f"{rel}: not valid Draft 2020-12: {exc}"
                )
    if count == 0:
        problems.append("no JSON Schema files were found to validate")
    return problems


def check_structured_files() -> List[str]:
    problems: List[str] = []
    for path in tracked_files():
        rel = path.relative_to(REPO_ROOT)
        suffix = path.suffix.lower()
        try:
            if suffix == ".json":
                json.loads(path.read_text(encoding="utf-8"))
            elif suffix in {".yaml", ".yml"}:
                yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            problems.append(f"{rel}: does not parse: {exc}")
    return problems


def check_credentials() -> List[str]:
    problems: List[str] = []
    for path in tracked_files():
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for label, pattern in CREDENTIAL_PATTERNS:
            match = pattern.search(text)
            if match:
                line = text.count("\n", 0, match.start()) + 1
                problems.append(
                    f"{path.relative_to(REPO_ROOT)}:{line}: possible {label}"
                )
    return problems


def check_paths() -> List[str]:
    problems: List[str] = []
    for path in tracked_files():
        rel = path.relative_to(REPO_ROOT)
        parts = rel.parts
        if any(part == ".." for part in parts):
            problems.append(f"{rel}: path contains a '..' component")
        if rel.is_absolute() or str(rel).startswith(("/", "~")):
            problems.append(f"{rel}: path is absolute")
        if ".." in path.name:
            problems.append(f"{rel}: file name contains a doubled dot")
    return problems


def check_bridge_defaults() -> List[str]:
    problems: List[str] = []
    for rel, pattern, description in BRIDGE_DEFAULTS:
        path = REPO_ROOT / rel
        if not path.is_file():
            problems.append(f"{rel}: file is missing, cannot confirm {description}")
            continue
        if not re.search(pattern, path.read_text(encoding="utf-8", errors="ignore")):
            problems.append(f"{rel}: no longer satisfies '{description}'")
    return problems


CHECKS = (
    ("JSON Schemas are valid Draft 2020-12", check_schemas),
    ("all YAML and JSON files parse", check_structured_files),
    ("no credential patterns in tracked files", check_credentials),
    ("no unsafe or traversal paths", check_paths),
    ("Workspace bridge safe defaults declared", check_bridge_defaults),
)


def main() -> int:
    problems: List[str] = []
    failed: List[str] = []
    for name, func in CHECKS:
        found = func()
        if found:
            failed.append(name)
            problems.extend(found)

    if problems:
        for problem in problems:
            print(f"ERROR: {problem}", file=sys.stderr)
        print(f"FAIL: {len(failed)} hygiene check(s) failed: {', '.join(failed)}", file=sys.stderr)
        return 1

    print(f"OK: {len(CHECKS)} hygiene checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
