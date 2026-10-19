# Grill — stress-test the plan

Adapted from [mattpocock grilling](https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md): design tree + frontier rounds.

## Goal

Interview until shared understanding. Map decisions as a **design tree**. Work in **rounds**. The **frontier** is every decision whose prerequisites are settled.

## Round format

```
❓ **Q1** - **<title>**: <body; choices OK>

➡️ <recommended answer>

---

❓ **Q2** - ...
```

Word questions so **"yes" accepts the recommendation**. Ask the **whole frontier** in one round; wait for answers before the next.

Finding **facts** is the agent's job (dispatch explore). Finding **decisions** is the user's.

## Done when

**Grill closed** = Notes `grill-skip` (parent-only + provenance) **or** `02b` Result `frontier-empty` only. Template / mid-write Result **`pending`** is **not** Done. Result `skipped` is **not** a paying close token (invent-waive ban — use Notes `grill-skip` via parent).

## grill-skip ownership (parent-only)

**Who writes:** Parent alone writes Notes `grill-skip` or preferred `grill skipped — <reason>` + provenance `grill-skip` ([hitl.md](hitl.md)). Stages / Tasks return **`candidate grill-skip`** only — **ban** Task writes of grill-skip Notes **and** ban Task Result `skipped` as a waive.

**Provenance:** user quote ≥12 chars **or** evidence of user skip grill.

## Grill open (derive)

**Grill unpaid** = no `02b-grill.md` **and** ¬Notes `grill-skip` (e.g. `grill skipped — <reason>`). Mode **full** / Mode simple **mid-open:** missing `02b` alone is unpaid — do **not** jump to Design ([derive-next.md](derive-next.md)). Mode **simple** true cold start: Prefer `design-phase` while Grill unpaid — do **not** fight the cold-start carve table below.

**Grill open** = ¬Notes `grill-skip` **and** (no `02b` **or** `02b` Result ≠ `frontier-empty`). Notes `grill-skip` closes even when `02b` is `pending`/`needs-round`. Template **`pending` alone does not close Grill.** Result `skipped` alone does **not** close.

**Grill closed** = ¬ **Grill open** = Notes `grill-skip` **or** Result `frontier-empty`.

**Mode full Prefer:** **Grill open** → Expected Next **`grill`** — first-match **before** ¬ Design present → `design` ([derive-next.md](derive-next.md) Pre-Build). Execution: Task `grill` **or** parent apply into `02b`; card Next stays `grill` until closed.

### Mode simple cold-start carve (SoT — one table)

| Condition | Prefer |
|-----------|--------|
| **cold-start carve** = none of {`02-analysis`, `03`, `04`} on disk **and** (**Grill unpaid** ∨ **Grill closed** / Notes `grill-skip`) | `design-phase` — **not** `design-verify-phase` |
| **Grill open** ∧ ¬ cold-start carve | `grill` — ban re-`design-phase` (mid-open ≡ full **Grill open**: invent Result `skipped`, any Result ≠ `frontier-empty` without Notes `grill-skip` — not only artifacts∨`needs-round`|`pending`) |
| **Grill open** + none of {`02-analysis`, `03`, `04`} on disk (true cold start) | only when **Grill unpaid** → carve → `design-phase` allowed; if `02b` exists with Result ≠ `frontier-empty` → ¬carve → Prefer `grill` |

Step 0 seeds **only** `00-run.md` — stubs never count as artifacts — [step-0.md](step-0.md). **Cold start** ≠ ¬(all three present): a partial set is mid-run / incomplete Design. Elsewhere: one-line pointer to this table — do not restate the carve.

**Mode simple Prefer / FIRST / unsafe-jump:** Prefer `grill` when **Grill open** ∧ ¬ cold-start carve; else carve → Prefer `design-phase` while ¬ Design present when carve allows.

**Mode full + Notes `design-stale`:** stay Pre-Build; Prefer **Grill open** → `grill` first (same close: Notes `grill-skip` **or** Result `frontier-empty`); then unpaid among **Analyze unpaid** → **Grill unpaid** → **design unpaid under design-stale** — do **not** Prefer `design` while Grill open; do **not** Prefer Isolated / design-review / design-verify / design-update / gate-b / build while stale ([derive-next.md](derive-next.md) · [step-0.md](step-0.md)).

## Prefer / fail-closed

- Do **not** start `design` / design-review / `design-verify-phase` / gate-b / build while **Grill open** (both Modes).  
- Mode simple `design-phase` ban/allow — cold-start carve table above.  
- Async-notify tier: stay `running`; settle frontier same turn — do **not** treat “continue” as advance to Design.
