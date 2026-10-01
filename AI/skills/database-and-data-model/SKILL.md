---
name: database-and-data-model
description: >-
  Reviews and designs database schemas, migrations, and query interactions
  against data-model best practices. Use when changing tables, columns, indexes,
  migrations, ORM schemas (Drizzle), raw SQL, or write/read ownership. Use for
  isolated DB design review and code-time database lenses in my-plan-flow.
---

# Database and data model

Make schema and query changes safe, clear, and hard to misuse. Prefer repo
patterns (`AGENTS.md`, existing `db/schema`, migrations) before inventing new
shapes.

## Project first

1. Read `AGENTS.md` / `docs/ARCHITECTURE.md` when present.
2. Match existing schema style (naming, ids, timestamps, soft-delete vs hard).
3. Prefer the project ORM/query builder (e.g. Drizzle) over ad-hoc SQL unless
   the repo already uses raw SQL for that path.

## Boundaries

| Tier | Rule |
|------|------|
| **Always** | Contract tables/columns before code. Migrations additive when possible. Ownership and indexes called out. Validate untrusted input before it reaches SQL. |
| **Ask first** | Dropping columns/tables; renaming with downtime; changing PK/FK shape; backfills that lock large tables; new PII columns without retention note. |
| **Never** | Bind JS arrays as Postgres array params incorrectly. Cast money/`SUM` of bigint to `::int`. Check-then-act without a unique constraint or transaction. Ship destructive migrations without a rollback/expand-contract plan. |

## Core rules

### 1. Schema contract first

- Name tables/columns for the domain; match repo conventions.
- Every new/changed table in design: purpose, key fields + types, indexes/uniques, **write owner**, **read owners**.
- Prefer explicit nullability and defaults; avoid silent `any` / untyped raw rows.

### 2. Migrations are product changes

- **Expand → migrate → contract** for breaking renames/drops (add new, dual-write or backfill, then remove old).
- Prefer **additive** migrations (new nullable column, new table, new index `CONCURRENTLY` when required by ops).
- One logical change per migration when practical; journal/meta stays consistent with the ORM tool.
- Document data backfill: online vs offline, idempotent, and who owns it.

### 3. Integrity and concurrency

- Uniques for natural keys and idempotency keys (claim with one insert, not select-then-insert).
- FKs when the repo uses them; otherwise document why not.
- Multi-step writes: transaction or documented compensating path.
- Avoid lost updates: optimistic version, `UPDATE … WHERE`, or serializable where needed.

### 4. Indexes and query shape

- Index what filters/joins/order-by actually use; do not index every column.
- Lists: bounded (`LIMIT` / cursor / page); no unbounded `SELECT *` for user-facing lists.
- Watch N+1: batch with `inArray` / joins; do not query per row in a loop.
- Hot filters + sort: composite index order matches the query.

### 5. Types and money / aggregates

- Keep Postgres types honest in app code (e.g. **bigint** money/`*_minor` stays bigint — never `SUM(…)::int`).
- Timestamps: timezone policy matches the repo (timestamptz vs local).
- Enums / check constraints for closed sets when the repo pattern allows.

### 6. Safe SQL (ORM and raw)

- Prefer query builder (`eq`, `inArray`, …) over string-built SQL.
- Raw `sql` templates: only bind **scalars**; never `${ids}::uuid[]` for a JS array — use `inArray` or `sql.join` of scalars.
- No string concatenation of user input into SQL.
- `prepare: false` (or repo equivalent) — follow existing `db/index` setup; do not “fix” prepare without understanding the driver.

### 7. Access and tenancy

- Every read/write path states **who** may touch the row (workspace, user, role).
- Queries filter by ownership/tenant id; do not trust client-supplied ids alone.
- PII columns: minimize; note retention and logging risk.

### 8. Design ↔ code match

- `03-design.md` Database contracts and example queries must match migrations + schema + server queries (and vice versa).
- Tasks include acceptance that would catch missing migration, wrong nullability, or missing unique.

## Checklist (design + code)

- [ ] Tables/columns typed; nullability and defaults clear
- [ ] Indexes / uniques match real filters and idempotency needs
- [ ] Write owner + read owners documented
- [ ] Migration additive or expand/contract plan stated
- [ ] Backfill (if any) idempotent and bounded
- [ ] Multi-write paths transactional or compensating
- [ ] No unsafe array/`::type[]` binds; prefer `inArray` / `sql.join`
- [ ] No bigint/`SUM` → `::int` casts on money or large aggregates
- [ ] Lists bounded; no obvious N+1
- [ ] Tenant/ownership filter on mutating and sensitive reads
- [ ] Contract in design matches schema + queries

## Workflow hooks (my-plan-flow)

| When | Isolated Task | Writes |
|------|---------------|--------|
| **Has DB = yes** (design review) | DB design review | `03a-design-review-log.md` → **DB design review** section |
| **Has DB = yes** (code review) | Database lens (`db` in SPM plan) | `05-lens-db.md` only |

Do not fold deep DB checks into general design review or Quality alone.

## References

- Repo: `AGENTS.md` → Database / Drizzle (postgres.js) when present
- OWASP injection / access control: https://owasp.org/Top10/ (pair with security lens for authz/injection)
- Expand-contract migrations: industry standard for zero-downtime schema change
