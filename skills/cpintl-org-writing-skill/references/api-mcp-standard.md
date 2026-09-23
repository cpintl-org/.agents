# API, OpenAPI, and MCP standard

## REST and Google-style APIs

Use plural lowercase kebab-case resource paths:

```text
/v1/{resources}
/v1/{resources}/{resource-id}
/v1/{resources}/{resource-id}:verb
```

Use nouns in paths and verbs in actions. Use lowerCamelCase JSON fields, stable opaque IDs, and explicit pagination. For Google-style resource names, use:

```text
projects/{project}/locations/{location}/{resources}/{resource}
```

Do not put secrets, personal data, or mutable display labels in URLs.

## OpenAPI

Use `operationId` values in `verbNoun` form, `PascalCase` schema names, lowerCamelCase properties, and plural resource tags. Keep path parameters aligned with the path and define response/error schemas. See `templates/openapi-naming-rules.yaml`.

## MCP objects

Use a stable server identity, descriptive tool names, explicit JSON schemas, and predictable resource URIs. A tool name should describe an action, for example `workspace.find_resource` or `repository.read_file`. Tool arguments must be typed and should preserve provider IDs separately from display paths.

## GitHub-to-Workspace bridge URI

Use a custom resource URI only when the MCP server documents the scheme:

```text
bridge://github-workspace/repos/{owner}/{repo}/tree/{ref}/{path}?drive_folder_id={encoded-id}&drive_path={encoded-path}
```

A synthetic concrete example is:

```text
bridge://github-workspace/repos/cpintl-org/example-service/tree/main/docs/reference?drive_folder_id=%7Bdrive-folder-id%7D&drive_path=Workspace%2FReference
```

Encode each variable path segment and query value independently. Keep the following tool input fields separate:

```json
{
  "repositoryOwner": "{github-owner}",
  "repository": "{repository}",
  "ref": "main",
  "repositoryPath": "docs/reference",
  "driveFolderId": "{drive-folder-id}",
  "drivePath": "Workspace/Reference",
  "mode": "read-only"
}
```

The MCP transport endpoint and a resource URI are different things. A transport endpoint might be `https://{mcp-host}/mcp`; the resource URI identifies a resource exposed through that server. Do not present a resource URI as a server transport URL.

## Security

Validate tool arguments, authorize every operation, default bridge operations to read-only, redact provider tokens, and log identifiers only when operationally necessary. A syntactically valid URI does not prove that the caller has permission.
