## Clarity check (parent)

### design-phase entry (Mode **simple** only)

Before launching **`design-phase`** (the Task that creates `02-analysis` / Grill / Design):

> Are Mode, instructions, and `01-idea` clear enough to proceed?

Confirm:

- `00-run.md` **Mode** is **simple** (Mode full must use Analyze → Grill → Design, not this bundle)
- `01-idea.md` **Problem map** — stub or Core problem line OK

Do **not** require `02-analysis.md` or Grill frontier yet — this Task writes them.

If no → ask the user; do not launch `design-phase`.

### Analyze / Grill / Design (Mode **full** standalone stages)

Before Analyze and Design:

> Are the instructions, dependencies, and reference files clear enough to proceed?

Before Grill / Design, also confirm:

- `01-idea.md` **Problem map** — Steps 1–2 + mind map + Core problem present
- `02-analysis.md` Deep dive answers (or user-confirmed open questions for):
  1. **What is this?**
  2. **Why do we need this?**
  3. **How to do this?** (other ways + best practices + **Solution branches** when Mode full)

Before Design, confirm Grill is **frontier-empty** or **skipped** (see `02b-grill.md` / Notes). Do not start Design on `needs-round`.

**Checklist note:** soft clarity lint is a **floor** (once-per-run presence-any — [parent-next.md](../../my-dev-flow/parent-next.md)). A soft token already in Notes does **not** skip opening this file — still confirm Problem map / What-Why-How (and Grill frontier) before Design. Soft clarity also does **not** skip must-hold stage gates (open Grill still blocks Design via derive/lint).

If no → ask the user; do not launch the next stage.

After pass, log `clarity-check ok — <boundary>` (e.g. `design-phase`, `analyze`, `grill`, `design`). Soft presence-any once-per-run: one token unlocks later soft lint boundaries; it does **not** unlock high-risk code stages (`tdd-review` / `build` / `fix-*` / `merge`).
