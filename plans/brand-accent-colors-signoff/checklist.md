# Task planning checklist — leadership sign-off on brand colors

**Task name:** `leadership-signoff-brand-accent-colors`
**Owner role:** `Health Program Manager`
**Date:** `2026-09-27`

> ✅ **DECISION RECORDED: all 16 accent colors approved by the Country Director on 2026-09-27.**
> Plain-language guide: [`review-pack.md`](./review-pack.md) ·
> Signed sheet: [`signoff-sheet.md`](./signoff-sheet.md)

## Before approving

- [x] The objective is one plain sentence.
- [x] A named reviewer role is written down (**Country Director**, 2026-09-27).
- [x] Sensitivity is set (`internal`; no personal, patient, or safeguarding information).
- [ ] Every source in the workspace is approved by a person and has a scope (the `brand-guide-pdf` Drive folder still needs a verified folder ID — see note below).
- [x] Tools are read-only or dry-run (none configured; the task is manual by design).
- [x] The policy denies network access by default and requires human review.
- [x] The model adapter contains no keys, passwords, or tokens (`manual-review`).
- [x] A manual fallback exists (the whole task is manual — a person does it by hand).
- [x] The checker reports no errors (run on 2026-09-27).
- [x] A plain-language review pack exists with a summary table (what/how/where/verify) and a check/uncheck decision sheet.

## Leadership decision (recorded)

- [x] Reviewer role written down: **Country Director**.
- [x] All 16 program codes confirmed — 14 proposed, 2 guide-fixed.
- [x] Guide-fixed codes (WASH, CleanEnergy) kept as CPI Blue/Teal.
- [x] Decision returned: **all approved** (all 16 ☑ Keep on the sign-off sheet).

## After the run

- [x] Sources were checked against the result (data files verified; the `brand-guide-pdf` Drive folder was not needed for the decision and remains unverified).
- [x] Nothing sensitive was exposed.
- [x] The Human Approval record (`human-approval.yaml`) is filled in: `approved`, Country Director, 2026-09-27.
- [x] Outcome and lessons are noted in the run record (`run.yaml`: phase `completed`).

> **One open follow-up (not blocking):** the `brand-guide-pdf` Drive folder ID was never
> verified, so `SourceValidated` stays `Unknown`. When the brand guide PDF is later attached as
> an approved source, update `workspace.yaml` with the verified folder ID and re-run the checker.