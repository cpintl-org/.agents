#!/usr/bin/env python3
"""Validate a read-only memory request without network access.

Usage: python validate_memory_request.py request.json
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ALLOWED = {"list_sources", "source_status", "search_memory", "get_evidence", "compare_revisions", "refresh_source"}
SENS = {"public", "internal", "restricted"}
SOURCE_ID = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$")
QUERY_LANGUAGE = re.compile(r"(?i)\b(match|return|select|drop|delete|merge|cypher|union)\b|[;{}<>`$\\]")
SECRET = re.compile(r"(?i)api[_-]?key|private[_-]?key|bearer |password|token")


def fail(message: str) -> None:
    raise SystemExit(f"INVALID: {message}")


def main() -> int:
    if len(sys.argv) != 2:
        fail("usage: validate_memory_request.py request.json")
    try:
        data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read request: {exc}")
    if not isinstance(data, dict):
        fail("request must be a JSON object")
    if data.get("operation") not in ALLOWED:
        fail("operation is not one of: " + ", ".join(sorted(ALLOWED)))
    if data.get("sensitivityCeiling") not in SENS:
        fail("sensitivityCeiling must be public, internal, or restricted")
    if not isinstance(data.get("requesterRole"), str) or not data["requesterRole"].strip():
        fail("requesterRole is required")
    ids = data.get("sourceIds", [])
    if not isinstance(ids, list) or len(ids) > 20 or any(not isinstance(i, str) or not SOURCE_ID.match(i) for i in ids):
        fail("sourceIds must be up to 20 registered source ids in lowercase-kebab-case")
    if data["operation"] in {"search_memory", "get_evidence", "compare_revisions", "refresh_source", "source_status"} and not ids:
        fail("this operation needs at least one registered source id")
    if data["operation"] == "search_memory":
        query = data.get("query")
        if not isinstance(query, str) or not query.strip() or len(query) > 200:
            fail("query must be 1-200 characters of plain words")
        if QUERY_LANGUAGE.search(query):
            fail("query looks like a database command; use plain words only")
        limit = data.get("limit", 5)
        if not isinstance(limit, int) or not 1 <= limit <= 20:
            fail("limit must be a whole number from 1 to 20")
    if data["operation"] == "refresh_source" and data.get("dryRun") is not True:
        fail("refresh_source must be a dry run until a person approves")
    if "path" in data or "filePath" in data:
        fail("free-form file paths are not allowed; use registered source ids")
    if SECRET.search(json.dumps(data)):
        fail("possible secret field")
    print("VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
