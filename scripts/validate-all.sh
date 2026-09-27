#!/usr/bin/env bash
#
# Run every repository check in one command.
#
# This is the local mirror of the "Validate agent skills" GitHub Actions
# workflow. Both call the same scripts, so a green run here means CI will be
# green too. Run it from anywhere; it locates the repository itself.
#
# Usage:
#   bash scripts/validate-all.sh
#   PYTHON=python bash scripts/validate-all.sh    # if python3 is unavailable
#
# Exit code is 0 only when every check passes.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${REPO_ROOT}" || exit 1

# ---------------------------------------------------------------- interpreter
if [[ -n "${PYTHON:-}" ]]; then
  PY="${PYTHON}"
elif command -v python3 >/dev/null 2>&1; then
  PY=python3
elif command -v python >/dev/null 2>&1; then
  PY=python
else
  echo "ERROR: no python interpreter found. Install Python 3 or set PYTHON=..." >&2
  exit 1
fi

echo "Repository : ${REPO_ROOT}"
echo "Python     : $(${PY} --version 2>&1)"
echo

# ------------------------------------------------------------- dependencies
missing=""
for module in yaml jsonschema; do
  if ! "${PY}" -c "import ${module}" >/dev/null 2>&1; then
    missing="${missing} ${module}"
  fi
done
if [[ -n "${missing}" ]]; then
  echo "ERROR: missing Python module(s):${missing}" >&2
  echo "       install them with: ${PY} -m pip install PyYAML jsonschema" >&2
  echo "       (do not install anything without asking first)" >&2
  exit 1
fi

if ! command -v node >/dev/null 2>&1; then
  echo "WARNING: node not found, the offline bridge tests will be skipped." >&2
  echo "         Install Node.js to run them, or ignore this warning." >&2
  echo
fi

PASSED=0
FAILED=0
FAILED_NAMES=()

run_check() {
  local name="$1"
  shift
  echo "--- ${name}"
  if "$@"; then
    PASSED=$((PASSED + 1))
  else
    FAILED=$((FAILED + 1))
    FAILED_NAMES+=("${name}")
  fi
  echo
}

# ------------------------------------------------------------------- checks
run_check "Skill packages (metadata + bundled references)" \
  "${PY}" schemas/scripts/validate_skill_packages.py

run_check "Naming policy (config/naming-policy.yaml)" \
  "${PY}" skills/cpintl-org-writing-skill/scripts/validate_repo_naming.py

run_check "CPI brand assets" \
  "${PY}" skills/cpintl-org-brand/scripts/validate_brand_assets.py

run_check "Free-resource matrix evidence" \
  "${PY}" skills/google-workspace-free-serverless/scripts/verify_free_matrix.py \
  skills/google-workspace-free-serverless/references/free-resource-matrix.md

run_check "Prompt library" \
  "${PY}" skills/prompt-authoring/scripts/validate_prompts.py prompts/library

run_check "Agent YAML templates and provider adapters" \
  "${PY}" skills/agent-task-planning/scripts/validate_agent_yaml.py \
  templates providers/adapters

run_check "Memory search request template" \
  "${PY}" skills/memory-search/scripts/validate_memory_request.py \
  skills/memory-search/templates/memory-search-request.json

run_check "Workspace bridge request fixture" \
  "${PY}" skills/workspace-drive-search/scripts/validate_bridge_request.py \
  skills/workspace-drive-search/references/example-request.json

run_check "Writing-skill bundled resources" \
  "${PY}" skills/cpintl-org-writing-skill/scripts/validate_resources.py

run_check "Naming-standard freshness register" \
  "${PY}" skills/cpintl-org-writing-skill/scripts/check_standards_freshness.py

run_check "Control panel CSVs against schemas/csv/" \
  "${PY}" schemas/scripts/validate_control_panel_csvs.py

run_check "Committed data files against their schemas" \
  "${PY}" schemas/scripts/validate_data_against_schemas.py

run_check "Repository hygiene (schemas, parse, secrets, paths, bridge defaults)" \
  "${PY}" schemas/scripts/validate_repo_hygiene.py

if command -v node >/dev/null 2>&1; then
  run_check "Workspace bridge offline behavioural tests" \
    node workspace-bridge/test-bridge.js
fi

run_check "No trailing-whitespace errors" \
  git diff --check

# ------------------------------------------------------------------ summary
echo "=============================================="
echo "passed: ${PASSED}   failed: ${FAILED}"
if [[ ${FAILED} -gt 0 ]]; then
  for name in "${FAILED_NAMES[@]}"; do
    echo "  FAILED: ${name}"
  done
  echo "=============================================="
  echo "Fix the messages above, then run this command again."
  exit 1
fi
echo "All checks passed. Safe to commit."