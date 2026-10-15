# Golden path — design-backloop after Build

Short recovery. SoT: [stages.md](../stages.md) Design-backloop · [invariants.md](../invariants.md) · [failure-playbook.md](../failure-playbook.md).

## Trigger

Build/Fix verify-fail (or review Critical/Major) cannot stay aligned with `03`/`04` without contract or IA change.

## Parent actions

1. Pause; **Decision N**: Amend design · Fix-only · Stop.
2. Prefer **Amend design** when contracts/IA must change.
3. Log Notes `design-backloop`; prior Gate B **invalid**.
4. Do **not** silently rewrite `03`/`04` inside Build/Fix.
5. Resume: `design-update` → design-review / design-verify-phase → **Gate B** again → Fix/Build.
6. Advance only on Result tokens in [results.md](../results.md) (`clean`, then `verify-pass`).

## Do not

- Go to Gate C with a known design mismatch
- Treat Gate B veto-after-Build as the same Decision (that shape is in [hitl.md](../hitl.md))
