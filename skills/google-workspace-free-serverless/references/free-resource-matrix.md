# Free and Free-Tier Resource Matrix for the NGO Operations Architecture

**Access date for all sources:** 2026-09-18  
**Scope:** Conservative synthesis of the supplied research on Google Workspace, Firebase Spark, and GitHub Free. The matrix treats “free” as a bounded operating condition, not as a promise of unlimited capacity, permanent product behavior, or absence of governance obligations.

## Executive conclusion

A small NGO or operations platform can be built with no recurring subscription payment by using a personal Google Account or Google Workspace Essentials Starter for the operational system of record, Google Forms for intake, Sheets for small structured registers, Drive for files, Calendar for scheduling, bounded Apps Script for automation, and Google Sites or GitHub Pages as a presentation layer. GitHub Free can provide source control and limited automation. Firebase Spark can be an optional application layer for a modest portal, using Hosting, Firestore or Realtime Database, and non-phone Authentication within the published Spark quotas.

The recommended zero-charge baseline is deliberately narrower than the full product catalog. It excludes billing-dependent Google Maps services, Firebase Cloud Storage, Cloud Functions, App Hosting, Phone Authentication, SQL Connect beyond its trial, Google Chat incoming webhooks, and production reliance on Gemini. These services may be useful, but they are not dependable components of a strict no-payment architecture. The baseline also avoids treating Sites, Tasks, GitHub Pages, Apps Script properties, Firebase free products, or GitHub artifacts as a durable case-management database or archival system.

“Always-free” below means that the source describes an ongoing $0 plan or an ongoing no-cost allowance, subject to product quotas and policy. “Free-tier” means a limited allowance that can be exhausted, shut off, or become billable. “Trial” means a temporary or one-time entitlement and is not accepted as a permanent baseline. Product terms, quotas, pricing, and API billing behavior are date-sensitive. Google’s standardized Workspace API quota and possible over-threshold billing transition is specifically planned for later in 2026, after notice, so current no-charge API use must be rechecked before launch.

## 1. Definitions used in this report

| Category | Conservative meaning for architecture decisions |
|---|---|
| **Always-free** | An ongoing $0 plan or documented ongoing no-cost product allowance. It remains quota-bounded and can still be subject to account storage, acceptable-use, retention, authentication, sharing, privacy, and security constraints. |
| **Free-tier / quota-bounded** | A continuing allowance with a hard product limit, rate limit, or fair-use boundary. Exceeding it may stop operations, return errors, require waiting for reset, or become billable when billing is enabled. It is suitable only with monitoring and graceful failure. |
| **Trial / promotional** | A time-limited, one-time, or promotional entitlement. It must not be used as the assumed long-term capacity of the system. |
| **Non-guaranteed / billing-dependent** | A service whose documented path requires billing, a paid plan, or a condition not guaranteed by the no-payment baseline. It may be included only as an optional, explicitly approved dependency. |

## 2. Conservative service matrix

Confidence describes confidence in the classification and stated limits based on the supplied official documentation, not a guarantee that the product will retain those terms after the access date. “High” means the supplied research states an explicit official plan or limit. “Medium” means the product behavior is dynamic, model/SKU-specific, or the official extracted material did not expose a complete numeric limit.

