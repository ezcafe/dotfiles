# Grill

Stress-test the design tree after Analyze (before Design). HITL Grill ≠ Gate B.

## When

- Mode full standalone `grill` stage, or inside simple `design-phase` when frontier open / Has API/DB.
- Solo: `grill` / `stress-test this plan` with Analyze or `01-idea` present.

## Output (`02b-grill.md`)

- Frontier questions (assumptions, failure modes, glossary gaps).
- Settled answers → update analysis Design tree when needed.
- May update repo `GLOSSARY.md` / one ADR when present.
- Result: `frontier-empty` \| `needs-round` \| `skipped`.

Do **not** start Design on `needs-round`.

## HITL Grill default

| Mode | Tier |
|------|------|
| full | async-notify (post digest; continue) |
| simple | auto |

Blocking Grill only when user asks or open Critical risk needs a pause.
