# `.agents` Repository TODO

**Repository:** `cpintl-org/.agents`  
**Inventory baseline:** `main` at commit `876274e4ef944b9f07b8d218b0b9517dd0a3e380`  
**Purpose:** Close verification, documentation, and pilot-readiness gaps before enabling production Workspace synchronization.

## Current inventory summary

- **Brains:** `brains/` contains role definitions and creation guidance.
- **Skills:** `skills/` contains seven reusable skills, bundled references, templates, and validators.
- **Guardrails:** `guardrails/` contains security, retention, and adoption-boundary rules.
- **Prompts:** `prompts/` contains the prompt convention, one example prompt, a shared partial, schemas, and synthetic fixtures.
- **Schemas:** `schemas/` contains neutral task, workspace, policy, model, agent, approval, checkpoint, lifecycle, and run schemas.
- **Providers:** `providers/` contains a provider catalog and adapters, including `manual-review`.
- **Memory:** `memory/` contains read-only memory contracts, provenance/freshness schemas, and short-term memory rules.
- **Evaluation:** `evaluation/` contains schemas, a human-review rubric, an example synthetic run record, and an empty reports area.
- **Templates:** `templates/` contains agent YAML templates and six Google Sheets control-panel CSV templates.
- **Workspace bridge:** `workspace-bridge/` contains Apps Script code, manifest, clasp placeholder, and deployment instructions.
- **Automation:** `.github/workflows/` contains skill validation and optional Workspace sync dispatch workflows.
- **Configuration:** `config/` contains naming, bridge mapping, and repository manifest files.

## Status at inventory time

- The earlier `Code.gs` declaration-order defect is fixed in the repository: `event` is parsed before `verifySecret_()` is called.
- `appsscript.json` uses `Asia/Dhaka`, V8, explicit Drive/Docs/external-request scopes, and anonymous web-app access.
- The bridge is still **not proven deployed, configured, or tested against the user's Apps Script project** from repository evidence.
- `DRY_RUN` remains the required safe starting mode.
- The previous CI recommendations were **not implemented**: the validation workflow still installs only `PyYAML` and does not run the prompt, agent-YAML, memory-request, or JSON Schema validators listed in the README and manifest.
- No completed real-data pilot, human approval record, evaluation report, or provider-backed run is present in the repository.

## P0 — Must complete before any write-mode or production pilot

### 1. Verify the Apps Script copy is exactly current

- [ ] Copy the current committed `workspace-bridge/Code.gs` into Apps Script.
- [ ] Confirm `event` is declared before `verifySecret_()` in `doPost()`.
- [ ] Confirm the GitHub API URL construction is complete and syntactically valid in Apps Script.
- [ ] Save the Apps Script project after pasting.
- [ ] Confirm there are no secrets, tokens, Drive IDs, or webhook URLs in `Code.gs`.

### 2. Verify Apps Script manifest and project settings

- [ ] Confirm `appsscript.json` has `timeZone: Asia/Dhaka` if that is the approved operating timezone.
- [ ] Confirm runtime is `V8`.
- [ ] Confirm the three required OAuth scopes are present.
- [ ] Confirm web-app execution is `USER_DEPLOYING`.
- [ ] Confirm anonymous access is allowed by the organization's policy before deployment.
- [ ] If anonymous web apps are prohibited, stop; do not deploy this configuration.
- [ ] Replace the placeholder in `workspace-bridge/clasp.json` only if clasp is actually used; otherwise leave it as documentation-only configuration.

### 3. Configure and verify Script Properties

Add these exact property names in Apps Script Project Settings → Script properties:

- [ ] `GITHUB_OWNER` = `cpintl-org`
- [ ] `GITHUB_REPOSITORY` = `.agents`
- [ ] `GITHUB_REF` = `main`
- [ ] `GITHUB_TOKEN` = fine-grained token limited to `cpintl-org/.agents`, Contents read-only
- [ ] `BRIDGE_SECRET` = independently generated random secret
- [ ] `DRIVE_ROOT_FOLDER_ID` = ID of a dedicated, non-sensitive test folder
- [ ] `DRY_RUN` = `true`
- [ ] `ALLOWED_PATHS` = `brains,skills,guardrails,templates,memory`
- [ ] Confirm no property value contains leading/trailing spaces.
- [ ] Confirm no property value is committed to GitHub or stored in a public document.
- [ ] Run `healthCheck` and confirm all eight configuration keys are reported as configured.

