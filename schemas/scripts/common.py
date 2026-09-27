#!/usr/bin/env python3
"""Common helpers for repo validators."""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Iterable, Optional


def read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise SystemExit(f"Failed to parse JSON: {path}: {exc}") from exc


def write_stderr(msg: str) -> None:
    print(msg, file=sys.stderr)


class ValidationError(Exception):
    pass
