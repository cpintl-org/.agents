# Quota telemetry and migration playbook

## Minimum telemetry register

Keep a small operational register in a restricted Sheet or approved datastore. Record the date, account/project, service, operation, requests, successes, retries, 403/429 errors, storage estimate, remaining allowance when available, and next review date. Avoid storing beneficiary data in telemetry.

Recommended fields are `observedAt`, `accountType`, `service`, `operation`, `count`, `errorCount`, `retryCount`, `estimatedUsage`, `limitSource`, `sourceAccessDate`, `ownerRole`, and `actionRequired`.

Use daily or weekly summaries rather than per-event logging. Retain only the period needed for operations and trend analysis. Export the register with the system backup and test that a human can understand it without execution logs.

## Migration triggers

Define triggers before launch. Examples include repeated quota exhaustion, sustained queue age above the service target, storage approaching the account limit, increased concurrent users, an approval requirement for sensitive data, unavailable recovery ownership, or a provider changing a free allowance. A trigger is a decision point, not proof that a paid service is automatically required.

## Migration sequence

1. Freeze new features and record the current schema, sharing model, OAuth scopes, retention rules, and export format.
2. Export Drive files, Sheets registers, audit rows, configuration, and synthetic test fixtures. Verify counts and checksums where practical.
3. Select the next service by data sensitivity, recovery needs, cost boundary, and operational capacity—not by marketing claims.
4. Build a dual-read or staged-import test with synthetic data first. Do not copy confidential data until access controls and retention are approved.
5. Reconcile counts, identifiers, timestamps, permissions, and audit history. Run recovery and rollback exercises.
6. Change the system-of-record declaration, update the component matrix and decision record, and retain the old export according to policy.
7. Decommission old triggers, public links, credentials, and integrations only after the owner verifies the cutover.