### 4. Deploy safely

- [ ] Authorize `healthCheck` using the intended Google account.
- [ ] Deploy a Web app using the deploying account.
- [ ] Copy the `/exec` URL, not `/dev`.
- [ ] Add repository secret `WORKSPACE_BRIDGE_WEBHOOK_URL` with the `/exec` URL.
- [ ] Add repository secret `WORKSPACE_BRIDGE_WEBHOOK_SECRET` with exactly the same value as `BRIDGE_SECRET`.
- [ ] Never add the GitHub token as a GitHub Actions secret for this bridge; the current code reads it from Apps Script Script Properties.
- [ ] Open the `/exec` URL and confirm the GET response reports `status: ok` and `dryRun: true`.

## P1 — Close verification and QA gaps

### 5. Bring CI into agreement with the repository documentation

- [ ] Update `.github/workflows/skill-validation.yml` to install both `PyYAML` and `jsonschema`.
- [ ] Run `skills/prompt-authoring/scripts/validate_prompts.py prompts/library` in CI.
- [ ] Run `skills/agent-task-planning/scripts/validate_agent_yaml.py templates providers/adapters` in CI.
- [ ] Run `skills/memory-search/scripts/validate_memory_request.py skills/memory-search/templates/memory-search-request.json` in CI.
- [ ] Validate every JSON Schema with `jsonschema.Draft202012Validator.check_schema`.
- [ ] Validate the committed prompt fixtures against their declared input schemas.
- [ ] Ensure a missing validator dependency fails CI rather than silently weakening checks.
- [ ] Update `config/repository-manifest.yaml` only if the implemented checks intentionally differ from the documented checks.

### 6. Add offline bridge behavior checks

Use a small, deterministic test fixture or existing repository-safe validation method. Do not add a new service or dashboard.

- [ ] Test empty POST body → `empty_body`.
- [ ] Test missing or incorrect secret → `invalid_secret`.
- [ ] Test malformed JSON → `bridge_exception` or an explicitly documented JSON error.
- [ ] Test unsupported event → `unsupported_event` / manual review.
- [ ] Test non-`main` ref → `unsupported_ref`.
- [ ] Test disallowed paths → zero processed files.
- [ ] Test `..`, absolute paths, control characters, and unsafe folder segments.
- [ ] Test dry-run → reports count and creates no Drive files.
- [ ] Test a nested path such as `skills/example/SKILL.md`.
- [ ] Test two same-named files under different folders, such as `brains/README.md` and `skills/README.md`.
- [ ] Test an existing unmarked same-name document → `duplicate_unidentified_filename` and no overwrite.
- [ ] Test a marked existing document → update the matching document only.
- [ ] Test GitHub API non-200 response → `github_content_fetch_failed` and no partial approval of the run.
- [ ] Test binary or non-text content separately; do not enable it for production based only on text tests.

### 7. Verify the GitHub workflow behavior

- [ ] Confirm the workflow only runs for approved `main` pushes and the listed path filters.
- [ ] Confirm missing bridge secrets cause an explicit intentional skip, not a false claim of synchronization.
- [ ] Confirm the workflow logs the bridge response without exposing the secret.
- [ ] Confirm `curl` failure causes the workflow to fail.
- [ ] Confirm workflow permissions remain `contents: read`.
- [ ] Confirm action references remain pinned and review any dependency-update PR before changing them.

## P1 — Resolve documentation and implementation drift

### 8. Reconcile bridge hierarchy documentation

The current committed code includes `ensureFolderPath_()`, which creates or reuses nested folders for **changed allowed files**. It does not create a complete mirror of every repository path automatically.

