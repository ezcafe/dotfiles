# Orchestrator rules (short)

**SoT for:** launch-time **Pre-launch checklist card** (links only) + short parent habits.  
Happy path: [stages.md](stages.md). Load budget: [step-0.md](step-0.md#load-budget). Design invalid: [design-backloop.md](design-backloop.md).  
Decision shapes + detailed checklist body: [invariants.md](invariants.md) (expand there; do not duplicate a second launch card).

## Pre-launch checklist card (≤15)

Before every Task — this is the only launch-time card; details live in linked SoT (do not expand here).  
**Numbering:** Card items are **not** 1:1 with [invariants.md](invariants.md) body numbers. Expand a card item only via that item’s link (or the linked SoT section); do not map by ordinal.  
**Applicability:** always **1**, **3–5**, **11–12**; **2** when Next ∈ clarity stages ([parent-next.md](parent-next.md)); **6** when `--next` emits Task handoff (exit 0) — if `do-not-launch`, stop and follow printed next action; **7** when Next=`build` (phase `--before-build`); **8** when Next=`merge` (`--before-merge`); **9** when Next ∈ design-review / design-verify / api|db-review / build (`--before-design-review` when Next ∈ design-review*); **10** when Next ∈ build / fix-* / test-* / smoke. Honor [Load budget](step-0.md#load-budget).

1. Card Mode / profile / Status — [invariants.md](invariants.md) (card matches Mode / profile / Status)
2. Clarity boundary + `clarity-check ok — <Next>` — [parent-next.md](parent-next.md)
3. `lint-run.py <run-dir> --next --derive` — phase gates **auto** from card Next (design-review* → `--before-design-review`; Adv / `code-review-phase` → `--before-code-review`; `build` → `--before-build`; `merge` → `--before-merge`) — [parent-next.md](parent-next.md) · [scripts/README.md](scripts/README.md)
4. Illegal Mode × profile / skip-review Next → `do-not-launch` unless `card-override` + provenance — [stages.md](stages.md)
5. Unsafe card vs derived → fix card or override — [parent-next.md](parent-next.md)
6. `handoff-for.py <stage-id>` + load `stages/<id>.md` only — [skills-path.md](skills-path.md)
7. Gate B / Build armed / provenance when Next=`build` — [hitl.md](hitl.md)
8. Gate C approved + provenance when Next=`merge` — [hitl.md](hitl.md)
9. Has API/DB + skip-review ban / Pending parallel — [lenses.md](lenses.md)
10. Verify commands before build/fix/test — [verify-and-fix.md](verify-and-fix.md)
11. Honor [Load budget](step-0.md#load-budget) — card + launch card + `--next --derive` + handoff + `stages/<id>.md` + parent-next Open (1–2) + clarity file when Next ∈ clarity stages (not a hard “one companion” cap)
12. After return: Result first line → update card — [results.md](results.md)

## Also

- Design-review update → re-review. Smoke/test fail → Fix (verify-pass) → re-run.
- No advance on verify-fail; max 3 → Decision N. Design invalid → [design-backloop.md](design-backloop.md).
- Mode full Task count ≥25 → Decision N ([invariants.md](invariants.md)).
