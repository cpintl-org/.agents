# Agent skill resource guidance

## When to use

Read this file when a task asks to find, design, update, package, or document reusable skills. A skill must be a self-contained directory with a required `SKILL.md` and optional `scripts/`, `references/`, and `templates/` resources.

## Progressive disclosure

Keep `SKILL.md` concise and under 500 lines. Put detailed variants into one-level-deep reference files. Put deterministic utilities in `scripts/` and reusable output boilerplate in `templates/`. Do not duplicate the same rule in several files. Do not add user-facing `README.md` or `CHANGELOG.md` files to the skill package unless the skill system explicitly requires them; use a reference file for source notes instead.

## Skill metadata

The YAML frontmatter must contain:

```yaml
name: cpintl-org-writing-skill
description: What the skill does and when to use it.
```

The description is the primary trigger mechanism. State both capability and triggering tasks. Keep it provider-neutral where possible.

## Quality checklist

Before delivery:

- Confirm the directory contains `SKILL.md`.
- Remove placeholder example files.
- Check every linked reference exists.
- Test every script with valid and invalid inputs.
- Validate all YAML and JSON templates.
- Search for secrets, user-specific identifiers, and unexplained domain nouns.
- Run the official skill validator.
- Package the skill with its directory root preserved.

## Applicability

Write instructions for any compatible agent, not for one named assistant or one private account. State which tools or command-line interfaces are optional, and provide a safe fallback when they are unavailable.
