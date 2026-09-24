# AGENTS.md — `.agents` (cpintl-org agent resources hub)

Provider-neutral repository of reusable agent **brains, skills, guardrails, templates,
memory schemas, prompts, providers, evaluation records**, plus an optional Google Workspace
bridge. It stores instructions and configuration templates — **not** beneficiary records, a
secret manager, or free hosting.

> A second instruction file is loaded from the parent folder: `../AGENTS.md` (CPI Bangladesh
> Workspace). It governs the `GoogleDrive/` + `RawFiles/` → `processed/` → `output/context/`
> pipeline, including its read-only Drive rules. Follow it for that pipeline; this file governs
> the `.agents` repository itself.

## Operator

Ariful is a **non-coder** — a Health Program Manager, not a developer. Use plain language,
prefer GUI click-by-click steps over raw commands, state the exact folder before any terminal
command, and explain each command in one plain sentence.

## Layout — what lives where

- `skills/<kebab-name>/SKILL.md` — 8 skills; the `description` frontmatter is the trigger.
  See `skills/README.md` for the index and package rules.
- `brains/` role docs · `guardrails/` security/retention rules · `templates/` agent YAML +
  control-panel CSVs · `prompts/` versioned `.prompt` files · `schemas/` neutral rulebooks
- `providers/` catalog + adapters · `memory/` read-only memory contracts · `evaluation/`
  rubrics + run records · `docs/` plain-language guides (start with `no-coder-maintenance.md`)
- `workspace-bridge/` — optional Apps Script bridge. CI enforces `DRY_RUN ... true`,
  `defaultMode: read-only`, and `allowWrite: false`; write mode stays off until a human approves.
- `config/` — `repository-manifest.yaml`, `mcp-bridge-mapping.yaml`, `naming-policy.yaml`.

## Environment gotchas (agents would guess these wrong)

- Use `python3` on this machine — `python` is not on PATH (CI runners use `python`). Validators
  are standard-library only except the pinned CI deps (`PyYAML`, `jsonschema`); do not `pip install`
  to run them.
- **Brand covers are generated, never stored.** `skills/cpintl-org-brand/build/` is gitignored;
  regenerate on demand and copy outputs into Drive. `scripts/validate_brand_assets.py` enforces
  this. Badge icons (SVG+PNG) are committed and small; Docs cannot take SVG, so PNGs exist too.
- Vendored Font Awesome Free 7.3.1 icons are **CC BY 4.0** — keep their inline license comments
  and `ATTRIBUTION.md`. Official CPI logo files are never redrawn, rotated, or recolored.
- `main` is the only permanent branch. Direct push to `main` is permitted for this operator
  (controlled maintenance; the validation workflow runs on every push). Normal contributors use
  pull requests.
- No new AI providers, paid tiers, or software installs without asking first. Quotas/pricing must
  be re-verified at execution time — `references/free-resource-matrix.md` is dated evidence, not a
  live promise (Gemini CLI pricing changed in June 2026; watch for similar drift).

## Verify before committing

Mirror of `.github/workflows/skill-validation.yml`, from the repo root:

```bash
python3 skills/google-workspace-free-serverless/scripts/verify_free_matrix.py skills/google-workspace-free-serverless/references/free-resource-matrix.md
python3 skills/prompt-authoring/scripts/validate_prompts.py prompts/library
python3 skills/agent-task-planning/scripts/validate_agent_yaml.py templates providers/adapters
python3 skills/memory-search/scripts/validate_memory_request.py skills/memory-search/templates/memory-search-request.json
python3 skills/workspace-drive-search/scripts/validate_bridge_request.py skills/workspace-drive-search/references/example-request.json
python3 skills/cpintl-org-brand/scripts/validate_brand_assets.py
node workspace-bridge/test-bridge.js
git diff --check
```

CI also enforces: every `SKILL.md` under 500 lines with `name:`/`description:` frontmatter and
every `references|scripts|templates/...` file existing; all YAML/JSON parse; a clean
secrets/unsafe-path scan.

## Hard rules — never violate

1. **Never invent a fact, URL, quota number, or "the docs say X" claim.** Cite a real source or
   mark it unverified — never present a guess as confirmed.
2. **No patient-identifiable or clinical data** in any AI prompt, free-tier model, or file
   outside an explicitly approved restricted system. Aggregate/program data only, unless Ariful
   approves a specific record type.
3. **Don't silently pick a system of record.** If data may already live in DHIS2, InfoMx, the
   volunteer HIS, or Oracle, ask which system is authoritative before writing automation.
4. **No destructive actions without confirmation.** Never delete, overwrite, un-share, or
   mass-modify real Drive files, Sheets rows, or Apps Script deployments without an explicit
   go-ahead for that specific action. Prefer dry-run/preview modes.
5. **Brand compliance for client- or leadership-facing work:** official CPI palette (`#D91E4D`,
   `#41273B`, `#2D2926`, `#948794`, `#4298B5`, `#615E9B`, `#D0C4C5`) and Arial in Workspace docs —
   use the `cpintl-org-brand` skill. Anything for wide rollout needs leadership sign-off first.
6. **Stay inside the free tier.** No paid tiers or card-required services; say plainly when
   something's pricing changed recently instead of assuming old notes are current.

## Working style

- Small, reversible steps; explain what you're about to do before doing it.
- Apps Script / Sheets / Drive automation follows patterns already validated in this repo's docs:
  `LockService` for concurrent writes, idempotent request IDs, self-scheduling triggers near the
  6-minute execution limit, metadata-as-code (`appProperties`) instead of hard-coded file IDs.
- Prefer extending the existing provisioner and template pack over building a parallel system.
- If a request needs patient-level data, a new Google Cloud project, or a paid service, stop and ask.

## Persona block — for tools that don't auto-read AGENTS.md (Continue, Cline)

You assist Mohammad Ariful, a non-coder Health Program Manager at CPI Bangladesh. Use plain
language; prefer GUI steps over commands; give the exact folder and one plain sentence per
command when a terminal command is unavoidable. Never invent facts, URLs, or quota numbers — cite
sources or mark unverified. No patient-identifiable or clinical data in prompts or outputs;
aggregate/program data only. No destructive actions without explicit confirmation. Use the
official CPI palette and Arial for branded material (`cpintl-org-brand` skill). Stay inside the
free tier; ask before adding paid services, new providers, or software installs.