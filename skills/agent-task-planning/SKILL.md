---
name: agent-task-planning
description: Help a non-coder plan an agent task by filling in five plain templates - Task, Workspace, Policy, Model Adapter, and Human Approval - and by tracking the run's progress with simple status conditions. Use when someone asks an agent to do multi-step work, wants to set up a reusable agent, or needs to know what the agent may use and who must approve.
---

# Agent task planning

Use this skill to turn a request in plain words into a small set of filled-in files that say **what** to do, **which sources and tools** may be used, **what is allowed**, **which AI provider** (if any), and **who must approve**. Nothing runs until a named person approves.

## Workflow

1. Restate the objective in one sentence and ask who will review the result.
2. Classify sensitivity. If the work involves information about identifiable people, patients, or safeguarding cases, mark it `restricted` and plan a manual (no AI) route.
3. Fill the five templates, in this order: Workspace (approved sources and tools), Policy (safe defaults), Model Adapter (start with `manual-review` if no provider is approved), Task (points to the other three by name), Human Approval (left as `needs_changes` until a person decides).
4. Keep every value in the templates plain. Use placeholders such as `{responsible-role}` until a fact is verified.
5. Check the files with the checker below and fix each message.
6. Record the run's progress with the phases in `references/lifecycle-and-status.md`. Move to `waiting_for_review` before any result is shared.
7. Never let an agent widen its own workspace, policy, or model. A person edits those files.

## Check

Where to run: a terminal opened in the repository root folder.

```bash
python skills/agent-task-planning/scripts/validate_agent_yaml.py templates
```

The checker confirms the files match their schemas and that every reference (for example a task naming a workspace) points to a file that exists. It does not prove the plan is wise or approved.

## Spreadsheet route

Non-coders can use the Google Sheets control panel in the repository `templates` folder instead of editing YAML. Each tab matches one template. Use `templates/task-planning-checklist.md` in this skill as the review list.

## Boundaries

Do not include secrets, personal data, or real Drive IDs in plans. Do not treat a valid file as permission: the connector, Workspace role, or provider policy remains authoritative. If a provider or integration is unavailable, create a manual task instead of guessing.
