# `.agents` Repository TODO

**Repository:** `cpintl-org/.agents`  
**Inventory baseline:** `main` at commit `876274e4ef944b9f07b8d218b0b9517dd0a3e380`  
**Current Milestone:** Verification, documentation, CI hardening, and low-risk pilot completion.

---

## Current inventory summary

- **Brains:** `brains/` contains role definitions and creation guidance.
- **Skills:** `skills/` contains seven reusable skills, bundled references, templates, and validators.
- **Guardrails:** `guardrails/` contains security, retention, and adoption-boundary rules.
- **Prompts:** `prompts/` contains the prompt convention, example prompts, shared partials, schemas, and synthetic fixtures.
- **Schemas:** `schemas/` contains neutral task, workspace, policy, model, agent, approval, checkpoint, lifecycle, and run schemas.
- **Providers:** `providers/` contains provider catalog and adapters, including verified `manual-review` and `google-gemini`.
- **Memory:** `memory/` contains read-only memory contracts, provenance/freshness schemas, registered pilot source, and short-term memory rules.
- **Evaluation:** `evaluation/` contains schemas, a human-review rubric, example synthetic run records, and completed pilot evaluation reports.
- **Templates:** `templates/` contains agent YAML templates and six Google Sheets control-panel CSV templates.
- **Workspace bridge:** `workspace-bridge/` contains Apps Script code, manifest, clasp configuration, deployment guide, and offline behavioral test suite (`test-bridge.js`).
- **Automation:** `.github/workflows/` contains hardened skill validation and safe Workspace sync dispatch workflows.
- **Configuration:** `config/` contains naming, bridge mapping, and repository manifest files.

---

## Status and Verification Milestones

- [x] Apps Script declaration-order defect is resolved: `event` parsed before `verifySecret_()` in `Code.gs`.
- [x] Manifest uses `Asia/Dhaka`, V8 runtime, explicit Drive/Docs/external-request scopes, and anonymous web-app access.
- [x] Apps Script web app is deployed and live: GET returns `{"status":"ok","service":"workspace-bridge","dryRun":true,"statusCode":200}`.
- [x] `DRY_RUN=true` remains the required safe operating mode across all automated steps.
- [x] CI validation workflow (`skill-validation.yml`) installs `PyYAML` and `jsonschema`, executing prompt, agent YAML, memory request, JSON Schema (Draft 2020-12), and offline bridge behavioral test suites.
- [x] Offline behavioral test suite (`workspace-bridge/test-bridge.js`) passes all 11 critical path and security test cases.
- [x] Low-risk baseline pilot completed: `cpi-technical-writing-guide` source registered, human review rubric evaluated, and evaluation report archived in `evaluation/reports/`.

---

## P0 — Apps Script Setup and Bridge Verification

### 1. Verify the Apps Script copy is exactly current

- [x] Copy the current committed `workspace-bridge/Code.gs` into Apps Script.
- [x] Confirm `event` is declared before `verifySecret_()` in `doPost()`.
- [x] Confirm the GitHub API URL construction is complete and syntactically valid in Apps Script.
- [x] Save the Apps Script project after pasting.
- [x] Confirm there are no secrets, tokens, Drive IDs, or webhook URLs in `Code.gs`.

### 2. Verify Apps Script manifest and project settings

- [x] Confirm `appsscript.json` has `timeZone: Asia/Dhaka`.
- [x] Confirm runtime is `V8`.
- [x] Confirm the three required OAuth scopes are present.
- [x] Confirm web-app execution is `USER_DEPLOYING`.
- [x] Confirm anonymous access is allowed by the organization's policy before deployment.
- [x] Configured `.gitignore` to prevent clasp credentials (`.clasprc.json`, `.clasp.json`) from being tracked in git.

### 3. Configure and verify Script Properties

Add these exact property names in Apps Script Project Settings → Script properties:

- [x] `GITHUB_OWNER` = `cpintl-org`
- [x] `GITHUB_REPOSITORY` = `.agents`
- [x] `GITHUB_REF` = `main`
- [x] `GITHUB_TOKEN` = fine-grained token limited to `cpintl-org/.agents`, Contents read-only
- [x] `BRIDGE_SECRET` = independently generated random secret
- [x] `DRIVE_ROOT_FOLDER_ID` = ID of dedicated, non-sensitive test folder
- [x] `DRY_RUN` = `true`
- [x] `ALLOWED_PATHS` = `brains,skills,guardrails,templates,memory`
- [x] Confirm no property value contains leading/trailing spaces.
- [x] Confirm no property value is committed to GitHub or stored in a public document.
- [x] Run `healthCheck` and confirm all eight configuration keys are reported as configured.

### 4. Deploy safely

- [x] Authorize `healthCheck` using the intended Google account.
- [x] Deploy a Web app using the deploying account.
- [x] Copy the `/exec` URL.
- [x] Add repository secret `WORKSPACE_BRIDGE_WEBHOOK_URL` with the `/exec` URL.
- [x] Add repository secret `WORKSPACE_BRIDGE_WEBHOOK_SECRET` with exactly the same value as `BRIDGE_SECRET`.
- [x] Confirm the GitHub token is stored only in Apps Script Script Properties, not in GitHub Actions secrets.
- [x] Open the `/exec` URL and confirm the GET response reports `status: ok` and `dryRun: true`.

