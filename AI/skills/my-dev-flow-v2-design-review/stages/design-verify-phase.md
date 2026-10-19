## design-verify-phase (0s) — Design verify phase (Verifier) — Fast|Medium — Mode **simple** only

**When:** Mode **simple**. One Task replaces isolated API/DB + general design-review. Mode **full** uses **api-contract-review** / **db-design-review** / **design-review** instead.

**subagent_type:** `generalPurpose`  
**model:** Fast preferred (Fast-on-simple); else Medium  
**Task description:** `Design verify phase`

**Done when:** Overall **clean** | **needs update** (same clean rule as SKILL.md). When Has API/DB = **yes** and Notes ≠ `tiny-contract-tweak`, matching `03a-api-contract-review.md` / `03a-db-design-review.md` **must** be written and Result **clean** — missing file ≠ skipped. When Has = no or Notes `tiny-contract-tweak`, treat as Notes-skip only (do not invent empty files).

**Task prompt:**

```
You are the design verifier for my-dev-flow-v2-design-review **design-verify-phase** (Mode simple). Fresh context only. Generation ≠ verification — you did NOT author 01–04. Do not rewrite 01–04. Do not write production code.

<Paste output of: compose handoff from {my-dev-flow-v2}/handoffs.md for design-verify-phase>

Read 00-run.md (Has API/DB), 01-idea, 02-analysis, 02b (if present), 03-design, 04-tasks, 02-skim (if present).

### If Has API = yes
- Notes `tiny-contract-tweak`: Notes-skip only — do **not** write `03a-api-contract-review.md`; fold light API checks into the general log below. Treat API as **skipped** for overall clean.
- Else: write 03a-api-contract-review.md using the API contract checklist from stage api-contract-review / {api-and-interface-design}. Result clean | needs update.
If Has API = no: Notes skip only — do not invent an empty API file. Treat as **skipped**.

### If Has DB = yes
- Notes `tiny-contract-tweak`: Notes-skip only — do **not** write `03a-db-design-review.md`; fold light DB checks into the general log below. Treat DB as **skipped** for overall clean.
- Else: write 03a-db-design-review.md using the DB checklist from stage db-design-review / {database-and-data-model}. Result clean | needs update.
If Has DB = no: Notes skip only — do not invent an empty DB file. Treat as **skipped**.

### Always
Write 03a-design-review-log.md using the general design-review checklist from stage design-review (gaps, System design, patterns, OWASP light). If API/DB isolated files exist, do not deep-duplicate those checks — point to them. Overall clean only if zero Critical/Major **and** API/DB are **clean|skipped** when required (skipped = Has no Notes-only, or Notes `tiny-contract-tweak`; Has yes not tiny → isolated file Result clean — never invent empty files) ({my-dev-flow-v2}/severity.md).

**Grill (Mode simple — same bar as Mode full):** Fail **Major** if `02b-grill.md` Result is **`needs-round`**, or Build-critical open frontier remains, or Design re-opens Settled grill decisions without new evidence. Notes grill-skip / Result **`skipped`** OK when frontier was empty. Do **not** overall-clean while Grill is open ({my-dev-flow-v2}/grill.md · {my-dev-flow-v2}/derive-next.md).

On re-entry after Update: do **not** invent or bump **Round** — parent increments before re-launch (`{my-dev-flow-v2}/decisions.md`).

### If Has UI = yes (Mode simple — thin UI-alignment; not full Gate A)
In the general log, add a short **UI alignment** subsection (fail Major on drift):
- Design `03` UI section present (not N/A) + Build↔UI lock stated
- Important info/action #1 and #2 named (from Design or thin idea) — do **not** re-litigate 80/20 goals
- Layout / chrome match existing app patterns called out in Design
If Has UI = no: skip this subsection.

Return FIRST LINE exactly: Result: clean | needs update
Then short summary + paths to 03a files written ({my-dev-flow-v2}/results.md).
```

**After:** needs update → design Update → **parent bumps Round** (+ Run metrics) before re-launch ([decisions.md](../../my-dev-flow-v2/decisions.md)) → re-run this stage (max 3 → Decision N in `{my-dev-flow-v2}/decisions.md`). **If clean:** parent continues (TDD → Gate B → Build). E1 independent Smoke: **N/A** (Mode simple). Lens plan: may set **api**/**db** now when Has API/DB and **not** tiny-tweak; parent **must** finalize Lens plan api/db per [lenses.md](../../my-dev-flow-v2/lenses.md) **before code review** (may set earlier before Gate B).

---