| Service | Free status | Important limits and uncertainty | Integration method | Confidence |
|---|---|---|---|---|
| **Google Drive** | Free or Essentials Starter at $0, quota-bounded; 15 GB Drive per Essentials user and personal-account pool. Standard API use is currently no additional cost within quotas, but Google plans over-threshold Workspace API billing later in 2026. | Storage is shared with Gmail, Photos, Meet recordings, and newer collaborative files. Over quota blocks uploads and new collaborative files; long-term overage may lead to deletion after notice. API limits include 1,000,000 quota units/minute/project, 325,000/minute/user/project, 1 TB/day egress threshold, 750 GB/day upload per user, and 5 TB maximum upload file. | Apps Script Drive service; Advanced Drive/REST API; OAuth; suitable service-account or Cloud identity patterns; Apps Script web apps; GitHub Actions with Google authentication. | **High** for stated plan and documented limits; **Medium** for future billing behavior. |
| **Google Sheets** | Ongoing no-charge use on personal accounts and Essentials Starter; API use currently no additional cost within quotas. | Shared Drive/account storage applies. Per-minute quotas apply; Google gives 300 read requests/minute/project as an example, recommends 2 MB maximum request payloads, and fails requests processing over 180 seconds. Sheets is not a transactional database. Future API overage billing is planned later in 2026. | Apps Script Spreadsheet service; Sheets REST API with OAuth; Forms response destinations; Sites embeds and charts; external HTTPS clients and GitHub Actions. | **High** for role and general limits; **Medium** for dynamic quota table and future billing. |
| **Google Forms** | Ongoing no-charge intake capability on personal accounts and Essentials Starter; normal API use currently no additional cost within quotas. | Per-minute limits and 429 responses apply; watches have additional limits. Responses and uploaded files consume Drive storage. API-created forms after 2026-06-30 are unpublished by default and must be explicitly published before accepting responses. | FormApp and Apps Script triggers; Forms REST API with OAuth; Sheet destinations; Drive uploads; Sites embeds; Apps Script web-app links. | **High**. |
| **Google Apps Script** | Ongoing no-separate-subscription automation layer, but not unlimited compute. Consumer and Workspace accounts have different quotas. | Consumer trigger runtime is 90 minutes/day versus 6 hours/day for Workspace; URL Fetch is 20,000/day versus 100,000/day; Calendar events are 5,000/day versus 10,000/day; executions are limited to 6 minutes; 30 simultaneous executions/user; 20 triggers/user/script; 500 KB Properties store; 50 MB URL Fetch response/POST. Quotas can change without notice. | Built-in Drive, Sheets, Forms, Calendar, Gmail and other services; UrlFetch; OAuth libraries; installable triggers; doGet/doPost web apps; external API calls. | **High** for supplied quotas; always recheck before launch. |
| **Google Calendar** | Ongoing no-charge consumer use and current standard API use within quota. | API quotas are 10,000 requests/minute/project and 600/minute/user/project, with a documented 1,000,000 requests/day billing threshold. Apps Script event limits are 5,000/day consumer and 10,000/day Workspace. Rapid-write and per-calendar operational limits can be tighter. Future over-threshold charges are planned. | CalendarApp; Calendar REST API/OAuth; Forms-to-calendar triggers; web apps; push notifications; GitHub Actions with Google authentication. | **High** for supplied figures; **Medium** for future billing. |
| **Google Tasks** | Ongoing consumer-usable service with a documented courtesy limit and no separate API price identified. | 50,000 queries/day courtesy limit; increases are discretionary. Documentation states up to 20,000 non-hidden tasks per list and 100,000 total tasks per user. It is user-scoped and is not a strong shared or auditable case queue. | REST/Advanced Tasks service with OAuth or UrlFetch; synchronization with Sheets, Gmail, and Calendar; custom Apps Script views. | **High** for classification; **Medium** for suitability as operational queue. |
| **Google Sites** | Ongoing free publishing and embedding layer for personal and Essentials accounts. | It is a presentation/container layer, not a general runtime, database, webhook system, or server-side data model. The Sites API is deprecated, classic-only, and not a safe dependency for modern Sites automation. Sharing, publication, embedding, and account permissions remain constraints. | Sites UI publication; embeds for Drive, Forms, Sheets/charts, Maps Embed, and deployed Apps Script web apps. | **High**. |
| **Google Chat** | Basic Chat may be available at no charge, but the documented incoming-webhook setup requires Business or Enterprise Workspace and administrator permission. | Incoming webhooks are one-way and bound to one space. They cannot receive interactions. Webhook delivery is limited to 1 request/second/space shared among webhooks. General quotas include 3,000 message writes/minute/project and 3,000 reads/minute/project. | Apps Script UrlFetch to webhook; Advanced Chat service; Chat REST API; interactive Chat apps where plan and administration permit. | **High** that webhooks are non-baseline; **Medium** for plan-specific feature availability. |
| **Google Maps Embed** | Documented as unlimited free usage. | Embed is the only Maps path classified as genuinely free in the supplied research. It is distinct from Maps JavaScript, Routes, Places, geocoding, and other metered APIs. | Embed iframe in Sites or Apps Script web apps. | **High** for the stated distinction; verify current terms before public launch. |
| **Other Google Maps Platform services** | Billing-dependent pay-as-you-go with SKU-specific monthly free caps, not an unlimited free tier. | A billing account is normally required. Free caps vary by SKU; supplied examples include 30,000 map loads/minute/project and 300/IP/minute, while current monthly caps are SKU-specific. Usage above caps is chargeable. NGO/public-program credits require eligibility and application. | Apps Script Maps service; REST APIs; API keys/OAuth; web apps; Cloud or GitHub Actions. | **High** that these are non-baseline; **Medium** for SKU-specific amounts. |
| **Gemini API and Gemini in Workspace** | Gemini API has an ongoing free tier for selected models, but model, project, and rate limited. Gemini Workspace features are plan-dependent. | Free-tier content may be used to improve Google products. Paid setup requires billing and may require prepaid credits. Limits and model access change. Sensitive beneficiary or safeguarding data must not be sent without an approved data policy. A non-AI fallback is required. | Server-side Apps Script UrlFetch; Vertex AI/REST where approved; protected GitHub Actions secrets; never expose keys client-side or in repositories. | **High** that it is not a privacy-preserving baseline; **Medium** for changing model/rate details. |
| **Firebase Hosting** | Ongoing Spark no-cost allowance; no payment method required. | 10 GB Hosting storage and 10 GB/month CDN transfer per project; deploys stop at the storage cap and sites may be disabled after the transfer cap. Maximum individual file is 2 GB. | Static hosting; GitHub Actions deployment; Apps Script can call hosted endpoints; Sites can embed Apps Script web apps. | **High**. |
| **Cloud Firestore Standard** | Ongoing Spark free tier; over-quota product use is shut off rather than automatically billed on Spark. | 1 GiB stored; 50,000 reads/day; 20,000 writes/day; 20,000 deletes/day; 10 GiB/month outbound. Quotas reset daily around midnight Pacific. TTL, PITR, backups, restores, and clones require billing. | REST API with Firebase ID tokens or Google OAuth/service-account tokens; Apps Script UrlFetch. Service-account IAM can bypass Security Rules, so use least privilege. | **High**. |
| **Firebase Realtime Database** | Ongoing Spark no-cost allowance. | 1 GB stored and 10 GB/month downloaded. Technical limits include 200,000 simultaneous connections per database. Download accounting includes protocol, TLS, and denied-operation traffic. | Native REST endpoint with Firebase ID tokens or Google OAuth/service-account tokens; Apps Script HTTPS calls. | **High**. |
| **Firebase Authentication, non-phone methods** | Ongoing Spark no-cost for supported email, social, anonymous, and custom methods, subject to operational limits. | Published Spark limits include 3,000 daily active users for Tier 1, 2 DAU for Tier 2, 100 account creations/hour/IP, 1,000 verification emails/day, 150 password-reset emails/day, and 5 email-link sign-ins/day. Registered accounts are unlimited. | Firebase ID tokens; Firebase Auth REST endpoints; server-side Apps Script integration. | **High** for supplied limits; **Medium** where Firebase tier classification applies. |
| **Firebase Cloud Messaging** | Ongoing no-cost Firebase product. | Payloads are limited to 4,096 bytes. Topic subscription operations are limited to 3,000 QPS/project. A trusted sender or app server is required. | Apps Script HTTPS requests using protected OAuth/service-account credentials; client apps receive messages. | **High**. |
| **Firebase Analytics, Crashlytics, App Check, In-App Messaging, Performance Monitoring, App Distribution** | Listed as no-cost products on Spark, with product-specific fair-use and feature limits. | These are telemetry, protection, messaging, and testing tools. They do not replace Workspace audit logs, case records, or durable retention. Crashlytics custom logging is cited at 64 kB; Analytics supports up to 500 distinct event types per app. | Firebase SDKs and product APIs; Apps Script can administer selected APIs. | **Medium** because feature and fair-use limits are product-specific. |
| **Firebase Remote Config and A/B Testing** | Ongoing no-cost allowance, but date-sensitive pricing applies. | Pricing states 100,000 Remote Config fetches/day/project no-cost, with pricing above that starting 2026-09-01. Values are client-readable and must not contain secrets or operational records. | Firebase APIs and SDKs; Apps Script administration. | **High** for the supplied dated threshold; recheck after the access date. |
| **Firebase Cloud Storage** | Not available on Spark since the September 2024 change; Blaze is required. | Spark projects lose bucket access and calls may return 402/403. Blaze has no-cost allowances but is a billing-enabled plan and can incur charges. | For strict zero billing, store files in Drive and expose controlled links. | **High**. |
| **Firebase Cloud Functions** | Not deployable on Spark; Blaze is required even though Blaze includes allowances. | Blaze allowances include 2M invocations/month, 400K GB-seconds/month, 200K CPU-seconds/month, and 5 GB/month outbound. Those are not a no-billing guarantee. | Use Apps Script web apps and UrlFetch for small webhooks in the Spark baseline. | **High**. |
| **Firebase App Hosting** | Not available on Spark; Blaze is required. | Blaze allowances are aggregated by billing account and can incur charges above allowance. It is a billing-enabled Google Cloud stack. | Use Firebase static Hosting for strict zero billing; GitHub integration remains optional. | **High**. |
| **Firebase SQL Connect / Cloud SQL** | Trial only on Spark, not ongoing free capacity. | One lifetime Spark trial instance for 90 days, about 8,000 operations/day and 330 MiB/day egress; then archive, with deletion after a further 90 days without upgrade. | Do not use as the long-lived system of record in a no-payment design. | **High**. |
| **GitHub Free account or organization** | Ongoing $0 plan with unlimited public/private repositories and collaborators, subject to limited private-repository features. | Private Free repositories include 2,000 Actions minutes/month, 500 MB pooled artifact/Packages storage, and 10 GB Actions cache per repository. Public standard-runner Actions and self-hosted runner use are free from GitHub-hosted-minute charges. | GitHub REST API, GitHub Apps, OAuth, webhooks, Apps Script UrlFetch, and Actions-to-Workspace HTTPS calls. | **High**. |
| **GitHub Actions, private Free repositories** | Free only within the recurring included allowance. | Minutes reset each billing cycle; artifacts/logs normally retain 90 days; inactive caches are evicted after 7 days. Standard job maximum is 6 hours; workflow maximum is 35 days; Free concurrency is 20. Overage may be billed if payment is enabled or blocked without a valid payment method. | Scheduled/build/deployment jobs calling Apps Script or Google APIs with protected secrets. | **High**. |
| **GitHub Actions, public repositories** | Standard GitHub-hosted runners are free and unlimited for public repositories; self-hosted runners are free from GitHub-hosted-minute charges. | Larger runners are charged even for public repositories. Public repositories expose source, workflows, issues, logs, and accidental artifacts, so they are unsuitable for confidential NGO data. | Actions can call Apps Script web apps or Google APIs; use private repositories for sensitive source and configuration. | **High**. |
| **GitHub Pages** | Free static hosting for public repositories. | It is not a backend or transactional data layer. Supplied limits include a recommended 1 GB source repository, 1 GB published site maximum, 10-minute deployment timeout, 100 GB/month soft bandwidth limit, and 10 builds/hour soft limit. GitHub prohibits using Pages as free hosting for an online business, e-commerce site, or primarily commercial SaaS and warns against sensitive transactions. | Static HTML/CSS/JavaScript front end calling approved HTTPS APIs; no secrets in client code. | **High** for its static-only role; **Medium** for soft limits. |
| **GitHub REST API, Apps, OAuth, and webhooks** | Registration, API access, and webhooks do not require a paid GitHub plan. | Primary REST limits are 60 requests/hour unauthenticated, 5,000/hour authenticated users, and 1,000/hour per repository for GITHUB_TOKEN. Secondary limits also apply. Apps Script web-app documentation does not establish direct HMAC-header validation, so use a header-aware intermediary for authenticated webhook ingestion. | Apps Script UrlFetch for outbound calls; GitHub Apps for fine-grained permissions and short-lived tokens; webhooks to a header-aware HTTPS endpoint. | **High** for rate-limit figures; **Medium** for the Apps Script webhook security caveat. |
| **Self-hosted GitHub Actions runners** | GitHub does not charge hosted-runner minutes for self-hosted runners, including private repositories. | The operator pays for and secures the machine, network, uptime, patching, egress, and secrets. It is not a zero-cost infrastructure guarantee. | Runner reaches Workspace APIs or Apps Script endpoints subject to their quotas and authentication. | **High**. |

