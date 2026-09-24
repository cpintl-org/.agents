# Plain-language guide to the agent layers

This guide explains the new parts of `.agents` without technical terms. You do not need to install anything to read it or to use the Google Sheets control panel.

## The big picture in one paragraph

To ask an AI to do useful work safely, we write down five things: **what** we want done (Task), **which sources and tools** it may use (Workspace), **what it is allowed to do** (Policy), **which AI, if any** (Model Adapter), and **who says yes** (Human Approval). We also save good instructions as **prompt files**, remember approved facts with their **source and freshness**, and record **how each run went**. Every piece can be edited in Google Sheets, Google Docs, or the GitHub website.

## Words you will see

| Word | Plain meaning | Where it lives |
|---|---|---|
| Brain | A role description for an agent, such as "careful researcher" | `brains` |
| Skill | A saved procedure an agent can follow | `skills` |
| Prompt file | A saved, versioned instruction with declared inputs and outputs | `prompts` |
| Task | What we want done, in plain words | `templates/agent-task.yaml` or the AgentTasks tab |
| Workspace | The approved sources and tools for one task | `templates/agent-workspace.yaml` or the AgentWorkspaces tab |
| Policy | Rules: privacy level, network access, review | `templates/agent-policy.yaml` or the AgentPolicies tab |
| Model adapter | The one file that names the AI provider and model | `providers` |
| Run | One attempt at a task, with a progress status | `templates/lifecycle-run.yaml` or the AgentRuns tab |
| Approval | A named person's yes or no | `templates/human-approval.yaml` or the AgentApprovals tab |
| Provenance | Where a fact came from, and which version | `memory` |
| Freshness | Whether a source is still current | `memory` |
| Schema | A rulebook for how a file must look | `schemas`, `memory`, `evaluation` |
| Evaluation | Checking whether the result was good and safe | `evaluation` |
| Adapter | A small file that translates between our neutral format and one provider | `providers/adapters` |

## What to do first (in this order)

1. **Read the safety rules.** Open `guardrails/README.md` and `guardrails/adoption-boundaries.md`. Anything about people, patients, or safeguarding is `restricted` and handled by a person.
2. **Make the control panel.** Follow `templates/agent-control-panel/README.md` to create the six-tab Google Sheet.
3. **Fill one small task.** Pick a low-risk internal task, such as summarizing a public policy document. Use `manual-review` as the model so no AI is involved at first.
4. **Get a person to approve it.** Record the decision in the AgentApprovals tab.
5. **Try one prompt file.** Follow `prompts/README.md` to copy the example prompt.
6. **Try one approved source.** Register one folder, not a whole Drive (see `memory/provenance-and-freshness.md`).
7. **Only then choose a provider.** Use `providers/README.md`, verify the provider's current official terms, and never use a free tier for restricted data.

## How the parts connect

```text
Request (Google Form) -> AgentTasks tab -> person checks ->
Workspace + Policy + Model adapter chosen -> run -> "waiting for review" ->
person approves -> result delivered -> run record saved
```

## If something goes wrong

- The checker shows a message: read `prompts/diagnostics.md`.
- A source looks out of date: mark it `stale` and ask its owner.
- The AI or a connection is unavailable: switch the task's model to `manual-review` and do it by hand.
- Unsure whether something is safe: stop and ask the responsible person. It is always fine to pause.

## Where commands run (only if you choose to use them)

Every command in this repository says where to run it. Unless it says otherwise, open a terminal in the folder that contains the repository (the folder that holds `README.md`), then type or paste the command. You never need a command to use the Sheets control panel or to edit files on the GitHub website.
