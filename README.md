# `.agents` — Universal AI Agent Command Center

Welcome to the central brain of **`cpintl-org`**! 🎨✨

This repository is designed specifically for **no-coders, vibe-coders, and creators**. You do not need to write complex code, learn terminal commands, or decipher complicated technical jargon to build and manage world-class AI agents here.

If you can type in Google Docs, organize files in Google Drive, or edit simple Markdown files on GitHub, you can control the entire AI universe of `cpintl-org`!

---

## 📜 Table of Contents

1. [🌟 What is This Hub?](https://www.google.com/search?q=%2523-what-is-this-hub&utm_source=gemini)
2. [🏗️ How Everything is Organized (The Lego Block System)](https://www.google.com/search?q=%2523%25EF%25B8%258F-how-everything-is-organized-the-lego-block-system&utm_source=gemini)
3. [📂 Repository Tree](https://www.google.com/search?q=%2523-repository-tree&utm_source=gemini)
4. [🔗 How GitHub & Google Workspace Connect in Real Time](https://www.google.com/search?q=%2523-how-github--google-workspace-connect-in-real-time&utm_source=gemini)
5. [💡 Beginner's Guide: How, What, & Where to Add Content](https://www.google.com/search?q=%2523-beginners-guide-how-what--where-to-add-content&utm_source=gemini)
* [Adding a New Agent Brain](https://www.google.com/search?q=%25231-adding-a-new-agent-brain&utm_source=gemini)
* [Adding a Reusable Skill](https://www.google.com/search?q=%25232-adding-a-reusable-skill&utm_source=gemini)
* [Adding a Guardrail or Rule](https://www.google.com/search?q=%25233-adding-a-guardrail-or-rule&utm_source=gemini)
* [Adding a Template](https://www.google.com/search?q=%25234-adding-a-template&utm_source=gemini)


6. [🛡️ Universal Provider Agnosticism & Security](https://www.google.com/search?q=%2523%25EF%25B8%258F-universal-provider-agnosticism--security&utm_source=gemini)
7. [🤝 Maintenance & Contribution Rules](https://www.google.com/search?q=%2523-maintenance--contribution-rules&utm_source=gemini)

---

## 🌟 What is This Hub?

Think of **`.agents`** as a master **AI Control Panel**.

Instead of locking your AI setups inside a single app (like only using ChatGPT or only using Gemini), this repository acts as a single, universal storage unit. You write your prompts, skills, and rules here, and they automatically sync with your **Google Workspace (Docs, Sheets, Shared Drives)**.

From here, you can connect your agent setup to **any AI provider**—including Gemini, Google AI Studio, Claude, OpenAI, GitHub Copilot, DeepSeek, or local tools—without ever re-writing your instructions!

---

## 🏗️ How Everything is Organized (The Lego Block System)

We structure everything like **Lego Blocks**. Each component does one specific job, and you can snap them together to build any AI agent you want!

```
┌────────────────────────────────────────────────────────────────────────┐
│                              AGENT BRAIN                               │
│                   (Personality, Role & Instructions)                   │
└──────────────────┬─────────────────────────────────┬───────────────────┘
                   │                                 │
                   ▼                                 ▼
┌─────────────────────────────────────┐   ┌──────────────────────────────┐
│               SKILLS                │   │          GUARDRAILS          │
│   (Tools, Actions & Capabilities)   │   │  (Safety Rules & Boundaries) │
└──────────────────┬──────────────────┘   └──────────────┬───────────────┘
                   │                                     │
                   └──────────────────┬──────────────────┘
                                      │
                                      ▼
┌────────────────────────────────────────────────────────────────────────┐
│                               TEMPLATES                                │
│                     (Google Docs / Sheets Outputs)                     │
└────────────────────────────────────────────────────────────────────────┘

```

1. **`brains/`**: The *Identity* (Who the agent is and what its goals are).
2. **`skills/`**: The *Capabilities* (What the agent knows how to do, step-by-step).
3. **`guardrails/`**: The *Safety Controls* (What the agent is allowed or forbidden to do).
4. **`templates/`**: The *Output Formats* (How documents, sheets, or emails should look).
5. **`memory/`**: The *Context Store* (How agents remember past interactions).
6. **`workspace-bridge/`**: The *Automation Engine* (The background magic that connects GitHub to Google Workspace).

---

## 📂 Repository Tree

Here is the exact layout of the `.agents` central repository:

```text
.agents/
├── README.md                          # You are here! Master guide for no-coders
├── LICENSE                            # Open/Internal usage terms
├── SECURITY.md                        # Security & vulnerability policies
├── .github/
│   └── workflows/
│       └── workspace-sync.yml         # Auto-sync engine running in the background
├── config/
│   ├── naming-policy.yaml             # Naming conventions for cpintl-org
│   └── mcp-bridge-mapping.yaml        # Maps GitHub folders to Google Drive folder IDs
├── brains/                            # AGENT PERSONALITIES & PROMPTS
│   ├── README.md                      # Guide to creating agent brains
│   ├── research-agent.md              # Research Assistant instructions
│   └── doc-writer-agent.md            # Technical Writer instructions
├── skills/                            # REUSABLE AGENT SKILLS
│   ├── README.md                      # Guide to packaging skills
│   ├── cpintl-org-writing-skill/      # Self-contained skill block
│   │   ├── SKILL.md                   # Primary trigger & skill instructions
│   │   ├── references/                # Deep reference docs (one level deep)
│   │   ├── scripts/                   # Utility helpers
│   │   └── templates/                 # Document outlines
│   └── workspace-drive-search/
│       └── SKILL.md
├── guardrails/                        # RULES, PRIVACY & SAFETY POLICIES
│   ├── README.md                      # Guide to setting agent boundaries
│   ├── security-rules.yaml            # Secret prevention & privacy rules
│   └── data-retention-policy.md       # Data handling rules
├── templates/                         # OUTPUT STRUCTURES & ASSETS
│   ├── README.md                      # Guide to creating templates
│   ├── google-docs-outline.md         # Document formatting rules
│   └── google-sheets-schema.json      # Structured spreadsheet definitions
├── memory/                            # AGENT CONTEXT & STATE SCHEMAS
│   ├── README.md                      # Guide to agent memory
│   └── short-term-memory-schema.json  # Context retention structures
└── workspace-bridge/                  # GOOGLE APPS SCRIPT ENGINE
    ├── appsscript.json                # Apps Script manifest
    ├── Code.gs                        # Listens for GitHub edits and syncs Drive
    └── clasp.json                     # Google Workspace CLI configuration

```

---

## 🔗 How GitHub & Google Workspace Connect in Real Time

You don't need to manually copy and paste text between GitHub and Google Docs!

```text
┌────────────────────────┐      Webhook Signal     ┌────────────────────────┐
│   GitHub (.agents)     │ ──────────────────────> │   Google Apps Script   │
│  Edit Markdown File    │                         │   (workspace-bridge)   │
└────────────────────────┘                         └───────────┬────────────┘
                                                               │
                                                               ▼
                                                   ┌────────────────────────┐
                                                   │   Google Shared Drive  │
                                                   │  Real-Time Updated Doc │
                                                   └────────────────────────┘

```

1. **Every GitHub folder corresponds to a Google Drive folder**:
* `brains/` ➡️ `[cpintl-org] Agentic Hub / Brains`
* `skills/` ➡️ `[cpintl-org] Agentic Hub / Skills`
* `guardrails/` ➡️ `[cpintl-org] Agentic Hub / Guardrails`


2. **Dual Identity**: Behind the scenes, every file keeps a clean link (a *Bridge URI*) connecting its GitHub location to its Google Drive File ID.
3. **Automatic Updates**: When you save a file on GitHub, a background job immediately updates the corresponding document in Google Workspace.

---

## 💡 Beginner's Guide: How, What, & Where to Add Content

### 1. Adding a New Agent Brain

* **Where to go**: The `brains/` folder.
* **What to add**: Create a new file ending in `.md` (e.g., `brains/social-media-agent.md`).
* **How to write it**: Use plain English! Define:
* Who the agent is (e.g., "You are an expert copywriter").
* What its goal is.
* Which skills it should use from the `skills/` folder.



### 2. Adding a Reusable Skill

* **Where to go**: The `skills/` folder.
* **What to add**: Create a folder named after your skill using lowercase letters and hyphens (e.g., `skills/format-excel-sheets/`).
* **Inside that folder, create**:
* `SKILL.md` (Required): Contains the trigger description and step-by-step instructions (under 500 lines).
* `references/` (Optional): A folder for detailed guides if the instructions are long.
* `templates/` (Optional): Pre-made example outputs.



### 3. Adding a Guardrail or Rule

* **Where to go**: The `guardrails/` folder.
* **What to add**: Create a Markdown file or simple list detailing safety boundaries.
* **Example**: "Never share personal email addresses; do not delete files; always ask for human approval before sending an email."

### 4. Adding a Template

* **Where to go**: The `templates/` folder.
* **What to add**: Markdown layouts, HTML snippets, or CSV structures that agents should use when creating Google Docs or Sheets.

---

## 🛡️ Universal Provider Agnosticism & Security

* **Provider Agnostic**: These prompt files do not belong to OpenAI, Gemini, or Claude. You can load these exact files into Google AI Studio, Claude Projects, OpenAI Custom GPTs, or local tools without modifying them.
* **Zero Secrets Allowed**: Never type passwords, API keys, or private tokens inside any document or file. Always use placeholders like `{GEMINI_API_KEY}` or `{DRIVE_FOLDER_ID}`.
* **Safe Filesystem Names**: Always use lowercase words separated by hyphens for folder and file names (e.g., `my-first-agent.md`). Do not use spaces or special symbols like `#`, `$`, `@`, or `%`.

---

## 🤝 Maintenance & Contribution Rules

As a no-coder maintainer or contributor, follow these simple rules to keep the system fast and error-free:

1. **Keep `SKILL.md` Concise**: Keep main skill files under 500 lines. Move extra details into a file inside the `references/` folder.
2. **Never Rename Folders Directly in Google Drive**: If you want to rename a folder, do it here in GitHub so the background links don't break.
3. **Use Simple English**: Write all prompts and guides clearly so anyone on your team can understand and update them!

### Main-only repository workflow

The permanent source of truth is the [`main` branch](https://github.com/cpintl-org/.agents/tree/main). Temporary working branches may be created automatically for a change, but they are removed after the change is merged. Automatic checks run for pull requests, updates to `main`, manual runs, and a weekly health check. No-coder maintenance instructions are in [`docs/no-coder-maintenance.md`](docs/no-coder-maintenance.md).

---

*Managed by `cpintl-org` — Powering Next-Generation No-Code & AI Workflows.*
