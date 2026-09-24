# Roadmap for the agent layers

Status values: **done** (files exist and pass the automatic checks), **pilot next** (do by hand, small), **later** (do not start yet).

| Step | What | Status |
|---|---|---|
| 1 | Neutral rulebooks for tasks, workspaces, policies, model adapters, instances, and lifecycle conditions (`schemas`) | done |
| 2 | Prompt file convention with schemas, synthetic test cases, and a plain-language checker (`prompts`, `skills/prompt-authoring`) | done |
| 3 | Read-only memory with source, revision, and freshness (`memory`, `skills/memory-search`) | done (contract only; no automatic indexing) |
| 4 | Plain templates and a six-tab Google Sheets control panel (`templates`) | done |
| 5 | Provider catalog and model adapter files (`providers`) | done (facts to verify before use) |
| 6 | Evaluation records, rubric, and replay notes (`evaluation`) | done (manual routine) |
| 7 | Pilot: one low-risk task, one approved Drive folder, `manual-review` first, then one approved provider | pilot next |
| 8 | Pausing, saving progress, capacity management, or an automatic control system | later |

## Pilot success measures

- A non-coder can fill in a task and get it approved without help.
- The result lists sources and marks gaps as `UNKNOWN`.
- A reviewer finds no invented facts and no sensitive data.
- The task can be done again with a different provider by changing only the model adapter.

## Decide before step 8

Step 8 needs a real runtime (a place where agents actually run) and a person who maintains it. Decide who that person is, what it costs, and how it is recovered if it fails. Until then, the manual route is the supported route.
