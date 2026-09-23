#!/usr/bin/env python3
"""Validate the minimum evidence contract for a free-resource matrix.

This checker is intentionally deterministic and network-free. It verifies that a
matrix retains the required cost classifications, service coverage, official
source links, and dated evidence marker. It does not certify that a provider's
current pricing or quota is still correct; recheck official sources at use time.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REQUIRED_TERMS = (
    "Always-free",
    "Free-tier",
    "Trial",
    "billing-dependent",
    "Apps Script",
    "Firebase",
    "GitHub",
    "Gemini",
    "Maps",
)
REQUIRED_URLS = (
    "developers.google.com/apps-script/guides/services/quotas",
    "firebase.google.com/pricing",
    "github.com/pricing",
    "ai.google.dev/gemini-api/docs/pricing",
)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check a free-resource matrix for classifications and sources."
    )
    parser.add_argument("matrix", type=Path, help="Path to the Markdown matrix")
    return parser.parse_args(argv)


def validate(path: Path) -> list[str]:
    if not path.is_file():
        return [f"missing matrix: {path}"]
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeError as exc:
        return [f"matrix is not valid UTF-8: {exc}"]

    errors: list[str] = []
    folded = text.casefold()
    for term in REQUIRED_TERMS:
        if term.casefold() not in folded:
            errors.append(f"missing required term: {term}")
    for url in REQUIRED_URLS:
        if url not in text:
            errors.append(f"missing official source URL: {url}")
    if not re.search(r"2026-09-18|18 September 2026|Access date", text, re.I):
        errors.append("missing access-date marker")
    if len(re.findall(r"https?://", text)) < 10:
        errors.append("too few source URLs for a research matrix")
    return errors


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    errors = validate(args.matrix)
    if errors:
        print("FAIL")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print(f"PASS: {args.matrix} contains required classifications, scope, and source coverage")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
