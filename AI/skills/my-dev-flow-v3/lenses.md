# Has flags / Lens plan / skip-review

## Has flags

`Has UI` · `Has API` · `Has DB` · `Has auth/PII/schema` — each `yes` \| `no` \| `unknown`.

**`unknown` ≠ `no` (fail-closed) — split SoT:**

| Concern | Predicate | Auth SoT |
|---------|-----------|----------|
| **Gate B auto** (Mode simple) | API=no ∧ DB=no ∧ auth/PII/schema=no (explicit `no` only) | [gate-b.md](gate-b.md) — **Has UI not in Gate B auto predicate** |
| **skip-review** legality | Has UI=no ∧ Has API=no ∧ Has DB=no ∧ Has auth/PII/schema=no | this file § skip-review |

When API **or** DB **or** auth/PII/schema is `unknown` (or **yes**): Gate B **blocking**. Has UI=`unknown` \| `yes` fail-closes **skip-review only** — does **not** alone force Gate B blocking / deny Gate B auto. Treat API/DB `unknown` like unpaid Isolated / required surface until resolved to `yes`\|`no` (same Prefer duties as Has=yes for that surface — **Design clean** / **Isolated unpaid** use `Has ∈ {yes, unknown}`).

**Who writes card Has (parent-only / labeled solo carve):** **Orchestrated Task:** return `proposed Has: UI=… API=… DB=… auth/PII/schema=…` (and `Has flip detected` when a flip applies) only — parent writes Has on `00-run.md` via [preflight.md](preflight.md) Always §4. **Labeled solo:** stamps Has when acting as orchestrator ([solo-entry.md](solo-entry.md) · [hitl.md](hitl.md)).

**`unknown` → `no` (resolve, not flip):** Parent **or** labeled solo (acting as orchestrator) writes card Has=`no` for that flag ([solo-entry.md](solo-entry.md) · [hitl.md](hitl.md)). **Do not** bump Gate B settle gen (no `has-flip` — flip is only toward **yes**). Same turn: re-derive Isolated unpaid / Design clean (that surface → N/A `skipped` without file) and skip-review legality (all UI/API/DB/auth explicit `no` may unlock skip-review) and Gate B tier (API=DB=auth explicit `no` may unlock Gate B auto when Mode simple — [gate-b.md](gate-b.md); Has UI not required for auto).

## Tiny / Notes `tiny-contract-tweak`

**All** must hold before the Note pays a skip:

- One field / column / validator / docs-only contract note  
- No new auth, PII, or cross-service boundary  
- Blast radius one package  

**Who writes:** **Parent** after Parent-relay **or** labeled solo after AskQuestion ([hitl.md](hitl.md) · [solo-entry.md](solo-entry.md)). Design / design-phase / design-update **After** returns `candidate tiny-contract-tweak` (orchestrated) — Tasks must **not** invent the Note to dodge unpaid Isolated. Stamp Notes **and** provenance key `tiny-contract-tweak` ([hitl.md](hitl.md) Notes↔provenance).

**Notes form:** `tiny-contract-tweak — <one-line reason>`.

**What it skips:**

| Surface | Effect |
|---------|--------|
| Isolated `03a-api` / `03a-db` | Treat as **`skipped`** — Notes-skip only; **never** invent empty files ([results.md](results.md)) |
| Mode simple `design-verify-phase` | Fold light API/DB checks into overall log; do not write Isolated files |
| Lens plan | Do **not** force `api` / `db` on Lens plan; may stay `none` for those surfaces |

**Design clean / Verify clean:** Has ∈ {yes, unknown} + Notes `tiny-contract-tweak` → Isolated N/A (`skipped`). Overall `03a` still must be **`clean`**. Has ∈ {yes, unknown} **without** the Note → Isolated file required (`clean`). Has=no → that surface N/A (`skipped` without file).

**Informal “Tiny”** elsewhere means the same criteria; prefer the Notes token when skipping Isolated or forced lenses.

## Has flip (`no` → `yes` **or** `unknown` → `yes`)

