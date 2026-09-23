# Supplied PDF: architecture inventory and audit

**Source:** `ServerlessGoogleWorkspaceArchitecture.pdf`, 22 pages. **Audit date:** 2026-09-18. The source proposes an NGO operations platform without standalone AWS/Azure/GCP infrastructure.

## Extracted resource inventory

| Layer | PDF resources and patterns | Safe interpretation |
|---|---|---|
| Identity and presentation | Google Accounts/Workspace identity, Google Sites, Apps Script HTML Service, embedded SPA/HTML, iframe sandbox, `ALLOWALL` | Sites is a shell; the deployed web app remains the authorization boundary. Do not weaken clickjacking protection without a controlled embed and CSP review. |
| Storage and content | Drive files/blobs, file IDs, MIME types, revisions, Shared Drives, appProperties, direct-download/thumbnail/user-content URLs, NDJSON archives, client-side WASM SQLite | Drive is an object/document store. Public URL behavior and `lh3`/`uc` delivery are implementation details to test, not a guaranteed CDN or CORS contract. |
| Structured data | Sheets workbooks/worksheets, header-as-schema, batch `getValues`/`setValues`, `TextFinder`, CacheService, PropertiesService, audit log, UUIDs | Sheets is a small operational register. It is not a relational database with transactions. Use single-writer queues, idempotency, backups, and batch writes. |
| Concurrency | LockService script/document/user locks, `flush`, snapshot/restore idea | Locks serialize cooperating Apps Script executions. Cache snapshots do not create durable rollback or ACID transactions; design compensating actions and audit records. |
| Compute and scheduling | Apps Script V8, `doGet`/`doPost`, installable/time-driven/form-submit triggers, self-rescheduling cursor loop, `UrlFetchApp`, `fetchAll` | Use bounded jobs that checkpoint before the execution limit. Quotas differ by account and can change. |
| Web transport | Apps Script 302 redirect, ContentService JSON, `text/plain` POST to avoid preflight, CORS observations | Test actual browser behavior. Do not promise wildcard CORS, supported OPTIONS, or security from a simple-request workaround. Validate origin, authentication, replay protection, and payload size. |
| Workspace integrations | Forms intake, Sheets destination, Gmail/MailApp, Calendar Advanced Service and Meet conference data, Tasks API, Chat webhooks/cardsV2, Maps geocoding/directions, Docs case journals, Keep discussion | Mark each service independently; feature availability often depends on plan/admin. Keep email/manual controls as fallbacks. |
| AI | Google AI Studio / Gemini OpenAI-compatible endpoint, structured JSON, multimodal extraction, embeddings and cosine similarity in V8 | Model names, endpoint formats, pricing, rate limits, data use, and embedding dimensions are date-sensitive. Redact sensitive data and keep a human/no-AI path. |
| Delivery and CI/CD | clasp, `appsscript.json`, Advanced Services, OAuth scopes, GitHub Actions, encrypted secrets, manifest-as-code | CI can deploy code but cannot bypass quotas. Never commit `.clasprc`, API keys, refresh tokens, or broad secrets. |
| Security/governance | Shared Drive restrictions, Google Groups, `Session.getActiveUser`, internal RBAC sheet, immutable Audit_Log | RBAC in a Sheet is application logic, not a complete IAM system. Add least privilege, access review, backups, retention, incident response, and testable recovery. |

## Claim status

