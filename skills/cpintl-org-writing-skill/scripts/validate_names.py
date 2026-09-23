#!/usr/bin/env python3
"""Validate portable names for cpintl-org-writing-skill."""
import argparse
import re
import sys

REPOSITORY = re.compile(r"[a-z0-9](?:[a-z0-9-]{0,98}[a-z0-9])?\Z")
SLUG = re.compile(r"[a-z][a-z0-9-]{0,62}\Z")
BRANCH = re.compile(r"(?:feat|fix|docs|chore|refactor|test|build|release)/[a-z0-9][a-z0-9-]{0,62}\Z")
TAG = re.compile(r"v(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?\Z")
ENV = re.compile(r"[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)*\Z")
MCP = re.compile(r"[A-Za-z][A-Za-z0-9_.-]{0,127}\Z")
RESERVED = {"CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1, 10)), *(f"LPT{i}" for i in range(1, 10))}


def common_errors(value: str):
    errors = []
    if not value:
        errors.append("must not be empty")
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in value):
        errors.append("must not contain control characters")
    if value.endswith((" ", ".")):
        errors.append("must not end with a space or period")
    if value in {".", ".."} or "../" in value or value.startswith("../"):
        errors.append("must not contain path traversal")
    if value.upper().split(".", 1)[0] in RESERVED:
        errors.append("must not use a Windows reserved name")
    return errors


def validate(kind: str, value: str):
    errors = common_errors(value)
    patterns = {
        "repository": REPOSITORY,
        "slug": SLUG,
        "branch": BRANCH,
        "tag": TAG,
        "environment": ENV,
        "mcp-tool": MCP,
    }
    if kind in patterns and not patterns[kind].fullmatch(value):
        errors.append(f"does not match the {kind} profile")
    if kind == "path":
        if "\\" in value or "//" in value:
            errors.append("must use single forward-slash separators")
        segments = value.split("/")
        if any(not segment or segment in {".", ".."} for segment in segments):
            errors.append("must contain non-empty safe segments")
        if any(not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}", segment) for segment in segments):
            errors.append("contains an unsafe path segment")
    return errors


def main():
    parser = argparse.ArgumentParser(description="Validate portable names and paths")
    parser.add_argument("--kind", required=True, choices=["repository", "slug", "branch", "tag", "environment", "mcp-tool", "path"])
    parser.add_argument("value")
    args = parser.parse_args()
    errors = validate(args.kind, args.value)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"OK: {args.kind}={args.value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