Same turn (**parent after Parent-relay / applying After signals **or** labeled solo when acting as orchestrator** — stage After returns `proposed Has: …` and/or `Has flip detected`; writer applies card Has + Notes / settle / profile drop via Always §4 — [solo-entry.md](solo-entry.md) · [hitl.md](hitl.md)):

1. If profile skip-review → drop to **lite** (mandatory; not Decision N Prefer-paid Else).  
2. Gate B → **blocking** when API **or** DB **or** auth/PII/schema → **yes** (or Mode simple auto predicate fails — any of those flags **yes**/**`unknown`**); **UI alone** does **not** deny Gate B auto / force blocking (still drops skip-review per §1 — [gate-b.md](gate-b.md) SoT).  
3. Bump **Gate B settle gen**; clear approved / armed / auto — for **any** flip (incl. UI-only).  
4. Notes `has-flip — <flags> — gen:<N>`.  
5. If API/DB newly **yes** (not tiny) **or** UI newly **yes** **or** auth/PII/schema newly **yes**: writer **must** set overall `03a` → `pending` same turn as Always §4 (prior `clean` does not pay). Then Prefer re-verify: Mode **full:** Prefer unpaid Isolated when required (API/DB newly **yes** ¬tiny, or Isolated still unpaid for Has ∈ {yes, unknown} ∧ ¬tiny — even if files exist) → then `design-review`; Mode **simple:** Prefer `design-verify-phase` (pays Isolated when needed). Keep API/DB Isolated duty as above. Has that remains **`unknown`** (no flip) still requires Isolated like yes for API/DB (Design clean / Isolated unpaid above · [derive-next.md](derive-next.md)).  

Checked on: design / design-phase / design-update After (proposed Has + flip signal only), preflight Always §4, Before Build.

## Lens plan

Default `none`. When Has API/DB ∈ {yes, unknown} (**not** Notes `tiny-contract-tweak`), finalize `api` / `db` / `api|db` **before Smoke and before Adv** (also gates code-review-phase / lenses / test).

**Missing required api/db:** Expected Next `finalize-lens-plan` (parent-inline **or** labeled solo as orchestrator — not a Task stage) — open this file, set Lens plan, re-derive ([derive-next.md](derive-next.md) · [solo-entry.md](solo-entry.md) · [hitl.md](hitl.md)). Prefer order: finalize **before Smoke and before Adv** (Prefer-re-smoke + E1/skip-review unpaid Smoke + Adv / lenses / test) — intentional; never Prefer Smoke or Adv with plan=`none` while required missing ([verify.md](verify.md) Prefer order vs finalize-lens-plan).

**Lenses paid / clean / dirty:** see [derive-next.md](derive-next.md). Prefer `merge-findings` only when planned lenses are **clean** **and** Merged unpaid (or after Fix re-unpay → re-lens) — **owns** Merged-unpaid dual-false. Lens **`needs fix`** → Prefer `fix-review` — never Prefer `test-*` / `gate-c` / `merge` while **Lenses dirty** or ¬ **Lenses clean**.

## skip-review legality

Only Mode **simple** + Has UI=no + Has API=no + Has DB=no + Has auth/PII/schema=no (explicit `no`; `unknown` ≠ `no`).  
**Has UI = yes or `unknown`:** illegal skip-review — drop to **lite** (or reclassify). UI is a real review surface (fail-closed skip-review; no tiny-UI exception). Does **not** alone force Gate B **blocking** / deny Gate B auto — Gate B auto SoT is API=no ∧ DB=no ∧ auth/PII/schema=no ([gate-b.md](gate-b.md)).  
Mode full + skip-review = Forbidden (Decision N cannot legalize).

## UI craft

When Has UI = yes, design and review stages should apply interface craft: hierarchy, a11y, copy, typography, color, polish — point agents at project UI skills / impeccable / better-interface when installed ([references.md](references.md)). Do not invent a second design system. Profile must be **lite** \| **full** (never skip-review — legality above).
