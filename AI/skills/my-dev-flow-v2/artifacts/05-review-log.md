Copy into `.my-docs/workflow/<slug>/`. [handoffs.md](../handoffs.md) · [CUTOVER.md](../CUTOVER.md).

# 05-review-log.md

```markdown
# Review log: <short title>

**Round:** 1
<!-- File-top Round is SoT for max-round Decision N ([decisions.md](../decisions.md)). Fix/re-review: parent increments Round — Task must not. -->
**Result:** pending | clean | needs fix
<!-- File-top Result is optional convenience — not required for resume. Do **not** equate file-top / **overall Result** with **Review clean**. **Review clean** = Adv + Quality section Results both `clean` (full and lite — no file-top fallback; lenses not required). **code-review unpaid** when Adv/Quality section Result missing/`pending` (Result-bearing bar — [derive-next.md](../derive-next.md)). **overall Result** = worst-of required sections (needs fix > pending > clean): Adv + Quality, and Merged when Lens plan 2+ is in scope. Profile full: Adv/Quality write section Results only — file-top may stay pending until merge-findings (plan 2+) or indefinitely if plan none/1; do not stall on file-top when Adv+Quality are clean. Profile lite: code-review-phase should set Adv+Quality section Results (and may set file-top to match; file-top alone never pays Review clean). After fix-review verify-pass, Prefer re-runs dirty verifier first (full: Adv/Quality; lite: code-review-phase; Mode merged-lenses | plan-1-lens → mark lenses unpaid → re-lens → merge-findings if 2+); already clean → continue table — [derive-next.md](../derive-next.md). -->

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
`05-lens-db.md`, `05-lens-security.md`, `05-lens-perf.md`, or
`05-lens-memory.md` for the active Lens plan only.

---
