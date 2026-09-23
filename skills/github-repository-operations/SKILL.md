---
name: github-repository-operations
description: Manage GitHub repositories, pull requests, branches, releases, settings, and Actions safely for no-code maintainers using the GitHub CLI or GitHub API. Use when a user wants repository setup, main-branch cleanup, pull-request handling, automation, or plain-language guidance about GitHub operations.
---

# GitHub repository operations

Use this skill as a no-coder adapter between a plain-language request and safe GitHub repository administration. Explain the outcome in simple terms, perform reversible checks first, and report the exact repository, branch, pull request, commit, and URL involved.

## Operating rules

1. Identify the verified `owner`, `repository`, `defaultBranch`, request type, intended scope, and whether the action changes code, access, billing, security, or published content. Preserve provider-issued IDs exactly.
2. Use the GitHub CLI (`gh`) when it is authenticated and available. Use the GitHub API only for settings or metadata not exposed by the CLI. If neither is available, provide a no-code checklist rather than inventing a result.
3. Treat `main` as the default release branch unless the repository explicitly documents another branch. Use temporary controlled branches such as `feat/{slug}` or `chore/{slug}` only when a pull request is required, then delete them after merge when policy permits.
4. Never expose tokens, private keys, OAuth refresh tokens, webhook secrets, or environment values. Never place credentials in issues, pull requests, Actions logs, artifacts, prompts, or repository files.
5. Make read-only inspection the default. Safe reversible actions include creating a branch, opening a pull request, adding documentation, enabling validation, and deleting a merged feature branch. Ask for confirmation before deleting repositories, data, collaborators, deploy keys, releases, or access controls.
6. Do not claim that a pull request is closed until its state is verified. A merged pull request is closed automatically; an abandoned pull request must be closed explicitly and its branch handled separately.
7. For automation, prefer deterministic GitHub Actions with pinned major versions or commit SHAs, least-privilege permissions, concurrency cancellation, clear failure messages, and no secret-dependent behavior in pull-request runs from forks.
8. After every write, verify the remote state and give the user a plain-language summary of what changed and what remains for them, if anything.

## No-coder workflow

### Inspect

Run or request the equivalent of:

```bash
gh repo view {owner}/{repository}
gh pr list --repo {owner}/{repository} --state open
gh api repos/{owner}/{repository}/branches --paginate
gh run list --repo {owner}/{repository}
```

Use the returned default branch and opaque identifiers. Do not derive IDs from display names.

### Handle a pull request

For a mergeable, reviewed pull request targeting the default branch, merge using the repository’s configured strategy, verify the merged commit, and delete only the merged feature branch. For a pull request that should not be merged, close it without deleting unrelated branches. Report both the pull-request URL and resulting commit URL.

### Keep only the main branch

First confirm that `main` is the default branch and that no required release, deployment, or recovery branch exists. Merge or close open pull requests one at a time. Delete only merged temporary branches; never delete `main`, a protected branch, or a branch with unreviewed work. Configure branch protection after required changes are complete so future edits use a simple pull-request flow.

### Configure automation

Add workflows under `.github/workflows/` only when they have a clear trigger and safe permissions. A baseline validation workflow should check Markdown links/paths, skill frontmatter, bundled scripts, YAML/JSON syntax, secret patterns, and `git diff --check`. Add concurrency cancellation and run it on pull requests and pushes to `main`. Never make a workflow silently publish, delete data, or spend money.

### Configure repository settings

Prefer settings that help a no-coder maintainer: `main` as the default branch, delete-head-branches after merge, pull-request merge queue or automatic update only when supported, issue forms or templates, security policy, and Actions permissions limited to read access unless a workflow needs more. Branch protection should require pull requests and passing checks only after the repository has a reliable validation workflow. Do not enable rules that make the maintainer unable to recover the repository.

## Output contract

Return a table with the repository locator, operation, before state, after state, verification URL, and any remaining human decision. Include a beginner explanation in one short paragraph. For code or configuration changes, list the files and validation commands. For a failed operation, state the exact provider error and a safe next step; never imply success.

## cpintl-org portability

Use lowercase ASCII kebab-case for new paths and branch slugs, `UPPER_SNAKE_CASE` for environment variables, and placeholders such as `{github-owner}`, `{repository}`, `{ref}`, `{branch}`, and `{pull-request-number}`. Keep `displayName`, `slug`, `providerId`, `canonicalLocator`, and `endpointTemplate` separate in structured records. Encode path/query components through the API client. Use repository URL forms only after verifying the owner and repository.

## References

Read `references/no-coder-github-guide.md` for plain-language explanations and `templates/repository-operation-record.md` for a reusable change record. Use the cpintl-org writing standard for naming, GitHub locators, API paths, and security review.