## 3. Recommended baseline stack for the PDF architecture

The safest baseline is a **Workspace-first, quota-bounded architecture**. Use a personal Google Account for the smallest pilot or Essentials Starter for up to 100 users where the absence of Gmail/custom business email is acceptable. Keep Drive as the controlled file store, Sheets as small structured registers and configuration tables, and Forms as the intake surface. Use Calendar only for scheduling and reminders. Use Tasks only for personal follow-up, not as the shared case-management queue.

Use Apps Script as the thin automation and integration layer. Design each workflow to batch operations, be idempotent, retry 429 and transient errors with exponential backoff, and record a compact operational status in Sheets or Drive. Avoid large synchronous jobs because of the six-minute execution limit. Keep durable evidence in Drive or a controlled Sheet rather than in execution logs or Script Properties. Explicitly publish API-created Forms after creation. Use email or a Sheet-based dashboard as the default notification path.

Use Google Sites as the human-facing presentation shell. Embed Forms, Sheets/charts, controlled Drive material, Maps Embed where needed, and Apps Script web apps. Do not build against the deprecated Sites API, and do not assume Sites supplies authentication, a database, webhooks, or durable application state.

Use GitHub Free for version control, issue tracking, documentation, and reproducible Apps Script or static-site deployment. Prefer private repositories for code that contains operational logic or configuration. Keep secrets in protected repository or organization secrets and avoid putting beneficiary data, credentials, donor records, or case data in repositories, issues, artifacts, logs, or caches. Keep production records in Workspace, not in GitHub Actions artifacts.

