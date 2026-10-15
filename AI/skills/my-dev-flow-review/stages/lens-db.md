## lens-db — DB (when Lens plan includes db)

**Stage id:** `lens-db`  
**Skills:** `{database-and-data-model}/SKILL.md`  
**When:** Lens plan includes **db** (auto-added when Has DB = yes **unless** tiny-tweak — `{my-dev-flow}/lenses.md`).  
**Task description:** `Database review`

**Task prompt:**

```
You are a Senior Verifier for my-dev-flow-review Database Review. Fresh context only. You run in parallel with other lenses when present — write ONLY 05-lens-db.md; do not edit 05-review-log.md or other lens files. Do not fix code.

<Stage-scoped handoff for stage id lens-db from {my-dev-flow}/handoffs.md>

Read {database-and-data-model}/SKILL.md.
Also read 03-design.md Database contracts + example queries, 04-tasks.md, and the draft schema / migration / query / server persistence files.
Also read project AGENTS.md Database / Drizzle section when present.

Review that persistence follows best practices and matches the design contracts:

- Typed columns / nullability; indexes and uniques match real queries and idempotency
- Write owner + read owners respected in code paths
- Migrations additive or expand/contract; journal/meta consistent; backfill safe if present
- Safe SQL binds — prefer query builder / inArray / sql.join; no bad JS-array → ::type[]
- No bigint / SUM → ::int on money or large aggregates
- Lists bounded; no obvious N+1
- Tenant/ownership filters on mutating and sensitive reads
- Multi-step writes transactional or compensating
- Contract in 03-design matches schema + migrations + queries (and vice versa)

Write .my-docs/workflow/<slug>/05-lens-db.md using the lens template (Lens: db).
Fill the DB checklist table. Result = **needs fix** if any Critical/Major open; **clean** if none ({my-dev-flow}/results.md · severity.md).
Return FIRST LINE exactly: Result: clean | needs fix
Then path to 05-lens-db.md.
```
