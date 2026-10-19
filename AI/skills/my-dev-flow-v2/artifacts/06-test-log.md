Copy into `.my-docs/workflow/<slug>/`. [handoffs.md](../handoffs.md) · [CUTOVER.md](../CUTOVER.md) · [verify.md](../verify.md) · [hitl.md](../hitl.md).

Gate C (full|lite): when Result is **success**, **Test path last run** must be `full` or `lite` matching Review profile — missing → fail closed. Also unpaid stale Notes cleared (`review-stale` / `test-stale`) — [gate-c.md](../gate-c.md) Test bar. LEGACY alias: **Mode last run** ([CUTOVER.md](../CUTOVER.md)).

Gate C (**skip-review**): require independent Smoke per [verify.md](../verify.md) Independent Smoke (SoT) **and** escape Notes↔provenance **and** unpaid stale Notes cleared (`review-stale` N/A cleared; `test-stale` cleared) ([gate-c.md](../gate-c.md)).

**Who writes Smoke source:**
- Build on verify-pass → `Build-verify` (Build-writes-Smoke).
- Independent Smoke Task on smoke-pass → `Smoke-Task`.
- Seed / unpaid → `pending`.

# 06-test-log.md

```markdown
# Test log: <slug>

**Result:** pending | smoke-pass | smoke-fail | success | failure
**Test path last run:** smoke | full | lite
<!-- LEGACY accept: Mode last run -->
**Round:** 1
**Updated:**
**Smoke source:** Build-verify | Smoke-Task | pending
<!-- Build → Build-verify; Smoke Task → Smoke-Task; skip-review Gate C: Smoke-Task required; Notes smoke-pass (re-run) = companion only (verify.md SoT) -->

## Smoke (build + unit — usually written by Build on verify-pass)

Use Verify commands from `00-run.md`.

| Step | Command | Exit | Notes |
|------|---------|------|-------|
| Build | | | |
| Unit | | | N/A if no unit suite |

**Smoke result:** pending | smoke-pass | smoke-fail

## Coverage (full mode only)

Map design success criteria / main flows → e2e.

| Criterion / flow | E2E file / test | Status (covered / MISSING / blocked) |
|------------------|-----------------|----------------------------------------|
| | | |

**E2E stack:** (playwright / cypress / none / …)
**E2E command:** (from Verify commands e2e when set)

## Runs (full / lite mode)

| Step | Command | Exit | Notes |
|------|---------|------|-------|
| Build | | | |
| Unit | | | |
| E2E | | | |

## Failures (if any)

For each failure:

- **What:**
- **Where:** file / test name
- **Excerpt:** short
- **Tied to requirement:** (design / task id)

## Fix ask for my-dev-flow-v2-code

Concrete work so the next smoke or full round can pass (aligned with 03-design.md / 04-tasks.md):

1.
2.

## Round notes

-
```

---
