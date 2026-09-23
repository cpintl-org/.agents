# Security and safety policy

This repository contains reusable instructions, schemas, templates, and optional integration code. It must not contain secrets, beneficiary records, health or safeguarding case data, private OAuth tokens, or unapproved public links.

## Required controls

| Area | Rule |
|---|---|
| Secrets | Never commit API keys, passwords, bearer tokens, refresh tokens, private keys, or service-account JSON. Use approved secret stores and placeholders. |
| Data | Treat personal, health, safeguarding, financial, and case data as restricted. Do not place it in prompts, GitHub, public Drive links, Actions logs, or model calls without an approved policy. |
| Identity | Use least privilege. Preserve provider-issued IDs; never derive access from display names. |
| Paths | Reject traversal, control characters, reserved names, unsafe Unicode, case-only collisions, and embedded credentials. |
| Integrations | Default to read-only and dry-run. Require human review for writes, sharing, publishing, deletion, migration, and security changes. |
| AI | Redact first, use an approved provider, record only minimum audit metadata, and keep a manual fallback. |
| Recovery | Export and test recovery before changing a system of record. Do not call a free tier an SLA or unlimited service. |

## Reporting

Do not disclose a suspected secret or vulnerability in a public issue. Use the repository owner’s verified private security contact or GitHub’s private vulnerability reporting feature when enabled. If no verified contact is available, tell the responsible organization administrator without copying the sensitive value into email, chat, or an issue.

Include only a redacted description, affected path or commit, impact, reproduction steps that do not expose secrets, and a safe contact method. The maintainer should acknowledge receipt, revoke or rotate affected credentials, preserve evidence safely, patch the issue, and document closure.

## Supported branch model

`main` is the only permanent branch and the canonical source. Temporary branches may exist during a pull request but should be deleted after merge or closure. Branch protection and required checks do not replace review of the code, data sensitivity, or external deployment configuration.
