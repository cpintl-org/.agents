---
doc: cpintl-org-standards-freshness-register
description: Version/status baseline for the open standards behind uri-naming-standard.md (URI, HTTP, TLS, JSON family, and the MCP/A2A/AGENTS.md agent-protocol layer). Re-check before relying on a version claim in output.
last_verified: 2026-09-27
next_review_due: 2026-12-27
review_cadence_days: 90
---

# Standards freshness register

Scope note: this register covers only the naming-decision pillars in
`uri-naming-standard.md` — general identification, interaction, representation, and
agent-protocol standards. For the CPI-BGD clinical/dev-stack baseline (FHIR, DHIS2, LOINC,
Node.js, PostgreSQL, etc.), see `verified-resource-index.md` §27–28 in this repository, which
already runs its own review cycle.

**Rule for every row:** `agentic protocols` (MCP/A2A/AGENTS.md/AAIF) move fast and get a
90-day cycle. `foundational web standards` (URI/HTTP/TLS/JSON) rarely change and get a
365-day cycle — they're listed here for completeness, not because churn is expected.

## Foundational web standards — 365-day cycle

| Standard | Current reference | Status as of `last_verified` | Official source |
|---|---|---|---|
| URI syntax | RFC 3986 (2005) | Stable; no successor in progress | https://www.rfc-editor.org/rfc/rfc3986 |
| DNS | RFC 1034/1035 + many updates | Stable core, incrementally extended | https://www.iana.org/domains/root/servers |
| HTTP/2 | RFC 9113 | Current | https://www.rfc-editor.org/rfc/rfc9113 |
| HTTP/3 | RFC 9114 | Current | https://www.rfc-editor.org/rfc/rfc9114 |
| TLS | TLS 1.3, RFC 8446 | Current | https://www.rfc-editor.org/rfc/rfc8446 |
| HTML | HTML Living Standard (WHATWG) | Continuously updated, no version number | https://html.spec.whatwg.org/ |
| JSON | RFC 8259 | Stable | https://www.rfc-editor.org/rfc/rfc8259 |
| JSON-LD | 1.1, W3C Recommendation | Current | https://www.w3.org/TR/json-ld11/ |
| JSON-RPC | 2.0 | Stable | https://www.jsonrpc.org/specification |
| XML | 1.0 (5th ed.) | Stable | https://www.w3.org/TR/xml/ |
| Protocol Buffers | Editions 2023+ | Current | https://protobuf.dev/editions/overview/ |
| OpenAPI Specification | 3.x line | Current | https://spec.openapis.org/ |

## Agentic AI protocol layer — 90-day cycle

| Project | Governance | Status as of `last_verified` | Official source |
|---|---|---|---|
| Agentic AI Foundation (AAIF) | Linux Foundation | Formed 2025-12-09; founding members include Anthropic, AWS, Block, Bloomberg, Cloudflare, Google, Microsoft, OpenAI | https://aaif.io/ |
| Model Context Protocol (MCP) | AAIF (donated by Anthropic) | Widely adopted (Claude, Copilot, Gemini, VS Code, ChatGPT); check the spec repo for the current dated revision before citing a version number | https://modelcontextprotocol.io/ |
| goose | AAIF (donated by Block) | Local-first agent framework built on MCP | https://github.com/block/goose |
| AGENTS.md | AAIF (donated by OpenAI) | Convention only (a Markdown file), no version negotiation needed | https://agents.md/ |
| Agent2Agent (A2A) | Linux Foundation (separate project from AAIF, donated by Google, June 2025) | Agent-to-agent interoperability; complements MCP rather than replacing it | https://a2a-protocol.org/ |

## What the automatic check does

`scripts/check_standards_freshness.py` reads `next_review_due` above and fails the repository's
validation run once today's date passes it. It does not fetch anything from the internet and
cannot tell you what changed — it only tells you it's time for a person (or an AI assistant, on
request) to re-check the "Official source" links above and update `last_verified`,
`next_review_due`, and any row whose status changed.

## How to refresh this file

1. Open each "Official source" link above.
2. Update any row whose status or reference number changed; add a new row for a new standard
   this repository starts depending on.
3. Set `last_verified` to today and `next_review_due` to `last_verified` plus the row's cycle
   (90 or 365 days).
4. Commit. The next validation run will pass again.