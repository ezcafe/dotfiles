## Clarity check (parent)

### design-phase entry (Mode **simple** only)

Before launching **`design-phase`** (the Task that creates `02-analysis` / Grill / Design):

> Are Mode, instructions, and `01-idea` clear enough to proceed?

Confirm:

- `00-run.md` **Mode** is **simple** (Mode full must use Analyze → Grill → Design, not this bundle)
- `01-idea.md` **Problem map** — stub or Core problem line OK

Do **not** require `02-analysis.md` or Grill frontier yet — this Task writes them.

If no → ask the user; do not launch `design-phase`.

### Analyze (Mode **full**)

Before launching **`analyze`**:

> Are the instructions, dependencies, and reference files clear enough to proceed?

Confirm:

- `01-idea.md` **Problem map** — Steps 1–2 + mind map + Core problem present (or user-confirmed stubs enough to Analyze)

Do **not** require `02-analysis.md` What/Why/How yet — Analyze writes those.

If no → ask the user; do not launch `analyze`.

### Grill (Mode **full**)

Before launching **`grill`**:

> Are the instructions, dependencies, and reference files clear enough to proceed?

Confirm:

- `01-idea.md` **Problem map** — Steps 1–2 + mind map + Core problem present
- `02-analysis.md` Deep dive answers (or user-confirmed open questions for):
  1. **What is this?**
  2. **Why do we need this?**
  3. **How to do this?** (other ways + best practices + **Solution branches** when Mode full)

If no → ask the user; do not launch `grill`.

### Grill (Mode **simple** re-entry)

Before launching **`grill`** when Mode is **simple** (re-entry / settle after `design-phase`, not cold-start `design-phase`):

Reuse **design-phase entry** clarity above **and** confirm Grill is still open ([grill.md](../../my-dev-flow-v2/grill.md) Grill open) — Expected Next stays `grill` until closed. Do **not** require the Mode-full Analyze What/Why/How checklist again.

If no → ask the user; do not launch `grill`.

### Design (Mode **full**)

Before launching **`design`**:

> Are the instructions, dependencies, and reference files clear enough to proceed?

Confirm the same Problem map + What/Why/How as Grill above.

Also confirm Grill is **not open**: Result **frontier-empty** or **skipped**, or Notes grill-skip — and `02b` exists **or** Notes grill-skip ([grill.md](../../my-dev-flow-v2/grill.md) Grill open). Do **not** start Design on **`needs-round`** or **unpaid Grill** (no `02b` and no Notes grill-skip).

If no → ask the user; do not launch `design`.

### Checklist note (all design boundaries)

Clarity checks are **boundary-matched** ([parent-next.md](../../my-dev-flow-v2/parent-next.md)). A prior token (e.g. `clarity-check ok — design-phase` or `analyze`) does **not** unlock a different Next — log `clarity-check ok — <exact Next>` for this launch. Opening this file for content checks is still required. Clarity tokens also do **not** skip must-hold stage gates (open Grill still blocks Design via [derive-next.md](../../my-dev-flow-v2/derive-next.md) / [preflight.md](../../my-dev-flow-v2/preflight.md)).

After pass, log `clarity-check ok — <boundary>` matching the Next stage id (e.g. `design-phase`, `analyze`, `grill`, `design`). Design-boundary tokens do **not** unlock high-risk code stages (`tdd-review` / `build` / `fix-*` / `merge`).
