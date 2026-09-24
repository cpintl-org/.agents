# `.agents` — cpintl-org Agent Resources Hub

`.agents` is a provider-neutral repository for reusable agent **brains**, **skills**, **guardrails**, **templates**, **memory schemas**, and Google Workspace bridge. It is designed for non-coders who can edit Google Docs, Google Drive, Markdown, or GitHub files. The repository stores instructions and configuration templates; it is not a database for beneficiary records, a secret manager, or a promise of unlimited free hosting.

## What is This Hub?

Think of ```.agents``` as a master AI Control Panel.

Instead of locking my AI setups inside a single app (like only using ChatGPT or only using Gemini), this repository acts as a single, universal storage unit. So any no coder can write my prompts, skills, and rules here, and they automatically sync with your Google Workspace (Docs, Sheets, Shared Drives).

From here, you can connect your agent setup to any AI provider—including Gemini, Google AI Studio, Claude, OpenAI, GitHub Copilot, DeepSeek, or local tools—without ever re-writing your instructions!

## How Everything Fits Together

We structure everything like Lego Blocks. Each component does one specific job, and you can snap them together to build any AI agent you want!

```
┌────────────────────────────────────────────────────────────────────────┐
│                              AGENT BRAIN                               │
│                   (Personality, Role & Instructions)                   │
└──────────────────┬─────────────────────────────────┬───────────────────┘
                   │                                 │
                   ▼                                 ▼
┌─────────────────────────────────────┐   ┌──────────────────────────────┐
│               SKILLS                │   │          GUARDRAILS          │
│   (Tools, Actions & Capabilities)   │   │  (Safety Rules & Boundaries) │
└──────────────────┬──────────────────┘   └──────────────┬───────────────┘
                   │                                     │
                   └──────────────────┬──────────────────┘
                                      │
                                      ▼
┌────────────────────────────────────────────────────────────────────────┐
│                               TEMPLATES                                │
│                     (Google Docs / Sheets Outputs)                     │
└────────────────────────────────────────────────────────────────────────┘

```

## How GitHub & Google Workspace Connect in Real Time

You don't need to manually copy and paste text between GitHub and Google Docs!

```text
┌────────────────────────┐      Webhook Signal     ┌────────────────────────┐
│   GitHub (.agents)     │ ──────────────────────> │   Google Apps Script   │
│  Edit Markdown File    │                         │   (workspace-bridge)   │
└────────────────────────┘                         └───────────┬────────────┘
                                                               │
                                                               ▼
                                                   ┌────────────────────────┐
                                                   │   Google Shared Drive  │
                                                   │  Real-Time Updated Doc │
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
| Configure GitHub-to-Workspace mapping | [`config/mcp-bridge-mapping.yaml`](config/mcp-bridge-mapping.yaml) |
| Deploy the optional bridge | [`workspace-bridge/README.md`](workspace-bridge/README.md) |
| Manage GitHub without coding | [`skills/github-repository-operations/SKILL.md`](skills/github-repository-operations/SKILL.md) |
| Understand the agent layers in plain words | [`docs/plain-language-guide.md`](docs/plain-language-guide.md) |
| Plan an agent task (Google Sheets, no coding) | [`templates/agent-control-panel/README.md`](templates/agent-control-panel/README.md) |
| Save a reusable prompt | [`prompts/README.md`](prompts/README.md) |
| Choose or switch an AI provider | [`providers/README.md`](providers/README.md) |
| Check whether a result was good and safe | [`evaluation/README.md`](evaluation/README.md) |
| See what comes next | [`docs/roadmap.md`](docs/roadmap.md) |

## How the pieces fit together

A **brain** defines an agent’s role and working method. A **skill** supplies a repeatable procedure. **Guardrails** define what is forbidden or requires review. **Templates** standardize outputs. **Memory** provides bounded, expiring context. The optional **workspace bridge** synchronizes approved repository paths with Google Drive after an owner deploys and configures it.

Three newer layers make agent work safer and easier to repeat. **Prompt files** save a good instruction with declared inputs and outputs. **Task, Workspace, Policy, and Model Adapter** files say what to do, what may be used, what is allowed, and which AI (or a person) does it. **Provenance-aware memory** shows where every remembered fact came from and whether it is still current. **Evaluation** records how each run went. `docs/plain-language-guide.md` explains all of them without technical terms.

The system is provider-agnostic. The same instructions may be used with Gemini, Claude, OpenAI-compatible services, local models, or no model at all. A provider is never assumed to be available, free, private, or suitable for restricted data. Every integration must have a manual fallback.

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
├── docs/
│   ├── no-coder-maintenance.md
│   ├── plain-language-guide.md        # Words and steps, no jargon
│   ├── roadmap.md                     # What is done, what is next
│   └── configure-google-appsscript-workspace-bridge.md
├── brains/
│   ├── README.md
│   ├── research-agent.md
│   └── doc-writer-agent.md
├── skills/
│   ├── README.md
│   ├── cpintl-org-writing-skill/       # Naming, structure, technical writing
│   ├── cpintl-org-brand/               # CPI palette, logos, department icons, covers
│   ├── google-workspace-free-serverless/ # Quota-safe Workspace patterns
│   ├── github-repository-operations/  # No-coder GitHub management
│   ├── workspace-drive-search/         # Approved Drive search contract and validator
│   ├── prompt-authoring/               # Write and check .prompt files
│   ├── memory-search/                  # Read-only memory with source and freshness
│   └── agent-task-planning/            # Fill Task, Workspace, Policy, Model, Approval
├── prompts/
│   ├── README.md
│   ├── diagnostics.md
│   ├── schemas/                        # Rules for the prompt header
│   └── library/                        # Example prompt, shared pieces, schemas, test cases
├── schemas/                            # Neutral rulebooks: task, workspace, policy, model, run, lifecycle
├── providers/
│   ├── README.md
│   ├── provider-catalog.yaml           # Checklist of providers (verify before use)
│   └── adapters/                       # One small file per provider, plus a no-AI default
├── guardrails/
│   ├── README.md
│   ├── security-rules.yaml
│   ├── adoption-boundaries.md          # What we learn from and what we never copy
│   └── data-retention-policy.md
├── templates/
│   ├── README.md
│   ├── google-docs-outline.md
│   ├── google-sheets-schema.json
│   ├── agent-task.yaml                 # Plain templates: task, workspace, policy,
│   ├── agent-workspace.yaml            #   model adapter, agent template, run status,
│   ├── ...                             #   checkpoint policy, human approval
│   └── agent-control-panel/            # Google Sheets tabs (CSV) and a request form outline
├── memory/
│   ├── README.md
│   ├── provenance-and-freshness.md
│   ├── short-term-memory-schema.json
│   └── *.schema.json                   # memory record, search result, source, freshness
├── evaluation/
│   ├── README.md
│   ├── rubrics/                        # Human review checklist
│   └── *.schema.json                   # test case, rubric, run record
└── workspace-bridge/
    ├── README.md
    ├── appsscript.json
    ├── Code.gs
    └── clasp.json
```

