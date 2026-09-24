# Memory contract

## Records, sources, and freshness

A **memory record** is a short summary plus where it came from (`source.uri`, optional `repositoryPath`, and `revision`), a confidence (`draft`, `reviewed`, `approved`), a freshness, a sensitivity, and a human-review state. The schema is `memory-record.schema.json` in the repository `memory` folder.

A **source registration** says a person approved a source: `sourceId`, type, locator, sensitivity, owner role, who approved, when, exclusion patterns, and how often to review.

**Freshness**

| Value | Meaning |
|---|---|
| `current` | The stored revision matches the source today |
| `stale` | The source changed since the record was made |
| `unknown` | It has not been checked yet |
| `source_missing` | The source could not be found |

## Request shape

```json
{
  "operation": "search_memory",
  "sourceIds": ["{registered-source-id}"],
  "query": "{short plain words}",
  "limit": 5,
  "sensitivityCeiling": "internal",
  "requesterRole": "{role}",
  "dryRun": true
}
```

## Result shape

Results follow `memory-search-result.schema.json`. Each has a `memoryId`, a bounded `excerpt` (600 characters at most), the `source` with `revision`, and `freshness`.

## Rules

- Excerpts are bounded. Do not paste whole documents.
- Provider-issued IDs stay exactly as returned and are treated as sensitive operational data.
- Logs keep only minimal audit fields (audit id, operation, status, role, time), never prompts or excerpts.
- A person approves every new source and every `refresh_source` that changes anything.
- If the bridge or a source is unavailable, return `manual_review` with the exact source and search words; never fabricate a result.
