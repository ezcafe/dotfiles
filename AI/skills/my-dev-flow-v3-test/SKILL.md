---
name: my-dev-flow-v3-test
description: >-
  Supports smoke (E1 / skip-review Prefer unpaid), test-full, and test-lite. Use
  when run my-dev-flow-v3-test or after review before merge.
---

# my-dev-flow-v3-test

## Solo FIRST

1. Min card: Mode, profile, Has flags, settle gen, Last Verify on `00-run.md`.  
2. Unpaid bans: E1 / skip-review Prefer unpaid independent Smoke (`Smoke source: Smoke-Task`); Build-writes-Smoke does not waive. Smoke fail → Prefer `fix-tests` first (Prefer-re-smoke only after fix-tests + verify-pass) — Mode×profile [../my-dev-flow-v3/stages.md](../my-dev-flow-v3/stages.md) · [stages/smoke.md](stages/smoke.md). Smoke FIRST leads with **missing required api/db**; test-full/lite FIRST order: (1) **missing required api/db** → (2) **Lenses dirty** / ¬ **Lenses clean** → (3) ¬ **Review clean** → `Result: blocked — …` (same FIRST on [stages/smoke.md](stages/smoke.md) · [stages/test-full.md](stages/test-full.md) · [stages/test-lite.md](stages/test-lite.md) — Prefer [../my-dev-flow-v3/derive-next-post.md](../my-dev-flow-v3/derive-next-post.md) · [../my-dev-flow-v3/preflight.md](../my-dev-flow-v3/preflight.md)).
3. Parent-only ([../my-dev-flow-v3/hitl.md](../my-dev-flow-v3/hitl.md)): never write escape Notes (`smoke-pass`, alias `smoke-pass (re-run)`, …) or provenance, **lifecycle Notes** (`design-stale` / `design-backloop` / `review-stale` / `test-stale` / `waiting — <reason>`), or **card Has** — Task sets Smoke source only; Stages return `candidate …` only.  
4. Derive Next: Prefer first-match SoT = parent [../my-dev-flow-v3/derive-next-post.md](../my-dev-flow-v3/derive-next-post.md) (+ [../my-dev-flow-v3/derive-next.md](../my-dev-flow-v3/derive-next.md) Definitions / Unsafe jumps). Local [stages.md](stages.md) = **negative guards only** — not Prefer Next lookup.  
5. Solo entry: [../my-dev-flow-v3/solo-entry.md](../my-dev-flow-v3/solo-entry.md).

## Start

1. Derive Expected Next.  
2. Smoke Task sets `Smoke source: Smoke-Task` only; parent owns Notes.  
3. On test-full/lite success: return `candidate clear test-stale` when Lite/full clear met (parent clears); Prefer `merge`\|`gate-c` only when **Tests success** **and** **Lenses clean** ([../my-dev-flow-v3/gate-c.md](../my-dev-flow-v3/gate-c.md) · [../my-dev-flow-v3/derive-next-post.md](../my-dev-flow-v3/derive-next-post.md)).

## Stages

| Id | File |
|----|------|
| smoke | [stages/smoke.md](stages/smoke.md) |
| test-full | [stages/test-full.md](stages/test-full.md) |
| test-lite | [stages/test-lite.md](stages/test-lite.md) |
