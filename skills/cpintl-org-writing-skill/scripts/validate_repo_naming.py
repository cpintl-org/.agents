#!/usr/bin/env python3
"""Repo-wide lint for the naming rules in ``config/naming-policy.yaml``.

Wired into ``scripts/validate-all.sh`` and the CI workflow, so it runs on
every local check and every push. It only reports problems and never edits
files.

The policy file is the single source of truth for portable names. This checker
walks the repository and confirms that the names we control actually follow it:

* top-level directories and skill directory names match the ``directory`` profile
* every ``SKILL.md`` frontmatter ``name`` matches its directory name
* the repository owner and name match the ``repository`` profile
* ``mainOnly.defaultBranch`` is listed in ``mainOnly.permanentBranches``
* Workspace bridge configuration keys match ``environmentVariable``, and every
  key declared in ``Code.gs`` is documented in the deployment guide
* no two top-level directories differ only by letter case
* no checked name contains control characters or a trailing space/period

An established name that cannot be renamed (for example this repository's own
name) is allowed only when the policy file records it under ``exceptions`` with
a written reason. Nothing is silently skipped.

Usage:  python3 skills/cpintl-org-writing-skill/scripts/validate_repo_naming.py
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Set

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required (pip install PyYAML)", file=sys.stderr)
    raise SystemExit(1)

REPO_ROOT = Path(__file__).resolve().parents[3]
POLICY_PATH = REPO_ROOT / "config" / "naming-policy.yaml"
BRIDGE_CODE = REPO_ROOT / "workspace-bridge" / "Code.gs"
DEPLOY_GUIDE = REPO_ROOT / "docs" / "configure-google-appsscript-workspace-bridge.md"
WORKFLOWS = REPO_ROOT / ".github" / "workflows"
ENV_TOKEN = re.compile(r"\b[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)+\b")
DOC_KEY_ROW = re.compile(r"^\|\s*`([A-Z][A-Z0-9_]*)`\s*\|", re.MULTILINE)
WORKFLOW_SECRET_REF = re.compile(r"secrets\.([A-Za-z0-9_-]+)")


def parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check repository names against config/naming-policy.yaml"
    )
    parser.add_argument(
        "--policy", type=Path, default=POLICY_PATH, help="Path to the naming policy"
    )
    return parser.parse_args(argv)


def load_policy(path: Path) -> Dict:
    if not path.is_file():
        raise SystemExit(f"missing naming policy: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "profiles" not in data:
        raise SystemExit(f"malformed naming policy (no 'profiles' mapping): {path}")
    return data


def exception_keys(policy: Dict) -> Dict[str, str]:
    """Return {name: reason} for names the policy explicitly allows."""
    allowed: Dict[str, str] = {}
    for item in policy.get("exceptions") or []:
        if isinstance(item, dict) and "name" in item:
            allowed[str(item["name"])] = str(item.get("reason", "no reason recorded"))
    return allowed


def common_problems(value: str, rules: Dict) -> List[str]:
    """Profile-independent rules from the policy's ``rules`` block."""
    problems: List[str] = []
    if rules.get("rejectControlCharacters", True) and any(
        ord(ch) < 32 or ord(ch) == 127 for ch in value
    ):
        problems.append("contains a control character")
    if rules.get("rejectTrailingSpacesOrPeriods", True) and value.endswith((" ", ".")):
        problems.append("ends with a space or a period")
    if rules.get("rejectPathTraversal", True) and (
        "../" in value or value in {".", ".."}
    ):
        problems.append("contains a path traversal")
    return problems


def check(
    name: str, profile: str, kind: str, policy: Dict, errors: List[str], allowed: Dict
) -> None:
    patterns = policy.get("profiles") or {}
    if profile not in patterns:
        raise SystemExit(f"policy has no '{profile}' profile")
    rules = policy.get("rules") or {}

    for problem in common_problems(name, rules):
        errors.append(f"{kind} {name!r}: {problem}")

    if name in allowed:
        return
    if not re.fullmatch(str(patterns[profile]), name):
        errors.append(
            f"{kind} {name!r} does not match the {kind} profile {patterns[profile]!r}"
        )


def skill_frontmatter_name(skill_md: Path) -> str | None:
    try:
        text = skill_md.read_text(encoding="utf-8")
    except OSError:
        return None
    if not text.startswith("---\n"):
        return None
    for line in text.split("---\n", 2)[1].splitlines():
        if line.startswith("name:"):
            return line.split(":", 1)[1].strip().strip("\"'")
    return None


def declared_config_keys() -> Set[str]:
    """Read the authoritative Script Properties list from the bridge code."""
    if not BRIDGE_CODE.is_file():
        return set()
    text = BRIDGE_CODE.read_text(encoding="utf-8", errors="ignore")
    match = re.search(r"CONFIG_KEYS\s*=\s*\[(.*?)\]", text, re.DOTALL)
    if not match:
        return set()
    return set(ENV_TOKEN.findall(match.group(1)))


