# Adoption boundaries: what we learn from, and what we do not copy

We borrow **ideas** from open projects (versioned prompts, provenance-aware memory, agent lifecycle, declarative tasks) and turn them into small neutral files. We do not copy their infrastructure or vendor assumptions.

## Ideas we adopt

| Idea | Where it appears here |
|---|---|
| Versioned prompt files with declared inputs and outputs | `prompts` |
| Provenance, revision, and freshness on every memory result | `memory` |
| Separating the logical agent from where it runs | `schemas/agent-template.schema.json`, `schemas/agent-instance.schema.json` |
| Task, workspace, policy, and model kept apart | `templates`, `providers` |
| Status conditions such as "HumanApproval: False" | `skills/agent-task-planning` |

## Things we do not copy into the core

- Cluster or server management, and database or cache operations.
- Any single cloud's identity, storage, or setup as a requirement.
- Model settings from one provider inside prompts or tasks.
- Unrestricted network access, or web addresses supplied while running.
- Broad command-line, process-debugging, or shell powers for agents.
- Unrestricted access to files or source code.
- Automatic indexing of all Drive or repository files.
- Free-form database or graph queries.
- Deleting memory without review.
- Automatic linking of memory between projects.
- Unreviewed upstream branding or governance.

## How optional runtimes fit

Core files in this repository stay neutral. If a team later chooses a runtime (a Google Workspace script, a local tool, or something bigger), it is added as an **adapter** that reads these files. The core never depends on the adapter.

```text
cpintl-org core files  ->  optional adapters  ->  Google Workspace, a local machine,
                                                  any AI provider, or a person by hand
```

## When in doubt

Use the stricter rule and ask a person. A plan that cannot be checked by a person is not ready.