Add Firebase Spark only when a browser or mobile portal genuinely needs an application data layer. A conservative Firebase addition is static Firebase Hosting plus either Firestore or Realtime Database and non-phone Authentication. Treat project quotas as shared across all applications. Do not assume Spark provides file storage, server-side functions, a SQL database, or a managed webhook runtime. Continue to hold authoritative files and audit evidence in Drive unless a separate retention and security design is approved.

The baseline should not require Maps APIs beyond Maps Embed, and it should not require Gemini. If either is later approved, isolate it behind an optional adapter, enforce quotas and budgets, and provide a manual fallback. Gemini must not receive sensitive beneficiary or safeguarding data without an approved data-protection policy. The system should remain operational when Gemini, Firebase, GitHub Actions, or an external API is unavailable.

Ownership and continuity are part of the baseline. A personal Google Account can be deleted after two years of inactivity, subject to notice and exceptions. Assign responsible owners, document recovery contacts, export critical data, review sharing and public links, and establish a handover procedure. “No monetary cost” does not remove OAuth, API-key, sharing, retention, acceptable-use, privacy, safeguarding, or incident-response responsibilities.

## 4. Services to exclude or label non-guaranteed

| Service or dependency | Treatment in the architecture | Reason |
|---|---|---|
| **Google Workspace Business Starter, Standard, or Plus** | Exclude from the strict baseline or label as paid after trial. | The supplied pricing is a 14-day no-cost trial, not a continuing free plan. |
| **Google Chat incoming webhooks** | Label non-guaranteed; do not make critical notifications depend on them. | The documented webhook path requires Business or Enterprise Workspace and administrator permission. Use email or a Sheet dashboard as fallback. |
| **Maps JavaScript, Routes, Places, geocoding, and related APIs** | Optional, billing-dependent, with budget and quota alerts. | They use pay-as-you-go billing with SKU-specific free caps. Only Maps Embed is documented as unlimited free. |
| **Gemini as a required backend or sensitive-data processor** | Exclude from the baseline; optional human-reviewed assistance only. | Free usage is model/rate limited, free-tier data use is not the paid privacy tier, and terms can change. |
| **Firebase Cloud Storage** | Exclude from Spark baseline. | Spark bucket access is unavailable; Blaze is required. Use Drive for files under the strict no-payment design. |
| **Firebase Cloud Functions and App Hosting** | Exclude from Spark baseline. | Deployment requires Blaze, which is billing-enabled even where free allowances exist. |
| **Firebase Phone Authentication/SMS** | Exclude from strict no-payment baseline. | It is not Spark-guaranteed and SMS pricing is region-dependent. Prefer email or Google sign-in where appropriate. |
| **Firebase SQL Connect / Cloud SQL** | Exclude as a long-lived datastore. | The Spark entitlement is a one-time 90-day trial with archival and deletion behavior. |
| **Public GitHub repositories, Pages, issues, artifacts, and logs for operational data** | Exclude confidential data; use private repositories where source must be protected. | Public visibility exposes content. Pages is static hosting, not a secure transactional backend. Artifacts and logs are temporary. |
| **Self-hosted GitHub Actions runners** | Label as infrastructure-dependent, not free infrastructure. | GitHub does not charge runner minutes, but the operator pays for and secures the machine and network. |
| **Apps Script execution logs and Script Properties as an audit archive or database** | Exclude as durable storage. | Logs are not a durable audit archive and the Properties store is only 500 KB with 9 KB/value limits. |
| **Google Tasks as a shared case-management queue** | Exclude; use a controlled Sheet or approved database pattern. | Tasks are primarily user-scoped and not a strong shared, auditable queue. |
| **Modern Sites API automation** | Exclude as a dependency. | The Sites API is deprecated and classic-only. Use Sites as a presentation and embedding shell. |

