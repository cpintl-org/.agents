# Apps Script quotas and free execution limits

**Research scope.** This report evaluates the Google Workspace/serverless platform represented by the architecture (Drive, Sheets, Apps Script, Forms, Sites, Calendar, Tasks, Chat, Maps and Gemini), with emphasis on whether a small NGO or operations system can run at **zero recurring monetary cost**. It distinguishes a genuinely free ongoing allowance from a trial, promotional credit, free usage cap that requires billing, or a paid Workspace edition. It also records integration paths, execution and API limits, retention/storage caveats, and date-sensitive changes. Sources were checked against Google’s official documentation on **18 September 2026**; quotas and prices can change without notice.

## Executive verdict

**Apps Script itself is usable indefinitely without a separate per-execution charge** on a consumer Google Account (for example, `gmail.com`) and on a paid Google Workspace account, but it is not an unlimited free server. Consumer accounts receive materially lower daily quotas than Workspace accounts, and all scripts are constrained to a six-minute execution, 90 minutes/day of trigger runtime, 20 triggers per user per script, 30 simultaneous executions per user, 50 MB URL-fetch response and POST sizes, and other hard limits. Google explicitly says quotas may be eliminated, reduced, or changed without notice. A paid Workspace subscription is **not** required for basic personal-account Apps Script, Drive, Sheets, Forms, Calendar, Tasks, Sites or ordinary consumer Google services; however, business identities, domain administration, Chat incoming webhooks and many organizational controls require a paid Workspace edition.

The architecture is therefore suitable for a small, low-throughput, asynchronous NGO system if it is designed around batch operations, installable time/form triggers, retry/backoff, idempotency and a human-operated control plane. It is not a safe assumption that the complete architecture is “free”: Google Workspace Business plans are recurring paid products after a 14-day trial; Google Maps is pay-as-you-go with monthly free caps and normally a billing account; Gemini API free tier is model- and project-rate-limited and may use prompts to improve Google products; and Google has announced that exceeding standard Workspace API quota thresholds is planned to incur Cloud billing later in 2026. Free allowances should be treated as **quota-limited and changeable**, not as an SLA or a permanent price promise.

## Comparison table

