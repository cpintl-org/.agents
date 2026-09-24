# Configure the Google Apps Script Workspace Bridge

The bridge connects:

```text
GitHub push to main
        ↓
GitHub Actions workspace-sync.yml
        ↓
Apps Script Web App
        ↓
Approved Google Drive folder
```

The bridge is **disabled by default** until you configure both Apps Script and GitHub.

Relevant repository files:

- [`workspace-bridge/README.md`](https://github.com/cpintl-org/.agents/blob/main/workspace-bridge/README.md)
- [`workspace-bridge/Code.gs`](https://github.com/cpintl-org/.agents/blob/main/workspace-bridge/Code.gs)
- [`workspace-bridge/appsscript.json`](https://github.com/cpintl-org/.agents/blob/main/workspace-bridge/appsscript.json)
- [`workspace-bridge/clasp.json`](https://github.com/cpintl-org/.agents/blob/main/workspace-bridge/clasp.json)
- [`config/mcp-bridge-mapping.yaml`](https://github.com/cpintl-org/.agents/blob/main/config/mcp-bridge-mapping.yaml)
- [`workspace-sync.yml`](https://github.com/cpintl-org/.agents/blob/main/.github/workflows/workspace-sync.yml)

---

## Part 1: Create the Apps Script project

1. Open [https://script.google.com](https://script.google.com).
2. Select **New project**.
3. Rename it to something like:

```text
cpintl-org-agent-hub-workspace-bridge
```

4. Open the repository file [`workspace-bridge/Code.gs`](https://github.com/cpintl-org/.agents/blob/main/workspace-bridge/Code.gs).
5. Copy its full content.
6. Paste it into the Apps Script editor, replacing the default code.
7. Rename the Apps Script file to:

```text
Code.gs
```

Do not paste any GitHub token, Drive ID, or bridge secret into `Code.gs`.

---

## Part 2: Configure the Apps Script manifest

In the Apps Script editor:

1. Click **Project Settings**.
2. Enable **Show `appsscript.json` manifest file in editor**.
3. Open `appsscript.json`.
4. Replace its content with:

```json
{
  "timeZone": "Asia/Dhaka",
  "exceptionLogging": "STACKDRIVER",
  "runtimeVersion": "V8",
  "dependencies": {},
  "oauthScopes": [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/script.external_request"
  ],
  "webapp": {
    "executeAs": "USER_DEPLOYING",
    "access": "ANYONE_ANONYMOUS"
  }
}
```

The `ANYONE_ANONYMOUS` setting allows GitHub Actions to call the web app without interactive Google login. The bridge still rejects requests without the configured secret.

If your organization prohibits anonymous web apps, do not deploy this configuration. You would need an authenticated relay or another approved integration pattern.

---

## Part 3: Create the Google Drive destination folder

1. Open Google Drive.
2. Create a dedicated folder, for example:

```text
cpintl-org Agent Hub Mirror
```

3. Open that folder.
4. Copy the folder ID from the URL.

For example:

```text
https://drive.google.com/drive/folders/1AbCdEfGhIjKlMnOp
```

The Drive folder ID is:

```text
1AbCdEfGhIjKlMnOp
```

The ID is an opaque provider identifier. Do not recreate or modify it.

For the first test, use a non-sensitive test folder. Do not use a folder containing beneficiary, health, safeguarding, financial, or confidential organizational records.

---

## Part 4: Create a GitHub fine-grained token

The Apps Script bridge needs to read files from the GitHub repository.

1. Open [GitHub token settings](https://github.com/settings/personal-access-tokens).
2. Select **Fine-grained tokens**.
3. Select **Generate new token**.
4. Configure:

| Setting | Recommended value |
|---|---|
| Token name | `cpintl-org-agent-hub-bridge-read` |
| Expiration | A short period such as 30 or 90 days |
| Resource owner | `cpintl-org` |
| Repository access | Only `cpintl-org/.agents` |
| Repository permission | **Contents: Read-only** |

5. Generate the token.
6. Copy it immediately.

Do not commit this token to GitHub. Do not put it in `Code.gs`, `config/`, Google Sheets, or a public document.

---

## Part 5: Generate a bridge secret

The bridge secret is separate from the GitHub token.

Use a password manager or a secure random generator. If you have a terminal, this produces a suitable value:

```bash
openssl rand -hex 32
```

It will look similar to:

```text
9b2f...random-value...72ac
```

Do not use a simple word or a short phrase.

You will use the same secret in:

- Apps Script property: `BRIDGE_SECRET`
- GitHub repository secret: `WORKSPACE_BRIDGE_WEBHOOK_SECRET`

---

## Part 6: Add Apps Script project properties

In the Apps Script editor:

1. Click **Project Settings**.
2. Find **Script Properties**.
3. Click **Add script property**.
4. Add the following properties.

| Property | Value |
|---|---|
| `GITHUB_OWNER` | `cpintl-org` |
| `GITHUB_REPOSITORY` | `.agents` |
| `GITHUB_REF` | `main` |
| `GITHUB_TOKEN` | Your fine-grained GitHub token |
| `BRIDGE_SECRET` | Your generated random secret |
| `DRIVE_ROOT_FOLDER_ID` | Your verified Google Drive folder ID |
| `DRY_RUN` | `true` |
| `ALLOWED_PATHS` | `brains,skills,guardrails,templates,memory` |

The complete property list should look like this:

```text
GITHUB_OWNER=cpintl-org
GITHUB_REPOSITORY=.agents
GITHUB_REF=main
GITHUB_TOKEN={your-fine-grained-read-only-token}
BRIDGE_SECRET={your-random-bridge-secret}
DRIVE_ROOT_FOLDER_ID={your-verified-drive-folder-id}
DRY_RUN=true
ALLOWED_PATHS=brains,skills,guardrails,templates,memory
```

Do not place actual values in the repository’s configuration files.

---

## Part 7: Authorize the Apps Script project

In the Apps Script editor:

1. Select the `healthCheck` function from the function menu.
2. Click **Run**.
3. Review the authorization request.
4. Select the Google account that owns or manages the test Drive folder.
5. Approve the requested permissions.

The bridge uses:

- Google Drive access.
- Google Docs access.
- External request access for GitHub API calls.

Review the scopes carefully. Do not approve them using an account that should not have access to the destination folder.

---

## Part 8: Perform a dry-run test before deployment

With `DRY_RUN=true`, the bridge will verify the request and report how many files would be processed without modifying Drive.

In Apps Script:

1. Select **Deploy**.
2. Select **New deployment**.
3. For deployment type, select **Web app**.
4. Configure:

| Setting | Value |
|---|---|
| Execute as | Me / the deploying account |
| Who has access | Anyone |
| Description | `cpintl-org agent hub bridge dry run` |

5. Click **Deploy**.
6. Copy the URL ending in:

```text
/exec
```

Use the `/exec` URL, not the `/dev` URL.

It will look similar to:

```text
https://script.google.com/macros/s/{deployment-id}/exec
```

Do not publish this URL in a public document if your security policy treats it as confidential. The URL alone is not sufficient to authorize a bridge request, but it should still be handled carefully.

---

## Part 9: Test the Apps Script endpoint

Open the `/exec` URL in a browser.

You should receive a response similar to:

```json
{
  "status": "ok",
  "service": "workspace-bridge",
  "dryRun": true,
  "statusCode": 200
}
```

This only tests that the web app is reachable. It does not test GitHub authentication or Drive synchronization.

---

## Part 10: Add GitHub repository secrets

Open the repository’s Actions secrets page:

[https://github.com/cpintl-org/.agents/settings/secrets/actions](https://github.com/cpintl-org/.agents/settings/secrets/actions)

Then:

1. Select **New repository secret**.
2. Add:

| Secret name | Secret value |
|---|---|
| `WORKSPACE_BRIDGE_WEBHOOK_URL` | Your Apps Script `/exec` URL |
| `WORKSPACE_BRIDGE_WEBHOOK_SECRET` | The same value as Apps Script `BRIDGE_SECRET` |

The final GitHub secret names must be exactly:

```text
WORKSPACE_BRIDGE_WEBHOOK_URL
WORKSPACE_BRIDGE_WEBHOOK_SECRET
```

Do not create a GitHub secret named `GITHUB_TOKEN` for this bridge. The GitHub token is currently stored in Apps Script Script Properties because the Apps Script code uses it to retrieve repository contents.

---

## Part 11: Run the GitHub dry-run

The workflow runs when changes are pushed to `main` under:

```text
brains/
skills/
guardrails/
templates/
memory/
config/mcp-bridge-mapping.yaml
```

You can test it without changing an important document:

1. Make a harmless documentation change in a test branch or through the authorized maintenance process.
2. Merge or publish it to `main`.
3. Open the **Actions** tab.
4. Select **Workspace bridge sync**.
5. Open the run associated with your commit.

With `DRY_RUN=true`, the Apps Script should return a successful dry-run result and should not modify Drive files.

The workflow should also pass:

- [Validate agent skills](https://github.com/cpintl-org/.agents/actions/workflows/skill-validation.yml)
- [Workspace bridge sync](https://github.com/cpintl-org/.agents/actions/workflows/workspace-sync.yml)

---

## Part 12: Verify the dry-run result

In Apps Script:

1. Open **Executions**.
2. Select the latest `doPost` execution.
3. Confirm that:
   - The request was accepted.
   - The ref was `main`.
   - The path was allowed.
   - The result was dry-run.
   - No Drive document was created or overwritten.

If the request is denied, check:

| Error | Likely cause |
|---|---|
| `invalid_secret` | GitHub secret and Apps Script `BRIDGE_SECRET` differ |
| `unsupported_ref` | `GITHUB_REF` is not `main` |
| `unsupported_event` | The workflow payload is not a push-style payload |
| `missing required bridge properties` | Token or Drive folder ID is missing |
| `github_content_fetch_failed` | Token scope, owner, repository, or path is incorrect |
| `403` from GitHub | Fine-grained token lacks read access to `.agents` |

---

## Part 13: Enable write mode only after review

Keep this setting:

```text
DRY_RUN=true
```

until all of the following have been confirmed:

- The destination Drive folder is correct.
- The GitHub token is limited to the `.agents` repository.
- The bridge secret works.
- The test payload is accepted.
- The bridge reads only approved paths.
- The test account has the intended Drive permissions.
- A recovery or deletion procedure is documented.
- No restricted or beneficiary data is included in the test.

Only then may you change the Apps Script property to:

```text
DRY_RUN=false
```

The current bridge writes the content of changed GitHub files into Google Docs. It is a basic first implementation, not a full bidirectional synchronization system. GitHub remains the canonical source. Do not treat Google Drive edits as authoritative unless a later approved workflow explicitly implements reverse synchronization.

## Hierarchy and synchronization behavior

The bridge creates nested folders idempotently for changed allowed files received in push events. Keep in mind the following operational boundaries:

1. **Changed files only**: Nested folders and Google Docs are created only for files present in a received push commit and matched by `ALLOWED_PATHS`.
2. **No automatic backfill**: Unchanged repository files are not backfilled into Drive automatically on new deployments.
3. **No automatic deletion**: Deletions in GitHub are not propagated to Drive, ensuring no accidental document destruction.
4. **Moves create new documents**: Renaming or moving a repository file creates a new document at the destination path and leaves the original Drive document untouched for manual review and archival.
5. **Text documents only**: Synchronized files are rendered as Google Docs text documents; binary formats are not approved for production synchronization.

---

The bridge supports nested folders and duplicate-safe synchronization:

## What changed

Published in commit [`12bc185`](https://github.com/cpintl-org/.agents/commit/12bc185242c5aafd1dea78f20c6d1bcc02372876).

Updated files:

- [`workspace-bridge/Code.gs`](https://github.com/cpintl-org/.agents/blob/main/workspace-bridge/Code.gs)
- [`workspace-bridge/README.md`](https://github.com/cpintl-org/.agents/blob/main/workspace-bridge/README.md)

The validation workflow passed:

- [Successful validation run](https://github.com/cpintl-org/.agents/actions/runs/35903112940)

## How nested folders are handled

A repository path such as:

```text
skills/workspace-drive-search/SKILL.md
```

is now recreated under the configured Drive root as:

```text
{Drive root}/skills/workspace-drive-search/SKILL.md
```

The bridge:

1. Splits the GitHub path into folder segments and the final filename.
2. Creates each missing folder under the correct parent.
3. Reuses an existing folder when the same folder already exists.
4. Rejects unsafe folder segments such as `..`, `.`, or control characters.
5. Reuses the existing folder structure on later synchronizations.

Folder creation is therefore **idempotent**: repeated syncs do not create duplicate folders.

## How duplicate filenames are avoided

The final filename is not used as the complete identity.

For example, these two files are treated as different documents:

```text
brains/README.md
skills/README.md
```

They are placed in different Drive folders, so their names do not collide.

Each synchronized Google Doc also receives a description marker based on:

```text
{GITHUB_OWNER}/{GITHUB_REPOSITORY}/{GITHUB_REF}/{repositoryPath}
```

For example:

```text
cpintl-org/.agents/main/skills/workspace-drive-search/SKILL.md
```

On a later sync, the bridge:

1. Searches only inside the correct destination folder.
2. Looks for the matching filename.
3. Checks the full-path identity marker.
4. Updates the matching document instead of creating a new one.

## What happens with old unmarked files

If a same-named Drive document already exists but has no bridge identity marker, the bridge **does not guess**.

Instead, it stops with:

```text
duplicate_unidentified_filename
```

This prevents accidental overwriting or creation of another duplicate. Resolve it manually by moving or renaming the unrelated file, then rerun the sync in dry-run mode.

## Recommended folder layout

Use a dedicated Drive root folder:

```text
cpintl-org Agent Hub Mirror/
├── brains/
│   ├── README.md
│   ├── research-agent.md
│   └── doc-writer-agent.md
├── skills/
│   ├── README.md
│   ├── cpintl-org-writing-skill/
│   ├── google-workspace-free-serverless/
│   └── workspace-drive-search/
├── guardrails/
├── templates/
└── memory/
```

Keep:

```text
DRY_RUN=true
```

until you have confirmed the hierarchy and resolved any legacy duplicate filenames.

## Important behavior when files move

A file move changes its repository path and therefore its identity.

For example:

```text
templates/google-docs-outline.md
```

moved to:

```text
templates/document/google-docs-outline.md
```

is treated as a new destination identity. The bridge does not automatically delete the old Drive document. Review and archive the old document manually to avoid destructive behavior.

GitHub remains the canonical source. Drive is a synchronized copy, not the system of record.
