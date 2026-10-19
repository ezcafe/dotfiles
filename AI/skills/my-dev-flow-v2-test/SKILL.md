---
name: my-dev-flow-v2-test
description: >-
  Supports smoke (Mode full + profile full requires independent Smoke before
  Adv; other paths usually skip when Build-writes-Smoke smoke-pass), test-full
  (coverage + e2e + suite), and test-lite (targeted e2e). Use when the user says
  run my-dev-flow-v2-test, smoke re-run, or after review is clean before merge.
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
- Mode full + profile full → independent Smoke before Adv.
- Set **Test path last run:** `full` or `lite` on success.
- Fail → fix-tests → verify-pass → re-smoke / re-test. Max 3 → Decision N.

## Start

1. Confirm which stage (smoke / test-full / test-lite).
2. Compose handoff; run `stages/<id>.md`.
3. Parent advance by stage: **smoke-pass** → review (or skip-review Prefer → Gate C); **test-*** success → Gate C; failure → Fix. Never “every success → Gate C”.