- [ ] Replace contradictory wording in `docs/configure-google-appsscript-workspace-bridge.md` that says the bridge does not create a complete folder hierarchy while also documenting nested-folder creation.
- [ ] State precisely: nested folders are created only for paths present in a received push event and allowed by `ALLOWED_PATHS`.
- [ ] State that unchanged files are not backfilled automatically.
- [ ] State that deletions are not propagated.
- [ ] State that moved files create a new destination identity and leave the old Drive document for manual review.
- [ ] State that binary files are not approved for production use by the current text-document implementation.
- [ ] Keep the duplicate-filename and nested-path warning until the tests above pass in the real test folder.

### 9. Reconcile operational claims

- [ ] Change or implement the README claim about verifying an “audit row/log”; current code returns an `auditId` but does not write a persistent audit row.
- [ ] Document that `status: ok` from the GitHub workflow means the HTTP request succeeded, not that every file was permanently synchronized.
- [ ] Align the README wording “secret header” with the current workflow, which sends `bridge_secret` in the JSON body. Prefer one documented transport and test it.
- [ ] Document that `config/mcp-bridge-mapping.yaml` is draft/read-only configuration and is not proof that the bridge is deployed.
- [ ] Update the deployment guide to reflect `Asia/Dhaka` if that timezone is now the approved repository setting.
- [ ] Review the historical `cpintl-agents-update.patch`; archive or remove it if it is not an intentional maintained artifact.

## P2 — Run the controlled pilot

### 10. Synthetic bridge pilot

- [ ] Use an empty, non-sensitive Drive test folder.
- [ ] Keep `DRY_RUN=true`.
- [ ] Trigger one harmless allowed change on `main`.
- [ ] Confirm the `Workspace bridge sync` workflow runs.
- [ ] Confirm the Apps Script execution receives the request.
- [ ] Confirm the secret and `main` ref are accepted.
- [ ] Confirm the allowed changed path is counted.
- [ ] Confirm no Drive file or folder is created in dry-run mode.
- [ ] Save a redacted test note outside the repository if it contains operational identifiers.

### 11. Real low-risk manual-review pilot

Do not use beneficiary, health, safeguarding, financial, credential, or other restricted data.

- [ ] Select one public or low-risk internal source.
- [ ] Register one approved source, not an entire Drive.
- [ ] Create one task using the existing task template/control-panel tabs.
- [ ] Use the `manual-review` adapter first.
- [ ] Record workspace, policy, model adapter, run status, and approval.
- [ ] Produce a result with named sources and `UNKNOWN` for gaps.
- [ ] Complete `evaluation/rubrics/human-review-rubric.yaml`.
- [ ] Save a redacted evaluation report and run record.
- [ ] Do not proceed if any blocking review criterion fails.
- [ ] Only after approval, repeat the same low-risk task with one verified provider adapter.

## P2 — Production-readiness gates

- [ ] Nested-path test passed.
- [ ] Duplicate-filename test passed.
- [ ] Existing unmarked-file safety test passed.
- [ ] Move and deletion behavior is understood and manually documented.
- [ ] Recovery/archive procedure is tested.
- [ ] CI validates all checks claimed by README and manifest.
- [ ] Real pilot has a completed human review and evaluation record.
- [ ] No restricted data was placed in GitHub, Actions logs, Drive mirror, prompts, or provider calls.
- [ ] A responsible maintainer is named for token rotation, Apps Script deployment, Drive permissions, and failure response.
- [ ] `DRY_RUN=false` remains prohibited until a human explicitly approves write mode.

## Explicit non-goals for this TODO

Do not add a new dashboard, UI, paid integration, automatic indexing system, broad runtime, bidirectional sync, deletion automation, or provider-specific abstraction. The immediate work is limited to making the existing bridge and documented repository checks accurate, testable, and safe for one controlled pilot.

## Completion definition

This TODO is complete only when:

1. The repository's automated checks match its documentation.
2. The current bridge code passes the offline and real test-folder safety checks.
3. The nested-folder and duplicate-identity behavior is demonstrated.
4. One low-risk pilot reaches human review and evaluation.
5. A maintainer explicitly approves any transition away from `DRY_RUN=true`.
