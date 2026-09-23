# Free-serverless verification checklist

## Account and cost

- [ ] The account or edition is named and its quotas are not confused with another edition.
- [ ] Each dependency has one explicit cost label.
- [ ] Trials, promotional allowances, billing-enabled plans, and payment-method behavior are called out.
- [ ] Official pricing and quota sources were rechecked on `{YYYY-MM-DD}`.
- [ ] The first migration trigger and a strict zero-billing go/no-go decision are documented.

## Data protection and identity

- [ ] OAuth scopes and sharing permissions follow least privilege.
- [ ] No API key, token, service-account key, webhook URL, or refresh token is in source, prompts, logs, or client code.
- [ ] Sensitive beneficiary, health, or safeguarding data has an approved location, retention period, and access review.
- [ ] AI use is optional, redacted, human-reviewed, and has a no-AI path.
- [ ] Backups, exports, ownership, handover, deletion, and incident response are testable.

## Quota and reliability

- [ ] Reads and writes are batched and bounded below execution limits.
- [ ] Work is idempotent and uses a key, status, retry timestamp, or equivalent checkpoint.
- [ ] Retry/backoff handles transient errors without a trigger storm.
- [ ] 403, 429, storage exhaustion, authentication failure, and provider outage have safe behavior.
- [ ] Manual intake, replay, notification, and recovery paths have been exercised.

## Release hygiene

- [ ] All names and paths follow the cpintl-org standard.
- [ ] Official source links and access dates are present.
- [ ] Scripts pass valid and invalid input tests.
- [ ] Markdown links and structured files validate.
- [ ] `git diff --check` and secret/path scans pass.
