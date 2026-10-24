# Grill — stress-test the plan

Adapted from [mattpocock grilling](https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md): design tree + frontier rounds.

## Goal

Interview until shared understanding. Map decisions as a **design tree**. Work in **rounds**. The **frontier** is every decision whose prerequisites are settled.

## HITL channel (orchestrated vs solo)

| Path | How questions reach the user |
|------|------------------------------|
| **Orchestrated** (parent spawned Task) | **Parent-relay** — Task never AskQuestion. Write frontier Qs into `02b-grill.md` + Return `Blocked / questions for user`. Hard-stop (`hitl:grill-frontier` or `hitl:grill-skip`). Parent presents; stamps Notes; re-spawns ([hitl.md](hitl.md) · [spawn-contract.md](spawn-contract.md)) |
| **Solo** | Direct conversation OK — end each message with one question; wait for answers before the next round; async-notify may stay `running` and settle frontier same turn |

## Round format

```
❓ **Q1** - **<title>**: <body; choices OK>

➡️ <recommended answer>

---

❓ **Q2** - ...
```

Word questions so **"yes" accepts the recommendation**. Ask the **whole frontier** in one round.

Finding **facts** is the agent's job (dispatch explore). Finding **decisions** is the user's.

## Done when

**Grill closed** / **Grill open** / **Grill unpaid** — Definitions SoT: [derive-next-defs-pre.md](derive-next-defs-pre.md). Template / mid-write Result **`pending`** is **not** Done. Result `skipped` is **not** a paying close token (invent-waive ban — use Notes `grill-skip` via parent after Parent-relay **or** labeled solo after AskQuestion — [hitl.md](hitl.md) · [solo-entry.md](solo-entry.md)).

## grill-skip ownership

| Path | Who writes Notes+provenance |
|------|-----------------------------|
| **Orchestrated** (parent spawned Task) | **Parent alone** after Parent-relay. Stages / Tasks return **`candidate grill-skip`** only — **ban** Task writes of grill-skip Notes **and** ban Task Result `skipped` as a waive ([hitl.md](hitl.md)) |
| **Labeled solo** | Solo stamps Notes `grill-skip` / preferred `grill skipped — <reason>` + provenance **after AskQuestion** ([solo-entry.md](solo-entry.md) · [hitl.md](hitl.md) labeled solo carve) |

**Provenance:** user quote ≥12 chars **or** evidence of user skip grill.

## Grill open (derive)

Prefer while **Grill open** / **Grill unpaid** — name+link only; cells in [derive-next-defs-pre.md](derive-next-defs-pre.md) · Prefer rows [derive-next-pre.md](derive-next-pre.md).

**Mode full Prefer:** **Grill open** → Expected Next **`grill`** — first-match **before** ¬ Design present → `design`. Execution: Task `grill` (Parent-relay) **or** solo apply into `02b`; card Next stays `grill` until closed.

### Mode simple cold-start carve (SoT — one table)

| Condition | Prefer |
|-----------|--------|
| **cold-start carve** = none of {`02-analysis`, `03`, `04`} on disk **and** (**Grill unpaid** ∨ **Grill closed** / Notes `grill-skip`) | `design-phase` — **not** `design-verify-phase` |
| **Grill open** ∧ ¬ cold-start carve | `grill` — ban re-`design-phase` (mid-open ≡ full **Grill open**: invent Result `skipped`, any Result ≠ `frontier-empty` without Notes `grill-skip` — not only artifacts∨`needs-round`|`pending`) |
| **Grill open** + none of {`02-analysis`, `03`, `04`} on disk (true cold start) | only when **Grill unpaid** → carve → `design-phase` allowed; if `02b` exists with Result ≠ `frontier-empty` → ¬carve → Prefer `grill` |

Step 0 seeds **only** `00-run.md` — stubs never count as artifacts — [step-0.md](step-0.md). **Cold start** ≠ ¬(all three present): a partial set is mid-run / incomplete Design. Elsewhere: one-line pointer to this table — do not restate the carve.

**Mode simple Prefer / FIRST / unsafe-jump:** Prefer `grill` when **Grill open** ∧ ¬ cold-start carve; else carve → Prefer `design-phase` while ¬ Design present when carve allows.

**Mode full + Notes `design-stale`:** stay Pre-Build; Prefer **Grill open** → `grill` first, then unpaid among **Analyze unpaid** → **Grill unpaid** → **design unpaid under design-stale** — [derive-next-defs-pre.md](derive-next-defs-pre.md) · [step-0.md](step-0.md).

## Prefer / fail-closed

- Do **not** start `design` / design-review / `design-verify-phase` / gate-b / build while **Grill open** (both Modes).  
- Mode simple `design-phase` ban/allow — cold-start carve table above.  
- **Orchestrated:** Parent-relay each frontier round — do **not** treat Task “continue” as advance to Design.  
- **Solo:** async-notify may stay `running`; settle frontier same turn — still do **not** advance to Design while Grill open.
