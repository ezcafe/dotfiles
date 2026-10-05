Copy into `.my-docs/workflow/<slug>/`. [handoffs.md](../handoffs.md) · [LEGACY.md](../LEGACY.md).

# 02b-grill.md

```markdown
# Grill: <slug>

**Result:** frontier-empty | needs-round | skipped
**Updated:**
**HITL:** auto | async-notify | blocking — from Gate B tier; prefer auto
**Size:** ≤ ~60 lines

## Design tree summary

- **Settled:** …
- **Open frontier:** … (empty when Result frontier-empty)
- **Blocked:** …

## Frontier round N

❓ **Q1** — **<title>**: <body; choices if 2+>

➡️ Recommended: … — user-first: …

**Settled as:** … (auto-pick | human) — rationale: …

---

❓ **Q2** — …

## Edge scenarios

| Scenario | Outcome / rule locked |
|----------|------------------------|
| | |

## Domain modeling

### Glossary updates
- Term → definition (or `none this round`)
- Paths touched: `GLOSSARY.md` | mapped context | none

### ADR
- **Wrote:** path — or **Skipped:** reason (fails three-part bar / obvious / easy to reverse)

## Auto-pick log

- `auto-pick — Qn → … — user-first: …; system: …`

## Grill digest (≤4 bullets)

1. What settled
2. Top residual risk (or none)
3. Glossary / ADR touch
4. Ready for Design? yes/no
```

---
