#!/usr/bin/env python3
"""Validate skill package metadata and bundled resource references.

Checks every ``skills/*/SKILL.md`` for:

* YAML frontmatter that starts on line 1 and declares ``name`` and ``description``
* fewer than 500 lines
* a ``name`` in the frontmatter (informational, cross-checked by the naming lint)
* every bundled path it mentions under ``references/``, ``scripts/``, or
  ``templates/`` actually existing

The reference scan is what stops a skill from advertising a file that was
renamed or deleted.

Usage:  python3 schemas/scripts/validate_skill_packages.py [skills_dir]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import List

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required (pip install PyYAML)", file=sys.stderr)
    raise SystemExit(1)

REPO_ROOT = Path(__file__).resolve().parents[2]
MAX_SKILL_LINES = 500
BUNDLED_REF = re.compile(r"(?:references|scripts|templates)/[A-Za-z0-9_./-]+")


def check_skill(skill_md: Path) -> List[str]:
    errors: List[str] = []
    rel = skill_md.relative_to(REPO_ROOT)
    skill_dir = skill_md.parent

    try:
        text = skill_md.read_text(encoding="utf-8")
    except UnicodeError as exc:
        return [f"{rel}: not valid UTF-8: {exc}"]

    if not text.startswith("---\n"):
        return [f"{rel}: must start with '---' YAML frontmatter on line 1"]

    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return [f"{rel}: frontmatter is not closed with '---'"]

    frontmatter_raw, body = parts[1], parts[2]

    try:
        meta = yaml.safe_load(frontmatter_raw)
    except Exception as exc:  # noqa: BLE001
        return [f"{rel}: frontmatter is not valid YAML: {exc}"]

    if not isinstance(meta, dict):
        return [f"{rel}: frontmatter is not a YAML mapping"]

    for field in ("name", "description"):
        if not meta.get(field):
            errors.append(f"{rel}: frontmatter is missing a non-empty '{field}:'")

    line_count = len(text.splitlines())
    if line_count >= MAX_SKILL_LINES:
        errors.append(f"{rel}: must stay under {MAX_SKILL_LINES} lines (is {line_count})")

    for ref in sorted(set(BUNDLED_REF.findall(body))):
        if not (skill_dir / ref).exists():
            errors.append(f"{rel}: bundled resource not found: {ref}")

    return errors


def main(argv: List[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    skills_dir = Path(args[0]) if args else REPO_ROOT / "skills"

    skill_files = sorted(skills_dir.glob("*/SKILL.md"))
    if not skill_files:
        print(f"ERROR: no SKILL.md found under {skills_dir}", file=sys.stderr)
        return 1

    problems: List[str] = []
    for skill_md in skill_files:
        problems.extend(check_skill(skill_md))

    if problems:
        for problem in problems:
            print(f"ERROR: {problem}", file=sys.stderr)
        return 1

    print(f"OK: {len(skill_files)} skill package(s) have valid metadata and references")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
