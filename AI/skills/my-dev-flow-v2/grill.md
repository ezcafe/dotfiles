# Grill

Stress-test the design tree after Analyze (before Design). HITL Grill ≠ Gate B.

## When

- Mode full standalone `grill` stage, or inside simple `design-phase` when frontier open / Has API/DB.
- Solo: `grill` / `stress-test this plan` with Analyze or `01-idea` present.

## Grill open (derive)

**Grill open** = Result **`needs-round`** **or** **unpaid Grill**.

**Unpaid Grill** = no `02b-grill.md` **and** no Notes grill-skip (e.g. `grill skipped — <reason>`). Missing `02b` alone is unpaid — do **not** jump to Design ([derive-next.md](derive-next.md)).

**Mode simple Prefer:** **Grill open** **and** (design artifacts present **or** `02b-grill.md` exists with Result **`needs-round`**) → Expected Next always **`grill`** until Result **`frontier-empty`** \| **`skipped`** or Notes grill-skip. Execution may be Task `grill` **or** parent apply into `02b`; card Next stays `grill` until Grill closed. Prefer `design-phase` on Grill open **only** for true cold start: no `02b` **needs-round** **and** no design artifacts → fall through to Prefer `design-phase` ([derive-next.md](derive-next.md) · [derive-next-pre.md](derive-next-pre.md)).

**Mode full + Notes `design-stale`:** stay Pre-Build; Mode-full first-match pays Gate A / skim if unpaid, then Prefer first unpaid among `analyze` → `grill` → `design` only — do **not** match Grill open / paid Mode-simple analysis, and do **not** Prefer API∥DB / design-review / gate-b / build while `design-stale` ([derive-next-pre.md](derive-next-pre.md) · [step-0.md](step-0.md)).

## Output (`02b-grill.md`)

- Frontier questions (assumptions, failure modes, glossary gaps).
- Settled answers → update analysis Design tree when needed.
- May update repo `GLOSSARY.md` / one ADR when present.
- Result: `frontier-empty` \| `needs-round` \| `skipped`.

Do **not** start Design / design-review / `design-verify-phase` / Gate B / Build on **Grill open** (`needs-round` or unpaid Grill) — both Modes. Ban `design-phase` on Grill open when design artifacts present **or** `02b` Result **`needs-round`**; allow Prefer `design-phase` **only** on true cold start (no `02b` needs-round and no design artifacts) ([derive-next.md](derive-next.md) Unsafe jumps).

## HITL Grill default

| Mode | Tier |
|------|------|
| full | async-notify (post digest; stay running; settle frontier same turn — do not advance to Design while Grill open) — [After](#after-parent) |
| simple | auto |

Blocking Grill only when user asks or open Critical risk needs a pause.

## After (parent)

| HITL Grill | Result **`needs-round`** |
|------------|--------------------------|
| **blocking** | Set Status **`paused`**; card **Next** = `grill` (do not advance to Design). Paste Grill digest + open questions; wait for human answers. After answers: re-run Task `grill` or parent applies answers into `02b` / analysis (card Next stays `grill` until Grill closed); set Status **`running`** and continue only when Result is **`frontier-empty`** or **`skipped`**. |
| **async-notify** | Do **not** treat digest-posted as settled. Parent user-first settles remaining frontier into `02b` (or re-run `grill`) until **`frontier-empty`** / **`skipped`** before Design / design-review / `design-verify-phase` / Gate B / Build. Mode simple: Grill open **and** (design artifacts present **or** `02b` **needs-round**) → Expected Next always **`grill`** (Task or parent apply); Prefer `design-phase` only on true cold start (no `02b` needs-round and no design artifacts) — [derive-next-pre.md](derive-next-pre.md). |
| **auto** | Same settle path as async-notify (should be rare if Task honored auto) — parent settles or re-runs; card Next stays `grill` until Grill closed; never advance on open **`needs-round`**. |

See [stages.md](stages.md) Status · [resume.md](resume.md) still-waiting · [hitl.md](hitl.md) · design stage [grill After](../my-dev-flow-v2-design/stages/grill.md).
