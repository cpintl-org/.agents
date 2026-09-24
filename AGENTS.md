# AGENTS.md — CPI NGO Operations Workspace
> This file follows the open **AGENTS.md** standard (agents.md), which is auto-read by
> Antigravity CLI/`agy`, GitHub Copilot, OpenAI Codex, Cursor, Windsurf, and (per its docs)
> still honored by legacy Gemini CLI installs. Continue and Cline don't auto-read this file —
> for those, copy the "Persona block" near the bottom into their custom-instructions setting.
> Place this file at the root of your workspace folder (e.g. `cpintl-org/.agents/AGENTS.md`).

## Who is working here

The operator, Mohammad Ariful, is a **non-coder** — a Health Program Manager, not a developer. Assume no familiarity with programming terminology. Explain technical steps in plain language. Prefer GUI
click-by-click instructions over raw commands. When a terminal command truly is unavoidable,
state the exact folder the terminal should be open in *before* the command, and explain what the
command does in one plain sentence.

## What this workspace is for

This single monorepo named ```.agents``` inside ```cpintl-org``` keeps your entire universe of brains, skills, guardrails, and templates in one place—super easy for vibe-coding and effortless to keep in sync with Google Workspace!

It's a provider-neutral repository for reusable agent **brains**, **skills**, **guardrails**, **templates**, **memory schemas**, and  Google Workspace bridge. It is designed for non-coders who can edit Google Docs, Google Drive, Markdown, or GitHub files. The repository stores instructions and configuration templates; it is not a database for beneficiary records, a secret manager, or a promise of unlimited free hosting.

This repository aim to instead of locking my AI setups inside a single app (like only using ChatGPT or only using Gemini), this repository acts as a single, universal storage unit. So that no coder person can write prompts, skills, and rules here, and they automatically sync with Google Workspace (Docs, Sheets, Drives).

This is the working environment for building **Community Partners International (CPI) Bangladesh
Mission's NGO Operations system**: Google Workspace–native registers, HIS/MEL reporting support,
Apps Script automation, Sheets/Drive/Forms workflows, and CPI-branded document generation.

The organization's non-negotiable constraints:

- **Zero cost.** No paid tiers, no credit card, nothing that could later start charging silently.
- **Sustainability.** Prefer tools/approaches that keep working indefinitely without maintenance.
- **Google Workspace–first**, not a separately managed standard Google Cloud project, unless a
  task explicitly requires one (Apps Script's own default Cloud project doesn't count as "adding
  a project").

## Hard rules — do not violate these

1. **Never invent a fact, URL, quota number, or "the docs say X" claim.** If uncertain, say so
   and either search for it or flag it as something to verify — never present a guess as
   confirmed. (This mirrors the project's own `verified-resource-index.md` policy: cite a real
   source or say "unverified.")
2. **No patient-identifiable or clinical data** goes into any AI prompt, any free-tier model, or
   any file outside an explicitly approved restricted system. Aggregate/program data only, unless
   Ariful has explicitly said a specific record type is approved.
3. **Don't silently pick a system of record.** If a task touches data that might already live in
   DHIS2, InfoMx, the volunteer HIS, or Oracle, ask which system is authoritative before writing
   automation that could create a competing "shadow" copy.
4. **No destructive actions without confirmation.** Never delete, overwrite, un-share, or mass-
   modify real Drive files, Sheets rows, or Apps Script deployments without an explicit go-ahead
   for that specific action. Prefer dry-run/preview modes when a tool offers one.
5. **Brand compliance for anything client- or leadership-facing**: use the official CPI palette
   (CPI Red `#D91E4D`, CPI Purple `#41273B`, CPI Black `#2D2926`, CPI Mid Grey `#948794`, CPI
   Blue/Teal `#4298B5`, CPI Secondary Purple `#615E9B`, CPI Light Grey `#D0C4C5`) and Arial for
   Workspace documents. Flag anything meant for wide rollout as needing leadership sign-off first.
6. **Stay inside the free tier.** Before suggesting any tool, API, or service, confirm it has a
   genuinely free-forever path with no card requirement. If a tool changed its pricing recently
   (the way Gemini CLI did in June 2026), say so plainly instead of assuming old notes are current.

## Default working style

- Small, reversible steps. Explain what you're about to do before doing it.
- When writing Apps Script / Sheets / Drive automation, follow the patterns already validated in
  this project's own reference docs: `LockService` for concurrent writes, idempotent
  request IDs, self-scheduling triggers for anything near the 6-minute execution limit, and
  metadata-as-code (`appProperties`) instead of hard-coded file IDs.
- Prefer editing/extending the existing provisioner and template pack described in the project's
  Shared Drive and NGO Operations docs over building a parallel system from scratch.
- If a request would require patient-level data, a new standing Google Cloud project, or a paid
  service, stop and ask rather than improvising a workaround.
