# Architecture decision record: {decision-title}

**Status:** proposed | accepted | superseded | rejected  
**Date:** {YYYY-MM-DD}  
**Owner:** {role-or-team}  
**Scope:** {system-or-component}

## Decision

{State the decision in one paragraph. Separate the user requirement, verified fact, assumption, and recommendation.}

## Account and cost boundary

- Account or edition: `{account-or-edition}`
- Billing enabled: `{yes|no|unknown}`
- Dependency labels: `{labels}`
- Explicit exclusions: `{excluded-services-or-features}`

## Evidence

| Claim | Status | Source URL | Access date | Confidence | Notes |
|---|---|---|---|---|---|
| {claim} | confirmed / partly confirmed / unsupported / date-sensitive | {official-url} | {YYYY-MM-DD} | high / medium / low | {correction-or-uncertainty} |

## Security and privacy

{Describe least privilege, secret isolation, data minimization, retention, access review, audit, incident response, and the no-AI fallback.}

## Failure and recovery

{Describe the first quota or dependency likely to fail, user-visible behavior, retry/backoff, manual fallback, backup, and recovery owner.}

## Migration trigger

{State the measurable condition that requires a paid, managed, or different storage/compute service.}

## Review conditions

{List the facts, quotas, policies, or dates that must be rechecked before launch or renewal.}
