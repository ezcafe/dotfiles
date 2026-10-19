---
name: my-dev-flow-v2-test
description: >-
  Supports smoke (E1 Mode full + profile full always Prefer unpaid independent
  Smoke before Adv; skip-review unpaid Prefer unpaid first — Build-writes-Smoke
  does not waive; lite paths may skip when Build-writes-Smoke smoke-pass),
  test-full (coverage + e2e + suite), and test-lite (targeted e2e). Use when the
  user says run my-dev-flow-v2-test, smoke re-run, or after review is clean
  before merge.
---

# my-dev-flow-v2-test

Test subflow of [`my-dev-flow-v2`](../my-dev-flow-v2/SKILL.md).

**Owned stages:** `smoke`, `test-full`, `test-lite` — load `stages/<id>.md` only.

| Topic | File |
|-------|------|
| Verify / Smoke | [`../my-dev-flow-v2/verify.md`](../my-dev-flow-v2/verify.md) |
| Gate C bar | [`../my-dev-flow-v2/gate-c.md`](../my-dev-flow-v2/gate-c.md) |
| skip-review | [`../my-dev-flow-v2/lenses.md`](../my-dev-flow-v2/lenses.md) |
| Handoffs | compose from [`../my-dev-flow-v2/handoffs.md`](../my-dev-flow-v2/handoffs.md) |
| Template | [`../my-dev-flow-v2/artifacts/06-test-log.md`](../my-dev-flow-v2/artifacts/06-test-log.md) |

## Principles

- Use Verify commands from `00-run.md`. Fast model.
- Mode full + profile full → independent Smoke before Adv (E1; Build-writes-Smoke never waives).
- skip-review unpaid → Prefer unpaid independent Smoke first; Build-writes-Smoke does **not** waive Prefer unpaid ([verify.md](../my-dev-flow-v2/verify.md)).
- Lite paths may skip Smoke when Build-writes-Smoke matching smoke-pass.
- Set **Test path last run:** `full` or `lite` on success.
- Fail → fix-tests → verify-pass → re-smoke / re-test. Max 3 → Decision N.

## Start

1. Confirm which stage (smoke / test-full / test-lite).
2. Compose handoff; run `stages/<id>.md`.
3. Parent advance by stage: **smoke-pass** → review (or skip-review Prefer paid → `merge` \| `gate-c`); **test-*** success → clear `test-stale` when Lite/full clear is met ([verify.md](../my-dev-flow-v2/verify.md) Stale), then Prefer `merge` \| `gate-c` only when **Tests success** ([derive-next.md](../my-dev-flow-v2/derive-next.md) · [derive-next-post.md](../my-dev-flow-v2/derive-next-post.md)); failure → Fix. Never “every success → Gate C”.