---

## P1 — Verification and CI Hardening

### 5. Bring CI into agreement with the repository documentation

- [x] Update `.github/workflows/skill-validation.yml` to install both `PyYAML` and `jsonschema`.
- [x] Run `skills/prompt-authoring/scripts/validate_prompts.py prompts/library` in CI.
- [x] Run `skills/agent-task-planning/scripts/validate_agent_yaml.py templates providers/adapters` in CI.
- [x] Run `skills/memory-search/scripts/validate_memory_request.py skills/memory-search/templates/memory-search-request.json` in CI.
- [x] Validate every JSON Schema with `jsonschema.Draft202012Validator.check_schema`.
- [x] Validate the committed prompt fixtures against their declared input schemas.
- [x] Ensure missing validator dependencies fail CI rather than silently weakening checks.
- [x] Run `node workspace-bridge/test-bridge.js` in CI.

### 6. Add offline bridge behavior checks

- [x] Test empty POST body → `empty_body` (400).
- [x] Test missing or incorrect secret → `invalid_secret` (403).
- [x] Test malformed JSON → `bridge_exception` (500).
- [x] Test unsupported event → `unsupported_event` / manual review (202).
- [x] Test non-`main` ref → `unsupported_ref` (403).
- [x] Test disallowed paths → zero processed files.
- [x] Test `..`, absolute paths, control characters, and unsafe folder segments.
- [x] Test dry-run → reports count and creates no Drive files.
- [x] Test nested paths such as `skills/example/SKILL.md`.
- [x] Test two same-named files under different folders.
- [x] Test existing unmarked same-name document → `duplicate_unidentified_filename` and no overwrite.
- [x] Test marked existing document → update matching document only.
- [x] Test health check reports configured keys accurately.

### 7. Verify the GitHub workflow behavior

- [x] Confirm the workflow only runs for approved `main` pushes and the listed path filters.
- [x] Confirm missing bridge secrets cause an explicit intentional skip.
- [x] Confirm the workflow logs the bridge response without exposing the secret.
- [x] Confirm `curl` failure causes the workflow to fail (`--fail-with-body`).
- [x] Confirm workflow permissions remain `contents: read`.
- [x] Confirm action references remain pinned.

---

## P1 — Resolve Documentation and Implementation Drift

### 8. Reconcile bridge hierarchy documentation

- [x] Reconcile wording in `docs/configure-google-appsscript-workspace-bridge.md` regarding nested-folder creation.
- [x] State precisely: nested folders are created only for paths present in a received push event and allowed by `ALLOWED_PATHS`.
- [x] State that unchanged files are not backfilled automatically.
- [x] State that deletions are not propagated.
- [x] State that moved files create a new destination identity and leave the old Drive document for manual review.
- [x] State that binary files are not approved for production use by the current text-document implementation.

### 9. Reconcile operational claims

- [x] Reconcile README claims: clarify that `auditId` is a transaction identifier returned by the web app, not an automatically written persistent Google Sheets row.
- [x] Document that `status: ok` means the HTTP request was accepted.
- [x] Align transport documentation: secret is sent in the JSON body as `bridge_secret`.
- [x] Update deployment guide to reflect `Asia/Dhaka`.
- [x] Archived `cpintl-agents-update.patch` into `docs/archive/`.
- [x] Fixed trailing whitespace and heading formatting in `README.md`.
- [x] Added `docs/ai-agent-development-setup.md` for Google Gemini and AI agentic setups.

---

## P2 — Controlled Pilot & Production Gates

### 10. Synthetic bridge pilot

- [x] Verified against empty, non-sensitive Drive test folder.
- [x] Kept `DRY_RUN=true`.
- [x] Confirmed `Workspace bridge sync` workflow dispatch executes cleanly.
- [x] Confirmed Apps Script execution receives the request and accepts secret and `main` ref.
- [x] Confirmed zero Drive files or folders created in dry-run mode.

### 11. Real low-risk manual-review pilot

- [x] Selected low-risk internal source: CPI Technical Writing Style Guide.
- [x] Registered approved source: `memory/pilot-cpi-style-source.json`.
- [x] Executed baseline evaluation using `manual-review` adapter: `evaluation/reports/pilot-run-record-001.json`.
- [x] Completed human review rubric: `evaluation/reports/pilot-run-report-001.md`.
- [x] Confirmed zero patient, clinical, safeguarding, or restricted data involved.
- [x] Configured `google-gemini` model adapter (`providers/adapters/google-gemini.yaml`) for subsequent provider runs.

### 12. Production-readiness gates

- [x] Nested-path test passed.
- [x] Duplicate-filename test passed.
- [x] Existing unmarked-file safety test passed.
- [x] Move and deletion behavior is understood and manually documented.
- [x] CI validates all checks claimed by README and manifest.
- [x] Real pilot has a completed human review and evaluation record.
- [x] No restricted data was placed in GitHub, Actions logs, Drive mirror, prompts, or provider calls.
- [ ] `DRY_RUN=false` remains prohibited until a human explicitly approves write mode.
