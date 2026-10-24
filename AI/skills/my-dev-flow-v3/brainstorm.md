# Brainstorm — shared understanding before Design

Adapted from [obra/superpowers brainstorming](https://github.com/obra/superpowers/blob/main/skills/brainstorming/SKILL.md).

## Hard-gate (always)

**Nothing gets designed or built** until the user confirms shared understanding of intent (in chat for small work; written framing for larger). Applies to **Mode full and Mode simple** — not Has-UI-only. Exceptions: user opts out of questions / throwaway spike they approved → parent writes Notes `ideation-skip` / preferred `ideation skipped — <reason>` + provenance (user quote ≥12 chars or evidence) — bare chat skip alone is **not** Done ([hitl.md](hitl.md)).

**ideation unpaid** — Definition SoT: [derive-next-defs-pre.md](derive-next-defs-pre.md). Prefer **`ideation`** until paid (both Modes) — before Gate A / skim / Analyze / `design` / `design-phase` ([derive-next.md](derive-next.md) Unsafe jumps). Stages `gate-a` / `skim` / `analyze` / `design` / `design-phase` FIRST → `blocked — ideation unpaid` when unpaid.

**Paid (durable):** Notes `ideation-confirmed` + provenance `ideation-confirmed` with `user: "<exact words ≥12 chars>"` (or Notes `ideation-skip` + provenance) — parent after Parent-relay **or** labeled solo after AskQuestion ([hitl.md](hitl.md)). Chat confirmation alone / file `01-idea` alone is **not** paid.

## HITL channel (orchestrated vs solo)

| Path | How questions reach the user |
|------|------------------------------|
| **Orchestrated** (parent spawned Task) | **Parent-relay** — Task never AskQuestion. Write the open question into `01-idea.md` (or draft) + Return `Blocked / questions for user`. Hard-stop (`hitl:ideation` / `hitl:ideation-confirm` / `hitl:ideation-skip`). Parent presents; stamps Notes; re-spawns ([hitl.md](hitl.md) · [spawn-contract.md](spawn-contract.md)) |
| **Solo** | Direct conversation OK — end each message with **one** question; play back ~200–300 words when a chunk is clear |

## ideation-confirmed / ideation-skip ownership

| Path | Who writes Notes+provenance |
|------|-----------------------------|
| **Orchestrated** (parent spawned Task) | **Parent alone** after Parent-relay. Stages / Tasks return **`candidate ideation-confirmed`** or **`candidate ideation-skip`** only — **ban** Task writes ([hitl.md](hitl.md)) |
| **Labeled solo** | Solo stamps Notes+provenance **after AskQuestion** — pays ideation without a separate parent ([solo-entry.md](solo-entry.md) · [hitl.md](hitl.md) labeled solo carve) |

**Provenance:** `ideation-confirmed` → user quote ≥12 chars; `ideation-skip` → user quote ≥12 chars **or** evidence of user skip ideation / approved throwaway spike.

## First message pattern

1. Offer skip: they can say “just start” → parent Notes `ideation-skip` + provenance (not bare Done); then state significant how-it-gets-made choices in one line.  
2. One open question that gets them **describing** (a real moment, not a menu).

## Conversation rules (solo; orchestrated Task writes into artifact)

- End each turn with **one** question (no example-answer laundry lists).  
- Play back ~200–300 words when a chunk is clear; mark guesses.  
- Size the work: quick task / small change / project with written design.  
- For projects: write framing under `.my-docs/workflow/<slug>/01-idea.md` (goals, non-goals, anti-goals, constraints).

## Hand-off

When understanding is confirmed → stamps Notes `ideation-confirmed` + provenance (parent after Parent-relay **or** labeled solo after AskQuestion) → Mode **full:** Gate A → skim → Analyze → Grill → Design (**Grill closed** before Design — [grill.md](grill.md)). Mode **simple:** enter `design-phase` (Analyze+Grill+Design bundled) while Grill unpaid on true cold start (cold-start carve — [grill.md](grill.md)). **Grill closed** applies after mid-open / Mode full — not as a ban on Mode simple cold-start `design-phase`.

**Waive Ideation:** user skip ideation / approved throwaway → Notes `ideation-skip` / `ideation skipped — <reason>` + provenance (parent **or** labeled solo) — orchestrated Stages return `candidate ideation-skip` only; Tasks never write ([hitl.md](hitl.md)).

**Confirm Ideation:** after shared understanding → orchestrated Stages return `candidate ideation-confirmed`; parent **or** labeled solo writes Notes `ideation-confirmed` + provenance — Tasks never write ([hitl.md](hitl.md)).

**Waive Grill:** user skip grill → Notes `grill-skip` / `grill skipped — <reason>` + provenance (parent **or** labeled solo) — orchestrated Stages return `candidate grill-skip` only; Tasks never write ([hitl.md](hitl.md) · [grill.md](grill.md)).