| PDF claim | Status | Correction required in future work |
|---|---|---|
| Drive + Sheets + Apps Script can approximate object storage, structured registers, and serverless orchestration | **Partly confirmed** | Valid for small/low-throughput systems; not equivalent to managed object storage, SQL, or an SLA-backed backend. |
| Workspace licensing is the only recurring cost | **Date-sensitive** | Essentials Starter/personal accounts may be no-subscription options; Business/Enterprise plans are paid. API over-threshold billing, external APIs, Maps, Gemini, and plan-gated features must be checked. |
| Drive `lh3.googleusercontent.com`, `uc`, thumbnail and usercontent endpoints provide reliable production delivery/CORS/cache behavior | **Unsupported as a contract** | Treat as undocumented/fragile delivery behavior. Use an official web host or Apps Script response and verify access, headers, cache, range, and embedding in the target browser. |
| Drive has no in-place byte mutation; use replacement/revisions/chunking | **Partly confirmed** | Version/replacement patterns are reasonable; confirm upload/revision API behavior and memory constraints for the selected method. |
| LockService + CacheService snapshot gives atomic Sheets transactions and rollback | **Unsupported** | Locks serialize cooperating writers; Cache is volatile. Use idempotent mutations, append-only audit, compensating actions, and tested backups. |
| Sheets has a hard 10-million-cell workbook limit and should be indexed with batch reads/TextFinder/cache | **Partly confirmed** | The optimization pattern is sound; verify current spreadsheet and API limits, and do not present latency estimates as guarantees. |
| Apps Script is 6 minutes/run, 30 concurrent/user, 6 hours/day Workspace, 100,000 UrlFetch/day Workspace | **Partly confirmed** | These are account-specific quota examples. Consumer accounts currently have lower daily quotas; quotas can change without notice. |
| Self-rescheduling triggers solve long-running work | **Confirmed with limits** | Checkpoint, bound batches, avoid trigger storms, delete completed triggers, and handle duplicate/retry execution. |
| `text/plain` POST avoids Apps Script JSON preflight issues | **Partly confirmed** | It can avoid a browser preflight in some cases, but it is not authentication or CORS policy. Test redirects, origins, CSRF/replay, and error responses. |
| Sites + Apps Script HTML can deliver a portal | **Confirmed with limits** | Sites is a presentation/container layer; iframe isolation, permissions, authorization prompts, and web-app deployment settings remain. |
| `ALLOWALL` is required for Sites embedding | **Date-sensitive / verify** | Test the current embedding path and use the least permissive setting that works; `ALLOWALL` increases clickjacking exposure. |
| clasp + GitHub Actions can provide CI/CD | **Confirmed with limits** | Protect credentials, pin actions, review logs, and remember CI does not provide hosting or remove runtime/API quotas. |
| Forms, Calendar, Tasks, Chat, Maps, Docs and Keep form a free native event bus | **Partly confirmed** | Integrations exist, but Chat webhooks, Maps APIs, Meet creation, Keep API, admin controls and quotas differ. Keep is not a general user-notes API for this use. |
| Apps Script Maps geocoding/directions are free without external keys | **Unsupported as a zero-cost promise** | Maps has product-specific quotas and billing/free caps; Maps Embed is the safer strict-free option. |
| Gemini API can be used with `gemini-2.0-flash`, structured output, multimodal input, embeddings, and no external cost | **Date-sensitive / unsafe as baseline** | Recheck model lifecycle, endpoint, rate limits, pricing, content-use policy, key requirements, and embedding API. Make AI optional and human reviewed. |
| “Enterprise-grade,” “high availability,” and “sub-second” performance follow from these patterns | **Unsupported** | These require measured load tests, monitoring, backup/recovery evidence, governance, and an availability target. |

## Resource-to-risk mapping

- **Sensitive beneficiary/medical data:** keep in restricted Drive/Sheets, minimize collection, review consent/retention, and do not send to free-tier AI or public endpoints without approved policy.
- **Public intake:** use Forms or a dedicated app with abuse controls; public forms and owner-executed web apps can expose data if permissions are wrong.
- **Large files/media:** Drive capacity and Apps Script payload/memory limits dominate; use resumable/controlled uploads or a paid/billing-approved store.
- **High-volume jobs:** queue and checkpoint in Sheets/Drive, use small idempotent batches, and expose a manual retry/control sheet.
- **External webhooks:** Apps Script web apps may lack the header/control surface needed for robust signature verification; use a header-aware intermediary when authenticity matters.
- **Static assets:** use an officially supported host or controlled Apps Script output; never depend solely on undocumented Drive URL tricks.

## Source handling

The PDF bibliography mixes official Google documentation with Stack Overflow, blogs, Reddit, and community posts. Treat official current documentation as authoritative for limits, pricing, authentication, and deprecation. Treat community URLs as hypotheses or troubleshooting context only.
