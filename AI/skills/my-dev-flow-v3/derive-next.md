# Derive next (Expected Next SoT)

**Load:** this file (selector + Unsafe jumps) **plus** matching defs + Prefer half before each Task. First-match wins among rows that produce a **concrete** Expected Next (stage id / Stop / Decision N). **Fall-through meta-rows** (Expected Next marked `*(fall-through …)*`, or Fix rows that match only when they emit a concrete id) **do not** consume first-match — keep evaluating later Prefer rows. Do **not** treat “continue” as a Next value.

| Half | Defs | Prefer table |
|------|------|--------------|
| **Pre-Build** | [derive-next-defs-pre.md](derive-next-defs-pre.md) | [derive-next-pre.md](derive-next-pre.md) |
| **Post-Build** | [derive-next-defs-post.md](derive-next-defs-post.md) | [derive-next-post.md](derive-next-post.md) |

**Prefer / Unsafe SoT** = this file + the active defs + Prefer half. Narrative files (**grill**, **brainstorm**, **results**, **preflight**, …) **must not** restate long predicate cells — name + link only.

## Selector Pre vs Post

| Condition | Half |
|-----------|------|
| Notes `design-backloop` or `design-stale` | **Pre-Build** — open defs-pre + [derive-next-pre.md](derive-next-pre.md) |
| No Build verify-pass for **current** Gate B settle gen | **Pre-Build** — open defs-pre + [derive-next-pre.md](derive-next-pre.md) |
| Build verify-pass with **Last verify settle-gen** == current settle gen | **Post-Build** — open defs-post + [derive-next-post.md](derive-next-post.md) |

On verify-pass, parent **or** labeled solo (acting as orchestrator) sets **Last verify settle-gen** = current **Gate B settle gen** ([hitl.md](hitl.md) · [solo-entry.md](solo-entry.md)).

## Definitions

**SoT:** [derive-next-defs-pre.md](derive-next-defs-pre.md) (Pre + Both) or [derive-next-defs-post.md](derive-next-defs-post.md) (Post + Both). Open **one** defs file per turn — Both terms are duplicated into each half so you never open both.

## Unsafe jumps (never Prefer / launch)

- Illegal Mode×profile  
- `gate-a` / `skim` / `analyze` / `design` / `design-phase` while **ideation unpaid** (Prefer `ideation` first — both Modes; paid = Notes `ideation-confirmed`|`ideation-skip` + provenance — [brainstorm.md](brainstorm.md))  
- Build / Post-Build while `design-stale` or `design-backloop` (until clear rules met)  
- Isolated / `design-review` / `design-verify-phase` / `design-update` while Notes `design-stale` (until Mode-full `design` + `03` rewrite clears Notes — Prefer **Grill open** → `grill` first, then unpaid among **Analyze unpaid** → **Grill unpaid** → **design unpaid under design-stale**)  
- `design` / `design-review` / `design-verify-phase` / `design-update` / `gate-b` / `build` while **Grill open** (both Modes — incl. under Notes `design-stale` / `design-backloop`; never Prefer `design` unpaid under design-stale until Grill closed; Prefer `grill` before `design-update`)  
- `design-phase` while **Grill open** ∧ ¬ **cold-start carve** — carve SoT [grill.md](grill.md); mid-open Prefer `grill`  
- Isolated / `design-review` / `design-verify-phase` while ¬ Design present (Mode full Prefer `design`; Mode simple Prefer `design-phase` per **cold-start carve** — [grill.md](grill.md); file alone / Result `pending` never pays)  
- Isolated / `design-review` / `design-verify-phase` while design-update unpaid (**backloop rewrite unpaid** **or** any `03a*` **`needs update`**) — Prefer **Grill open** → `grill` first; else Prefer `design-update` first  
- `gate-b` / `build` while **04a unpaid / dirty** (requires **planned tests present**; missing / `pending` / `needs more tests` alone when ¬ planned tests → **04a ok**)  
- `gate-c` / `merge` while ¬ Tests success or unpaid stale Notes  
- `test-*` / `gate-c` / `merge` while **Lenses dirty** **or** ¬ **Lenses clean** (covers Merged-unpaid dual-false when plan 2+ — Prefer `merge-findings`; plan=`none` dual-false → **missing required api/db** row)  
- Prefer-re-smoke / unpaid `smoke` / Adv / `code-review-phase` / `lens-*` / `test-*` / `gate-c` / `merge` while **missing required api/db** (Prefer `finalize-lens-plan` first — before Smoke **and** before Adv — even if Lens plan=`none`)  
- `merge` unless Tests success **and** **Lenses clean** **and** `merge` ∈ Gate C approved  
- Prefer `merge` when Last=`merge` ∧ Result=`success` (or Status `done`) — parent already stamped / should stamp Status; do not re-launch merge  
- Stages while Status `done` \| `stopped`  
- Post-Build while verify settle-gen ≠ current Gate B settle gen  
- Prefer design-stale unpaid / Mode-full `design` rewrite while Mode **simple** ∧ Notes `design-stale` — Decision N / Upgrade first ([step-0.md](step-0.md)); never Prefer `design` on simple card under design-stale  

`card-override` cannot waive these.

## Halves

See table at top (defs + Prefer links).
