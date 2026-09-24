#!/usr/bin/env python3
"""Check agent YAML files (task, workspace, policy, model, template, run) in plain language.

Usage: python validate_agent_yaml.py PATH [PATH ...]
PATH may be a .yaml file or a folder. Files that are not agent files are skipped.
Also checks that references (for example a task pointing to a workspace) match a file
in the same set. Needs: pip install pyyaml jsonschema. No network access.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[3]
SCHEMAS = ROOT / "schemas"
KIND_TO_SCHEMA = {
    "AgentTask": "agent-task", "AgentWorkspace": "agent-workspace", "AgentPolicy": "agent-policy",
    "ModelAdapter": "model-adapter", "AgentTemplate": "agent-template", "AgentInstance": "agent-instance",
    "CheckpointPolicy": "checkpoint-policy",
}
REF_FIELDS = {"AgentTask": ("workspaceRef", "policyRef", "modelRef"),
              "AgentInstance": ("templateRef", "taskRef", "checkpointPolicyRef")}


def load_schema(name: str) -> dict:
    return json.loads((SCHEMAS / f"{name}.schema.json").read_text(encoding="utf-8"))


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    files: list[Path] = []
    for a in argv:
        p = Path(a)
        files += sorted(p.rglob("*.y*ml")) if p.is_dir() else [p]
    errors = 0
    known: set[tuple[str, str]] = set()
    docs: list[tuple[Path, dict]] = []
    for f in files:
        try:
            data = yaml.safe_load(f.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            print(f"ERROR  bad-yaml: {f}: {exc}")
            errors += 1
            continue
        if not isinstance(data, dict):
            continue
        if "approvalId" in data:
            schema_name = "human-approval"
        elif data.get("kind") in KIND_TO_SCHEMA and str(data.get("apiVersion", "")).startswith("agents.cpintl.org/"):
            schema_name = KIND_TO_SCHEMA[data["kind"]]
        else:
            continue  # not an agent file
        problems = list(jsonschema.Draft202012Validator(load_schema(schema_name)).iter_errors(data))
        for err in problems:
            loc = ".".join(str(x) for x in err.path) or "top level"
            print(f"ERROR  bad-value: {f}: {loc}: {err.message}")
        errors += len(problems)
        if not problems:
            print(f"OK     {f} ({data.get('kind', 'HumanApproval')})")
            if "kind" in data:
                known.add((data["kind"], data["metadata"]["name"]))
                docs.append((f, data))
    for f, data in docs:
        for field in REF_FIELDS.get(data["kind"], ()):
            ref = data["spec"].get(field)
            if ref and (ref["kind"], ref["name"]) not in known:
                print(f"ERROR  broken-reference: {f}: {field} points to {ref['kind']} '{ref['name']}' which was not found in the files checked")
                errors += 1
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
