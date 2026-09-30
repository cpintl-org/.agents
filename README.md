# `.agents` — cpintl-org agent resources hub

`.agents` is a provider-neutral repository for reusable agent **brains**, **skills**, **guardrails**, **templates**, **memory schemas**, and an optional Google Workspace bridge. It is designed for non-coders who can edit Google Docs, Google Drive, Markdown, or GitHub files. The repository MUST be used only for instructions and configuration templates. It MUST NOT be used as a database for beneficiary records, a secret manager, or a promise of unlimited free hosting.

## What this hub is

`.agents` functions as a master AI control panel. Rather than locking an agent setup inside a single application, this repository acts as one universal storage unit: prompts, skills, and rules are written here and synchronized with Google Workspace (Docs, Sheets, Shared Drives). From here, the agent setup MAY connect to any AI provider — including Gemini, Google AI Studio, Claude, OpenAI, GitHub Copilot, DeepSeek, or local tools — without requiring the instructions to be rewritten.

## How the components fit together

```text
┌────────────────────────────────────────────────────────────────────────┐
│                              AGENT BRAIN                               │
│                   (Personality, role & instructions)                   │
└──────────────────┬─────────────────────────────────┬───────────────────┘
                    │                                 │
                    ▼                                 ▼
┌─────────────────────────────────────┐   ┌──────────────────────────────┐
│               SKILLS                │   │          GUARDRAILS          │
│   (Tools, actions & capabilities)   │   │  (Safety rules & boundaries) │
└──────────────────┬──────────────────┘   └──────────────┬───────────────┘
                    │                                     │
                    └──────────────────┬──────────────────┘
                                       │
                                       ▼
┌────────────────────────────────────────────────────────────────────────┐
│                               TEMPLATES                                │
│                     (Google Docs / Sheets outputs)                     │
└────────────────────────────────────────────────────────────────────────┘
```

## How GitHub and Google Workspace connect

```text
┌────────────────────────┐      Webhook signal      ┌────────────────────────┐
│   GitHub (.agents)      │ ──────────────────────>  │   Google Apps Script   │
│  Edit Markdown file     │                          │   (workspace-bridge)   │
└────────────────────────┘                           └───────────┬────────────┘
                                                                  │
                                                                  ▼
                                                      ┌────────────────────────┐
                                                      │   Google shared drive   │
                                                      │  Updated document copy │
                                                      └────────────────────────┘
```

## Start here

| If you want to… | Open |
|---|---|
| Understand the repository | This README and [`docs/no-coder-maintenance.md`](docs/no-coder-maintenance.md) |
| Create an agent role | [`brains/README.md`](brains/README.md) |
| Add a reusable capability | [`skills/README.md`](skills/README.md) |
| Apply safety and privacy rules | [`guardrails/README.md`](guardrails/README.md) |
| Produce a document or spreadsheet | [`templates/README.md`](templates/README.md) |
| Understand context retention | [`memory/README.md`](memory/README.md) |
| Configure the GitHub-to-Workspace mapping | [`config/mcp-bridge-mapping.yaml`](config/mcp-bridge-mapping.yaml) |
| Deploy the optional bridge | [`workspace-bridge/README.md`](workspace-bridge/README.md) |
| Manage GitHub without coding | [`skills/github-repository-operations/SKILL.md`](skills/github-repository-operations/SKILL.md) |
| Understand the agent layers in plain words | [`docs/plain-language-guide.md`](docs/plain-language-guide.md) |
| Plan an agent task (Google Sheets, no coding) | [`templates/agent-control-panel/README.md`](templates/agent-control-panel/README.md) |
| Save a reusable prompt | [`prompts/README.md`](prompts/README.md) |
| Choose or switch an AI provider | [`providers/README.md`](providers/README.md) |
| Check whether a result was good and safe | [`evaluation/README.md`](evaluation/README.md) |
| See what comes next | [`docs/roadmap.md`](docs/roadmap.md) |

## How the pieces fit together

