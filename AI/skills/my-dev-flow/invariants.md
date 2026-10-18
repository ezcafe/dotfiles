# Parent invariants + max-round Decisions

**This file is SoT for:** Decision shapes (max-round / hard stops) + the **detailed** pre-launch checklist body below.  
**Launch-time card (links only):** [orchestrator-rules.md](orchestrator-rules.md). Habit + `--next --derive`: [parent-next.md](parent-next.md). Do **not** treat this file as a second launch-time entry; open it when you need Decision shapes or to expand a checklist item.  
**Numbering:** Body items below are **not** 1:1 with [orchestrator-rules.md](orchestrator-rules.md) card numbers (card has 12 link-only items; body groups detail). Expand only via each card item’s link; do not assume ordinal parity (e.g. card **9** ≠ body **9**).  
Decision option shape: [handoffs.md](handoffs.md).  
Hard stops / what to chat: [failure-playbook.md](failure-playbook.md).  
**Lint (required):** `scripts/lint-run.py .my-docs/workflow/<slug>/` at Step 0. Phase flags also **auto** from card Next (and via `--next --derive`): design-review* → `--before-design-review`; Adv / `code-review-phase` → `--before-code-review`; `build` → `--before-build`; `merge` → `--before-merge`. Pre-launch habit: `lint-run.py <run-dir> --next --derive` ([orchestrator-rules.md](orchestrator-rules.md) · [parent-next.md](parent-next.md) · R8).

## Pre-launch checklist body (≤10)

Expand from the [orchestrator-rules.md](orchestrator-rules.md) card **via that card item’s link** (not by matching ordinals):

