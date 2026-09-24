# Prompt checker messages in plain language

| Message starts with | What it means | What to do |
|---|---|---|
| `missing-header` | The file has no header block between two `---` lines | Copy the header from the example prompt |
| `bad-header` | A header field is missing or has an invalid value | Fix the named field (see `prompts/schemas`) |
| `provider-field` | The header contains a model or provider setting | Remove it; put it in a Model Adapter |
| `schema-missing` | The input or output shape file is not found | Check the path is relative to the prompt file |
| `undefined-variable` | The text uses `{{x}}` but the input shape has no `x` | Add `x` to the input schema or remove it |
| `unused-variable` | The input shape lists `x` but the text never uses it | Use it or remove it (a warning) |
| `unsupported-syntax` | A helper other than if, each, or partial is used | Rewrite using only the allowed syntax |
| `partial-missing` | `{{> name}}` points to a file that does not exist | Create `partials/name.prompt` |
| `partial-cycle` | Shared pieces include each other in a loop | Break the loop |
| `secret-like` | Text looks like a key, token, or password | Remove it and rotate the real secret |
| `unsafe-url` | A `http:`, `file:`, or `data:` link is present | Use a reviewed `https:` link or remove it |
| `fixture-mismatch` | A test case does not match the input shape | Fix the test input |
