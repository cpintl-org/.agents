---
name: prompt-authoring
description: Write, review, and check versioned prompt files (.prompt) that are provider-neutral, have declared inputs and outputs, shared pieces, synthetic test cases, and plain-language checks. Use when someone wants a reusable instruction for an AI, wants to turn a good chat prompt into a saved one, or must review a prompt before it is added to the repository.
---

# Prompt authoring

Use this skill to turn a useful instruction into a saved **prompt file** that any AI provider can use. A prompt file has a short header and the instruction text. The format is inspired by Google's open Dotprompt idea but never depends on Gemini, Genkit, or Google AI Studio.

## Workflow

1. Ask what the prompt should do, who will read the result, and whether any information about people, patients, or safeguarding cases is involved. If yes, set `sensitivity: restricted` and stop: a person handles that work by hand.
2. Copy `templates/prompt-template.prompt`. Give it a lowercase kebab-case name, version `1.0.0`, an owner role, and a sensitivity of `public`, `internal`, or `restricted`.
3. Write the instruction in plain sentences. Use only the four allowed pieces of syntax listed in `references/prompt-format.md`.
4. Declare every input in an input schema file and the expected result in an output schema file. Paths are relative to the prompt file.
5. Add two or three **synthetic** test cases. Never use real names, patient details, or case notes.
6. Keep provider settings out. Model name, temperature, and similar settings belong in a Model Adapter template, never in a prompt file.
7. Run the checker (see below), fix each message, and ask a person to review the wording before it is merged.

## Rules

- Do not invent sources or tools. The prompt must tell the AI to say plainly when a source or tool was unavailable.
- Mark missing information as `UNKNOWN`; do not guess.
- Never put secrets, keys, private links, or personal data in a prompt, schema, or test case.
- Every prompt for consequential output must say that a person reviews it before use.
- A prompt without a working manual fallback (a person doing the task by hand) is incomplete.

## Check

Where to run: a terminal opened in the repository root folder.

```bash
python skills/prompt-authoring/scripts/validate_prompts.py prompts/library
```

Read `references/prompt-format.md` for the header fields, syntax, and what each check message means. Use `scripts/validate_prompts.py` only as a structure check; it does not judge whether the prompt is good, safe, or true.