## 5. Operating controls required even on $0 plans

A no-payment deployment still needs an owner, a second recovery contact, documented OAuth scopes, least-privilege sharing, and a review of every public link and embedded file. Service-account credentials, API keys, GitHub tokens, Apps Script secrets, and Firebase administration credentials must remain server-side and outside Sheets cells, Sites pages, client JavaScript, public repositories, and logs.

Quota control should be explicit. Add counters for Apps Script executions, URL Fetch calls, Forms submissions, Calendar writes, Firebase reads/writes, Hosting transfer, GitHub Actions minutes, artifact storage, and API errors. Batch operations and use exponential backoff. Treat 403 and 429 responses as expected control-flow events. Configure budget and quota alerts before enabling any billing-dependent Google Cloud or Maps path. If a payment method is attached, understand that the failure mode can change from blocking to billable overage.

Data protection should be explicit. Do not place safeguarding details or beneficiary-sensitive content in Gemini free tier, public GitHub resources, public Sites, client-readable Remote Config, or unreviewed third-party integrations. Define retention, deletion, export, incident response, and handover rules. Keep a manual workflow for intake, scheduling, and notification so that the platform remains usable during quota exhaustion or API outage.

## References

All references below were accessed or supplied as current on **2026-09-18**. Product pages and quota tables are dynamic; the access date is therefore part of each citation.

