# No-coder maintenance guide

The `.agents` repository uses **`main` as the only permanent branch**. You do not need to manage branches yourself. When a change is requested, the system may create a temporary working branch, run automatic checks, open a pull request, merge the approved change into `main`, and remove the temporary branch.

A **pull request** is simply a review page for a proposed change. If it passes the automatic checks and is approved, merging it places the change into `main`. The pull request then closes automatically. The final source of truth is always the `main` branch URL:

`https://github.com/cpintl-org/.agents/tree/main`

Automatic checks review skill metadata, bundled resource paths, YAML/JSON where applicable, the free-resource matrix, likely credential patterns, unsafe paths, and whitespace. The checks run for pull requests, updates to `main`, manual requests, and a weekly health check. They do not publish external content, send messages, spend money, or delete repository data.

For ordinary maintenance, describe the desired outcome in plain English. Examples include “add a new skill for spreadsheet validation,” “update the quota reference,” or “clean up a merged branch.” Before any destructive action—such as deleting a repository, removing access, changing billing, or deleting a release—review the exact target and effect.

If an automatic check fails, the change stays outside `main` until it is corrected. The failure message and pull-request URL are the starting point for recovery; do not delete the repository or recreate it.
