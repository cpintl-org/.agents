#!/usr/bin/env python3
"""Check .prompt files in plain language. No network access, no credentials.

Usage: python validate_prompts.py PATH [PATH ...]
PATH may be a .prompt file or a folder (searched recursively; partials are skipped).
Exit code 0 = no errors (warnings allowed). Exit code 1 = at least one error.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

try:  # optional but recommended: pip install jsonschema
    import jsonschema
except ImportError:  # pragma: no cover
    jsonschema = None

HEADER = re.compile(r"\A---\n(.*?)\n---\n(.*)\Z", re.S)
TAG = re.compile(r"\{\{(.*?)\}\}", re.S)
VAR = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
PARTIAL_NAME = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$")
REQUIRED = ("name", "version", "owner", "sensitivity", "input_schema", "output_schema")
PROVIDER_KEYS = {"model", "config", "temperature", "maxOutputTokens", "max_tokens", "top_p",
                 "top_k", "provider", "ext", "tools", "toolChoice", "genkit"}
SECRET = re.compile(
    r"AKIA[0-9A-Z]{16}|BEGIN (?:RSA|OPENSSH|EC|DSA) PRIVATE KEY|ghp_[A-Za-z0-9]{20,}|"
    r"sk-[A-Za-z0-9]{20,}|AIza[0-9A-Za-z_-]{20,}|"
    r"(?i:(?:api[_-]?key|secret|password|access[_-]?token)\s*[:=]\s*[^\s{'\"]{6,})")
UNSAFE_URL = re.compile(r"(?i)(?:\bhttp://|\bfile://|\bjavascript:|\bdata:[a-z]+/[a-z0-9.+-]+)")


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, code: str, msg: str) -> None:
        self.errors.append(f"ERROR  {code}: {msg}")

    def warn(self, code: str, msg: str) -> None:
        self.warnings.append(f"WARN   {code}: {msg}")


def scan_body(text: str, where: str, rep: Report):
    """Return (variables, partial_names). Reports unsupported syntax and unbalanced blocks."""
    variables: set[str] = set()
    partials: list[str] = []
    stack: list[str] = []
    if "{{{" in text:
        rep.error("unsupported-syntax", f"{where}: triple curly brackets are not allowed")
    for raw in TAG.findall(text):
        tag = raw.strip()
        if tag.startswith("#if ") or tag.startswith("#each "):
            kind, name = tag[1:].split(None, 1)
            name = name.strip()
            if not VAR.match(name):
                rep.error("unsupported-syntax", f"{where}: '{{{{{tag}}}}}' needs a plain variable name")
            else:
                variables.add(name)
            stack.append(kind)
        elif tag in ("/if", "/each"):
            if not stack or stack[-1] != tag[1:]:
                rep.error("unsupported-syntax", f"{where}: unexpected '{{{{{tag}}}}}'")
            else:
                stack.pop()
        elif tag == "else":
            if not stack or stack[-1] != "if":
                rep.error("unsupported-syntax", f"{where}: 'else' is only allowed inside if")
        elif tag == "this":
            if "each" not in stack:
                rep.error("unsupported-syntax", f"{where}: 'this' is only allowed inside each")
        elif tag.startswith(">"):
            name = tag[1:].strip()
            if not PARTIAL_NAME.match(name):
                rep.error("unsupported-syntax", f"{where}: bad shared-piece name '{name}'")
            else:
                partials.append(name)
        elif VAR.match(tag):
            variables.add(tag)
        else:
            rep.error("unsupported-syntax", f"{where}: '{{{{{tag}}}}}' is not allowed (only variables, if, each, and > piece)")
    if stack:
        rep.error("unsupported-syntax", f"{where}: block '{stack[-1]}' is never closed")
    return variables, partials


def collect(prompt_dir: Path, body: str, where: str, rep: Report, seen: list[str]):
    variables, partials = scan_body(body, where, rep)
    for name in partials:
        if name in seen:
            rep.error("partial-cycle", f"{where}: shared pieces loop: {' -> '.join(seen + [name])}")
            continue
        path = prompt_dir / "partials" / f"{name}.prompt"
        if not path.is_file():
            rep.error("partial-missing", f"{where}: partials/{name}.prompt not found")
            continue
        text = path.read_text(encoding="utf-8")
        check_text_safety(text, f"partials/{name}.prompt", rep)
        m = HEADER.match(text)
        sub_vars = collect(prompt_dir, m.group(2) if m else text, f"partials/{name}.prompt", rep, seen + [name])
        variables |= sub_vars
    return variables


def check_text_safety(text: str, where: str, rep: Report) -> None:
    if SECRET.search(text):
        rep.error("secret-like", f"{where}: text looks like a key, token, or password")
    if UNSAFE_URL.search(text):
        rep.error("unsafe-url", f"{where}: only reviewed https links are allowed (no http, file, or data links)")


def load_schema(path: Path, label: str, rep: Report):
    if not path.is_file():
        rep.error("schema-missing", f"{label} file not found: {path.name}")
        return None
    try:
        schema = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        rep.error("schema-missing", f"{label} is not valid JSON: {exc}")
        return None
    if not isinstance(schema, dict) or schema.get("type") != "object":
        rep.error("bad-header", f"{label} must describe an object (type: object)")
        return None
    if jsonschema:
        try:
            jsonschema.Draft202012Validator.check_schema(schema)
        except jsonschema.SchemaError as exc:
            rep.error("schema-missing", f"{label} is not a valid schema: {exc.message}")
            return None
    return schema


def check_prompt(path: Path) -> Report:
    rep = Report()
    text = path.read_text(encoding="utf-8")
    m = HEADER.match(text)
    if not m:
        rep.error("missing-header", f"{path.name}: no header between two --- lines")
        return rep
    try:
        header = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as exc:
        rep.error("bad-header", f"{path.name}: header is not valid YAML: {exc}")
        return rep
    if not isinstance(header, dict):
        rep.error("bad-header", f"{path.name}: header must be a list of name: value lines")
        return rep
    for key in sorted(PROVIDER_KEYS & set(header)):
        rep.error("provider-field", f"{path.name}: '{key}' is a provider setting; move it to a Model Adapter")
    for key in REQUIRED:
        if key not in header:
            rep.error("bad-header", f"{path.name}: missing header field '{key}'")
    if jsonschema and not rep.errors:
        schema_file = Path(__file__).resolve().parents[3] / "prompts" / "schemas" / "prompt-frontmatter.schema.json"
        if schema_file.is_file():
            schema = json.loads(schema_file.read_text(encoding="utf-8"))
            for err in jsonschema.Draft202012Validator(schema).iter_errors(header):
                loc = ".".join(str(p) for p in err.path) or "header"
                rep.error("bad-header", f"{path.name}: {loc}: {err.message}")
    check_text_safety(text, path.name, rep)
    if rep.errors:
        return rep

    folder = path.parent
    in_schema = load_schema(folder / header["input_schema"], "input_schema", rep)
    load_schema(folder / header["output_schema"], "output_schema", rep)
    used = collect(folder, m.group(2), path.name, rep, [])
    if in_schema is not None:
        declared = set((in_schema.get("properties") or {}).keys())
        for name in sorted(used - declared):
            rep.error("undefined-variable", f"{path.name}: '{{{{{name}}}}}' is used but not in the input schema")
        for name in sorted(declared - used):
            rep.warn("unused-variable", f"{path.name}: input '{name}' is declared but never used")
    fixtures = header.get("fixtures")
    if fixtures and in_schema is not None and jsonschema:
        fx = folder / fixtures
        if not fx.is_file():
            rep.error("fixture-mismatch", f"fixtures file not found: {fixtures}")
        else:
            data = yaml.safe_load(fx.read_text(encoding="utf-8")) or {}
            for case in data.get("cases", []):
                cid = case.get("caseId", "?")
                if case.get("synthetic") is not True:
                    rep.error("fixture-mismatch", f"case '{cid}' must say synthetic: true")
                for err in jsonschema.Draft202012Validator(in_schema).iter_errors(case.get("input", {})):
                    rep.error("fixture-mismatch", f"case '{cid}': {err.message}")
    return rep


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    files: list[Path] = []
    for arg in argv:
        p = Path(arg)
        if p.is_dir():
            files += [f for f in sorted(p.rglob("*.prompt")) if "partials" not in f.parts]
        elif p.is_file():
            files.append(p)
        else:
            print(f"ERROR  path-missing: {arg}")
            return 1
    if not files:
        print("ERROR  no-prompts: no .prompt files found")
        return 1
    failed = False
    for f in files:
        rep = check_prompt(f)
        for line in rep.warnings + rep.errors:
            print(line)
        if rep.errors:
            failed = True
        else:
            print(f"OK     {f}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