| Service | Ongoing no-money status | Important limits / restrictions | Workspace integration and best use |
|---|---|---|---|
| **Apps Script runtime and built-in services** | **Always available at no separate execution charge** for consumer accounts and included with Workspace; not an unlimited free compute tier. Workspace itself is paid for business plans. | Consumer versus Workspace quotas differ. Daily quotas reset 24 hours after the first request and are per user. Six minutes per execution; 90 minutes/day trigger runtime for consumers and 6 hours/day for Workspace; 30 simultaneous executions/user; 1,000/script; 20 triggers/user/script; 200 versions/script. URL Fetch: 20,000/day consumer or 100,000/day Workspace; 50 MB response and POST, 2 KB URL, 100 headers, 8 KB headers. Properties: 500 KB store and 9 KB/value. | Native Drive, Sheets, Forms, Calendar, Gmail, Maps, etc.; OAuth scopes and installable triggers. `doGet(e)`/`doPost(e)` web apps provide inbound HTTP; `UrlFetchApp` provides outbound HTTPS. Use for orchestration, validation, batching and lightweight APIs, not long-running workers. |
| **Drive API / Drive service** | Standard Drive API usage is currently no additional cost under documented quotas; storage is still subject to the account’s Drive allowance/Workspace plan. | Drive API: 1,000,000 quota units/min/project, 325,000/min/user/project, 1 TB/day/project egress threshold in current docs; method costs vary. 750 GB/day upload/copy per user; max upload 5 TB, max copy 750 GB. Google says over-quota usage is planned to incur Cloud billing later in 2026. | Apps Script Drive service or Advanced Drive service; REST API with OAuth; web apps and GitHub Actions can call via OAuth. Files persist until deleted/retention policy; free personal storage is shared across Google services and should be budgeted, not assumed unlimited. |
| **Sheets API / Spreadsheet service** | Standard Sheets API usage is currently no additional cost within quota; Sheets/Drive storage remains account-dependent. | Recommended maximum request payload is 2 MB; a single request timing out after 180 seconds fails. Reads/writes are per-minute quotas (the official page renders the numeric table dynamically); no daily request limit while staying within per-minute quotas. Over-quota billing is planned later in 2026. Apps Script adds its own execution, trigger, property and simultaneous-run limits. | Native Spreadsheet service; Advanced Sheets API/REST with OAuth; Forms can write responses to Sheets; GitHub Actions can use OAuth/service-account patterns where permitted. Batch reads/writes and atomic batch updates are essential. |
| **Forms / Forms API** | Google Forms and the standard Forms API are currently available at no additional API charge within quota; creating/using Forms can be done from a consumer account. | API page states that, while per-minute quotas are respected, there is no request/day limit; exceeding a quota returns 429 and requires exponential backoff. The official page does not expose the numeric quota table in extracted text, so do not invent a numeric ceiling. Form watches have additional limits. Apps Script FormApp can create/open/modify Forms and install form-submit triggers. Planned over-quota Cloud billing later in 2026 applies to the standard API model. | Native FormApp; Forms API via Advanced service/REST; form-submit triggers and response-to-Sheets workflows. Good for intake, approvals and field collection. Public form access and response retention/permissions are controlled by the Form owner/domain; do not put sensitive beneficiary data in a public form without access review. |
| **Calendar / Calendar API** | Consumer Calendar and standard Calendar API usage are currently no additional cost within quota; paid Workspace is only needed for business-domain administration and certain organizational features. | Apps Script daily events created: 5,000/day consumer, 10,000/day Workspace. Calendar API: 10,000 requests/min/project and 600/min/user/project; 1,000,000 requests/day/project threshold before planned billing. Per-calendar operational limits can be tighter; use push notifications rather than polling and exponential backoff. | CalendarApp or Advanced Calendar API/REST with OAuth; time-driven triggers and web apps can synchronize schedules. Calendar data remains subject to user/domain retention and sharing settings; event creation can generate email notifications, so control side effects. |
| **Tasks / Tasks API** | Google Tasks is usable with a consumer account and the API has a documented courtesy quota without a separate API price. | Official limit is **50,000 queries/day**. Quota increases are discretionary; service-account calls count as one account. The API is not a high-volume queue or durable job system. | No first-class built-in Apps Script Tasks service is listed in the standard service catalog; use the Tasks API through an Advanced service or `UrlFetchApp` with OAuth. Suitable for human follow-up lists, not reliable distributed work queues. |
| **Sites** | Google Sites can be created and published from a normal Google Account; no separate Sites API or hosting bill is required for a basic site. Workspace domain controls may require Workspace administration. | Sharing, publishing, and embed access are permission-controlled; a parent-managed Google Account cannot use Sites. Sites is a presentation/container layer, not a server runtime or general database. | Embed a deployed Apps Script web app using **Insert > Embed URL**. Viewers may need to authorize the web app; site and web-app permissions must both allow access. No normal Apps Script Sites-management service should be assumed. |
| **Chat / incoming webhooks** | **Not reliably free for the target architecture.** Official incoming-webhook quickstart requires a Business or Enterprise Google Workspace account with access to Chat and admin permission to add webhooks. | Incoming webhooks are one-way and space-specific; they cannot receive user events or converse. Per-space `spaces.messages.create` quota is 1 request/second shared among webhooks. General Chat quotas include 3,000 message writes/min/project, 3,000 reads/min/project, 300 searches/min/project, and per-space 15 reads/sec/1 write/sec. | Apps Script Advanced Chat service, REST API, or plain HTTPS webhook from `UrlFetchApp`, GitHub Actions or another server. Treat Chat webhook as a paid-Workspace dependency; for no-cost consumer deployments use email or a Sites/web-app interface instead. |
| **Maps Platform / Apps Script Maps service** | **Free cap, not a pure no-billing guarantee.** Maps uses pay-as-you-go billing and monthly free billable-event caps reset on the first day of each month. A billing account is normally required; usage over cap is chargeable. March 2025 replaced the old $200 monthly credit with SKU free caps. | Essentials SKUs generally have 10,000 free events/SKU/month (Map Tiles APIs generally 100,000; exact SKU matters). Apps Script Maps daily quotas: 1,000 static-map renders/day consumer or 10,000 Workspace; directions, geocoding and elevation: 1,000/day consumer or 10,000 Workspace each. Non-billable consumer Maps web usage and free-cap API usage are not equivalent. | Apps Script Maps service can create static maps, geocode, directions and elevation; REST APIs use API keys/OAuth as applicable; web apps can embed maps. For a strict zero-charge NGO deployment, disable billing overages and use cached/manual coordinates or an alternative unless a verified nonprofit credit and budget guard are in place. |
| **Gemini API / Gemini in Workspace** | Gemini API has an ongoing **Free tier** for selected models with free input/output tokens, but it is rate-limited, model-dependent and not a production guarantee. Gemini in Workspace is plan-dependent; current Workspace pricing shows limited Gemini on Starter and broader features on higher plans. | Free/paid model access and quotas change. Rate limits are per project, not per key; RPD resets midnight Pacific. Free tier content may be used to improve Google products; paid tier says content is not used for that purpose. Standard API keys are moving to auth keys: new AI Studio keys are auth keys from 28 May 2026, and standard-key rejection is scheduled for September 2026. Never expose keys client-side or in GitHub. | Call Gemini from Apps Script with `UrlFetchApp` and a restricted key, or use Vertex AI Advanced service/REST. Store secrets outside source code; Apps Script Properties is not a full secret manager. GitHub Actions can call APIs using repository secrets. Treat Gemini as optional, human-reviewed assistance, not a required free backend. |
| **GitHub / GitHub Actions** | GitHub’s product pricing/free Actions minutes are separate from Google services; public-repository Actions and free-account allowances may be usable at no charge, but the allowance and runner/storage policy are GitHub terms, not an Apps Script quota. | Actions is ephemeral CI, not guaranteed always-on hosting. Secrets, OAuth refresh tokens and `.clasp.json` must be protected. Runners have time, concurrency and monthly included-minute limits that can change by account/repository. | Google’s clasp guide documents local development, version/deployment management and GitHub Actions CI/CD. Use Actions to lint/test/push Apps Script with `CLASPRC_JSON` and `CLASP_JSON` secrets; it does not remove Apps Script runtime quotas or make Workspace features free. |

