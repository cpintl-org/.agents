# `.agents` — cpintl-org Agent Resources Hub

`.agents` is a provider-neutral repository for reusable agent **brains**, **skills**, **guardrails**, **templates**, **memory schemas**, and an optional Google Workspace bridge. It is designed for non-coders who can edit Google Docs, Google Drive, Markdown, or GitHub files. The repository stores instructions and configuration templates; it is not a database for beneficiary records, a secret manager, or a promise of unlimited free hosting.

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

## How the pieces fit together

A **brain** defines an agent’s role and working method. A **skill** supplies a repeatable procedure. **Guardrails** define what is forbidden or requires review. **Templates** standardize outputs. **Memory** provides bounded, expiring context. The optional **workspace bridge** synchronizes approved repository paths with Google Drive after an owner deploys and configures it.

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
├── brains/
│   ├── README.md
│   ├── research-agent.md
│   └── doc-writer-agent.md
├── skills/
│   ├── README.md
│   ├── cpintl-org-writing-skill/       # Full skill with references, scripts, templates
│   ├── google-workspace-free-serverless/ # Quota-safe Workspace patterns
│   ├── github-repository-operations/  # No-coder GitHub management
│   └── workspace-drive-search/         # Approved Drive search contract and validator
├── guardrails/
│   ├── README.md
│   ├── security-rules.yaml
│   └── data-retention-policy.md
├── templates/
│   ├── README.md
│   ├── google-docs-outline.md
│   └── google-sheets-schema.json
├── memory/
│   ├── README.md
│   └── short-term-memory-schema.json
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

The validation workflow runs on pull requests, pushes to `main`, manual runs, and a weekly schedule. It checks skill metadata and references, the free-resource evidence matrix, YAML/JSON structure, likely secret patterns, unsafe paths, and whitespace. The workspace workflow validates the bridge mapping and skips external dispatch when secrets are not configured.

For local checks, use:

```bash
python /home/ubuntu/skills/skill-creator/scripts/quick_validate.py skills/{skill-name}
python skills/google-workspace-free-serverless/scripts/verify_free_matrix.py skills/google-workspace-free-serverless/references/free-resource-matrix.md
python skills/workspace-drive-search/scripts/validate_bridge_request.py skills/workspace-drive-search/references/example-request.json
```

## Assumptions and boundaries

This repository intentionally uses placeholders for Google Drive folder IDs, Apps Script project IDs, tokens, domains, and Workspace roles. Current quotas, pricing, model availability, provider data-use terms, and API behavior must be verified at execution time. A green repository check proves structure and policy checks passed; it does not grant external authorization, prove a Drive mapping exists, or certify a production deployment.

Maintained by `cpintl-org` as a provider-neutral, no-coder agent resource hub.
