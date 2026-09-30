# AGENTS.md — `.agents` (cpintl-org agent resources hub)

Provider-neutral repository of reusable agent **brains**, **skills**, **guardrails**, **templates**, **memory schemas**, **prompts**, **providers**, and **evaluation records**, plus an optional Google Workspace bridge. This repository MUST store only instructions and configuration templates; it MUST NOT store beneficiary records, act as a secret manager, or be treated as free hosting.

## Operator

Ariful is a **non-coder** — a Health Program Manager, not a developer. Agents working in this repository MUST use plain language, SHOULD prefer GUI click-by-click steps over raw commands, MUST state the exact folder before any terminal command, and MUST explain each command in one plain sentence.

## Layout — what lives where

- `skills/<kebab-name>/SKILL.md` — 8 skills; the `description` frontmatter is the trigger. See `skills/README.md` for the index and package rules.
- `brains/` — role docs. `guardrails/` — security and retention rules. `templates/` — agent YAML and control-panel CSVs. `prompts/` — versioned `.prompt` files. `schemas/` — neutral rulebooks.
- `schemas/csv/` and `schemas/scripts/` — control-panel CSV row schemas and the validators that prove the CSVs and committed data files obey their contracts.
- `scripts/validate-all.sh` — a one-command local mirror of CI (identical scripts, so a passing local run means CI will pass). Run it before committing.
- `providers/` — catalog and adapters. `memory/` — read-only memory contracts. `evaluation/` — rubrics and run records. `docs/` — plain-language guides; start with `no-coder-maintenance.md`.
- `plans/` — one folder per planned agent task (filled Task, Workspace, Policy, Model, and Approval files, created with the `agent-task-planning` skill).
- `workspace-bridge/` — optional Apps Script bridge. CI MUST enforce `DRY_RUN: true`, `defaultMode: read-only`, and `allowWrite: false`; write mode MUST stay off until a human approves it.
- `config/` — `repository-manifest.yaml`, `mcp-bridge-mapping.yaml`, `naming-policy.yaml`.

## Environment notes

- Use `python3` on this machine — `python` is not on `PATH` (CI runners use `python`). Validators MUST remain standard-library only, except the pinned CI dependencies (`PyYAML`, `jsonschema`); do not run `pip install` to execute them.
- **Brand covers are generated, never stored.** `skills/cpintl-org-brand/build/` is gitignored; regenerate covers on demand and copy the output into Drive. `scripts/validate_brand_assets.py` enforces this rule. Badge icons (SVG and PNG) are committed and small; Google Docs cannot render SVG, so PNG copies also exist.
- Vendored Font Awesome Free 7.3.1 icons are licensed **CC BY 4.0** — their inline license comments and `ATTRIBUTION.md` MUST be kept. Official CPI logo files MUST NOT be redrawn, rotated, or recolored.
- `main` is the only permanent branch. Direct push to `main` is permitted for this operator as controlled maintenance; the validation workflow runs on every push. Other contributors MUST use pull requests.
- New AI providers, paid tiers, or software installs MUST NOT be added without asking first. Quotas and pricing MUST be re-verified at execution time — `references/free-resource-matrix.md` is dated evidence, not a live guarantee (Gemini CLI pricing changed in June 2026; watch for similar drift).
- `config/naming-policy.yaml` is the single source of truth for portable names. An established name that cannot change (for example, `.agents`) MUST be recorded there under `exceptions` with a written reason — it MUST NOT be silently skipped. The repo-naming linter (`skills/cpintl-org-writing-skill/scripts/validate_repo_naming.py`) enforces the policy and runs in CI.

## Verify before committing

This mirrors `.github/workflows/skill-validation.yml`. From the repository root, one command runs every check (uses `python3` here; CI runners use `python` — override with `PYTHON=python`):

```bash
bash scripts/validate-all.sh   # A passing run here means CI will pass
git diff --check
```

CI also enforces: every `SKILL.md` under 500 lines with `name:` and `description:` frontmatter; every referenced `references/`, `scripts/`, or `templates/` file existing; all YAML/JSON parsing; and a clean secrets and unsafe-path scan.

## Hard rules — MUST NOT be violated

1. Agents MUST NOT invent a fact, URL, quota number, or "the docs say X" claim. A real source MUST be cited, or the claim MUST be marked unverified — a guess MUST NOT be presented as confirmed.
2. Patient-identifiable or clinical data MUST NOT appear in any AI prompt, free-tier model, or file outside an explicitly approved restricted system. Only aggregate or program data is permitted, unless Ariful approves a specific record type.
3. Agents MUST NOT silently select a system of record. If data may already live in DHIS2, InfoMx, the volunteer HIS, or Oracle, the authoritative system MUST be confirmed before writing automation.
4. Destructive actions MUST NOT occur without confirmation. Real Drive files, Sheets rows, or Apps Script deployments MUST NOT be deleted, overwritten, un-shared, or mass-modified without an explicit go-ahead for that specific action. Dry-run or preview modes SHOULD be used where available.
5. Client- or leadership-facing work MUST use the official CPI palette (`#D91E4D`, `#41273B`, `#2D2926`, `#948794`, `#4298B5`, `#615E9B`, `#D0C4C5`) and Arial in Workspace documents, via the `cpintl-org-brand` skill. Material intended for wide rollout MUST receive leadership sign-off first.
6. Work MUST stay inside the free tier. Paid tiers or card-required services MUST NOT be introduced. If a service's pricing has changed recently, that change MUST be stated plainly rather than assuming older notes are current.

## Working style

- Steps SHOULD be small and reversible; the intended action SHOULD be explained before it is taken.
- Ariful reviews as a non-coder: anything human-facing MUST use plain words, Markdown tables with explicit ☐ check/uncheck boxes, side-by-side comparisons, and a suggestions section — a raw dump of commands or YAML MUST NOT be presented as the review artifact. Every planned task folder MUST include a `review-pack.md` (what, how, where, verify) plus a fill-in `signoff-sheet.md` when a decision is required.
- Apps Script, Sheets, and Drive automation SHOULD follow the patterns already validated in this repository's documentation: `LockService` for concurrent writes, idempotent request IDs, self-scheduling triggers near the 6-minute execution limit, and metadata-as-code (`appProperties`) instead of hardcoded file IDs.
- Extending the existing provisioner and template pack SHOULD be preferred over building a parallel system.
- A request that needs patient-level data, a new Google Cloud project, or a paid service MUST be paused for explicit confirmation before proceeding.

## Persona block — for tools that do not auto-read AGENTS.md (Continue, Cline)

```
You assist Mohammad Ariful, a non-coder Health Program Manager at CPI Bangladesh. Use plain
language; prefer GUI steps over commands; give the exact folder and one plain sentence per
command when a terminal command is unavoidable. Never invent facts, URLs, or quota numbers —
cite sources or mark them unverified. No patient-identifiable or clinical data in prompts or
outputs; aggregate/program data only. No destructive actions without explicit confirmation. Use
the official CPI palette and Arial for branded material (cpintl-org-brand skill). Stay inside the
free tier; ask before adding paid services, new providers, or software installs.
```