A **brain** defines an agent's role and working method. A **skill** supplies a repeatable procedure. **Guardrails** define what is forbidden or requires review. **Templates** standardize outputs. **Memory** provides bounded, expiring context. The optional **workspace bridge** synchronizes approved repository paths with Google Drive after an owner deploys and configures it.

Three additional layers support repeatable, auditable agent work. **Prompt files** save an instruction with declared inputs and outputs. **Task**, **Workspace**, **Policy**, and **Model Adapter** files declare what to do, what may be used, what is permitted, and which AI (or person) performs it. **Provenance-aware memory** records where a remembered fact came from and whether it remains current. **Evaluation** records how each run went. See [`docs/plain-language-guide.md`](docs/plain-language-guide.md) for a non-technical explanation of each layer.

The system MUST remain provider-agnostic. The same instructions MAY be used with Gemini, Claude, OpenAI-compatible services, local models, or no model at all. A provider MUST NOT be assumed to be available, free, private, or suitable for restricted data. Every integration MUST have a manual fallback.

## Repository tree

```text
.agents/
├── README.md
├── LICENSE
├── SECURITY.md
├── .github/workflows/
│   ├── skill-validation.yml
│   └── workspace-sync.yml
├── config/
│   ├── naming-policy.yaml
│   ├── mcp-bridge-mapping.yaml
│   └── repository-manifest.yaml
├── scripts/
│   └── validate-all.sh                 # Runs every repository check in one command
├── plans/                              # One folder per planned agent task
├── docs/
│   ├── no-coder-maintenance.md
│   ├── plain-language-guide.md         # Plain-language explanation of the agent layers
│   ├── roadmap.md                      # Status of each build step
│   └── configure-google-appsscript-workspace-bridge.md
├── brains/
│   ├── README.md
│   ├── research-agent.md
│   └── doc-writer-agent.md
├── skills/
│   ├── README.md
│   ├── cpintl-org-writing-skill/        # Naming, structure, technical writing
│   ├── cpintl-org-brand/                # CPI palette, logos, department icons, covers
│   ├── google-workspace-free-serverless/ # Quota-safe Workspace patterns
│   ├── github-repository-operations/    # No-coder GitHub management
│   ├── workspace-drive-search/          # Approved Drive search contract and validator
│   ├── prompt-authoring/                # Write and check .prompt files
│   ├── memory-search/                   # Read-only memory with source and freshness
│   └── agent-task-planning/             # Fill Task, Workspace, Policy, Model, Approval
├── prompts/
│   ├── README.md
│   ├── diagnostics.md
│   ├── schemas/                         # Rules for the prompt header
│   └── library/                         # Example prompt, shared pieces, schemas, test cases
├── schemas/                             # Neutral rulebooks: task, workspace, policy, model, run, lifecycle
│   ├── csv/                             # Control-panel CSV row schemas
│   └── scripts/                         # Shared validators (skill packages, CSVs, data, hygiene)
├── providers/
│   ├── README.md
│   ├── provider-catalog.yaml            # Checklist of providers; verify before use
│   └── adapters/                        # One file per provider, plus a no-AI default
├── guardrails/
│   ├── README.md
│   ├── security-rules.yaml
│   ├── adoption-boundaries.md           # What is adopted and what is deliberately excluded
│   └── data-retention-policy.md
├── templates/
│   ├── README.md
│   ├── google-docs-outline.md
│   ├── google-sheets-schema.json
│   ├── agent-task.yaml                  # Task, workspace, policy,
│   ├── agent-workspace.yaml             #   model adapter, agent template, run status,
│   ├── ...                              #   checkpoint policy, human approval
│   └── agent-control-panel/             # Google Sheets tabs (CSV) and a request form outline
├── memory/
│   ├── README.md
│   ├── provenance-and-freshness.md
│   ├── short-term-memory-schema.json
│   └── *.schema.json                    # Memory record, search result, source, freshness
├── evaluation/
│   ├── README.md
│   ├── rubrics/                         # Human review checklist
│   └── *.schema.json                    # Test case, rubric, run record
└── workspace-bridge/
    ├── README.md
    ├── appsscript.json
    ├── Code.gs
    └── clasp.json
```

