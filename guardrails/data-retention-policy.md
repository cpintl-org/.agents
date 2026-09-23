# Data retention policy

This repository stores reusable instructions and schemas, not beneficiary records or secrets. Data minimization is the default.

| Data type | Default handling | Retention | Deletion or review |
|---|---|---:|---|
| Public documentation | Repository or approved Workspace location | While useful | Owner reviews annually |
| Internal configuration | Restricted repository/Drive scope | Until superseded, then 90 days | Owner confirms replacement |
| Restricted case or health data | Do not store in this repository | Not permitted by default | Follow the approved program policy |
| Prompt or model output | Store only a necessary redacted summary | 30 days unless policy requires less | Delete after review |
| Audit metadata | Keep minimum fields, no raw content | 180 days | Review for minimization |
| Backups/exports | Encrypted/restricted, documented owner | Per system policy | Test restore before deletion |

## Rules

Do not treat Git history, Drive trash, Actions logs, cached outputs, or provider history as automatic deletion. When a deletion request applies, locate all approved copies, record the action without retaining the sensitive content, and obtain the owner’s confirmation. Legal, medical, safeguarding, government, or donor requirements override this default only when documented by the responsible organization.
