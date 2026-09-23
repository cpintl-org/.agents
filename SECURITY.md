# Security & Safety Policy — `.agents` Hub

The **`cpintl-org`** organization is dedicated to maintaining a secure, privacy-compliant, and leak-free environment across all AI agent brains, skills, templates, and Google Workspace integrations.

---

## 🛡️ Non-Negotiable Security Rules for No-Coders

To protect our organization, Google Drive resources, and external API services, all maintainers and vibe-coders MUST observe the following rules:

1. **NO Hardcoded Credentials or Secrets**:
   * Never paste API keys, passwords, bearer tokens, service account credentials, or private credentials inside any Markdown document, prompt file, script, or sheet template.
   * Use structured placeholders at all times (e.g., `{GEMINI_API_KEY}`, `{WORKSPACE_OAUTH_TOKEN}`, `{DRIVE_FOLDER_ID}`).

2. **No Confidential Data Leaks**:
   * Avoid putting personally identifiable information (PII), proprietary financial records, or private user IDs into agent prompts or skill descriptions.

3. **Validate Filenames and Paths**:
   * Restrict file and folder names to lowercase kebab-case (`a-z`, `0-9`, and hyphens `-`).
   * Do not use reserved system characters, path traversal markers (`../`), or embedded tokens in naming structures.

4. **Read-Only Operations as Default**:
   * Automated MCP bridges and workspace sync triggers operate with read-only access by default unless write access is explicitly authorized in `config/mcp-bridge-mapping.yaml`.

---

## 🔒 Supported Versions

Only the active default branch (`main`) of the `.agents` monorepo receives security updates, policy updates, and sync workflow fixes.

| Component / Scope | Supported Version | Security Sync Active |
| ----------------- | ----------------- | -------------------- |
| `.agents/main`    | `1.0.x`           | Yes                  |
| Feature Branches  | Experimental      | No                   |

---

## 🚨 Reporting a Vulnerability

If you discover a potential security vulnerability, exposed credential placeholder, or data leakage risk within `cpintl-org/.agents`, **do not open a public GitHub issue**.

Please report vulnerabilities privately:

1. **Email Notification**: Contact the maintainers directly at `security@cpintl-org.internal` (or notify your designated system administrator).
2. **Details to Include**:
   * Description of the vulnerability or exposed file path.
   * Steps to reproduce or locate the issue.
   * Impact on Google Workspace, MCP servers, or connected LLM API services.

### Incident Response Process

* **Acknowledgment**: Reports will be acknowledged within 24 hours.
* **Triage & Remediation**: The security lead will investigate the reported resource, revoke any affected keys or tokens, and issue a patch or branch update within 72 hours.
* **Public Disclosure**: Once patched, a summary of the security advisory will be published if external dependencies were affected.

***

*Maintained by the `cpintl-org` Security and Governance Team.*