## No-coder workflow

Describe the desired outcome in plain language. A maintainer can prepare a temporary working branch, run checks, open a pull request, merge an approved change into `main`, and delete the temporary branch. The only permanent branch is `main`. Normal contributors should not push directly to it; an authorized administrator may bypass the rule only for controlled recovery or testing.

When adding a brain, define role, goal, inputs, boundaries, evidence, output, and escalation. When adding a skill, create a lowercase kebab-case folder with a concise `SKILL.md`; move detailed material into references and reusable structures into templates. When adding a guardrail, state the data class, prohibited action, approval requirement, and fallback. When adding a template, keep facts out of it and retain placeholders until verified.

## Workspace bridge reality

The bridge is optional and is not automatically active merely because `workspace-bridge/` exists. The owner must deploy Apps Script, set Script Properties, verify the Drive folder IDs, configure GitHub secrets, run a synthetic dry-run, and approve any write mode. The default bridge mapping is read-only and uses placeholders. Without an endpoint and secrets, the sync workflow intentionally skips external delivery.

The bridge should be treated as event-assisted synchronization, not a guaranteed real-time or enterprise service. GitHub remains the canonical source for repository files. Drive is a mapped copy or working view. Do not store secrets, restricted case data, health information, or OAuth tokens in this repository.

## Security and provider independence

The repository rejects hardcoded secrets, unsafe paths, fabricated provider IDs, unrestricted external writes, and unreviewed destructive actions. See [`SECURITY.md`](SECURITY.md) and [`guardrails/security-rules.yaml`](guardrails/security-rules.yaml). AI is optional: redact data first, use approved providers only, require human review for consequential outputs, and preserve a no-AI path.

## Validation

The validation workflow runs on pull requests, pushes to `main`, manual runs, and a weekly schedule. It checks skill metadata and references, the free-resource evidence matrix, YAML/JSON structure, prompt files, agent task templates, model adapters, memory requests, likely secret patterns, unsafe paths, and whitespace. The workspace workflow validates the bridge mapping and skips external dispatch when secrets are not configured.

For local validation, run:

```bash
# Verify free resource matrix and bridge schema
python skills/google-workspace-free-serverless/scripts/verify_free_matrix.py skills/google-workspace-free-serverless/references/free-resource-matrix.md
python skills/workspace-drive-search/scripts/validate_bridge_request.py skills/workspace-drive-search/references/example-request.json

# Validate prompt library, agent YAML templates, and memory requests
python skills/prompt-authoring/scripts/validate_prompts.py prompts/library
python skills/agent-task-planning/scripts/validate_agent_yaml.py templates providers/adapters
python skills/memory-search/scripts/validate_memory_request.py skills/memory-search/templates/memory-search-request.json

# Run offline bridge behavioral tests
node workspace-bridge/test-bridge.js

# Validate CPI brand skill assets (palette, 16 departments, Font Awesome icons, no stored covers)
python skills/cpintl-org-brand/scripts/validate_brand_assets.py
```


## Assumptions and boundaries

This repository intentionally uses placeholders for Google Drive folder IDs, Apps Script project IDs, tokens, domains, and Workspace roles. Current quotas, pricing, model availability, provider data-use terms, and API behavior must be verified at execution time. A green repository check proves structure and policy checks passed; it does not grant external authorization, prove a Drive mapping exists, or certify a production deployment.

Maintained by `cpintl-org` as a provider-neutral, no-coder agent resource hub.
