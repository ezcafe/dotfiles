---
name: my-dev-flow-v3-test
description: >-
  Supports smoke (E1 / skip-review Prefer unpaid), test-full, and test-lite. Use
  when run my-dev-flow-v3-test or after review before merge.
---

# my-dev-flow-v3-test

## Start

1. Derive Expected Next.  
2. Smoke Task sets `Smoke source: Smoke-Task` only; parent owns Notes.  
3. On test-full/lite success: clear `test-stale` when Lite/full clear met; Prefer `merge`\|`gate-c` only when **Tests success** ([../my-dev-flow-v3/gate-c.md](../my-dev-flow-v3/gate-c.md)).

## Stages

| Id | File |
|----|------|
| smoke | [stages/smoke.md](stages/smoke.md) |
| test-full | [stages/test-full.md](stages/test-full.md) |
| test-lite | [stages/test-lite.md](stages/test-lite.md) |
