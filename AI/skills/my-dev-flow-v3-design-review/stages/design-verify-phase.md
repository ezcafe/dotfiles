# Design-verify-phase (Mode simple)

**Stage id:** `design-verify-phase`  
**When:** Mode **simple**. One Task replaces isolated API/DB Prefer stages + general design-review. Mode **full** uses `api-contract-review` / `db-design-review` / `design-review` instead. Isolated write duty when Has API/DB ∈ {yes, unknown} ∧ ¬tiny — same as Mode-full Isolated Prefer.  
**Skills:** same checklists as Isolated + general design-review; fold light API/DB only when Notes `tiny-contract-tweak` ([../../my-dev-flow-v3/lenses.md](../../my-dev-flow-v3/lenses.md)).

**Done when:** Overall `03a-design-review-log.md` Result **`clean`** only (for advance / Design clean / Verify clean). Writing **`needs update`** is **allowed** ≠ Done — unpaid under **design-update unpaid** ([../../my-dev-flow-v3/derive-next-defs-pre.md](../../my-dev-flow-v3/derive-next-defs-pre.md) · [design-review.md](design-review.md) · [../../my-dev-flow-v3/results.md](../../my-dev-flow-v3/results.md)).

| Has / Notes | Isolated write duty |
|-------------|---------------------|
| Has API ∈ {**yes**, **unknown**} and Notes ≠ `tiny-contract-tweak` | **Must** write `03a-api-contract-review.md` with Result **`clean`** \| **`needs update`**. Missing file ≠ skipped. |
| Has DB ∈ {**yes**, **unknown**} and Notes ≠ `tiny-contract-tweak` | **Must** write `03a-db-design-review.md` with Result **`clean`** \| **`needs update`**. Missing file ≠ skipped. |
| Has API/DB = **no**, or Notes `tiny-contract-tweak` | **Notes-skip only** — do **not** invent empty Isolated files. Treat that surface as **`skipped`** for overall clean. (`unknown` ≠ skip.) |

**Design clean / Verify clean** (Mode simple ≡): overall **`clean`** **and** required Isolated paid (`clean`\|`skipped`). This stage **pays** required Isolated when Has ∈ {yes, unknown} (not tiny) — never launch Isolated Prefer stages under Mode simple ([../../my-dev-flow-v3/derive-next.md](../../my-dev-flow-v3/derive-next.md)).

**Allowed Results** (FIRST LINE of overall `03a-design-review-log.md`): `clean` \| `needs update` \| `pending` — **Advance-on-clean** (Done when = `clean` only); writing **`needs update`** allowed ≠ Done — Hard stop; parent re-derives ([../../my-dev-flow-v3/derive-next-defs-pre.md](../../my-dev-flow-v3/derive-next-defs-pre.md)).

## FIRST

1. ¬ **Design present** → `Result: blocked — Design not present` — **Hard stop**; parent re-derives ([../../my-dev-flow-v3/derive-next.md](../../my-dev-flow-v3/derive-next.md) · [../../my-dev-flow-v3/handoffs.md](../../my-dev-flow-v3/handoffs.md)).  
2. **Grill open** → `Result: blocked — Grill open` (fail-closed — do **not** launch while Grill unsettled; Mid-task Grill soft-fail Major below may remain) ([../../my-dev-flow-v3/grill.md](../../my-dev-flow-v3/grill.md) · [../../my-dev-flow-v3/derive-next.md](../../my-dev-flow-v3/derive-next.md) unsafe jumps).  
3. Notes `design-stale` → `Result: blocked — design-stale` ([../../my-dev-flow-v3/derive-next.md](../../my-dev-flow-v3/derive-next.md) unsafe jumps).  
4. **design-update unpaid** → `Result: blocked — design-update unpaid` ([../../my-dev-flow-v3/derive-next.md](../../my-dev-flow-v3/derive-next.md) · [../../my-dev-flow-v3/handoffs.md](../../my-dev-flow-v3/handoffs.md)).  
5. Else proceed.

**Task duties (summary):**

1. Read `00-run` (Has flags), `01-idea`, `02-analysis` / `02b` if present, `03-design`, `04-tasks`, skim if present.  
2. If Has API ∈ {yes, unknown} (not tiny): write Isolated API file + Result. If Has API no or tiny: Notes-skip only.  
3. If Has DB ∈ {yes, unknown} (not tiny): write Isolated DB file + Result. If Has DB no or tiny: Notes-skip only.  
4. Always write overall `03a-design-review-log.md`. Overall **clean** only if zero Critical/Major **and** API/DB **`clean`\|`skipped`** when required.  
5. Grill bar (Mode simple = Mode full): fail Major if Grill open / Build-critical frontier open ([../../my-dev-flow-v3/grill.md](../../my-dev-flow-v3/grill.md)).  
6. Return FIRST LINE: `Result: clean | needs update` + paths to `03a*` written.

**After:** Return Result → **Hard stop** — do **not** Prefer Next. Parent bumps Round / pays Run-log after `design-update` Task complete / re-derives ([../../my-dev-flow-v3/design-backloop.md](../../my-dev-flow-v3/design-backloop.md) · [../../my-dev-flow-v3/preflight.md](../../my-dev-flow-v3/preflight.md) Always §8 · [../../my-dev-flow-v3/derive-next-pre.md](../../my-dev-flow-v3/derive-next-pre.md) · [../../my-dev-flow-v3/derive-next-post.md](../../my-dev-flow-v3/derive-next-post.md)). Not a Pre-Build duty after this stage.

Never write Gate B consent.
