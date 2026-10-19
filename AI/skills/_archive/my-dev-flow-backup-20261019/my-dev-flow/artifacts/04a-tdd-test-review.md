Copy into `.my-docs/workflow/<slug>/`. [handoffs.md](../handoffs.md) · [LEGACY.md](../LEGACY.md).

# 04a-tdd-test-review.md

**Only create when** `04-tasks.md` has planned test cases. If none → skip; note in `00-run.md` (`04a skipped — no planned test cases`).

```markdown
# TDD test-case review: <slug>

**Result:** pending | clean | needs more tests
**Round:** 1
**Updated:**

## Planned / existing test cases reviewed

| Task | Scenario type (real / edge) | Test case | Covered? |
|------|-----------------------------|-----------|----------|
| | | | yes / no / partial |

## Gaps (must add before or during Build)

| Severity | Task | Missing scenario | Suggested test |
|----------|------|------------------|----------------|
| Critical / Major / Enhancement | | | |

## Real scenarios checked

- Happy path:
- User-visible failures:
- Empty / loading / permission:

## Edge scenarios checked

- Boundaries / invalid input:
- Concurrency / double-submit / idempotency:
- Offline / partial data / race (if relevant):

## Fix ask for Build

Concrete tests to add or strengthen:

1.
2.

## Round notes

-
```

---
