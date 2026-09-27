# Task planning checklist

**Task name:** `{task-name}`  **Owner role:** `{owner-role}`  **Date:** `{YYYY-MM-DD}`

## Before approving

- [ ] The objective is one plain sentence.
- [ ] A named reviewer role is written down.
- [ ] Sensitivity is set. Personal, patient, or safeguarding information means `restricted` and no AI.
- [ ] Every source in the workspace is approved by a person and has a scope.
- [ ] Tools are read-only or dry-run unless a person approved otherwise.
- [ ] The policy denies network access by default and requires human review.
- [ ] The model adapter contains no keys, passwords, or tokens.
- [ ] A manual fallback exists if the AI or an integration is unavailable.
- [ ] The checker reports no errors.
- [ ] A plain-language `review-pack.md` exists in the plan folder: what to check, how to check (no code), where the files are, and what is already verified.
- [ ] Every decision leaders must make is one row in a Markdown check/uncheck table (☐ Keep / ☐ Change), with a summary table and suggestions.
- [ ] The two (or more) "guide fixes this" facts are marked so only the genuinely open decisions get re-decided.

## After the run

- [ ] Sources were checked against the result.
- [ ] Nothing sensitive was exposed.
- [ ] The Human Approval record is filled in.
- [ ] Outcome and lessons are noted in the run record.
