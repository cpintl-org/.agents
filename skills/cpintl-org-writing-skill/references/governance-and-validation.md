# Governance and validation

## Review gates

Before creating or changing a resource, review: owner, provider, visibility, sensitivity, naming profile, lifecycle, permissions, endpoint exposure, backup approach, and rollback plan. Read-only inspection is the default. Ask for confirmation before destructive or externally visible operations.

## Validation layers

1. **Lexical validation:** permitted characters, length, case, separators, reserved names, and Unicode policy.
2. **Structural validation:** repository tree, parent-child relationship, schema shape, required fields, and endpoint grammar.
3. **Provider validation:** GitHub, Drive, API, or MCP-specific rules.
4. **Collision validation:** case-insensitive filesystem collisions, duplicate slugs, duplicate display names in the same parent, and conflicting routes.
5. **Security validation:** secrets, traversal, injection, privilege escalation, sensitive data, and public exposure.
6. **Operational validation:** ownership, backup, monitoring, retention, and migration path.

## Exceptions

Record exceptions rather than silently weakening the standard:

```yaml
exceptionId: EXC-{number}
object: "{provider}:{object-type}:{identifier}"
risk: low|medium|high
reason: "{why the provider or project requires this exception}"
compensatingControls:
  - "{control}"
owner: "{responsible-role}"
expiresAt: "{rfc3339-timestamp}"
status: proposed|approved|expired|rejected
```

## Migration

When renaming, create a mapping from old identity to new identity. Preserve provider IDs, update links and automation, retain redirects or aliases where supported, test case-insensitive filesystems, and communicate the cutover. Do not rename solely to make a display label look cleaner if it breaks stable API consumers.

## CI checks

A repository may run:

```bash
python scripts/validate_names.py --kind repository "$REPOSITORY_NAME"
git check-ref-format --branch "$BRANCH_NAME"
```

Also validate YAML/JSON syntax, scan for secrets, check path length, check duplicate case-insensitive names, and inspect endpoint templates for unencoded variables.

## Security boundaries

Never log or publish access tokens, private keys, cookies, service-account secrets, database URLs containing credentials, or personal data. Use placeholders in examples. Do not infer that an endpoint is authorized because it is syntactically valid. Preserve opaque IDs exactly but classify them as operational metadata when resources are private.
