# Workspace bridge contract

## Request

```json
{
  "operation": "search_metadata",
  "owner": "{github-owner}",
  "repository": "{repository}",
  "ref": "main",
  "repositoryPath": "{repository-path}",
  "driveFolderId": "{drive-folder-id}",
  "query": "{user-approved-query}",
  "sensitivity": "public|internal|restricted",
  "requesterRole": "{role}",
  "dryRun": true
}
```

## Response

```json
{
  "status": "ok|manual_review|denied|error",
  "results": [{"fileId":"{opaque-id}","name":"{display-name}","mimeType":"{mime-type}","modifiedTime":"{provider-time}","repositoryPath":"{repository-path}"}],
  "redactionApplied": true,
  "auditId": "{audit-id-or-null}",
  "errorCode": "{code-or-null}"
}
```

`driveFolderId` and `fileId` are opaque provider identifiers. Keep them exactly as returned. `dryRun` must default to true for a new deployment.