## Apps Script quotas that drive architecture

Google’s official quota table distinguishes **consumer accounts (for example, `gmail.com`)** from **Google Workspace accounts**. The quotas are per user and reset 24 hours after the first request, rather than necessarily at midnight. Current daily examples are:

| Apps Script feature | Consumer | Workspace |
|---|---:|---:|
| Calendar events created | 5,000/day | 10,000/day |
| Documents created | 250/day | 1,500/day |
| Files converted | 2,000/day | 4,000/day |
| Email recipients/day (MailApp example) | 100/day | 1,500/day |
| Email recipients/day within domain | 100/day | 2,000/day |
| Properties read/write | 50,000/day | 500,000/day |
| Spreadsheets created | 250/day | 3,200/day |
| Trigger total runtime | 90 min/day | 6 hr/day |
| URL Fetch calls | 20,000/day | 100,000/day |
| Static Map renders | 1,000/day | 10,000/day |
| Google Maps Directions queries | 1,000/day | 10,000/day |
| Google Maps Geocode calls | 1,000/day | 10,000/day |
| Translate calls | 5,000/day | 20,000/day |
| Apps Script projects created | 50/day | 50/day |

Important per-execution and storage limits apply to both account classes: six minutes per execution; 30 seconds for custom functions and Workspace add-ons; 30 simultaneous executions per user and 1,000 per script; 20 triggers per user per script; 200 versions per script; 250 email attachments/message; 50 recipients/message; 25 MB total attachments/message; 9 KB per Properties value and 500 KB per property store; 50 MB URL Fetch response and POST; 100 URL Fetch headers; 8 KB total header size; and 2 KB URL length. Email body size is 200 KB for consumer accounts and 400 KB for Workspace accounts.

