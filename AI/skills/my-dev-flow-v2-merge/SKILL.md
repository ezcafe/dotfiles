---
name: my-dev-flow-v2-merge
description: >-
  After explicit user Gate C approval, commits (if approved), pushes the branch,
  opens a PR, then merges. Never commit or push without that yes. Use when the
  user says run my-dev-flow-v2-merge, merge the workflow, or after the Gate C
  test bar is met.
---

# my-dev-flow-v2-merge

Merge subflow of [`my-dev-flow-v2`](../my-dev-flow-v2/SKILL.md).

**Owns:** `merge` — load [`stages/merge.md`](stages/merge.md) only. Gate C ask is usually the **parent**.

| Topic | File |
|-------|------|
| Gate C / test bar | [`../my-dev-flow-v2/gate-c.md`](../my-dev-flow-v2/gate-c.md) |
| Consent / provenance | [`../my-dev-flow-v2/hitl.md`](../my-dev-flow-v2/hitl.md) |
| Preflight Merge | [`../my-dev-flow-v2/preflight.md`](../my-dev-flow-v2/preflight.md) |
| PR template | [`../my-dev-flow-v2/artifacts/pr-body.md`](../my-dev-flow-v2/artifacts/pr-body.md) |
| Results | [`../my-dev-flow-v2/results.md`](../my-dev-flow-v2/results.md) |

## Principles

- Gate C always **blocking**. Name each action: commit / push / PR / merge.
- Parent sets **Gate C approved** + provenance before launch.
- Never commit secrets; never force-push; do not skip hooks.
- Honor subsets (“PR only” → stop after PR). Result `success` \| `aborted`.
- Status `done` only when Result success **and** `merge` ∈ Gate C approved.

## Start

1. If Gate C not yet settled: paste [gate-c.md](../my-dev-flow-v2/gate-c.md) **Read before you decide**, ask named commit/push/PR/merge; parent sets **Gate C approved** + provenance.
2. Confirm Gate C bar or waiver+provenance; Gate C approved set.
3. Clarity-check Merge ([../my-dev-flow-v2-code/stages/clarity-check.md](../my-dev-flow-v2-code/stages/clarity-check.md#merge)); preflight Merge checks.
4. Compose handoff; run [`stages/merge.md`](stages/merge.md) for approved actions only.
