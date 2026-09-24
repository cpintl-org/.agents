---
name: google-workspace-free-serverless
description: Design, audit, or implement quota-bounded no-subscription serverless systems using Google Workspace, Apps Script, Drive, Sheets, Forms, Sites, Calendar, Tasks, Firebase Spark, GitHub, and optional AI providers. Use whenever a request claims a Google/NGO stack is free, always free, serverless, provider-agnostic, or needs a zero-billing baseline.
---

# Google Workspace free-serverless architecture

## Purpose

Use this skill to produce a **source-verified, quota-bounded design**, not a promise of unlimited hosting or permanent pricing. Keep Google Workspace as the system of record when the brief is Workspace-first. Add Firebase, GitHub, external APIs, or AI only when their current no-payment boundary, data handling, and failure behavior are explicit.

Treat “free” as a cost classification, never as a synonym for unlimited, private, durable, supported, or SLA-backed. Preserve the access date for every pricing, quota, model, policy, and deprecation claim.

## Required workflow

1. **Classify the account and billing boundary.** Record whether the deployment uses a consumer Google Account, Essentials Starter, paid Workspace, nonprofit grant, Firebase Spark, GitHub Free, or a billing-enabled project. Never apply Workspace quotas to a consumer account, and never call a trial permanent.
2. **Read the relevant references.** Use `references/free-resource-matrix.md` for the dated service matrix, `references/implementation-patterns.md` for patterns and limits, and `references/pdf-architecture-audit.md` when auditing claims from the supplied architecture. Use `references/pdf-source-extract.txt` only as source context, not as authoritative current documentation.
3. **Verify official sources at execution time.** Recheck pricing, quotas, plan eligibility, API authentication, model availability, data-use terms, and deprecations. Prefer first-party sources. Record the URL, access date, confidence, and what remains uncertain. Use community sources only as hypotheses.
4. **Label every dependency.** Use exactly one of: `always-free/no-subscription`, `free-tier/quota-bounded`, `trial/promotional`, `billing-dependent`, or `paid-plan requirement`. State whether payment-method attachment can convert an exhausted allowance into a charge.
5. **Choose the smallest safe baseline.** Prefer Drive + Sheets + Forms + Apps Script + Calendar + Tasks + Sites, with email and manual control paths. Prefer Maps Embed over metered Maps APIs. Treat Gemini or any other AI provider as optional, redacted, human-reviewed assistance with a no-AI fallback.
6. **Engineer quota safety.** Batch reads and writes; cache stable reference data; queue bounded work in Sheets/Drive; use idempotency keys, single-writer coordination, sparse triggers, checkpoints, truncated exponential backoff, retry limits, and graceful quota exhaustion. Do not present Sheets, Tasks, Properties, or Cache as a transactional database, durable queue, secret manager, or archive.
7. **Protect identity and data.** Apply least privilege, restricted Drive sharing, explicit roles, audit rows, exports/backups, retention and deletion rules, and access review. Keep API keys, service-account keys, webhook URLs, OAuth refresh tokens, beneficiary data, and health/safeguarding data out of client HTML, public Sites, Sheets cells, GitHub, logs, and public links.
8. **Report cost and failure separately.** Explain no-charge conditions, the first quota likely to fail, what stops or becomes billable, recovery behavior, retention, ownership/handover, and the migration trigger. Do not call a system production-ready, enterprise-grade, highly available, or secure without evidence for those claims.
9. **Produce the output contract below.** For implementation work, include the manual fallback and a testable verification checklist, not just an architecture diagram.

## Decision rules

| Need | Default choice | Do not assume |
|---|---|---|
| Small structured registers | Sheets with batch access and a single-writer queue | SQL transactions, row locks, foreign keys, or high concurrency |
| Files and exports | Drive with controlled sharing and periodic export | Unlimited storage, public-link security, CDN behavior, or archival guarantees |
| Intake | Forms → installable trigger → normalized Sheet row | API-created Forms are published or safe for sensitive public intake |
| Lightweight API/UI | Apps Script web app embedded in Sites | Guaranteed uptime, unrestricted ingress, safe owner-token exposure, or CORS guarantees |
| Human follow-up | Calendar, email digest, or Tasks | Tasks as a distributed durable queue |
| Notifications | Email or Sites control panel | Chat incoming webhooks on a no-cost account |
| Maps | Maps Embed or cached/manual coordinates | Geocoding, Routes, Places, or Maps APIs as always-free |
| AI assistance | Optional server-side provider adapter with redaction and review | Stable model names, guaranteed free access, or sensitive-data privacy |
| Static frontend/CI | Firebase Hosting Spark or GitHub Free within limits | Firebase Storage/Functions/App Hosting on Spark or GitHub as a confidential database |

