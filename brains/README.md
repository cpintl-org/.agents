# Agent brains

A **brain** is a provider-neutral role definition: purpose, audience, working method, boundaries, skills, and output contract. Brains are instructions, not credentials or autonomous permissions.

## Create a brain

1. Copy `research-agent.md` or `doc-writer-agent.md`.
2. Use a lowercase kebab-case filename ending in `.md`.
3. State the role, objective, inputs, output format, evidence requirements, and escalation conditions.
4. Reference skills by repository path; do not embed long technical manuals.
5. Keep private data, API keys, Drive IDs, and provider-specific system prompts out of the file.
6. Test the brain against a synthetic example and ask a human to review sensitive outputs.

Every brain must preserve uncertainty, avoid fabricated facts, follow `guardrails/`, and provide a manual fallback when a provider or integration is unavailable.
