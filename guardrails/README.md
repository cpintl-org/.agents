# Guardrails

Guardrails define what an agent may do, must not do, and must escalate. They apply across brains, skills, templates, memory, GitHub, Google Workspace, and external AI providers.

## Use

Read `security-rules.yaml` before any external integration. Read `data-retention-policy.md` before storing prompts, outputs, logs, or Workspace metadata. Treat `restricted` data as human-review only unless an approved policy explicitly permits a bounded operation.

Guardrails do not grant authorization. The connector, GitHub permission, Workspace role, or provider policy remains authoritative. When rules conflict, choose the stricter rule and create a human-review task.
