Copy into `.my-docs/workflow/<slug>/`. [handoffs.md](../handoffs.md) · [LEGACY.md](../LEGACY.md).

# 05-review-log.md

```markdown
# Review log: <short title>

**Round:** 1
<!-- File-top Round is SoT for max-round lint. Fix/re-review: parent increments Round — Task must not. -->
**Result:** pending | clean | needs fix
<!-- File-top Result is overall SoT. When section Results exist, lint uses worst-of (needs fix > pending > clean). -->

## Adversarial test review

| Severity | Location | Finding | Status |
|----------|----------|---------|--------|
| | | | open / fixed |

**Result:** pending | clean | needs fix

**Round notes:**

---

## Quality

| Severity | Location | Finding | Status |
|----------|----------|---------|--------|
| | | | |

**Result:** pending | clean | needs fix

**Round notes:**

---

## Merged lenses (API ‖ DB ‖ Security ‖ Performance ‖ Memory)

Filled by the **Merge findings** arbiter after each parallel round. Lens raw output lives in `05-lens-*.md` (only files for lenses in **Lens plan** this round).

**Result:** pending | clean | needs fix

### Winners (fix these)

| Severity | Sources (api/db/security/perf/memory) | Finding | Decision |
|----------|---------------------------------------|---------|----------|
| | | | keep / merged |

### Conflicts resolved (losers)

| Dropped / demoted finding | Lost to | Why |
|---------------------------|---------|-----|
| | | |

### Fix ask (for Fix agent)

1.
2.

**Round notes:**

---

## Deferred (Enhancements — do not block clean)

Optional polish / Enhancements logged but not in Fix ask:

-

---

## Fix notes (TDD skipped)

List any docs-only items where TDD was skipped:
```

---

## Lens files

Per-lens templates: [05-lens.md](05-lens.md) → write `05-lens-api.md`,
`05-lens-db.md`, `05-lens-security.md`, `05-lens-performance.md`, or
`05-lens-memory.md` for the active Lens plan only.

---
