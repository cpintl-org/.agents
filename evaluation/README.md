# Evaluation and replay

Evaluation answers two questions: **did the prompt and AI do what we asked?** and **could someone repeat the run and get a comparable result?** It is simple record-keeping, not software you need to install.

## What is here

| Item | Purpose |
|---|---|
| `test-case.schema.json` | Shape of a test case (synthetic data only) |
| `rubric.schema.json` | Shape of a human review checklist |
| `run-record.schema.json` | Shape of a record of one run |
| `rubrics/human-review-rubric.yaml` | A ready rubric for reviewers |
| `example-run-record.json` | A filled example |
| `reports/` | Where short summaries (no restricted content) can be kept |

## What a run record captures

Prompt name and version, brain and skill versions, provider and model, how sensitive the input was, which tools were called, whether the output matched its expected shape, the human decision, time taken, a short usage note, safety findings, and a 1-5 factuality score.

## What is never stored here

Raw prompts or outputs that contain restricted or personal information, patient or case details, secrets, or tokens. Keep those outside the repository under the approved program policy. A run record stores the *classification* of the input, not the input.

## Simple routine

1. Run the prompt against its synthetic test cases.
2. A reviewer fills in the rubric (yes/no or 1-5 for each question).
3. Save one run record per run.
4. If any blocking question is answered "no", do not use the prompt until it is fixed and its version number is raised.

## Reproducibility note

AI results can differ each time. Record the prompt version and provider/model so a person can see what changed when results differ.
