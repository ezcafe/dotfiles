## db-design-review (0b) — DB design review (Verifier) — Medium — when Has DB

**When:** Mode **full** and (`00-run.md` **Has DB = yes**, or `03-design.md` defines new/changed Database contracts / migrations and Has DB is unknown — treat as yes), **unless** Notes `tiny-contract-tweak` (`{my-dev-flow-v2}/lenses.md` fold). Mode **simple** uses **design-verify-phase** instead.

**Parallel:** When Has API and Has DB are both yes (and not tiny-tweak): both **Isolated unpaid** (missing **or** Result unpaid/pending) → launch **api-contract-review** ∥ **db-design-review** in the **same** turn; resume Prefer only unpaid/pending sibling; Prefer re-run even if files exist. See [lenses.md](../../my-dev-flow-v2/lenses.md).

**Generation ≠ verification:** you did not write these contracts. Do not rewrite docs here.

**subagent_type:** `generalPurpose`  
**model:** resolved Medium (Fast if Medium unavailable)  
**Task description:** `DB design review`

**Done when:** `03a-db-design-review.md` has Result **clean** or **needs update**. Overall round stays **needs update** if this file is not clean. Do **not** require this file when Has DB = no or Notes `tiny-contract-tweak`.

**Task prompt:**

```
You are a Senior Database designer verifier for my-dev-flow-v2-design-review. Fresh context only. You did NOT author these design docs. Generation ≠ verification — find schema/migration/query gaps; do not rewrite 01–04 yourself.

<Paste output of: compose handoff from {my-dev-flow-v2}/handoffs.md for db-design-review>

Read {database-and-data-model}/SKILL.md.
Read 00-run.md, 02-analysis.md, 03-design.md (Database contracts + example queries + sequence), 04-tasks.md, and 02-skim.md if present.
Also read project AGENTS.md (Database / Drizzle section when present), docs/ARCHITECTURE.md, and existing db/schema + migration patterns when present.

Review database design against best practices:

- Schema contract: tables/columns typed; nullability/defaults clear
- Indexes / uniques match real filters, joins, and idempotency needs
- Write owner + read owners documented per table
- Migrations additive or expand→migrate→contract for breaks; backfill plan if needed
- Multi-step writes: transaction or compensating path
- Example queries use safe binds (no bad JS-array → ::type[]; prefer inArray / sql.join)
- Money/large aggregates stay bigint — no SUM → ::int
- Lists bounded; no obvious N+1 in the designed access path
- Tenant/ownership filters on mutating and sensitive reads
- Tasks include acceptance that would catch missing migration, wrong nullability, or missing unique
- Sequence diagram covers main DB reads/writes + key failure returns when DB is in scope

Write/update ONLY 03a-db-design-review.md (template: {my-dev-flow-v2}/artifacts/03a-db-design-review.md).

Rules:
- Clean only if zero Critical and Major ({my-dev-flow-v2}/severity.md). Defer Enhancement to Round notes.
- Simple plain words.
- Do not edit 01–04 or 03a-design-review-log.md. Do not write production code.
- Do not run the general design review or API contract review — those are separate Tasks.
- Re-entry: do **not** invent or bump **Round** — parent increments before re-launch (`{my-dev-flow-v2}/decisions.md`).

Return FIRST LINE exactly: Result: clean | needs update | skipped
Then short summary + path to 03a-db-design-review.md ({my-dev-flow-v2}/results.md).

**Result skipped** only when Has DB = no or Notes skip / `tiny-contract-tweak` — **never** invent an empty file to mark skipped.
```

**If needs update:** parent may run design Update for DB Fix ask items, then **parent bumps Round** and re-runs this stage before or with general design review (re-run isolated only when present and not tiny-tweak). Max 3 → Decision N (`{my-dev-flow-v2}/decisions.md`).

**If Has DB = no:** skip this stage — Notes skip only; **never** invent an empty `03a-db-design-review.md`.

**After:** clean → wait sibling `api-contract-review` if parallel unpaid → `design-review`. needs update → `design-update` → re-run this stage ([derive-next.md](../../my-dev-flow-v2/derive-next.md)).

---
