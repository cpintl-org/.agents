# AI Agentic Development Setup Guide

This guide explains how to set up and run AI agents in the `cpintl-org/.agents` hub using **Google Gemini**, **Antigravity CLI (`agy`)**, **GitHub Copilot**, **Claude**, or other AI development environments.

All configurations strictly observe CPI's non-negotiable constraints:
- **Zero Cost**: Only free-forever tiers and local development setups.
- **Privacy & Safeguarding**: Strictly zero patient, clinical, or personally identifiable information (PII).
- **Human in the loop**: Every agent recommendation requires human review and sign-off.
- **Brand Compliance**: Arial font and official CPI color palette.

---

## 1. Google Gemini & Antigravity Setup

Antigravity CLI (`agy`) and Google Gemini provide an agentic development environment natively connected to this workspace.

### A. Environment Configuration
Store your Google AI Studio API key in your user shell environment (never commit it to git):

```bash
# Add to ~/.bashrc or run in your private terminal:
export GEMINI_API_KEY="your-gemini-api-key"
```

### B. Provider Adapter
The repository includes a ready-to-use model adapter configured for Gemini:
- File: [`providers/adapters/google-gemini.yaml`](../providers/adapters/google-gemini.yaml)
- Model: `gemini-2.0-flash` (or `gemini-1.5-pro`)
- Capabilities: Structured outputs, multimodal vision, tool calling
- Rate Limits & Free Quotas: Standard Google AI Studio free tier limits apply

---

## 2. Using AGENTS.md Across Different AI Tools

The [`AGENTS.md`](../AGENTS.md) file at the root of this monorepo is the universal system prompt and operating handbook for all AI assistants.

| AI Environment | How it Reads AGENTS.md |
|---|---|
| **Antigravity CLI / `agy`** | Auto-detected and loaded automatically at startup from the workspace root. |
| **Gemini CLI** | Auto-detected from root `AGENTS.md` or `.gemini/` rules directory. |
| **GitHub Copilot** | Auto-read as workspace instructions in VS Code / GitHub Codespaces. |
| **Cursor / Windsurf** | Auto-read as repository instructions. |
| **Claude / Web UIs** | Copy the Persona and Guardrails block from `AGENTS.md` into Custom Instructions or system prompt. |

---

## 3. How to Execute an Agent Task (Step-by-Step for Non-Coders)

1. **Step 1: Pick or Write a Prompt**
   - Check [`prompts/library/`](../prompts/library/) for existing approved tasks (e.g. `evidence-summary.prompt`).
   - Use [`skills/prompt-authoring/`](../skills/prompt-authoring/) to create a new `.prompt` file.

2. **Step 2: Choose Your Provider Adapter**
   - Use `adapters/manual-review.yaml` when reviewing by hand or handling internal-only text.
   - Use `adapters/google-gemini.yaml` when running with Google Gemini.

3. **Step 3: Run Validation Locally**
   Before sharing or executing, run the fast local checker:
   ```bash
   python skills/prompt-authoring/scripts/validate_prompts.py prompts/library
   python skills/agent-task-planning/scripts/validate_agent_yaml.py templates providers/adapters
   node workspace-bridge/test-bridge.js
   ```

4. **Step 4: Review Output Against the Rubric**
   - Score the agent output using [`evaluation/rubrics/human-review-rubric.yaml`](../evaluation/rubrics/human-review-rubric.yaml).
   - Confirm every fact cites an approved source.
   - Confirm missing information is marked `UNKNOWN` rather than guessed.
   - Record the result in [`evaluation/reports/`](../evaluation/reports/).

---

## 4. System of Record Boundaries

| Category | Authoritative System | AI Role |
|---|---|---|
| Beneficiary & Clinical Data | DHIS2 / InfoMx / Volunteer HIS | **NEVER send to AI** |
| Financial & Procurement | Oracle Financials | **NEVER send to AI** |
| Technical Writing & Ops Guides | This `.agents` GitHub repository | Allowed (drafting, formatting, syncing) |
| Workspace Mirror | Google Drive (`cpintl-org Agent Hub Mirror`) | Read-only mirror via Workspace Bridge |