## Minimum output contract

For an architecture, audit, or implementation plan, return:

- **Account and cost boundary:** edition, project, payment method, explicit exclusions, and the meaning of “free.”
- **Component matrix:** service, purpose, status label, current limit, integration path, data sensitivity, failure behavior, source URL, access date, and confidence. Use `templates/component-matrix.csv` when a reusable table is needed.
- **Claim audit:** `confirmed`, `partly confirmed`, `unsupported`, or `date-sensitive`, with correction and evidence.
- **Quota-safe flow:** intake, validation, lock/write, queue, notification, retry, audit, backup, and manual replay.
- **Security and privacy controls:** least privilege, secret handling, retention, access review, incident response, and a no-AI path.
- **Go/no-go verdict:** whether strict zero billing is realistic, the first migration trigger, and what changes if billing is enabled.

## Red flags — stop and verify

- “Google Workspace is free” without naming the account or edition.
- Workspace quota numbers used for a personal account.
- “Free tier” presented as unlimited, permanent, private, or an SLA.
- Gemini model name, rate, endpoint, or data-use policy copied from an old document without a live source check.
- Maps geocoding, Routes, Places, Cloud Functions, Firebase Storage, App Hosting, SQL Connect, or Chat webhooks included in a strict zero-payment baseline.
- Drive `lh3`, `uc`, thumbnail, CORS, Range, or iframe behavior treated as a guaranteed public CDN contract.
- Cache/Properties called a secret manager; Sheets rollback called a database transaction.
- Public links or owner-executed Apps Script used for confidential beneficiary data.
- API keys or OAuth tokens included in prompts, examples, source code, logs, templates, or client-side JavaScript.

## cpintl-org portability rules

Use lowercase ASCII kebab-case for new directories and portable files; use `UPPER_SNAKE_CASE` for environment variables and `lowerCamelCase` for new JSON fields. Preserve provider-issued IDs exactly, but use placeholders such as `{github-owner}`, `{repository}`, `{drive-folder-id}`, `{project-id}`, and `{mcp-server-url}` when an ID is unknown. Encode URI path and query components by component; never concatenate unchecked input into an endpoint.

Keep provider identity, display name, slug, canonical locator, and endpoint template as separate fields. The canonical repository locator for this package is `{github-owner}/{repository}@{ref}:skills/google-workspace-free-serverless/`; replace placeholders only with verified values. Do not invent organization members, domains, Drive IDs, tokens, or business meanings.

## Bundled resources

- `references/free-resource-matrix.md`: dated service/cost matrix and official source links; recheck before use.
- `references/implementation-patterns.md`: account-aware quotas, integration patterns, security, and recovery.
- `references/pdf-architecture-audit.md`: claim-by-claim audit of the supplied architecture.
- `references/pdf-source-extract.txt`: supplied source extract for traceability only.
- `references/ai-adapter-pattern.md`: provider-neutral AI contract, redaction, review, and no-AI fallback.
- `references/telemetry-and-migration.md`: quota telemetry, migration triggers, and staged migration sequence.
- `scripts/verify_free_matrix.py`: deterministic completeness check; it performs no network calls and needs no credentials.
- `templates/component-matrix.csv`: reusable evidence and dependency register.
- `templates/architecture-decision-record.md`: decision, evidence, risk, and migration record.
- `templates/verification-checklist.md`: pre-launch and change-review checklist.
- `templates/account-boundary.yaml`: account, billing, sensitivity, and verification intake form.

## Enhancement roadmap

Future revisions may add official-source freshness reporting, account decision forms, synthetic Apps Script fixtures for idempotent queues and recovery, provider-neutral AI adapter examples, secret/path/link linting in GitHub Actions, quota telemetry, and versioned migration playbooks. Add each enhancement as a separately testable resource; never weaken the no-AI, no-secret, or fail-closed baseline.

## Validation

Run the bundled checker from the skill directory:

```bash
python scripts/verify_free_matrix.py references/free-resource-matrix.md
```

For repository work, also validate names and paths with the cpintl-org writing standard, check Markdown links and structured files, scan for secrets and traversal, run `git diff --check`, and test every script with valid and invalid inputs.

## Related skills

When the resulting Doc, Sheet, Slide, or template must carry the official CPI look, pair this
skill with `cpintl-org-brand` (official palette, Arial, logos, department icons, cover pages).
