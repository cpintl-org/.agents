# Workspace bridge

This Apps Script project is an optional, user-deployed bridge. It does not create a public sync endpoint until the owner configures Script Properties and deploys the web app.

## Required Script Properties

- `GITHUB_OWNER`: `cpintl-org`
- `GITHUB_REPOSITORY`: `.agents`
- `GITHUB_REF`: `main`
- `GITHUB_TOKEN`: fine-grained token with only repository contents read access, stored in Script Properties—not in Git
- `BRIDGE_SECRET`: random webhook secret stored in Script Properties
- `DRIVE_ROOT_FOLDER_ID`: verified Drive folder ID
- `DRY_RUN`: `true` for first deployment
- `ALLOWED_PATHS`: comma-separated paths such as `brains,skills,guardrails,templates`

## Deployment

1. Create or open an Apps Script project owned by the responsible Workspace account.
2. Copy `Code.gs` and `appsscript.json`, set properties through the Apps Script editor, and keep `DRY_RUN=true`.
3. Deploy as a Web app only after reviewing access and data sensitivity. The endpoint is called by the GitHub Actions workflow with the bridge secret in the JSON payload (`bridge_secret`).
4. Send a synthetic `push` event and verify the returned `auditId` and Apps Script execution log before allowing writes.
5. Change `DRY_RUN` only after human approval and a recovery test.

This bridge is not a guaranteed real-time service. If properties, token, mapping, or permissions are unavailable, it returns an error or manual-review status without changing Drive.

## Nested folders and duplicate filenames

The bridge recreates each repository directory below `DRIVE_ROOT_FOLDER_ID`. For example, `skills/workspace-drive-search/SKILL.md` is placed under:

```text
{Drive root}/skills/workspace-drive-search/SKILL.md
```

The document title is only the final filename. The synchronization identity is the full tuple `{GITHUB_OWNER, GITHUB_REPOSITORY, GITHUB_REF, repositoryPath}`, stored as a non-sensitive description marker on the Google Doc. This prevents `README.md` in `brains/` from being confused with `README.md` in `skills/`, and makes repeated pushes update the existing document rather than create another copy.

Folder creation is idempotent: an existing folder with the same name at the same parent is reused. Path segments are checked for traversal and control characters. Keep the repository path stable; moving a file creates a new destination identity, so review and archive the old Drive document rather than silently deleting it.

If the destination already contains an unmarked document with the same final filename, the bridge stops with a duplicate-identity error instead of guessing. Resolve that case manually by moving the unrelated document, confirming the correct repository file, and then running another dry-run.

The bridge currently treats synchronized files as text documents. Test binary files separately and keep `DRY_RUN=true` until the resulting hierarchy and collision behavior have been reviewed by the owner.
