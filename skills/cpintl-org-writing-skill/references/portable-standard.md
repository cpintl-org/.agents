# Portable naming and syntax standard

## Scope

Apply these rules to new names unless a provider requires a documented exception. The standard is intentionally conservative so names survive Git, Windows, macOS, Linux, shells, URLs, APIs, JSON, Google Workspace, and MCP clients.

## Identity layers

| Field | Meaning | Example |
|---|---|---|
| `displayName` | Human-facing label | `Reference Workspace` |
| `slug` | Local machine-friendly key | `reference-workspace` |
| `providerId` | Opaque ID assigned by a platform | `{drive-folder-id}` |
| `canonicalName` | Provider-defined resource name | `projects/{project}/locations/{location}/resources/{resource}` |
| `locator` | Human/API lookup coordinate | `{owner}/{repository}@{ref}:{path}` |
| `endpointTemplate` | Documented route pattern | `https://api.example.test/resources/{resourceId}` |

Never substitute one layer for another. A display name can change; an opaque provider ID should not be derived from it.

## Default grammars

```text
organization       := [a-z][a-z0-9-]{1,62}
repository         := [a-z0-9](?:[a-z0-9-]{0,98}[a-z0-9])?
slug               := [a-z][a-z0-9-]{0,62}
portable-segment   := [a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?
branch             := (feat|fix|docs|chore|refactor|test|build|release)/[a-z0-9][a-z0-9-]{0,62}
semver-tag         := v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?
environment        := [A-Z][A-Z0-9]*(?:_[A-Z0-9]+)*
mcp-tool          := [A-Za-z][A-Za-z0-9_.-]{0,127}
```

Prefer lowercase ASCII and hyphens. Avoid leading or trailing hyphens, repeated separators, spaces, tabs, control characters, backslashes, `..`, shell metacharacters, and ambiguous Unicode. Preserve case where the provider already owns the identifier.

## Filesystem rules

Use lowercase kebab-case for directories and portable files. Use conventional all-caps names only when a tool expects them, such as `README.md`, `LICENSE`, and `SECURITY.md`. Reject Windows reserved basenames such as `CON`, `PRN`, `AUX`, `NUL`, and `COM1` through `COM9`, including extension variants. Reject trailing periods and spaces. Prevent case-only collisions.

## Writing rules

Use sentence-case headings, descriptive filenames, short paragraphs, and tables where comparison matters. State assumptions explicitly. Separate normative rules using **MUST**, **MUST NOT**, **SHOULD**, and **MAY**. Mark synthetic examples as synthetic. Cite external facts with reference-style links and include a References section.