1. **Card matches Mode / Review profile** in `00-run.md`. **Status** is `running|paused|stopped|done` (not a stage id).
2. **Next stage id** matches Full/Simple order ([stages.md](stages.md)). Run `--next --derive`; unsafe card vs derived → fix card or Notes `card-override — <reason>` + provenance `card-override` ([parent-next.md](parent-next.md)).
3. **Has API / Has DB** are `yes` or `no` (not unknown) before design-review / design-verify-phase. If either **yes**, Review profile must **not** be `skip-review` ([lenses.md](lenses.md)). Mode **full** + both yes (not tiny): **Pending parallel** `api|db` until both `03a-*` exist, then `none` ([lenses.md](lenses.md)). Mode **simple** keeps Pending parallel `none` (API/DB in design-verify-phase).
4. **Verify commands** set before `build` / `fix-*` / test stages ([verify-and-fix.md](verify-and-fix.md)).
5. **Gate B settled** before `build`: HITL **blocking** → **Gate B approved** `yes` (or named pick) **+ quality provenance**; **auto** → allow without yes; **async-notify** → **Build armed** + turn-boundary gap (arm HH:MM later than digest + Notes `async-gap-pending` + `.lint-async-gap` from prior `--next`) ([hitl.md](hitl.md)). Notes `design-backloop` → do not Build (`--next` redirects `build` only; `gate-b` settle allowed until token cleared). Lint: `--before-build` / Next=`build` / `--next`.
6. **`Gate B veto`** is `none` before launching Build; if `pending` → do not Build ([hitl.md](hitl.md)). Veto window open without **Build armed** / incomplete async gap → do not Build.
7. **Next=`merge`** → **Gate C approved** must be a non-empty subset of `commit,push,pr,merge` (not `none`) **+ quality provenance** before handoff ([hitl.md](hitl.md)). Lint errors otherwise. **Before Adv / `code-review-phase`:** Lens plan includes **api**/**db** when Has API/DB yes (unless tiny-tweak / Notes fold) — lint `--before-code-review` ([lenses.md](lenses.md)).
8. Handoff = **required** `python3 {my-dev-flow}/scripts/handoff-for.py <stage-id>` (prints Description) + load **`stages/<stage-id>.md`** only ([parent-next.md](parent-next.md) · [skills-path.md](skills-path.md)). Do **not** load whole [handoffs.md](handoffs.md) for launch (edit SoT / debug only). **Clarity-check:** every clarity boundary (`design-phase` / `analyze` / `grill` / `design` / `tdd-review` / `build` / `fix-*` / `merge`) → boundary-matched `clarity-check ok — <Next>` ([parent-next.md](parent-next.md)). Still open the clarity file for content checks (Problem map / What-Why-How). Clarity tokens ≠ stage gates (derive/lint still enforce e.g. open Grill blocks Design). If it fails → ask the user; do not launch.
9. Load **one** subflow `SKILL.md` for the phase (or when Mode/profile changes). Do **not** re-read orchestrator SKILL every step. Model tier from [models.md](models.md) (Fast-on-simple when Mode simple). Soft Task-count budget: Mode **full** ≥25 → Decision N (below). **main-thread fallbacks ≥ 3** → Decision N (below). Honor [Load budget](step-0.md#load-budget) (Open row 1–2 + clarity when Next ∈ clarity stages — not a hard “one companion” cap).
10. After return: read **Result first line** ([results.md](results.md); ~40 lines max); update Orchestrator card + Last Verify; do **not** advance on `verify-fail`. Step 0 / after SoT edits: `./AI/skills/sync-to-cursor.sh --check` (or sync) when `AI/skills/my-dev-flow` exists — drift is a hard stop ([skills-path.md](skills-path.md)).

## Built-in Decision shapes (max rounds / hard stops)

Use **Decision N** + Option 1/2/3 with What / Example / Pros / Cons / Recommendation ([handoffs.md](handoffs.md)).

| When | Option 1 | Option 2 | Option 3 | Default recommend |
|------|----------|----------|----------|-------------------|
| **Gate A escalate** (`01a` Result `escalate`) | Re-run Gate A (ideation-update if Fix ask needs it) | Human override: set Result `ok` + Notes **only after explicit user yes** | Stop | Ask user; never invent Result `ok` on resume |
| **Design-backloop** (design invalid after Build) | Amend design → Notes `design-backloop`, **Gate B approved: none**, clear Build armed / veto-window, Next `design-update` (no prior `03a` Fix ask) → re-review → Gate B (token until settle) → Fix/rebuild | Fix-only under current design | Stop | 1 if contracts/IA must change; else 2 |
| **Gate B veto after Build** | Discard draft; re-open Gate B (**approved: none**, clear armed/window, Next `gate-b`) | Keep draft; re-open Gate B (same reset) | Stop | Per user intent |
| **verify-fail after 3 attempts** | Narrow scope / waive failing command (user) | Re-open with different Verify commands | Stop | Ask user; prefer 1 or 3 |
| **design-review / design-verify max 3 rounds** | Another Update round (user raises cap) | Ship with open Enhancement only (no Critical/Major) | Stop / reclassify | 3 if Critical/Major remain; else 2 only if clean |
| **review Fix max 3 rounds** | Another Fix round (user raises cap) | Defer remaining Enhancements; proceed if clean | Stop / design-backloop | 2 if clean; 1 or design-backloop if not |
| **test↔fix max 3 rounds** | Another Fix + re-test (user raises cap) | User waive green tests → Gate C | Stop | Ask user |
| **Mid-run reclassify** | Stay simple | Upgrade to full | New slug / stop | 2 when API/DB/auth appears |
| **Task-count soft cap** (Mode **full**, Task count ≥ **25**, Status `running`) | Continue (user raises awareness) | Reclassify / slim scope | Stop / new slug | Ask user; prefer slim or stop if thrashing |
| **Main-thread fallback soft pause** (`main-thread fallbacks` ≥ **3**, Status `running`) | Continue (user aware) | Reclassify / change model path | Stop / new slug | Ask user; prefer fix inherit path if thrashing |

## Soft Task-count budget

**Expected bands** (guidance; do not change metric semantics without a Notes note):

| Shape | Typical Task count |
|-------|--------------------|
| Mode **simple** + Review profile **lite** | ~8–12 |
| Mode **full** + API+DB (+ parallel lenses) | ~14–22 |

**Soft cap:** Mode **full**, **Task count ≥ 25**, Status `running` → pause with **Decision N** (continue / reclassify / stop). Lint warns (`SOFT_TASK_CAP = 25`). Cap sits above the ~14–22 expected band so golden API+DB paths do not pause early. Clean parallel lens waves may approach / briefly hit the cap — that alone is not thrash; Decision N still applies. Mode simple has no soft cap (phase bundles keep count low).

**Main-thread fallback soft pause:** When **main-thread fallbacks ≥ 3** and Status `running` → pause with **Decision N** (continue / reclassify / stop). Lint warns. See [failure-playbook.md](failure-playbook.md).

## Run metrics

On `00-run.md` **Run metrics**:

**Required (keep filled when the section exists):**

- Task count
- verify-fail count
- main-thread fallbacks

**Optional:** design-review / design-verify rounds; smoke↔fix / test↔fix rounds; Gate B / Grill HITL tier; inherit retries.

Do not block the pipeline on empty optional metrics. Empty **required** metrics → warn via `scripts/lint-run.py`.
