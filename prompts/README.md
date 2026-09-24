# Prompt library

A **prompt file** is a saved, versioned instruction for an AI. It is a plain text file ending in `.prompt`. It has two parts: a short **header** (name, version, owner, privacy level, and which input/output shapes it uses) and the **instruction text**.

The format is inspired by Google's open Dotprompt idea, but it is **not tied to Google, Gemini, or any provider**. Provider settings (model name, temperature, and so on) never go in a prompt file. They live in a Model Adapter (see `templates/model-adapter.yaml`).

## Folder layout

```text
prompts/
├── README.md
├── diagnostics.md              # plain-language meaning of each check message
├── schemas/                    # rules for the header
└── library/
    ├── evidence-summary.prompt # example prompt
    ├── partials/               # small shared pieces, used as {{> piece-name}}
    ├── schemas/                # the shape of inputs and outputs
    └── fixtures/               # synthetic test cases
```

## How to add a prompt

1. Copy `library/evidence-summary.prompt` and give the copy a lowercase name such as `monthly-report-outline.prompt`.
2. Edit the header: new `name`, `version` (start at `1.0.0`), your `owner`, and `sensitivity` (`public`, `internal`, or `restricted`).
3. Write the instruction. Put each thing a user must supply in double curly brackets, such as `{{topic}}`.
4. Copy the two schema files in `library/schemas/`, rename them, and list your inputs and outputs.
5. Add two or three synthetic test cases in `library/fixtures/`.
6. Open a pull request. The automatic check runs the prompt checker and tells you in plain words what to fix.

## What the checker looks for

Missing or invalid header, variables used but not declared, declared but never used, broken schema links, circular shared pieces, unsupported helpers, secret-like text, unsafe web or file links, provider-specific settings, and input/output shape mismatches. See `diagnostics.md`.

## Allowed instruction syntax (kept deliberately small)

| Write this | It means |
|---|---|
| `{{name}}` | Insert the value called `name` |
| `{{#if name}} ... {{/if}}` | Only if `name` was supplied |
| `{{#each list}} ... {{this}} ... {{/each}}` | Repeat for each item |
| `{{> piece}}` | Include `partials/piece.prompt` |

Nothing else is allowed, so every prompt stays easy to read and to check.

## Run the checker yourself (optional)

Where to run: a terminal opened in the folder that contains `.agents` (the repository root).

```bash
python skills/prompt-authoring/scripts/validate_prompts.py prompts/library
```
