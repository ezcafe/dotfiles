Copy into `.my-docs/workflow/<slug>/` as `05-lens-<name>.md` for the active lens.
See [INDEX.md](INDEX.md) · [severity.md](../severity.md) · [LEGACY.md](../LEGACY.md).

# 05-lens.md

One file per parallel lens per round (overwrite each round). Do **not** edit
`05-review-log.md` from lens Tasks — Merge findings copies winners later.

```markdown
# Lens: <api | db | security | performance | memory> — <slug>

**Result:** pending | clean | has findings
**Round:** 1
**Updated:**

## Findings

| Id | Severity | Location | Finding | Suggestion |
|----|----------|----------|---------|------------|
| A1 / D1 / S1 / P1 / M1 | Critical / Major / Enhancement / Nit | file:line | | |

## API checklist (api lens only)

| Check | Status (pass / fail / N/A) | Note |
|-------|----------------------------|------|
| Typed input/output | | |
| One error format | | |
| Validate at edges only | | |
| Lists paginated | | |
| Additive fields / no silent breaks | | |
| Naming matches repo | | |
| Idempotency for mutating endpoints | | |
| Contract matches `03-design.md` | | |

Skill: `api-and-interface-design`

## DB checklist (db lens only)

| Check | Status (pass / fail / N/A) | Note |
|-------|----------------------------|------|
| Typed columns / nullability | | |
| Indexes / uniques match queries | | |
| Write owner + read owners | | |
| Migration additive or expand/contract | | |
| Safe SQL binds (`inArray` / no bad `::type[]`) | | |
| No bigint/`SUM` → `::int` on money/large aggregates | | |
| Lists bounded; no obvious N+1 | | |
| Tenant/ownership filters | | |
| Contract matches schema + queries | | |

Skill: `database-and-data-model`

## OWASP coverage (security lens only)

| OWASP | Status (pass / fail / N/A) | Note |
|-------|----------------------------|------|
| A01 | | |
| A02 | | |
| A03 | | |
| A04 | | |
| A05 | | |
| A06 | | |
| A07 | | |
| A08 | | |
| A09 | | |
| A10 | | |

Source: https://owasp.org/Top10/

## Round notes

-
```