## No-coder workflow

Describe the desired outcome in plain language. A maintainer MAY prepare a temporary working branch, run checks, open a pull request, merge an approved change into `main`, and delete the temporary branch. `main` MUST be the only permanent branch. Contributors SHOULD use a pull request rather than push directly to `main`; an authorized administrator MAY bypass this rule only for controlled recovery or testing.

When adding a brain, the definition MUST state role, goal, inputs, boundaries, evidence, output, and escalation. When adding a skill, create a lowercase kebab-case folder with a concise `SKILL.md`; move detailed material into references and reusable structures into templates. When adding a guardrail, state the data class, prohibited action, approval requirement, and fallback. When adding a template, the template MUST NOT contain facts; it MUST retain placeholders until a value is verified.

## Workspace bridge status

The bridge is optional and MUST NOT be assumed active merely because `workspace-bridge/` exists. The owner MUST deploy Apps Script, set Script Properties, verify the Drive folder IDs, configure GitHub secrets, run a synthetic dry-run, and approve any write mode before the bridge processes real data. The default bridge mapping is read-only and uses placeholders. Without an endpoint and secrets, the sync workflow MUST intentionally skip external delivery.

The bridge SHOULD be treated as event-assisted synchronization, not a guaranteed real-time or enterprise service. GitHub remains the canonical source for repository files; Drive is a mapped copy or working view. Secrets, restricted case data, health information, and OAuth tokens MUST NOT be stored in this repository.

## Security and provider independence

The repository MUST reject hardcoded secrets, unsafe paths, fabricated provider IDs, unrestricted external writes, and unreviewed destructive actions — see [`SECURITY.md`](SECURITY.md) and [`guardrails/security-rules.yaml`](guardrails/security-rules.yaml). AI use is optional: data MUST be redacted first, only approved providers MAY be used, consequential outputs MUST require human review, and a no-AI path MUST be preserved.

## Validation

The validation workflow runs on pull requests, pushes to `main`, manual runs, and a weekly schedule. It checks skill metadata and references, the naming policy, the free-resource evidence matrix, YAML/JSON structure, prompt files, agent task templates, model adapters, memory and bridge requests, control-panel CSVs, committed data files, secret patterns, unsafe paths, bridge safe defaults, and whitespace. The workspace sync workflow validates the bridge mapping and MUST skip external dispatch when secrets are not configured.

Run every check locally with one command, which mirrors the CI workflow:

```bash
bash scripts/validate-all.sh
```

On this machine, use `python3` (`python` is the CI interpreter; the runner selects the correct one automatically; `PYTHON=python bash scripts/validate-all.sh` forces the CI-style interpreter). The same checks are also available individually:

```bash
# Verify the free-resource matrix and bridge schema
python3 skills/google-workspace-free-serverless/scripts/verify_free_matrix.py skills/google-workspace-free-serverless/references/free-resource-matrix.md
python3 skills/workspace-drive-search/scripts/validate_bridge_request.py skills/workspace-drive-search/references/example-request.json

# Validate the prompt library, agent YAML templates, and memory requests
python3 skills/prompt-authoring/scripts/validate_prompts.py prompts/library
python3 skills/agent-task-planning/scripts/validate_agent_yaml.py templates providers/adapters
python3 skills/memory-search/scripts/validate_memory_request.py skills/memory-search/templates/memory-search-request.json

# Run offline bridge behavioral tests
node workspace-bridge/test-bridge.js

# Validate CPI brand skill assets (palette, 16 departments, Font Awesome icons, no stored covers)
python3 skills/cpintl-org-brand/scripts/validate_brand_assets.py
```

## Assumptions and boundaries

This repository intentionally uses placeholders for Google Drive folder IDs, Apps Script project IDs, tokens, domains, and Workspace roles. Current quotas, pricing, model availability, provider data-use terms, and API behavior MUST be verified at execution time. A passing repository check proves structure and policy checks passed; it does not grant external authorization, prove a Drive mapping exists, or certify a production deployment.

Maintained by `cpintl-org` as a provider-neutral, no-coder agent resource hub.
