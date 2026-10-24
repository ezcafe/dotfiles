# Derive next — Post-Build (first-match)

Load with Unsafe jumps from [derive-next.md](derive-next.md) + Definitions from [derive-next-defs-post.md](derive-next-defs-post.md). First-match wins among concrete Next cells; fall-through meta-rows do **not** consume first-match ([derive-next.md](derive-next.md)). Unmatched Prefer → Decision N ([failure.md](failure.md)).

Skip-review Smoke order SoT = [verify.md](verify.md) Skip-review ordered recovery (pointer only).

| State | Expected Next |
|-------|---------------|
| Status `done` \| `stopped` | Stop |
| **paused-wait** (Status `paused` ∧ (Build armed unpaid on async path ∨ Gate C approved non-empty without `merge` ∨ Notes `waiting — <reason>` — parent **or** labeled solo set+clear ([hitl.md](hitl.md) · [solo-entry.md](solo-entry.md); Stages return `candidate waiting — …` only))) | Stop — stay paused ([resume.md](resume.md)) |
| Status `paused` ∧ ¬ **paused-wait** | *(fall-through — evaluate next Prefer row; re-derive next unpaid; do **not** invent Notes `waiting — <reason>` — parent **or** labeled solo only)* |
| Last=`merge` ∧ Result=`success` (or Status `done`) | Stop — do **not** Prefer `merge` again (parent **or** labeled solo stamps Status from `candidate Status` — [hitl.md](hitl.md) · [solo-entry.md](solo-entry.md) · [../my-dev-flow-v3-merge/stages/merge.md](../my-dev-flow-v3-merge/stages/merge.md)) |
| Last Verify ≠ `verify-pass` after Build/Fix | re-`build` / same Fix if attempts &lt; 3 else Decision N |
| verify-pass + Last verify-pass at none | Stop — stamp ISO local ([results.md](results.md)) |
| **missing required api/db** (Has API/DB ∈ {yes, unknown}, not tiny, plan lacks matching `api`/`db`) | `finalize-lens-plan` (parent-inline **or** labeled solo as orchestrator — open [lenses.md](lenses.md); set Lens plan; then re-derive — [solo-entry.md](solo-entry.md) · [hitl.md](hitl.md)). **Above** Prefer-re-smoke / unpaid Smoke **and** Adv / lenses / test — [verify.md](verify.md). Do **not** Prefer Smoke / Adv / lenses / test while missing |
| Last stage `fix-tests` + verify-pass ∧ ¬ **missing required api/db** ∧ Smoke unpaid/**fail** (Prefer-re-smoke eligible) | `smoke` — do **not** stay on `fix-tests` |
| Last stage `fix-tests` + verify-pass ∧ ¬ **missing required api/db** ∧ test-fail unpaid | Prefer unpaid `test-*` — do **not** stay on `fix-tests` |
| Last stage `fix-review` + verify-pass ∧ (dirty Adv/Quality unpaid **or** `code-review-phase` unpaid) | Prefer re-run dirty Adv/Quality / `code-review-phase` — do **not** stay on `fix-review` |
| Last stage `fix-review` + verify-pass ∧ Mode `merged-lenses`\|`plan-1-lens` (re-unpay planned lenses + Merged done or owed) | Prefer re-lens → `merge-findings` if plan 2+ — do **not** stay on `fix-review` |
| Smoke fail / test fail (**Does not match when** Last stage `fix-tests` + verify-pass — Prefer re-smoke / re-test row owns) | `fix-tests` (**before** Prefer re-smoke / re-test) |
| E1 or skip-review Smoke unpaid ∧ ¬ **missing required api/db** (**not** smoke-fail unpaid — fail hits fix-tests / Prefer-re-smoke rows above) | Prefer unpaid `smoke` (Build-writes-Smoke does not waive) |
| Review needs fix | `fix-review` |
| code-review unpaid (profile full) | Prefer unpaid Adv then Quality |
| code-review unpaid (profile lite) | `code-review-phase` |
| Notes `review-stale` (not skip-review) | Prefer unpaid review ([verify.md](verify.md) clear duty) — **above** Lens plan unpaid when Adv/Quality still look `clean` |
| Review clean, any planned lens / Merged **`needs fix`** | `fix-review` Mode `merged-lenses` (plan 2+) / `plan-1-lens` (plan 1) — **not** Prefer `merge-findings` while dirty |
| Review clean, Lens plan unpaid (Lens plan ≠ `none` — vacuous when plan=`none`) | Prefer unpaid `lens-*`. Plan=`none` + Review clean → **not** this row — fall through **only** when **Lenses clean** truly vacuous (¬ **missing required api/db**); else **missing required api/db** row already Preferred `finalize-lens-plan` (before Smoke **and** Adv). Do **not** Prefer `test-*` while required api/db missing |
| Plan 2+, planned lenses **clean**, Merged unpaid | `merge-findings` (**owns** Merged-unpaid dual-false: clean=false ∧ dirty=false — do **not** Prefer `test-*` / `gate-c` / `merge` here) |
| Notes `test-stale` | skip-review → Prefer unpaid Smoke; else Prefer unpaid `test-*` |
| Legal skip-review Prefer paid (**skip-review Prefer paid** predicate) | **Lenses clean** + Tests success + `merge` ∈ approved → `merge`; else **Lenses clean** + Tests success + Gate C unpaid → `gate-c`; else Decision N ([verify.md](verify.md)) |
| Legal skip-review **and** `Smoke source: Smoke-Task` **and** ¬ Prefer paid (**skip-review Prefer paid** unmet — e.g. escape Notes missing / stale uncleared) | Decision N ([verify.md](verify.md) §4 Else · [stages.md](stages.md) Mode×profile) — do **not** fall through with no Next |
| Review clean + Lenses clean, Tests unpaid (lite/full) | Prefer unpaid `test-full` / `test-lite` |
| Tests success + **Lenses clean** + `merge` ∈ approved | `merge` |
| Tests success + **Lenses clean** + Gate C unpaid | `gate-c` |
| *(unmatched — no Prefer row above)* | Decision N ([failure.md](failure.md) · [decisions.md](decisions.md)) — do **not** invent Next |
