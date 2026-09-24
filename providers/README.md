# Providers and model adapters

An AI **provider** is a company or program that supplies a model (for example a chat app, an API, or a model on your own computer). This repository does not depend on any one provider. Each provider is reached through a small **model adapter** file, so switching providers means changing one file and nothing else.

## What is here

| File | Purpose |
|---|---|
| `provider-catalog.yaml` | A checklist of providers you may want to use, with what must be verified before use |
| `adapters/manual-review.yaml` | No AI at all: the task becomes a checklist for a person (the safe default) |
| `adapters/openai-compatible.yaml` | For any service that accepts requests in the common "OpenAI-compatible" style |
| `adapters/google-gemini.yaml` | Placeholder settings for Google's Gemini models |
| `adapters/anthropic-claude.yaml` | Placeholder settings for Anthropic's Claude models |
| `adapters/local-model.yaml` | For a model that runs on your own computer |

The shape of an adapter is defined in `schemas/model-adapter.schema.json`. Provider-specific settings go **only** under `extensions`.

## Rules

1. Never write a key, token, or password in an adapter. `credentialRef` is only the name of a secret stored somewhere approved.
2. Model names, limits, prices, and data-use terms change. Every adapter has `verifiedOn`; leave it as a placeholder until a person has checked the provider's current official page.
3. Free tiers may allow the provider to use your prompts to improve its products. Treat every free-tier provider as **not allowed for restricted data** unless a written policy says otherwise.
4. Every task needs a manual fallback. Use `manual-review` when no provider is approved, unavailable, or the data is restricted.
5. Do not copy a provider's setting into a prompt file. The prompt checker rejects it.

## How to switch providers (no coding)

1. Open `templates/model-adapter.yaml` and copy it (or copy one file from `adapters`).
2. Change `metadata.name`, `provider`, and `model`, and fill `credentialRef` with the secret's name.
3. After a person verifies the provider's official terms, fill `verifiedOn` with the date.
4. In your task file, change `modelRef.name` to the new adapter's name.

## Checking

Where to run: a terminal opened in the repository root folder.

```bash
python skills/agent-task-planning/scripts/validate_agent_yaml.py providers/adapters
```
