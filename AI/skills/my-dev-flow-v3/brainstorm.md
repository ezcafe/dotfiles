# Brainstorm — shared understanding before Design

Adapted from [obra/superpowers brainstorming](https://github.com/obra/superpowers/blob/main/skills/brainstorming/SKILL.md).

## Hard-gate (always)

**Nothing gets designed or built** until the user confirms shared understanding of intent (in chat for small work; written framing for larger). Applies to **Mode full and Mode simple** — not Has-UI-only. Exceptions: user opts out of questions / throwaway spike they approved → parent writes Notes `ideation-skip` / preferred `ideation skipped — <reason>` + provenance (user quote ≥12 chars or evidence) — bare chat skip alone is **not** Done ([hitl.md](hitl.md)).

**ideation unpaid** = ¬Notes `ideation-skip` **and** ¬Notes `ideation-confirmed`. Prefer **`ideation`** until paid (both Modes) — before Gate A / skim / Analyze / `design` / `design-phase` ([derive-next.md](derive-next.md) Unsafe jumps). Stages `gate-a` / `skim` / `analyze` / `design` / `design-phase` FIRST → `blocked — ideation unpaid` when unpaid.

**Paid (durable):** parent stamps Notes `ideation-confirmed` + provenance `ideation-confirmed` with `user: "<exact words ≥12 chars>"` (or Notes `ideation-skip` + provenance). Chat confirmation alone / file `01-idea` alone is **not** paid.

## ideation-confirmed / ideation-skip ownership (parent-only)

**Who writes:** Parent alone writes Notes `ideation-confirmed` or `ideation-skip` / preferred `ideation skipped — <reason>` + matching provenance ([hitl.md](hitl.md)). Stages / Tasks return **`candidate ideation-confirmed`** or **`candidate ideation-skip`** only — **ban** Task writes of those Notes.

**Provenance:** `ideation-confirmed` → user quote ≥12 chars; `ideation-skip` → user quote ≥12 chars **or** evidence of user skip ideation / approved throwaway spike.

## First message pattern

1. Offer skip: they can say “just start” → parent Notes `ideation-skip` + provenance (not bare Done); then state significant how-it-gets-made choices in one line.  
2. One open question that gets them **describing** (a real moment, not a menu).

## Conversation rules

- End each message with **one** question (no example-answer laundry lists).  
- Play back ~200–300 words when a chunk is clear; mark guesses.  
- Size the work: quick task / small change / project with written design.  
- For projects: write framing under `.my-docs/workflow/<slug>/01-idea.md` (goals, non-goals, anti-goals, constraints).

## Hand-off

When understanding is confirmed → parent stamps Notes `ideation-confirmed` + provenance → Mode **full:** Gate A → skim → Analyze → Grill → Design (**Grill closed** before Design — [grill.md](grill.md)). Mode **simple:** enter `design-phase` (Analyze+Grill+Design bundled) while Grill unpaid on true cold start (cold-start carve — [grill.md](grill.md)). **Grill closed** (Notes `grill-skip` **or** Result `frontier-empty` only) applies after mid-open / Mode full — not as a ban on Mode simple cold-start `design-phase`.

**Waive Ideation:** user skip ideation / approved throwaway → parent writes Notes `ideation-skip` / `ideation skipped — <reason>` + provenance (user quote ≥12 chars or evidence) — Stages return `candidate ideation-skip` only; Tasks never write ([hitl.md](hitl.md)).

**Confirm Ideation:** after shared understanding → Stages return `candidate ideation-confirmed`; parent writes Notes `ideation-confirmed` + provenance — Tasks never write ([hitl.md](hitl.md)).

**Waive Grill:** user skip grill → parent writes Notes `grill-skip` / `grill skipped — <reason>` + provenance (user quote ≥12 chars or evidence) — Stages return `candidate grill-skip` only; Tasks never write ([hitl.md](hitl.md) · [grill.md](grill.md)).
