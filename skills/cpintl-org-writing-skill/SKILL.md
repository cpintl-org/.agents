---
name: cpintl-org-writing-skill
description: Cross-platform naming, repository structure, Google Workspace identity, API endpoint construction, MCP URI mapping, and style-consistent technical writing for the cpintl-org GitHub organization. Use for designing, reviewing, validating, migrating, documenting, or generating repository names, paths, files, folders, APIs, environment variables, MCP servers/tools/resources/prompts, and structured technical content. Apply to any agent or automation workflow; do not assume a specific domain, program, product, or resource type unless the user supplies it.
---

# cpintl-org writing and integration standard

Use this skill to produce consistent, portable, auditable names and technical content across GitHub, local filesystems, Google Workspace/Drive, APIs, OpenAPI, and MCP. The organization namespace is configurable; the default examples use `cpintl-org` only because the user requested this scope. Keep all domain, project, program, and resource nouns as placeholders unless the user explicitly provides them.

## Non-negotiable principles

1. Separate `display_name`, `slug`, `provider_id`, `canonical_name`, `locator`, and `endpoint_template`.
2. Prefer lowercase ASCII kebab-case for new repositories, directories, portable filenames, URL IDs, and public slugs.
3. Use `UPPER_SNAKE_CASE` for environment variables, `lowerCamelCase` for new JSON fields, `UpperCamelCase` for API types, and `VerbNoun` for Google-style methods.
4. Preserve opaque GitHub, Google Drive, Workspace, package, node, and hash identifiers exactly as returned. Never regenerate them from a display name.
5. Encode variable URI path segments and query values by component. Never concatenate unchecked input into endpoints.
6. Reject control characters, path traversal, Windows reserved names, trailing spaces or periods, case-only collisions, ambiguous Unicode, and embedded secrets unless a provider requires a documented exception.
7. Treat provider rules as authoritative and this standard as a stricter portability layer.
8. Do not invent organization members, repositories, projects, domains, Drive IDs, tokens, hashes, endpoints, or business meanings. Use placeholders such as `{organization}`, `{repository}`, `{resource-id}`, and `{mcp-server-url}`.
9. Do not infer a domain-specific noun from a filename, repository name, or URL. Ask for clarification or retain a neutral placeholder.
10. Write for a general agent: explain assumptions, cite sources when research is performed, and produce reproducible artifacts.

## Workflow

### 1. Classify the request

Identify the provider, object type, scope, lifecycle, display label, machine slug, provider-issued ID, parent relationship, intended endpoint, audience, sensitivity, and output format. If any field is unknown, preserve it as a placeholder rather than guessing.

### 2. Load only the relevant reference

- Read [references/portable-standard.md](references/portable-standard.md) for universal rules and grammars.
- Read [references/github-standard.md](references/github-standard.md) for repositories, refs, trees, branches, tags, and GitHub APIs.
- Read [references/workspace-standard.md](references/workspace-standard.md) for Drive and Workspace objects.
- Read [references/api-mcp-standard.md](references/api-mcp-standard.md) for REST, OpenAPI, MCP, and bridge URIs.
- Read [references/writing-style-guidance.md](references/writing-style-guidance.md) for technical-writing structure and Google-style source guidance.
- Read [references/governance-and-validation.md](references/governance-and-validation.md) for CI, migration, exceptions, security, and review.
- Read [references/agent-skill-resources.md](references/agent-skill-resources.md) when selecting or documenting reusable agent skills.

### 3. Select the profile

| Target | Default profile |
|---|---|
| Repository, directory, portable file | lowercase kebab-case |
| Git branch | controlled namespace plus lowercase kebab-case |
| SemVer tag | `vMAJOR.MINOR.PATCH` |
| Environment variable | `UPPER_SNAKE_CASE` |
| JSON field | `lowerCamelCase` unless provider-defined |
| Google API type/method | `UpperCamelCase` / `VerbNoun` |
| MCP tool | `verb_noun` or provider-supported dotted form |
| MCP server | reverse-DNS-like namespace plus lowercase slug, when required |
| Workspace display label | human-readable structured title |
| Technical document title | clear noun phrase, sentence case |

### 4. Validate before producing or changing names

Use the bundled validator:

```bash
python scripts/validate_names.py --kind repository cpintl-org-example-service
python scripts/validate_names.py --kind branch feat/resource-index
python scripts/validate_names.py --kind mcp-tool workspace.find_resource
python scripts/validate_names.py --kind path docs/reference/index.md
```

For Git refs, also run `git check-ref-format --branch`. For endpoint work, validate component encoding and decode/encode round trips. Validation does not grant authorization and does not prove that a resource exists.

### 5. Construct endpoints and MCP URIs

Use the bundled bridge URI generator:

```bash
python scripts/generate_bridge_uri.py \
  --owner '{github-owner}' \
  --repo '{repository}' \
  --ref main \
  --repo-path docs/reference \
  --drive-folder-id '{drive-folder-id}' \
  --drive-path 'Workspace/Reference'
```

Keep the repository, ref, repository path, Drive folder ID, and Drive display path as separate typed fields even when represented in one URI.

### 6. Produce the requested artifact

Use templates from `templates/`:

- `naming-policy.yaml`: configurable organization naming policy.
- `repository-layout.yaml`: neutral repository tree declaration.
- `mcp-bridge-mapping.yaml`: GitHub-to-Workspace mapping.
- `workspace-resource-record.json`: provider identity record.
- `openapi-naming-rules.yaml`: API naming rules.
- `technical-document-outline.md`: neutral writing outline.

When writing, distinguish facts, user-provided requirements, assumptions, recommendations, and unresolved questions. Never turn a placeholder into a fictional fact.

## Neutrality rules

Use `{domain}`, `{project}`, `{component}`, `{resource}`, `{period}`, and `{state}` as placeholders. Do not insert sector terms, program names, grant names, product names, patient terms, or other business meanings unless explicitly supplied by the user. If a user requests examples, label them clearly as synthetic examples.

Preferred neutral forms:

```text
{organization}-{domain}-{component}
{organization}/{domain}/{resource}
io.github.{organization}/{server-slug}
bridge://github-workspace/repos/{owner}/{repo}/tree/{ref}/{path}
```

## Safety

Names can become shell arguments, filesystem paths, URLs, SQL identifiers, API selectors, package coordinates, or authorization inputs. Reject traversal and injection risks. Do not expose credentials in names, examples, logs, templates, or generated documentation. Do not modify or delete external resources merely to validate names. For live operations, confirm authorization and preserve provider-issued IDs.

## Completion checklist

Before returning results, confirm that the output has no unexplained organization-specific nouns, no fabricated IDs or URLs, no secrets, no unused examples, no invalid YAML/JSON, and no script that has not been tested. Include a short assumptions section whenever the user did not specify the domain or resource model.
