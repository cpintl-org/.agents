# Prompt file format

## Shape of a file

```text
---
name: evidence-summary
version: 1.0.0
owner: health-program-team
description: One sentence.
sensitivity: internal
input_schema: schemas/evidence-summary-input.json
output_schema: schemas/evidence-summary-output.json
fixtures: fixtures/evidence-summary.tests.yaml
requires:
  - web-research
---
Instruction text with {{variables}} goes here.
```

## Header fields

| Field | Required | Meaning |
|---|---|---|
| `name` | yes | Lowercase kebab-case, same as the file name without `.prompt` |
| `version` | yes | Three numbers such as `1.0.0`. Change it whenever the wording changes |
| `owner` | yes | A role or team, not a personal email |
| `sensitivity` | yes | `public`, `internal`, or `restricted` |
| `input_schema` | yes | Path to the input shape file |
| `output_schema` | yes | Path to the output shape file |
| `fixtures` | no | Path to synthetic test cases |
| `requires` | no | Names of skills or capabilities the prompt expects |
| `description` | no | One plain sentence |

Any other field is rejected. Provider fields (`model`, `config`, `temperature`, `tools`, and similar) get a `provider-field` message.

## Allowed syntax

`{{name}}`, `{{#if name}} ... {{else}} ... {{/if}}`, `{{#each list}} ... {{this}} ... {{/each}}`, and `{{> piece}}` (shared piece stored in a `partials` folder next to the prompt as `piece.prompt`). Everything else is refused so prompts stay readable and checkable.

## Versioning rule

Patch (`1.0.1`) for wording fixes, minor (`1.1.0`) for a new optional input, major (`2.0.0`) for a change that breaks existing inputs or outputs. Keep a short note in the pull request describing why.

## Evaluation link

Each prompt should have at least one synthetic test case and, before wide use, a human review using the rubric in the repository `evaluation` folder.
