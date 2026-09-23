---
name: workspace-drive-search
description: Search and retrieve approved Google Drive or Workspace resources through a provider-neutral bridge with least privilege, exact identity matching, sensitivity checks, and a manual fallback. Use when an agent needs to locate repository-linked documents, Sheets, or folders in Google Workspace.
---

# Workspace Drive search

Use the bridge only after the user has authorized the Workspace scope and the mapping in `config/mcp-bridge-mapping.yaml` identifies the approved repository path and Drive folder. Never infer a Drive ID from a display name.

## Workflow

1. Classify the request as metadata search, content retrieval, or write/sync. Default to metadata and read-only.
2. Validate `owner`, `repository`, `ref`, repository path, Drive folder ID, sensitivity, and requester role.
3. Search within the mapped folder, using exact or narrowly bounded terms. Do not search an entire personal Drive for convenience.
4. Match by provider-issued file ID and mapped path; treat display names as non-unique.
5. Return title, MIME type, file ID, mapped repository path, modified time, access state, and a link only when the caller is authorized.
6. Do not expose file contents or links for restricted data without a human-approved purpose.
7. If the bridge, credentials, or mapping is unavailable, return a manual task with the exact folder and search terms; never fabricate a result.

## Safety

Do not put OAuth tokens, service-account keys, beneficiary data, or private file contents in logs. Do not follow public links outside the mapped scope. A search result is not permission to edit, share, delete, or publish.

## References

Read `references/bridge-contract.md` for the typed request/response contract and `scripts/validate_bridge_request.py` for network-free validation.
