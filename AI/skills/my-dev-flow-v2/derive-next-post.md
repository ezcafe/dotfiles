# Derive next — Post-Build

Open with [derive-next.md](derive-next.md) (Definitions + selector). Use **only** when selector says **Post-Build**.

## Post-Build

**First-match:** scan top→bottom; stop at the first matching row.

**Lenses paid** / **Lenses clean:** full tables in [lenses.md](lenses.md). **Unpaid-check exception only:** after `fix-review` **verify-pass** for Fix Mode `merged-lenses` or Mode `plan-1-lens`, treat planned `05-lens-*` + Merged as **unpaid** until Result is **`clean`** again (Prefer re-lens below).

**Review needs fix** / **code-review unpaid** ([derive-next.md](derive-next.md) Definitions): unpaid → Prefer profile review rows below; needs fix → Prefer `fix-review` (not lenses).

| State | Expected Next |
|-------|---------------|
| Status **`done`** \| **`stopped`** | Stop — do not Prefer stages |
| Status **`paused`** and still waiting on user (Gate B/C AskQuestion open, async veto without arm, Grill blocking open) | Stop — stay paused ([resume.md](resume.md)) |
| Tests success, `merge` ∈ **Gate C approved** (+ provenance `gate-c-approved`) (**Does not match when** unpaid `review-stale` / `test-stale` — **¬Tests success**) | `merge` |
| Tests success, **Gate C approved** non-empty but `merge` ∉ approved (PR-only / commit-only) (**Does not match when** unpaid stale Notes — **¬Tests success**) | `gate-c` (ask remaining named actions) **or** stop while Status **`paused`** |
| Tests success, **Gate C approved** `none` / empty (**Gate C unpaid**) (**Does not match when** unpaid stale Notes — **¬Tests success**) | `gate-c` |
| Last Verify = **verify-pass** **and** **Last verify-pass at** = **none** | Stop — fix card (same-turn timestamp required — [preflight.md](preflight.md) · [results.md](results.md)); do **not** Prefer Smoke / Adv / gate-c |
| Last stage `build` + Last Verify = **verify-fail** | Prefer `build` again if Verify attempts < 3; else Decision N ([decisions.md](decisions.md)) |
| Last stage `fix-review` \| `fix-tests` + Last Verify = **verify-fail** | Prefer that same Fix stage if Verify attempts < 3; else Decision N ([decisions.md](decisions.md)) |
| Last stage `fix-tests` + Last Verify = **verify-pass** | Prefer: `smoke` if Smoke unpaid/fail (or Notes re-smoke); else `test-full` / `test-lite` if test-fail unpaid (or Notes re-test); else continue table below. **Do not** stay on `fix-tests`. |
| Last stage `fix-review` + Last Verify = **verify-pass** | Prefer: re-run **dirty** verifier by Fix Mode / profile — (1) Mode `code-review-phase` (lite) → `code-review-phase`; (2) Mode `adversarial-tests` \| `quality` (full) → that section; both dirty/unclear → `adversarial` then `quality`; (3) Mode `merged-lenses` \| `plan-1-lens` → mark planned `05-lens-*` + Merged **unpaid**/pending → Prefer re-run dirty `lens-*` (or all planned) → `merge-findings` if 2+. If already clean → else continue table below. **Do not** stay on `fix-review`. Examples: [fix-review-rereview.md](examples/fix-review-rereview.md) · [fix-review-relens.md](examples/fix-review-relens.md). |
| Smoke fail / test fail (**Does not match when** Last stage is `fix-tests` **and** Last Verify is **verify-pass** — earlier Prefer re-smoke / re-test row owns that case) | `fix-tests` (wins over skip-review Prefer and Smoke unpaid; re-smoke / re-test only after verify-pass — [verify.md](verify.md)) |
| **Legal skip-review** (after Build verify-pass; **not** smoke-fail / test-fail) | Ordered recovery ([verify.md](verify.md) Skip-review + Smoke · Stale): Notes `test-stale` **or** Smoke unpaid/fail → Prefer unpaid independent Smoke (`smoke`); clear `test-stale` when `Smoke source: Smoke-Task` is fresh after **Last verify-pass at**. Notes `review-stale` = N/A under skip-review (clear; do not Prefer review). **Prefer paid** → when bar met (**Tests success**) **and** `merge` ∈ **Gate C approved** (+ provenance) → Prefer **`merge`** (same as Tests-success row); else → **`gate-c`** only when stale Notes cleared **and** Prefer-paid bar met; **else** → Decision N ([decisions.md](decisions.md) Skip-review else). Gate C bar: [gate-c.md](gate-c.md). **Do not** match review/test rows below while profile stays skip-review. |
| Mode full + profile full, Smoke unpaid (**not** smoke-fail) | `smoke` (Notes `smoke re-run`) |
| Notes `review-stale` (**profile ≠ skip-review**) | Prefer: unpaid review (next verifier by profile) — prior clean not paid; clear `review-stale` only per [verify.md](verify.md) Lite/full clear |
| Notes `test-stale` (**profile ≠ skip-review**) | Prefer: unpaid `test-full` / `test-lite` — prior success not paid; clear `test-stale` only per [verify.md](verify.md) Lite/full clear |
| Review needs fix (**profile ≠ skip-review**; **Does not match when** Last stage is `fix-review` **and** Last Verify is **verify-pass** — earlier Prefer re-verify row owns that case) | `fix-review` |
| Has API or Has DB = **yes** (not tiny) **and** Lens plan missing matching `api` / `db` (**profile ≠ skip-review**) | Stop — parent finalize Lens plan ([lenses.md](lenses.md) Finalize deadline); do **not** Prefer code-review unpaid |
| Profile full, code-review unpaid (**≠ skip-review**) | next unpaid in order: `adversarial` then `quality` |
| Profile lite, code-review unpaid (**≠ skip-review**) | `code-review-phase` (does **not** pay lenses) |
| Lens plan **2+**, every planned `05-lens-*` is Result-bearing (`clean` \| `needs fix`), Merged lenses unpaid/pending (**profile ≠ skip-review**) | Prefer: `merge-findings` — **above** launch-lens (do **not** rematch launch when only Merged is unpaid; planned still **`pending`** = Lens plan unpaid, not this row) |
| Review clean, **Lens plan unpaid** (**profile ≠ skip-review**) — some planned `05-lens-*` missing or Result missing/**`pending`** (not Result-bearing); **excludes Merged** ([derive-next.md](derive-next.md) Definitions) | parent launches unpaid planned `lens-*` **only** (parallel when 2+; serial only when parent chose serial) → wait siblings; never treat in-band notes as paid. After every planned `05-lens-*` is Result-bearing → Prefer `merge-findings` if plan **2+** (row above), not re-launch |
| Review clean **and** Lens plan **`needs fix`** — Merged (plan **2+**) or planned `05-lens-*` (plan **1**) (**profile ≠ skip-review**; **Does not match when** Last stage is `fix-review` **and** Last Verify is **verify-pass** — earlier Prefer re-lens row owns that case) | `fix-review` Mode `merged-lenses` (plan **2+**) or Mode `plan-1-lens` (plan **1**) — **not** Prefer `merge-findings` / re-lens while Fix is pending (unpaid-check treats **`needs fix`** as paid) |
| Review clean (+ lenses **clean** / plan `none`), **Tests unpaid** ([derive-next.md](derive-next.md) Definitions) | `test-full` (profile full) or `test-lite` (lite) |
