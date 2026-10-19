---
name: my-dev-flow-v2-design-review
description: >-
  Reviews design artifacts against best practices, then hands findings to
  design-update. Mode full: isolated API∥DB reviews (both 03a-* missing →
  same-turn parallel) then general design-review. Mode simple: one
  design-verify-phase Task. Use when the user says run my-dev-flow-v2-design-review,
  review the design, or after my-dev-flow-v2-design before Build.
---

# my-dev-flow-v2-design-review

Design-review subflow of [`my-dev-flow-v2`](../my-dev-flow-v2/SKILL.md).

| Topic | File |
|-------|------|
| Runtime order | [`../my-dev-flow-v2/stages.md`](../my-dev-flow-v2/stages.md) |
| Stage prompts | load **`stages/<id>.md` only** |
| Has API/DB / tiny-tweak / Pending parallel | [`../my-dev-flow-v2/lenses.md`](../my-dev-flow-v2/lenses.md) |
| Handoffs | compose from [`../my-dev-flow-v2/handoffs.md`](../my-dev-flow-v2/handoffs.md) |
| Severity / Results | [`../my-dev-flow-v2/severity.md`](../my-dev-flow-v2/severity.md) · [`../my-dev-flow-v2/results.md`](../my-dev-flow-v2/results.md) |
| Preflight | [`../my-dev-flow-v2/preflight.md`](../my-dev-flow-v2/preflight.md) |

## Principles

- Result **clean** = zero Critical/Major **and** API/DB `clean`|`skipped` when required (Has=yes not tiny → isolated stage ran with Result clean, or Notes `tiny-contract-tweak`; Has=no → skipped via Notes only — “no file” alone is **not** skipped when Has=yes).
- `needs update` → design-update → re-review.
- Mode full + both API+DB yes (not tiny): both `03a-*` missing → same-turn parallel; one exists → missing only.
- Never invent empty `03a-api` / `03a-db` when skipped or tiny-tweak. Result **skipped** only with Notes skip / Has=no.
- Max 3 rounds → Decision N. Do not Gate B from this skill.

## Pipeline

```
Full:   (api-contract-review ∥ db-design-review) → design-review → clean | needs update
Simple: design-verify-phase → clean | needs update
```

## Start

1. Confirm Has API/DB/auth yes\|no; preflight design-review checks.
2. Compose handoff; run matching `stages/<id>.md`.
3. Parent: on clean → TDD/Gate B; on needs update → design-update.
