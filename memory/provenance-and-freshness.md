# Provenance and freshness

**Provenance** means "where did this come from?" **Freshness** means "is it still true?" Every memory record must answer both.

## Every record shows

| Field | Plain meaning |
|---|---|
| `source.uri` and `repositoryPath` | The approved place it came from |
| `source.revision` | Which version of that place was read |
| `excerpt` or `summary` | A short bounded extract, never a whole file |
| `confidence` | `draft`, `reviewed`, or `approved` by a person |
| `freshness` | `current`, `stale`, `unknown`, or `source_missing` |
| `sensitivity` | `public`, `internal`, or `restricted` |
| `humanReview` | Has a person checked it? |

## Registering a source

A person approves each source before it can be searched. Use `source-registration.schema.json`. Write down the owner role, who approved, when, patterns to exclude (for example files that may hold secrets), and how many days between reviews.

Sources are never added automatically. Do not register a whole Drive or a whole repository "just in case". Register one folder for one purpose.

## Checking freshness

Compare the revision stored in the record with the source's revision today (its last-modified time or version). If they differ, mark the record `stale` and ask the source owner to review. Use `freshness-status.schema.json` for the result.

## Comparing versions

`compare_revisions` gives a short plain summary of what changed between two revisions. It does not copy the full text of either.

## Reading the results

If freshness is not `current`, the first sentence of any answer must say so. Never present stale memory as current fact.

## Where to keep records

Approved, non-restricted summaries can live in the repository or an approved Google Sheet. Restricted material stays in its approved system and is only referenced by ID. See `guardrails/data-retention-policy.md`.
