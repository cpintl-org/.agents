#!/usr/bin/env python3
"""Fail if the standards-freshness register is overdue for review.

This does not fetch anything from the internet and cannot tell you what changed
upstream. It only reads the ``next_review_due`` date declared in the register's
frontmatter and compares it to today. A red result means: a person (or an AI
assistant, on request) should re-check the official sources listed in the
register and bump ``last_verified`` / ``next_review_due``.

Usage:  python3 skills/cpintl-org-writing-skill/scripts/check_standards_freshness.py
"""
from __future__ import annotations

import sys
from datetime import date, datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required (pip install PyYAML)", file=sys.stderr)
    raise SystemExit(1)

REPO_ROOT = Path(__file__).resolve().parents[3]
REGISTER = REPO_ROOT / "skills" / "cpintl-org-writing-skill" / "references" / "standards-freshness-register.md"
REQUIRED_KEYS = ("doc", "last_verified", "next_review_due", "review_cadence_days")


def load_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise SystemExit(f"ERROR: {path.relative_to(REPO_ROOT)}: missing '---' frontmatter")
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        raise SystemExit(f"ERROR: {path.relative_to(REPO_ROOT)}: frontmatter is not closed with '---'")
    data = yaml.safe_load(parts[1])
    if not isinstance(data, dict):
        raise SystemExit(f"ERROR: {path.relative_to(REPO_ROOT)}: frontmatter is not a YAML mapping")
    return data


def as_date(value, field: str, path: Path) -> date:
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    try:
        return datetime.strptime(str(value), "%Y-%m-%d").date()
    except ValueError as exc:
        raise SystemExit(
            f"ERROR: {path.relative_to(REPO_ROOT)}: '{field}' is not a YYYY-MM-DD date: {value!r}"
        ) from exc


def main() -> int:
    if not REGISTER.is_file():
        print(f"ERROR: register not found: {REGISTER}", file=sys.stderr)
        return 1

    meta = load_frontmatter(REGISTER)
    missing = [key for key in REQUIRED_KEYS if key not in meta]
    if missing:
        print(
            f"ERROR: {REGISTER.relative_to(REPO_ROOT)}: frontmatter missing {missing}",
            file=sys.stderr,
        )
        return 1

    last_verified = as_date(meta["last_verified"], "last_verified", REGISTER)
    next_due = as_date(meta["next_review_due"], "next_review_due", REGISTER)
    today = date.today()

    if next_due < last_verified:
        print(
            f"ERROR: {REGISTER.relative_to(REPO_ROOT)}: next_review_due ({next_due}) is "
            f"before last_verified ({last_verified})",
            file=sys.stderr,
        )
        return 1

    if today > next_due:
        days_overdue = (today - next_due).days
        print(
            f"FAIL: standards-freshness-register.md is {days_overdue} day(s) overdue "
            f"(last verified {last_verified}, was due {next_due}).",
            file=sys.stderr,
        )
        print(
            "       Re-check the official sources listed in the register, then update "
            "'last_verified' and 'next_review_due' in its frontmatter.",
            file=sys.stderr,
        )
        return 1

    days_left = (next_due - today).days
    print(
        f"OK: standards-freshness-register.md is current "
        f"(last verified {last_verified}, next review in {days_left} day(s), due {next_due})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())