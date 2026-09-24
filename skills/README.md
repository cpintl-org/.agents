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

## Validation

Each skill ships its own deterministic checker where useful (see its `scripts/`), but the
repository workflow (`.github/workflows/skill-validation.yml`) is the authoritative gate. It
requires:

- `SKILL.md` under 500 lines with YAML frontmatter containing `name` and `description`.
- Every `references/`, `scripts/`, or `templates/` path linked in `SKILL.md` to exist.
- YAML/JSON structure to parse, the prompt / agent-YAML / memory-request / bridge validators to
  pass, a clean secrets and unsafe-path scan, and no trailing whitespace (`git diff --check`).

Run the same checks locally from the repository root before pushing — see `AGENTS.md` →
"Verify before committing" for the exact command list (use `python3` on this machine).

## Skills for agent work

| Skill | Use it to |
|---|---|
| `cpintl-org-brand` | Apply the official CPI palette, logos, and department icons to Docs/Sheets/Slides, cover pages, and CPI-branded material |
| `cpintl-org-writing-skill` | Keep names, repository structure, APIs, and MCP wiring consistent across cpintl-org |
| `google-workspace-free-serverless` | Design quota-safe, zero-billing Workspace systems (audit/implement) |
| `github-repository-operations` | Manage GitHub repos, pull requests, branches, and Actions safely for non-coders |
| `workspace-drive-search` | Find approved Drive resources through the read-only bridge |
| `prompt-authoring` | Save and check reusable prompts |
| `memory-search` | Recall approved facts with source and freshness (read-only) |
| `agent-task-planning` | Plan a task with a workspace, policy, model, and approval |
