---
name: memory-search
description: Find and quote evidence from approved, registered sources with source, revision, and freshness shown on every result, using only read-only operations. Use when an agent needs to recall a decision, check whether a source is still current, or compare two versions of an approved document without copying restricted content.
---

# Memory search (read-only)

Use this skill when an answer must be traced back to an approved source. Every result carries where it came from, which revision it was, how fresh it is, and how sensitive it is. The skill only reads. It never indexes new sources by itself, never deletes, and never runs free-form queries.

## Allowed operations

| Operation | What it does | Writes anything? |
|---|---|---|
| `list_sources` | Lists approved, registered sources | No |
| `source_status` | Shows freshness of one source | No |
| `search_memory` | Searches approved sources for a short phrase, at most 20 results | No |
| `get_evidence` | Returns a short bounded excerpt for one memory record | No |
| `compare_revisions` | Summarizes what changed between two revisions of one source | No |
| `refresh_source` | Asks a person to re-check a source; dry-run only until approved | Only after human approval |

Any other operation is refused.

## Workflow

1. Confirm the source is registered (a person approved it, with owner, sensitivity, and review date). If not, stop and create a manual task to register it.
2. Build a request like `templates/memory-search-request.json`. Keep the query short and plain words.
3. Check the request with the checker below.
4. Return only bounded excerpts (short quotes with source and revision), never whole files.
5. Show freshness. If a result is `stale`, `unknown`, or `source_missing`, say so in the first sentence and suggest `refresh_source`.
6. For `restricted` sources, do not return excerpts. Return a manual-review task naming the source owner.

## Not allowed

- Arbitrary database or graph queries, or free-form file paths.
- Automatic background indexing of all Drive or repository files.
- Cross-project linking, memory deletion, or unbounded semantic search.
- Storing secrets, personal data, or restricted case details as memory.

## Check

Where to run: a terminal opened in the repository root folder.

```bash
python skills/memory-search/scripts/validate_memory_request.py skills/memory-search/templates/memory-search-request.json
```

Read `references/memory-contract.md` for the request and result shapes and the freshness rules. The checker only checks structure; it does not grant access.