def documented_config_keys() -> Set[str]:
    """Read configuration keys named in the deployment guide's tables."""
    if not DEPLOY_GUIDE.is_file():
        return set()
    return set(DOC_KEY_ROW.findall(DEPLOY_GUIDE.read_text(encoding="utf-8", errors="ignore")))


def workflow_secrets() -> Set[str]:
    """Read GitHub Actions secret names referenced by the workflows."""
    if not WORKFLOWS.is_dir():
        return set()
    found: Set[str] = set()
    for path in sorted(WORKFLOWS.rglob("*.yml")) + sorted(WORKFLOWS.rglob("*.yaml")):
        found.update(WORKFLOW_SECRET_REF.findall(path.read_text(encoding="utf-8", errors="ignore")))
    return found


def main(argv: List[str] | None = None) -> int:
    args = parse_args(argv)
    policy = load_policy(args.policy)
    allowed = exception_keys(policy)
    errors: List[str] = []

    # 1. Top-level directories.
    top_dirs = sorted(
        p.name
        for p in REPO_ROOT.iterdir()
        if p.is_dir() and not p.name.startswith(".")
    )
    for name in top_dirs:
        check(name, "directory", "directory", policy, errors, allowed)

    # 2. Case-only collisions among top-level directories.
    lowered: Dict[str, str] = {}
    for name in top_dirs:
        if (policy.get("rules") or {}).get("rejectCaseOnlyCollisions", True):
            if name.lower() in lowered:
                errors.append(
                    f"directories {lowered[name.lower()]!r} and {name!r} differ only by case"
                )
            else:
                lowered[name.lower()] = name

    # 3. Skill directory names and their SKILL.md frontmatter agreement.
    skills_dir = REPO_ROOT / "skills"
    if skills_dir.is_dir():
        for skill_dir in sorted(p for p in skills_dir.iterdir() if p.is_dir()):
            check(skill_dir.name, "directory", "skill directory", policy, errors, allowed)
            skill_md = skill_dir / "SKILL.md"
            if not skill_md.is_file():
                errors.append(f"skill directory {skill_dir.name!r} has no SKILL.md")
                continue
            declared = skill_frontmatter_name(skill_md)
            if declared is None:
                errors.append(f"{skill_md.relative_to(REPO_ROOT)}: missing frontmatter 'name:'")
            elif declared != skill_dir.name:
                errors.append(
                    f"{skill_md.relative_to(REPO_ROOT)}: frontmatter name {declared!r} "
                    f"does not match its directory {skill_dir.name!r}"
                )

    # 4. Repository owner and name.
    manifest = REPO_ROOT / "config" / "repository-manifest.yaml"
    if manifest.is_file():
        data = yaml.safe_load(manifest.read_text(encoding="utf-8")) or {}
        repository = data.get("repository") or {}
        for field in ("owner", "name"):
            value = repository.get(field)
            if value:
                check(
                    str(value),
                    "repository",
                    f"repository {field}",
                    policy,
                    errors,
                    allowed,
                )
    else:
        errors.append("missing config/repository-manifest.yaml")

    # 5. main-only branch consistency.
    main_only = policy.get("mainOnly") or {}
    default_branch = main_only.get("defaultBranch")
    permanent = main_only.get("permanentBranches") or []
    if default_branch and permanent and default_branch not in permanent:
        errors.append(
            f"mainOnly.defaultBranch {default_branch!r} is not listed in "
            f"mainOnly.permanentBranches {permanent!r}"
        )

    # 6. Workspace bridge configuration keys and their documentation coverage.
    code_keys = declared_config_keys()
    doc_keys = documented_config_keys()
    if not code_keys:
        errors.append(f"no CONFIG_KEYS list found in {BRIDGE_CODE.relative_to(REPO_ROOT)}")
    if not doc_keys:
        errors.append(
            f"no configuration keys found in {DEPLOY_GUIDE.relative_to(REPO_ROOT)}"
        )

    for token in sorted(code_keys | doc_keys | workflow_secrets()):
        check(token, "environmentVariable", "configuration key", policy, errors, allowed)

    # A Script Property declared in code must be documented, and a documented
    # Script Property must still be declared in code. GitHub Actions secrets live
    # in a different namespace, so they are not expected in CONFIG_KEYS.
    for key in sorted(code_keys - doc_keys):
        errors.append(
            f"configuration key {key!r} is declared in Code.gs but is not documented "
            f"in {DEPLOY_GUIDE.name}"
        )
    for key in sorted((doc_keys - code_keys) - workflow_secrets()):
        errors.append(
            f"configuration key {key!r} is documented in {DEPLOY_GUIDE.name} but is "
            f"not declared in Code.gs CONFIG_KEYS"
        )

    if errors:
        print(f"FAIL: {len(errors)} naming problem(s)")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"PASS: repository names follow {args.policy.relative_to(REPO_ROOT)} "
        f"({len(top_dirs)} directories checked)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
