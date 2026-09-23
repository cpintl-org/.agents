#!/usr/bin/env python3
"""Validate bundled JSON/YAML resources and required skill links."""
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
errors = []
required = [
    root / 'SKILL.md',
    root / 'references' / 'portable-standard.md',
    root / 'references' / 'github-standard.md',
    root / 'references' / 'workspace-standard.md',
    root / 'references' / 'api-mcp-standard.md',
    root / 'references' / 'writing-style-guidance.md',
    root / 'references' / 'agent-skill-resources.md',
    root / 'references' / 'governance-and-validation.md',
    root / 'scripts' / 'validate_names.py',
    root / 'scripts' / 'generate_bridge_uri.py',
]
for path in required:
    if not path.exists():
        errors.append(f'missing required file: {path.relative_to(root)}')

for path in root.rglob('*.json'):
    try:
        json.loads(path.read_text(encoding='utf-8'))
    except Exception as exc:
        errors.append(f'invalid JSON {path.relative_to(root)}: {exc}')

try:
    import yaml
    for path in root.rglob('*.yaml'):
        try:
            yaml.safe_load(path.read_text(encoding='utf-8'))
        except Exception as exc:
            errors.append(f'invalid YAML {path.relative_to(root)}: {exc}')
except ImportError:
    errors.append('PyYAML is required to validate YAML resources')

skill = (root / 'SKILL.md').read_text(encoding='utf-8')
if not skill.startswith('---\nname: cpintl-org-writing-skill\n'):
    errors.append('SKILL.md frontmatter does not start with the expected skill name')
if len(skill.splitlines()) >= 500:
    errors.append('SKILL.md must remain under 500 lines')
for _, match in re.findall(r'\[([^\]]+)\]\((references/[^)]+)\)', skill):
    if not (root / match).exists():
        errors.append(f'broken reference link: {match}')
for path in root.rglob('*'):
    if path.is_file() and path.name not in {'validate_resources.py'}:
        text = path.read_text(encoding='utf-8', errors='ignore')
        if re.search(r'(?i)(api[_-]?key|secret|private[_-]?key|access[_-]?token)\s*[:=]\s*[^\{\"\']', text):
            errors.append(f'possible embedded secret-like value: {path.relative_to(root)}')
if errors:
    for error in errors:
        print(f'ERROR: {error}')
    raise SystemExit(1)
print('Resource validation passed')
