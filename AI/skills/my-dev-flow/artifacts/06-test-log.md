Copy into `.my-docs/workflow/<slug>/`. [handoffs.md](../handoffs.md) · [LEGACY.md](../LEGACY.md).

# 06-test-log.md

```markdown
# Test log: <slug>

**Result:** pending | smoke-pass | smoke-fail | success | failure
**Mode last run:** smoke | full
**Round:** 1
**Updated:**

## Smoke (build + unit only — before code review)

| Step | Command | Exit | Notes |
|------|---------|------|-------|
| Build | | | |
| Unit | | | |

**Smoke result:** pending | smoke-pass | smoke-fail

## Coverage (full mode only)

Map design success criteria / main flows → e2e.

| Criterion / flow | E2E file / test | Status (covered / MISSING / blocked) |
|------------------|-----------------|----------------------------------------|
| | | |

**E2E stack:** (playwright / cypress / none / …)
**E2E command:**

## Runs (full mode)

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
