# Google Workspace and Drive standard

## Display names versus IDs

Use human-readable display names for people. Use structured titles for folders and documents when humans need context. Use the provider-issued Drive file or folder ID as the stable machine reference. Never derive or guess a Drive ID from a folder name.

Synthetic display-path pattern:

```text
{organization}/
  {domain}/
    {resource}/
      {period}/
        {state}/
```

A display path is not a complete identity because names may repeat and folders may be moved. Store both the ID and the observed parent relationship.

## Resource record

```json
{
  "provider": "google-drive",
  "resourceType": "folder",
  "displayName": "{resource}",
  "displayPath": "{organization}/{domain}/{resource}",
  "fileId": "{drive-folder-id}",
  "driveId": "{shared-drive-id-or-null}",
  "parentIds": ["{parent-folder-id}"],
  "webUrl": "{provider-url}",
  "mimeType": "application/vnd.google-apps.folder",
  "retrievedAt": "{rfc3339-timestamp}"
}
```

Preserve `fileId`, `driveId`, MIME type, URL, and timestamps exactly as returned. Treat IDs and URLs as sensitive operational metadata when the resource is private.

## Files and folders

Use sentence case or a structured human title for Workspace display names. Avoid trailing spaces, duplicate separators, misleading extensions, and names that expose confidential information. Keep machine slugs and display labels in separate fields.

## API lookup

Use the Drive API with a quoted, escaped query. A folder listing should identify the parent by ID rather than relying on a path string. Example shape:

```text
GET https://www.googleapis.com/drive/v3/files?q='{parent-id}' in parents and trashed = false&fields=files(id,name,mimeType,parents,webViewLink)
```

The exact query must be encoded by the client. Do not expose access tokens in logs or URI examples.
