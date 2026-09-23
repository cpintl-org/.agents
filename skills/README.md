# Reusable skills

A skill is a self-contained `SKILL.md` plus optional `references/`, `scripts/`, and `templates/` resources. The metadata description is the trigger; the body is the compact procedure; references are loaded only when needed.

## Required package rules

- Use lowercase ASCII kebab-case for the skill directory.
- Include YAML frontmatter with `name` and `description`.
- Keep `SKILL.md` under 500 lines and write imperative instructions.
- Do not include a README or changelog inside an individual skill package.
- Do not hardcode secrets, opaque IDs, or provider assumptions.
- Add deterministic scripts only when they are tested and useful.
- Link every referenced resource with a repository-relative path.
- Include a no-provider or manual fallback for integrations.

Validate with:

```bash
python /home/ubuntu/skills/skill-creator/scripts/quick_validate.py skills/{skill-name}
```

The repository workflow also checks metadata, references, free-resource evidence, likely secrets, unsafe paths, and whitespace.