These limits mean that a free design should:

1. **Batch and cache.** Read/write ranges in bulk, use batch APIs, cache stable reference data, and avoid per-row service calls.
2. **Queue work in Sheets/Drive, not in memory.** Use an idempotency key, status column and retry timestamp; a trigger should process a bounded batch and exit well before six minutes.
3. **Spread work over time.** Use time-driven triggers and jitter/backoff. Do not run a midnight full poll of every calendar or external endpoint.
4. **Keep triggers sparse.** Form-submit triggers are preferable to polling; use one dispatcher trigger per project where possible.
5. **Treat email and Maps as scarce.** Send digests rather than one message per record, and geocode once then cache coordinates.
6. **Monitor.** Use `MailApp.getRemainingDailyQuota()`, Apps Script execution history, and the Google Cloud Console for standard-cloud-project API quota usage.

Google states that exceeding quotas stops execution with an exception, and that quotas can be changed or removed without notice. A script may also hit an associated product quota before its Apps Script-specific quota.

## Integration and network model

**Inbound HTTP.** A standalone or bound project can be deployed as a web app when it defines `doGet(e)` or `doPost(e)` returning `HtmlOutput` or `TextOutput`. Query parameters and POST bodies arrive in the event object. A deployment may execute as the owner or as the accessing user; this changes the authorization boundary. The `/dev` test URL is only for editors. A production web app can be embedded in Sites, but both Sites and web-app permissions must permit access and viewers may see authorization prompts. Protect owner-executed deployments carefully: do not send `ScriptApp.getOAuthToken()` to the browser.

**Outbound HTTP.** `UrlFetchApp` calls external HTTP/HTTPS endpoints and is subject to the Apps Script URL Fetch quotas and payload limits above. Use signed requests, restricted API keys, short timeouts where supported, retries with truncated exponential backoff, and an allowlist/manifest policy for external URLs. It is outbound-only from the script; a partner cannot call `UrlFetchApp` directly, so expose a web-app endpoint or use a supported webhook.

**OAuth and Workspace APIs.** Built-in services manage authorization scopes; Advanced services are thin wrappers around Workspace APIs. The Apps Script API can create, modify, deploy and execute projects remotely, but the official concepts page says it **does not work with service accounts** and requires enabling the API and granting third-party access. For user-data APIs, use user OAuth or an approved service-account/domain-delegation design where the specific API and Workspace policy permit it. A service account also concentrates quota under one account for some APIs.

**GitHub Actions.** Google’s official clasp guide supports local source control, versions, deployment and GitHub Actions. CI stores `.clasprc.json` (refresh token) and `.clasp.json` as GitHub Secrets; these must never be committed. Actions deploys code but does not provide persistent runtime, bypass quotas, or turn paid Workspace/Chat/Maps/Gemini features into free services.

## Service-specific findings and caveats

### Google Workspace pricing and the “free trial” trap

The current Workspace pricing page lists Business Starter, Standard and Plus as paid per-user plans and shows **“No cost for 14 days.”** That is a trial, not an ongoing free plan. The page also notes promotional introductory prices and that promotional features may be time-limited. A nonprofit may qualify for separate nonprofit offers, but eligibility and product terms must be checked before treating them as permanent. A consumer Google Account remains the simplest zero-subscription route for Apps Script, Drive, Sheets, Forms, Calendar, Tasks and Sites, subject to consumer quotas, personal storage and account-policy constraints.

Apps Script quota documentation also warns that trial accounts have additional limits and that after converting a trial to paid, limits increase only after the domain has cumulatively paid at least USD 100 (or equivalent) and at least 60 days have passed since reaching that threshold. Do not size production operations around a trial account.

### API quota billing change in 2026

