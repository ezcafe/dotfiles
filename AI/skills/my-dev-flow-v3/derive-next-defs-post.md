# Derive-next Definitions — Post (+ Both)

Open with [derive-next.md](derive-next.md) Unsafe jumps + [derive-next-post.md](derive-next-post.md). **Long Prefer predicates live only here** (and Pre twin) — narrative files name+link.

| Term | Meaning |
|------|---------|
| **Design clean** / **Verify clean** | Overall `03a` **clean** **and** Isolated API/DB paid when required (`clean`\|`skipped`; Has ∈ {yes, unknown} ∧ ¬tiny / ¬Notes `tiny-contract-tweak` → file required; Mode simple: `design-verify-phase` writes those files). Notes `tiny-contract-tweak` → Isolated N/A skipped ([lenses.md](lenses.md)). **Mode simple:** Verify clean ≡ Design clean (same predicate) |
| **Review clean** | Adv + Quality section Results both **clean** (file-top alone never pays) |
| **code-review unpaid** | Planned Adv/Quality missing **or** section Result missing/`pending` (not `needs fix`) |
| **Review needs fix** | Adv and/or Quality section Result = `needs fix` |
| **missing required api/db** | Has API/DB ∈ {yes, unknown} ∧ ¬tiny / ¬Notes `tiny-contract-tweak` ∧ Lens plan lacks matching `api`/`db` (incl. plan=`none`) — Prefer `finalize-lens-plan` ([derive-next-post.md](derive-next-post.md) · [lenses.md](lenses.md)) |
| **Lens plan unpaid** | Lens plan ≠ `none` **and** (planned `05-lens-*` missing **or** Result missing/`pending`) — incl. Result `pending`. Result-bearing = `clean`\|`needs fix` only. Prefer unpaid `lens-*` **only** when this holds. Lens plan `none` → **not** unpaid; **Lenses clean** vacuous only when ¬ **missing required api/db** (else Prefer `finalize-lens-plan`) |
| **Lenses dirty** | Lens plan ≠ `none` **and** (Lens plan unpaid **or** any planned / Merged Result = `needs fix`). **Dual-false notes** (clean=false ∧ dirty=false — intentional): (1) plan=`none` ∧ **missing required api/db** → Prefer / unsafe-jump owner is **missing required api/db** → `finalize-lens-plan`, **not** Lenses dirty; (2) plan 2+ ∧ planned lenses **clean** ∧ **Merged unpaid** → Prefer `merge-findings` owns it ([derive-next-post.md](derive-next-post.md)); unsafe also bans `test-*` / `gate-c` / `merge` while ¬ **Lenses clean** |
| **Lenses clean** | (Lens plan `none` **and** ¬ **missing required api/db**) **or** (every planned `05-lens-*` **clean** **and** (plan 2+ → Merged **clean**)). Plan=`none` with **missing required api/db** → **not** clean. Plan 2+ with Merged unpaid/pending → **not** clean. **Dual-false notes:** same two cases as **Lenses dirty** — Prefer owners `finalize-lens-plan` / `merge-findings`; do **not** Prefer `test-*` / `gate-c` / `merge` while ¬ clean |
| **Smoke unpaid** | E1 or skip-review: unpaid until `Smoke source: Smoke-Task`. Lite: Build-writes-Smoke may pay |
| **Smoke fail** | Independent Smoke (or `06` smoke) Result **fail** / **smoke-fail**. Prefer-re-smoke eligible = Last stage `fix-tests` + verify-pass; Prefer-re-smoke proceed only when Smoke unpaid∨fail ∧ Prefer-re-smoke eligible (same Prefer as unpaid — not eligible alone when Smoke paid/success) |
| **Tests success** | ≡ Gate C test bar ([gate-c.md](gate-c.md)) |
| **Tests unpaid** | Profile ≠ skip-review **and** ¬(`06` success **and** path matches profile) |
| **skip-review Prefer paid** | Legal skip-review **and** Tests success (verify-pass + `Smoke source: Smoke-Task` + escape Notes↔provenance + stale cleared — [gate-c.md](gate-c.md) · [verify.md](verify.md)) |
| **Gate C unpaid** | approved `none`/empty **or** remaining named actions unpaid |
| **Gate B settled** | Token gen == current settle gen ([gate-b.md](gate-b.md)) |
