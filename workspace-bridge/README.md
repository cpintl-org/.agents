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
3. Deploy as a Web app only after reviewing access and data sensitivity. The endpoint should be called by the GitHub workflow with the secret header.
4. Send a synthetic `push` event and verify the audit row/log before allowing writes.
5. Change `DRY_RUN` only after human approval and a recovery test.

This bridge is not a guaranteed real-time service. If properties, token, mapping, or permissions are unavailable, it returns an error or manual-review status without changing Drive.
