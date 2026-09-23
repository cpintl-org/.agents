#!/usr/bin/env python3
"""Validate a provider-neutral Workspace bridge request without network access."""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

SLUG = re.compile(r"^[a-z0-9][a-z0-9-]{0,98}[a-z0-9]$|^[a-z0-9]$")
SAFE_PATH = re.compile(r"^[A-Za-z0-9._/-]+$")
REQUIRED = ("operation", "owner", "repository", "ref", "repositoryPath", "driveFolderId", "query", "sensitivity", "requesterRole")

def fail(message: str) -> None:
    raise SystemExit(f"INVALID: {message}")

def main() -> int:
    if len(sys.argv) != 2:
        fail("usage: validate_bridge_request.py request.json")
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    missing = [key for key in REQUIRED if not isinstance(data.get(key), str) or not data[key].strip()]
    if missing:
        fail("missing fields: " + ", ".join(missing))
    if data["operation"] not in {"search_metadata", "get_content", "sync_content"}:
        fail("unsupported operation")
    if data["sensitivity"] not in {"public", "internal", "restricted"}:
        fail("unsupported sensitivity")
    if data["repository"] != ".agents" or data["ref"] != "main":
        fail("request is outside the canonical repository scope")
    if ".." in data["repositoryPath"] or not SAFE_PATH.fullmatch(data["repositoryPath"]):
        fail("unsafe repositoryPath")
    if any(token in json.dumps(data).lower() for token in ("api_key", "private_key", "bearer ", "password")):
        fail("possible secret field")
    print("VALID")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
