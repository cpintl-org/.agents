# GitHub naming and repository standard

## Repository names

Use `{organization}-{domain}-{component}` only when the domain and component are known. Otherwise use `{organization}-{project}` or a user-provided name. Apply lowercase kebab-case, keep names concise, avoid secrets and internal classifications, and do not encode a mutable team or person into the repository name.

Examples below are synthetic:

```text
cpintl-org-example-service
cpintl-org-reference-web
cpintl-org-shared-config
```

GitHub provider constraints remain authoritative. This standard is stricter for portability; validate names against the live provider before creation.

## Repository tree

```text
README.md
LICENSE
SECURITY.md
CONTRIBUTING.md
CHANGELOG.md                 # only when the project uses one
.github/
  workflows/
  ISSUE_TEMPLATE/
  PULL_REQUEST_TEMPLATE.md
docs/
  architecture/
  operations/
  reference/
src/                         # when source code exists
tests/                       # when tests exist
config/                      # non-secret configuration only
scripts/                     # deterministic utilities
```

Do not create empty directories merely to appear complete. Keep secrets, credentials, private keys, dumps, and confidential exports out of the repository. Use `.gitignore` and secret scanning where available.

## Git refs

Use one of the controlled namespaces `feat/`, `fix/`, `docs/`, `chore/`, `refactor/`, `test/`, `build/`, or `release/`, followed by a lowercase kebab description. Use `main` as the default branch unless the project has a documented reason otherwise. Use `vMAJOR.MINOR.PATCH` tags for releases.

Run:

```bash
git check-ref-format --branch 'feat/resource-index'
```

Do not use branch names that differ only by case. Do not put provider IDs, tokens, or personal data in branch names.

## Canonical locators

Use typed records instead of an ambiguous string:

```json
{
  "owner": "{github-owner}",
  "repository": "{repository}",
  "ref": "main",
  "path": "docs/reference/index.md",
  "blobSha": "{opaque-sha}",
  "canonicalLocator": "{github-owner}/{repository}@main:docs/reference/index.md"
}
```

The GitHub REST pattern for repository content is:

```text
https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={ref}
```

Encode path and query values according to the API client; do not hand-build URLs from unchecked input.