[1]: https://workspace.google.com/essentials/ "Google Workspace Essentials Starter"
[2]: https://support.google.com/googleone/answer/9312312?hl=en "Google One storage and quota behavior"
[3]: https://developers.google.com/drive/api/guides/limits "Google Drive API usage limits"
[4]: https://developers.google.com/workspace/sheets/api/limits "Google Sheets API usage limits"
[5]: https://developers.google.com/apps-script/guides/web "Apps Script web apps"
[6]: https://developers.google.com/apps-script/guides/services/quotas "Apps Script quotas"
[7]: https://developers.google.com/apps-script/guides/services/external "Apps Script external APIs"
[8]: https://developers.google.com/workspace/forms/api/limits "Google Forms API usage limits"
[9]: https://developers.google.com/apps-script/reference/forms "Apps Script Forms service"
[10]: https://developers.google.com/workspace/forms/api/guides/api-changes-to-google-forms "Google Forms API changes"
[11]: https://support.google.com/sites/answer/6372880?hl=en "Google Sites sharing and publication"
[12]: https://developers.google.com/workspace/sites "Google Sites API"
[13]: https://developers.google.com/calendar/api/guides/quota "Google Calendar API quota"
[14]: https://developers.google.com/tasks "Google Tasks developer documentation"
[15]: https://developers.google.com/workspace/tasks/limits "Google Tasks API limits"
[16]: https://developers.google.com/workspace/tasks/reference/rest/v1/tasks/list "Google Tasks list reference"
[17]: https://support.google.com/chat/answer/9291345?hl=en "Google Chat availability"
[18]: https://developers.google.com/workspace/chat/quickstart/webhooks "Google Chat incoming webhooks"
[19]: https://developers.google.com/workspace/chat/limits "Google Chat API quotas"
[20]: https://developers.google.com/maps/documentation/embed/get-started "Maps Embed API"
[21]: https://developers.google.com/maps/billing-and-pricing/overview "Google Maps Platform billing and pricing"
[22]: https://developers.google.com/maps/documentation/javascript/usage-and-billing "Maps JavaScript API usage and billing"
[23]: https://ai.google.dev/gemini-api/docs/pricing "Gemini API pricing"
[24]: https://ai.google.dev/gemini-api/docs/billing "Gemini API billing"
[25]: https://ai.google.dev/gemini-api/docs/rate-limits "Gemini API rate limits"
[26]: https://ai.google.dev/gemini-api/docs/api-key "Gemini API keys"
[27]: https://workspace.google.com/pricing "Google Workspace pricing"
[28]: https://firebase.google.com/pricing "Firebase pricing and Spark plan"
[29]: https://firebase.google.com/docs/hosting/usage-quotas-pricing "Firebase Hosting quotas and pricing"
[30]: https://firebase.google.com/docs/hosting/github-integration "Firebase Hosting GitHub integration"
[31]: https://firebase.google.com/docs/firestore/quotas "Cloud Firestore quotas"
[32]: https://firebase.google.com/docs/firestore/use-rest-api "Cloud Firestore REST API"
[33]: https://firebase.google.com/docs/database/usage/billing "Realtime Database billing"
[34]: https://firebase.google.com/docs/database/usage/limits "Realtime Database limits"
[35]: https://firebase.google.com/docs/database/rest/auth "Realtime Database REST authentication"
[36]: https://firebase.google.com/docs/auth/limits "Firebase Authentication limits"
[37]: https://firebase.google.com/docs/reference/rest/auth "Firebase Authentication REST API"
[38]: https://firebase.google.com/docs/storage/faqs-storage-changes-announced-sept-2024 "Firebase Cloud Storage plan change"
[39]: https://firebase.google.com/docs/storage/web/start "Firebase Cloud Storage web setup"
[40]: https://firebase.google.com/docs/functions/quotas "Cloud Functions quotas"
[41]: https://firebase.google.com/docs/projects/billing/firebase-pricing-plans "Firebase billing plans"
[42]: https://firebase.google.com/docs/cloud-messaging "Firebase Cloud Messaging"
[43]: https://firebase.google.com/docs/analytics "Google Analytics for Firebase"
[44]: https://firebase.google.com/docs/remote-config/quotas-limits "Firebase Remote Config quotas and limits"
[45]: https://firebase.google.com/docs/app-hosting/costs "Firebase App Hosting costs"
[46]: https://firebase.google.com/docs/app-hosting "Firebase App Hosting"
[47]: https://firebase.google.com/docs/sql-connect/pricing "Firebase SQL Connect pricing"
[48]: https://github.com/pricing "GitHub pricing"
[49]: https://docs.github.com/en/get-started/learning-about-github/githubs-products "GitHub products"
[50]: https://docs.github.com/en/billing/reference/product-usage-included "GitHub included product usage"
[51]: https://docs.github.com/billing/managing-billing-for-github-actions/about-billing-for-github-actions "GitHub Actions billing"
[52]: https://docs.github.com/en/actions/reference/limits "GitHub Actions limits"
[53]: https://docs.github.com/actions/using-jobs/choosing-the-runner-for-a-job "Choosing a GitHub Actions runner"
[54]: https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api "GitHub REST API rate limits"
[55]: https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/differences-between-github-apps-and-oauth-apps "GitHub Apps and OAuth apps"
[56]: https://docs.github.com/en/webhooks/about-webhooks "GitHub webhooks"
[57]: https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries "Validating GitHub webhook deliveries"
[58]: https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages "What is GitHub Pages"
[59]: https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits "GitHub Pages limits"
[60]: https://developers.google.com/apps-script/reference/url-fetch/url-fetch-app "Apps Script UrlFetchApp"

*Prepared from the researched results supplied for this synthesis. This report preserves stated uncertainty and does not treat any trial, promotion, free cap, or undocumented behavior as a permanent entitlement.*
