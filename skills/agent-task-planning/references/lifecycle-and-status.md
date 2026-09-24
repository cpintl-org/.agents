# Lifecycle and status conditions

## Phases of a run

| Phase | Plain meaning |
|---|---|
| `created` | The request is written down. Nothing has started |
| `preparing` | Sources and permissions are being checked |
| `ready` | Everything is checked and waiting for a person to start |
| `running` | Work is in progress |
| `waiting_for_review` | Work is done; a named person must decide |
| `paused` | Stopped on purpose; can continue |
| `suspended` | Stopped and saved (see checkpoint policy); can continue later |
| `completed` | A person approved and the result was delivered |
| `failed` | Something went wrong; read the note and decide what to do |
| `terminated` | Ended for good; will not continue |

## Conditions

Conditions are yes/no facts, each with a status of `True`, `False`, or `Unknown`, and an optional short reason.

| Condition type | Meaning |
|---|---|
| `SourceValidated` | Every source is approved and current |
| `PolicyChecked` | The policy allows this task |
| `HumanApproval` | A named person has approved |
| `OutputValidated` | The result matches the expected shape |

## Separating the pieces

The **template** is the reusable recipe. The **instance** is one run. The **workspace** is what it may see. The **policy** is what it may do. The **model adapter** is which AI (or a person) does the work. Keeping these apart lets you change one without touching the others.

## Not required now

Pausing, saving progress, and resuming are planning ideas. Nothing in this repository runs an agent automatically. Add runtime tooling only after a small manual pilot works.