Drive, Sheets, Forms and Calendar official quota pages currently state that standard API use is available at no additional cost, but that exceeding quota request limits is **planned to incur charges to the Google Cloud billing account later in 2026**, with more details and at least 90 days’ notice. The pages also show new daily billing-threshold concepts (for example, Calendar 1,000,000 requests/day and Drive 400,000,000 quota units/day) and say thresholds cannot be increased. This is a major date-sensitive caveat: in a no-billing NGO environment, use budget alerts, quotas, conservative batching and a fail-closed design before any announced change takes effect.

### Data retention and outbound/inbound restrictions

Apps Script execution history and logs are operational telemetry, not a durable audit archive. Script Properties are tiny key/value storage, not a database; Drive/Sheets are the practical free persistence layer, but their storage, sharing, trash and organizational retention policies apply. Google Sites is a front end, not a data store. Chat webhooks are one-way and cannot receive interaction events. Tasks is a human task list, not a durable message queue. Calendar push notifications and form-submit triggers are preferable to high-rate polling, but any watch/trigger expiration and reauthorization must be handled in the design.

Never publish beneficiary or health data in a public Form, Sheet, Site, Chat webhook or client-side Gemini prompt without a data-protection review. API keys, webhook URLs, OAuth refresh tokens and owner-executed web-app endpoints are credentials. Keep them in restricted properties/secret stores and GitHub Secrets, rotate them, and assume URLs can leak through logs or browser history.

## Recommended zero-cost reference architecture

For a genuinely no-recurring-bill pilot, use a consumer Google Account (or a verified nonprofit Workspace grant) as the owner; Drive folders and Sheets as the record store; Forms as intake; Apps Script as a bounded dispatcher; Calendar and Tasks for human coordination; Sites as a simple authenticated/public information front end; email or a manually configured alternative for notifications; and Gemini only as optional free-tier assistance with explicit human review. Avoid Chat incoming webhooks unless a paid Business/Enterprise Workspace account is already available. Avoid Maps API billing dependencies unless a hard quota/budget guard or a nonprofit credit is confirmed. Use batch processing, idempotency, trigger-runtime budgeting, exponential backoff and a manual replay sheet from day one.

## Official sources

1. [Apps Script quotas and limits](https://developers.google.com/apps-script/guides/services/quotas)
2. [Apps Script web apps](https://developers.google.com/apps-script/guides/web)
3. [Apps Script service reference](https://developers.google.com/apps-script/reference)
4. [Apps Script external APIs / UrlFetch](https://developers.google.com/apps-script/guides/services/external)
5. [Apps Script API concepts](https://developers.google.com/apps-script/api/concepts)
6. [Apps Script clasp and GitHub Actions](https://developers.google.com/apps-script/guides/clasp)
7. [Google Workspace pricing](https://workspace.google.com/pricing)
8. [Google Drive API quotas, limits and pricing](https://developers.google.com/drive/api/guides/limits)
9. [Google Sheets API limits and pricing](https://developers.google.com/sheets/api/limits)
10. [Google Forms API usage limits and pricing](https://developers.google.com/workspace/forms/api/limits)
11. [Google Calendar API quotas and pricing](https://developers.google.com/calendar/api/guides/quota)
12. [Google Tasks API quotas](https://developers.google.com/workspace/tasks/limits)
13. [Google Chat API usage limits](https://developers.google.com/workspace/chat/limits)
14. [Google Chat incoming webhooks](https://developers.google.com/workspace/chat/quickstart/webhooks)
15. [Google Sites: create and publish](https://support.google.com/sites/answer/6372878)
16. [Google Maps Platform pricing overview](https://developers.google.com/maps/billing-and-pricing/overview)
17. [Google Maps Platform core pricing list](https://developers.google.com/maps/billing-and-pricing/pricing)
18. [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing)
19. [Gemini API rate limits](https://ai.google.dev/gemini-api/docs/rate-limits)
20. [Gemini API key security and migration](https://ai.google.dev/gemini-api/docs/api-key)
