# Agent control panel (Google Sheets, no coding)

This folder turns the technical templates into **six tabs of one Google Sheet**. A person fills in rows; nothing runs by itself. A run only starts after a named person approves it.

| Tab (sheet name) | File to import | What it answers |
|---|---|---|
| AgentTasks | `agent-tasks.csv` | What do we want done? |
| AgentWorkspaces | `agent-workspaces.csv` | Which approved sources and tools may be used? |
| AgentPolicies | `agent-policies.csv` | What is allowed (privacy, network, review)? |
| AgentRuns | `agent-runs.csv` | Where is each run right now? |
| AgentApprovals | `agent-approvals.csv` | Who said yes or no, and when? |
| AgentSources | `agent-sources.csv` | Are our sources still current? |

## Create the Sheet (click by click)

1. On your computer, open Google Sheets in a browser and click **Blank spreadsheet**. Name it `agent-control-panel`.
2. Click **File → Import → Upload**, then drag in `agent-tasks.csv`.
3. Choose **Replace current sheet** for the first file, then click **Import data**. Rename the tab to `AgentTasks`.
4. For each remaining file: **File → Import → Upload**, choose **Insert new sheet(s)**, click **Import data**, then rename the new tab (see the table).
5. Turn on drop-down lists (recommended): click a column letter such as `phase` in `AgentRuns` → **Data → Data validation → Add rule** → **Drop-down** and type the allowed values below.

## Allowed values for drop-downs

| Column | Values |
|---|---|
| `sensitivity` | public, internal, restricted |
| `phase` | created, preparing, ready, running, waiting_for_review, paused, suspended, completed, failed, terminated |
| `decision` | approved, rejected, needs_changes |
| `freshness` | current, stale, unknown, source_missing |
| `outputFormat` | google-docs, google-sheets, markdown, manual |

## Rules that keep it safe

- Do not type names, phone numbers, patient details, passwords, or keys into any tab.
- `restricted` rows are for people to handle by hand. No AI runs on them unless a written policy allows it.
- Share the Sheet only with named people or groups, never "anyone with the link".
- If a source is `stale` or `source_missing`, pause the task and ask the source owner.
