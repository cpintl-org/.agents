# URI-grounded naming standard for cpintl-org

## Why this file exists

A name is documentation. A human, a script, and an AI agent should all be able to look at a
path and know what it is without opening it. This file turns the open standards that make the
web and AI-agent ecosystems work — URIs, DNS, HTTP, TLS, JSON, and the current agent protocols
(MCP, A2A, AGENTS.md) — into one concrete naming rule for every name created inside
`cpintl-org` repositories, starting with `.agents`.

This file is normative. `references/portable-standard.md` and `references/github-standard.md`
still hold the character-level grammars; this file holds the decision of *which* grammar to use
*where*, and *why*, so a non-coder reviewer can check a proposed name against one rule instead of
several scattered ones.

## The rule

```text
org / repo / category / specific-thing.extension
```

- **org** — the GitHub organization, `cpintl-org`. Fixed; never re-decided per file.
- **repo** — the repository, e.g. `.agents`. One repository per distinct system or hub.
- **category** — the top-level folder a reader already recognizes: `brains`, `skills`,
  `guardrails`, `templates`, `memory`, `prompts`, `providers`, `evaluation`, `schemas`, `docs`,
  `plans`, `config`, `workspace-bridge`, `scripts`. A category answers "what kind of thing lives
  here", not "what project is this for" — project/topic goes inside the filename, not as a new
  top-level folder.
- **specific-thing.extension** — lowercase, hyphen-separated, no spaces, and an extension that
  matches the file's actual format, not its subject. The extension is what a script or agent
  parses first, before it ever reads the content.

This is the same logic DNS and URLs already use (a short number of fixed segments, most specific
last), applied one level below the organization boundary.

## Category → extension decision table

| If the file is... | Extension | Example (from this repo) |
|---|---|---|
| A human- or agent-readable instruction, role, or guide | `.md` | `brains/research-agent.md`, `AGENTS.md` |
| A reusable procedure an agent follows | `SKILL.md` inside `skills/<kebab-name>/` | `skills/prompt-authoring/SKILL.md` |
| A versioned instruction sent to a model | `.prompt` | `prompts/library/evidence-summary.prompt` |
| A machine-enforced rulebook / structural contract | `.schema.json` | `schemas/agent-task.schema.json` |
| Fill-in configuration a person edits directly | `.yaml` | `templates/agent-task.yaml`, `config/naming-policy.yaml` |
| A flat table meant for Google Sheets import | `.csv` | `templates/agent-control-panel/agent-tasks.csv` |
| A data record produced by a run (not hand-edited) | `.json` | `evaluation/example-run-record.json` |
| A deterministic utility a script runs | `.py` / `.sh` / `.gs` / `.js` | `scripts/validate-all.sh`, `workspace-bridge/Code.gs` |
| A GitHub Actions workflow | `.yml` under `.github/workflows/` | `.github/workflows/skill-validation.yml` |
| An OpenAPI-style API description | `.yaml` under a `references/` or `schemas/` folder | (none yet — apply when one is added) |

If a file doesn't fit a row, its category is wrong, not its extension — move it, don't invent a
new extension.

## Worked examples from the current repository

These already follow the rule; they're recorded here as the reference examples future names are
checked against:

```text
cpintl-org / .agents / skills   / prompt-authoring/SKILL.md
cpintl-org / .agents / schemas  / agent-task.schema.json
cpintl-org / .agents / providers/ adapters/google-gemini.yaml
cpintl-org / .agents / plans    / brand-accent-colors-signoff/task.yaml
```

A name that breaks the rule usually breaks it one of three ways:
- **Category doing double duty as a topic** — e.g. `skills/cpi-hcv-reporting.md` instead of
  `skills/cpi-hcv-reporting/SKILL.md` plus a `references/` file for the detail.
- **Extension describing the subject instead of the format** — e.g. naming a JSON Schema file
  `agent-task-rules.txt`.
- **A new top-level category invented for one file** — if only one file would live there, it
  belongs inside an existing category instead.

## Applying this alongside the existing standard

Use in this order:
1. This file — decide the category and extension.
2. `references/portable-standard.md` — apply the character grammar (lowercase kebab-case, no
   trailing periods, no reserved Windows names, etc.) to the `specific-thing` segment.
3. `references/github-standard.md` or `references/workspace-standard.md` — apply provider-specific
   rules (branch prefixes, Drive IDs) if the object lives on that provider.
4. `scripts/validate_names.py --kind path <the-path>` — mechanically check the result before
   committing it.

## Keeping the underlying standards current

The web and interaction standards this rule is built on (RFC 3986 URI, DNS, HTTP/2 and HTTP/3,
TLS 1.3, JSON/JSON-LD/JSON-RPC, XML, Protocol Buffers) change rarely and don't need frequent
re-checking. The agent-protocol layer (MCP, A2A, AGENTS.md, and the Agentic AI Foundation that
now governs them) is new and moves fast. `references/standards-freshness-register.md` tracks
both groups with a review date; `scripts/check_standards_freshness.py` fails the repository's
automatic checks once that date passes, so a stale naming assumption gets flagged instead of
silently going out of date.