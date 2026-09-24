# Repository inventory: `cpintl-org/.agents`

**Snapshot reviewed:** `main` at commit [`7b90fe4`](https://github.com/cpintl-org/.agents/commit/7b90fe4ee96f39eef18bd3f66bb12a1c0851c436)
**Inventory:** 2 workflows, 2 brains, 9 skills, 5 guardrail/config areas, 5 memory schemas, prompt library, 10 neutral schemas, provider adapters, evaluation records, control-panel templates, Apps Script bridge, and documentation.

## Executive recommendation

**Do not add new integrations or abstractions yet.** The repository has a strong documented safety model, but it is not yet operationally ready for a real-data pilot. First close the small number of blocking verification and implementation gaps, then run exactly one low-risk, manual-review pilot and record its evaluation.

## Critical findings

### 1. Verification gaps and QA holes

**High priority**

- **The committed workflow does not run the newer validators described by the repository documentation.**
  The current [`skill-validation.yml`](https://github.com/cpintl-org/.agents/blob/7b90fe4ee96f39eef18bd3f66bb12a1c0851c436/.github/workflows/skill-validation.yml) installs only `PyYAML` and does not run:
  - `validate_prompts.py`
  - `validate_agent_yaml.py`
  - `validate_memory_request.py`
  - JSON Schema validation

  This conflicts with the updated README, manifest, and recent structural-layer changes.

- **`jsonschema` is required by `validate_agent_yaml.py`, but the workflow does not install it.**
  The script imports it unconditionally. The workflow therefore cannot validate agent YAML files as documented.

- **Prompt validation can silently become weaker without `jsonschema`.**
  [`validate_prompts.py`](https://github.com/cpintl-org/.agents/blob/7b90fe4ee96f39eef18bd3f66bb12a1c0851c436/skills/prompt-authoring/scripts/validate_prompts.py) treats `jsonschema` as optional. That means CI can pass while skipping frontmatter and fixture schema validation.

- **Schemas are parsed but not comprehensively exercised.**
  YAML and JSON syntax checks exist, but the workflow does not validate representative files against every applicable schema.

- **The Apps Script bridge has a blocking runtime defect.**
  In [`workspace-bridge/Code.gs`](https://github.com/cpintl-org/.agents/blob/7b90fe4ee96f39eef18bd3f66bb12a1c0851c436/workspace-bridge/Code.gs#L23-L31), `verifySecret_(e, event, ...)` is called before `event` is declared. This causes a JavaScript `ReferenceError`, caught as `bridge_exception`, so POST synchronization will fail before normal event processing.

- **Bridge testing is only configuration-level, not behavior-level.**
  The workflow checks mapping text and defaults, but does not test:
  - invalid secrets
  - unsupported events
  - traversal paths
  - duplicate filenames
  - malformed GitHub content responses
  - dry-run POST behavior
  - successful file synchronization

- **The bridge workflow does not actually prove synchronization.**
  Missing webhook secrets intentionally cause a successful skip. Therefore a green workflow does not mean Workspace synchronization happened.

### 2. Real-data pilot status

No completed real-data pilot is present.

The repository explicitly marks the pilot as **“pilot next”** in [`docs/roadmap.md`](https://github.com/cpintl-org/.agents/blob/7b90fe4ee96f39eef18bd3f66bb12a1c0858b5b9/docs/roadmap.md#L7-L14). The evidence shows:

- only a synthetic prompt fixture exists;
- `evaluation/example-run-record.json` is explicitly synthetic;
- no real approved Drive source registration is committed;
- no completed human approval record is present;
- no evaluation report exists beyond the README;
- no provider-backed run has been recorded;
- no evidence shows a result reached human review and was accepted or rejected.

**Conclusion:** the documented pilot loop has not reached real-data review/evaluation.

### 3. Pending proposals, approval queues, and distillation queues

- No open pull request is visible.
- The only permanent branch is `main`; no temporary branch remains.
- No populated approval, task, run, source, or workspace queue is committed under the control-panel templates.
- The evaluation directory contains schemas and an example only, not actual review records.
- No separate distillation queue or pending-proposal file is present.

The four returned pull requests are all closed:

```list type="pr" id=2e61fffe-defd-478a-8911-d93df55973d3
```

The repository therefore has **no detected GitHub-side pending proposal queue**, but its operational approval queue is also not yet instantiated with real records.

### 4. Documentation and implementation drift

Important mismatches:

- [`README.md`](https://github.com/cpintl-org/.agents/blob/7b90fe4ee96f39eef18bd3f66bb12a1c0851c436/README.md) describes expanded validation, but the committed workflow still contains the older validation steps.
- `config/repository-manifest.yaml` declares `promptValidation` and `agentTemplateValidation`, but CI does not enforce them.
- The manifest lists `evaluation`, `providers`, `schemas`, `prompts`, and `docs` as first-class components, while [`workspace-sync.yml`](https://github.com/cpintl-org/.agents/blob/7b90fe4ee96f39eef18bd3f66bb12a1c0851c436/.github/workflows/workspace-sync.yml) only triggers on:
  - `brains`
  - `skills`
  - `guardrails`
  - `templates`
  - `memory`
  - bridge mapping

  This may be intentional, but it is undocumented as an exclusion policy.
- `config/mcp-bridge-mapping.yaml` is marked `status: draft`, while the bridge workflow is named and described as an approved sync process.
- `workspace-bridge/README.md` says the bridge should be called with a secret header, but the workflow places `bridge_secret` in the JSON body. The code accepts the body, but the documented transport contract is inconsistent.
- `workspace-bridge/README.md` refers to verifying an audit row/log, while the implementation generates an `auditId` but does not write an audit row to a spreadsheet or persistent store.
- The README’s local validation commands now imply a broader validation system than the active CI workflow actually provides.
- `cpintl-agents-update.patch` is committed as a large patch artifact duplicating the structural-layer change. It is not referenced by the repository documentation or workflows and can become stale or misleading.

### 5. Ship hygiene and unrelated dirty files

GitHub does not expose a developer’s local uncommitted working tree, so local “dirty files” cannot be verified remotely.

From the repository state:

- `main` is protected.
- No temporary branches are listed.
- No open pull request is blocking shipment.
- The committed patch artifact is the main hygiene concern: `cpintl-agents-update.patch` appears to be a historical change artifact rather than an active repository input.
- Recent dependency pull requests were closed without merge commits, while the main branch still contains pinned action SHAs. This is not currently a blocker, but dependency status should be checked before the next change.

## Recommended order of work

### P0 — Fix before any pilot

1. Fix the undeclared `event` reference in `workspace-bridge/Code.gs`.
2. Update `skill-validation.yml` to install `PyYAML jsonschema`.
3. Run the prompt, agent-template, memory-request, and schema validators in CI.
4. Make `jsonschema` mandatory for prompt validation rather than optional in CI.
5. Add offline bridge behavior tests for secret validation, dry-run handling, path rejection, and duplicate filenames.

### P1 — Reconcile the current structure

6. Update README and manifest wording so they accurately describe what CI validates.
7. Document whether `prompts`, `providers`, `schemas`, `evaluation`, and `docs` are intentionally excluded from Workspace synchronization.
8. Align the bridge secret transport documentation with the actual workflow.
9. Clarify that `auditId` is only an identifier unless persistent audit storage is implemented.
10. Remove or clearly label `cpintl-agents-update.patch` as archival.

### P2 — Run one controlled pilot

Use the existing structure only:

1. Select one public or low-risk internal document.
2. Register one approved source.
3. Use `manual-review` first.
4. Record the task, workspace, policy, run, and approval.
5. Produce a result with named sources and `UNKNOWN` gaps.
6. Complete the human-review rubric.
7. Save a redacted evaluation report and run record.
8. Only after approval, repeat the same task with one approved provider.

**Go/no-go rule:** do not use restricted or personal data until the bridge bug, CI validation gaps, and the manual pilot evaluation are complete.

---

# What Done After The Repository Inventory Report Generation

-  I created a Google Drive folder for the mirror
-  I copied the Drive folder URL and extracted the folder ID
-  I generated a random BRIDGE_SECRET using a password manager or openssl
-  I saved BRIDGE_SECRET in my password manager
-  I added BRIDGE_SECRET to Apps Script Script Properties
-  I added GITHUB_OWNER = cpintl-org
-  I added GITHUB_REPOSITORY = .agents
-  I added GITHUB_REF = main
-  I added GITHUB_TOKEN = my fine-grained GitHub token
-  I added DRIVE_ROOT_FOLDER_ID = my folder ID
-  I added DRY_RUN = true
-  I added ALLOWED_PATHS = brains,skills,guardrails,templates,memory
-  I fixed the Apps Script bug where event is used before declaration
-  I authorized the Apps Script project
-  I deployed the web app
-  I copied the /exec URL
-  I added WORKSPACE_BRIDGE_WEBHOOK_URL to GitHub repo secrets
-  I added WORKSPACE_BRIDGE_WEBHOOK_SECRET = same as BRIDGE_SECRET
-  I kept DRY_RUN = true
-  I tested the dry-run flow
-  I confirmed no files were created in Drive
