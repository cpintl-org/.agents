# Output templates

Templates define structure, not facts. Use them for Google Docs, Sheets, Markdown reports, reviews, and bridge records.

## Rules

- Keep placeholders such as `{project}`, `{period}`, and `{drive-folder-id}` until verified.
- Do not add secrets or restricted data to examples.
- Use `google-docs-outline.md` for narrative documents and `google-sheets-schema.json` for structured records.
- Include owner, status, source/access date, sensitivity, and review date where relevant.
- Validate JSON and preserve provider-issued IDs exactly.

## Agent planning templates

| File | Answers |
|---|---|
| `agent-task.yaml` | What should be done? |
| `agent-workspace.yaml` | Which approved sources and tools may be used? |
| `agent-policy.yaml` | What is allowed (privacy, network, review)? |
| `model-adapter.yaml` | Which AI provider and model, or a person by hand? |
| `agent-template.yaml` | A reusable recipe for one kind of agent |
| `lifecycle-run.yaml` | One run and its progress status |
| `checkpoint-policy.yaml` | When progress is saved |
| `human-approval.yaml` | A person's yes or no |
| `agent-control-panel/` | The same ideas as six Google Sheets tabs, plus a request form outline |

Start with `agent-control-panel/README.md` if you prefer Google Sheets to editing files. Placeholders in curly brackets, such as `{responsible-role}`, stay until a person fills in a verified value.
