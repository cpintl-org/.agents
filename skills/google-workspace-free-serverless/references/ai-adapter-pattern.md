# Provider-neutral AI adapter pattern

Use AI only as an optional assistance layer. The operational workflow must remain usable when no model is configured, a model is unavailable, a quota is exhausted, or a data-protection review rejects the request.

## Adapter contract

Expose a provider-neutral operation such as `classify`, `extract`, `summarize`, or `draft`. Keep the provider name, model name, endpoint, authentication method, and rate limit in configuration outside prompts and source files. Return a structured result with `status`, `output`, `provider`, `model`, `reviewRequired`, `redactionApplied`, `usageEstimate`, and `errorCode` fields. Do not expose keys or raw provider responses to the browser.

## Required controls

1. Minimize and redact data before transmission. Do not send beneficiary identifiers, health information, safeguarding details, credentials, or unrestricted case notes to a free-tier model without an approved policy.
2. Record the decision to use AI, the redaction state, the provider/model classification, and the human reviewer; do not store unnecessary prompts or sensitive outputs in logs.
3. Require human review before an AI result changes a record, sends a notification, assigns a person, or creates a safeguarding or health-related conclusion.
4. Bound prompt and response size, rate, retries, and daily spend. Treat 401, 403, 429, timeout, and provider-policy errors as expected failure paths.
5. Preserve a manual or deterministic fallback: a human form, rule-based classifier, blank draft, or queued review task.

## Provider mapping

Map any provider—Gemini, Claude, OpenAI-compatible API, local model, or another approved service—to the same contract. Verify current model lifecycle, data-use terms, pricing, API endpoint, and authentication at execution time. Never infer privacy or free status from a model name.

## No-AI path

When `aiAllowed` is false, skip the provider call and return `status: manual_review` with a clear human task. The system must not fail closed by losing the record; it should preserve the input, queue the manual action, and provide a safe retry route after approval.
