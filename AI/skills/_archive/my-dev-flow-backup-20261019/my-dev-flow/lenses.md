# Has API / Has DB + Lens plan

Canonical contract flags and code-review lenses for [`my-dev-flow`](SKILL.md).  
**This file is SoT for:** Has API/DB, tiny-tweak, Lens plan, skip-review ban.  
Other files **link here** — do not restate these rules elsewhere.  
Pipeline order: [stages.md](stages.md). Resume aliases: [LEGACY.md](LEGACY.md).

## Has API / Has DB (force yes|no before design-review)

Set during Analyze/Design (or earlier if obvious). **Before design-review**, parent must set **yes|no** (not unknown):

- Unknown + Design has API contracts / public handlers → **Has API = yes**
- Unknown + Design has DB contracts / migrations / persistence writes → **Has DB = yes**
- Else → **no**

| Flag | Yes when | When yes, parent must |
|------|----------|------------------------|
| **Has API** | New/changed REST/GraphQL/routes/server actions, edge validators, cross-boundary public types | Full: isolated **API contract review** Task (∥ DB when both), **unless** [tiny tweak](#tiny-apidb-tweak). Simple: include in **design-verify-phase**. Include **api** in Lens plan (unless Notes fold into Quality / code-review-phase) |
| **Has DB** | New/changed tables/columns/indexes/migrations/ORM, notable writes/transactions/raw SQL | Full: isolated **DB design review** Task (∥ API when both), **unless** tiny tweak. Simple: include in **design-verify-phase**. Include **db** in Lens plan (unless Notes fold into Quality / code-review-phase) |

Independent flags. Skills: `{api-and-interface-design}`, `{database-and-data-model}` — resolve per [skills-path.md](skills-path.md) (`~/.cursor/skills` or `AI/skills`; not necessarily under this tree).

### API/DB Mode rule (hard) — skip-review ban

When **Has API = yes** or **Has DB = yes**:

1. Always set the flag(s) **yes** (do not leave unknown).
2. **Never** keep Review profile **`skip-review`**. Legal skip-review → Gate C is **Mode simple only** ([stages.md](stages.md)). Mid-run flip → Decision N reclassify; drop skip-review. Before Gate C under legal skip-review: **require** Notes `smoke-waive` / `smoke-pass (re-run)` / `gate-c-test-override` / Complexity/Notes `docs-only` **each with matching provenance** — else lint `--before-merge` **errors** (fail-closed; [verify-and-fix.md](verify-and-fix.md) · [hitl.md](hitl.md)).
3. Mode may stay **simple** only if [tiny tweak](#tiny-apidb-tweak) criteria all hold (Notes fold into Quality / code-review-phase; design-verify-phase covers contracts). Otherwise prefer **full** (or Decision N).
4. Lint: `scripts/lint-run.py <run-dir>` errors on skip-review + Has API/DB yes on **default lint** (when profile is skip-review), and via `--before-build` / `--before-design-review` / `--check-skip-review`.
5. Mode **full** + both Has API and Has DB **yes** (not tiny tweak): set **Pending parallel:** `api|db` until both isolated `03a-*` exist, then `none` ([artifacts/00-run.md](artifacts/00-run.md); lint `--before-design-review`). Derive emits parallel hint when both `03a-*` missing; serializes only when one exists (resume).
6. Mode **full** + single Has API or Has DB **yes** (not tiny): Pending parallel stays `none`, but derive still requires the matching `03a-*` before general design-review; lint `--before-design-review` errors when that file is missing (unless Next is the matching isolated stage).
7. Before code review: Lens plan must include **api** / **db** when the matching Has flag is yes (unless Notes fold into Quality / code-review-phase — e.g. `tiny-contract-tweak`). Lint: `--before-code-review` (also auto when card Next is `adversarial` or `code-review-phase`).
8. After review clean: if Lens plan ≠ `none`, matching `05-lens-*.md` must be **clean** (and **merge-findings** when 2+) before test / Gate C. `--next` prefers `do-not-launch` on test/merge when unpaid.

### Tiny API/DB tweak

When **all** are true, parent may fold contract checks (no isolated API/DB Task; no forced api/db lens) — Mode **full** or **simple**:

- Change is one field / one column / one validator / docs-only contract note
- No new auth, PII, or cross-service boundary
- Blast radius stays inside one package
- Notes: `tiny-contract-tweak — Notes fold into Quality / code-review-phase`

Otherwise: Mode **full** → isolated API∥DB + forced lenses; Mode **simple** → API/DB inside **design-verify-phase** + Lens plan api/db (unless tiny tweak).

**Never invent** empty `03a-api-contract-review.md` / `03a-db-design-review.md` when skipped or tiny-tweak — [handoffs.md](handoffs.md).

## Conditional lenses / Lens plan

Before code review, set **Lens plan** in `00-run.md`. Launch only matching lenses.

**Default: `none`.** Start with **none**. Add a lens only when a signal below is clearly true (or Has API / Has DB forces api/db, except tiny tweak). Do not pre-load security/perf/memory “just in case.”

**Auto-add api/db:** Parent adds **api** / **db** to Lens plan only when Has API/DB = yes **and** none of: (1) Notes fold into Quality / code-review-phase (e.g. `tiny-contract-tweak`), (2) Lens plan already records that fold. Finalize Lens plan before code review; may draft api/db at design-review clean.

| Lens | Stage id | Launch when |
|------|----------|-------------|
| **API** | `lens-api` | Has API = yes (not tiny tweak), or new/changed public contracts / edge validators |
| **DB** | `lens-db` | Has DB = yes (not tiny tweak), or new/changed schema/migrations/persistence queries |
| **Security** | `lens-security` | auth, sessions, PII, uploads, SQL/raw, secrets, permissions |
| **Performance** | `lens-perf` | lists/tables, charts, fetch, bundle-sensitive UI, heavy client compute |
| **Memory** | `lens-memory` | subscriptions, large client caches, websockets/realtime, media buffers |

- **none** → after Quality / Lite combined clean, skip lenses → test per Review profile
- **api/db when Lens plan includes them (not tiny-tweak)** → always **isolated** Tasks (even under lite; even if only one lens). Do not fold contract checks into Quality / code-review-phase.
- **lite + tiny-tweak** → fold API/DB contract checks into `code-review-phase` (no forced api/db lens)
- **1 non-api/db lens** (e.g. security) → that lens only; under lite may run inside `code-review-phase` when practical; parent copies Result (`clean` \| `needs fix`) into Merged lenses (no Merge Task; [results.md](results.md))
- **2+ lenses** → **must** launch in parallel (after Lite combined when profile lite) → Merge findings Task

API lens → `05-lens-api.md`. DB lens → `05-lens-db.md`.

## TDD test-case review (Step 4a)

Run `04a` **only if** `04-tasks.md` lists concrete tests to create. Else Notes `04a skipped — no planned test cases`; do not invent `04a`.

**Derive:** after design-review / design-verify-phase **clean**, `--next --derive` returns `tdd-review` until `04a-tdd-test-review.md` exists **or** Notes have `04a skipped`; then `gate-b` / `build`.
