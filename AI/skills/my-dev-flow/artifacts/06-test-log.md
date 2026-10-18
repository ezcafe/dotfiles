Copy into `.my-docs/workflow/<slug>/`. [handoffs.md](../handoffs.md) · [LEGACY.md](../LEGACY.md) · [verify-and-fix.md](../verify-and-fix.md) · [hitl.md](../hitl.md).

Gate C (full|lite): when Result is **success**, **Test path last run** must be `full` or `lite` matching Review profile — missing → fail closed. LEGACY alias: **Mode last run** ([LEGACY.md](../LEGACY.md)).

# 06-test-log.md

```markdown
# Test log: <slug>

**Result:** pending | smoke-pass | smoke-fail | success | failure
**Test path last run:** smoke | full | lite
<!-- LEGACY accept: Mode last run -->
**Round:** 1
**Updated:**
**Smoke source:** Build-verify | Smoke-Task | pending

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

## Fix ask for my-dev-flow-code

Concrete work so the next smoke or full round can pass (aligned with 03-design.md / 04-tasks.md):

1.
2.

## Round notes

-
```

---
