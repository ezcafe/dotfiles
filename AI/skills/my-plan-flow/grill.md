# Grill (inside my-plan-flow)

Design-tree frontier interview + domain modeling. Adapted from
[mattpocock/skills grill-with-docs](https://github.com/mattpocock/skills/tree/main/skills/engineering/grill-with-docs),
[grilling](https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md), and
[domain-modeling](https://github.com/mattpocock/skills/blob/main/skills/engineering/domain-modeling/SKILL.md).

**Where it runs:** after Analyze, before Design (`my-design-subflow` Step 2g).
May also run alone when the user says `grill`, `grill-with-docs`, or
`stress-test this plan`.

Also follow [`documentation-and-adrs`](../documentation-and-adrs/SKILL.md) for ADR
file location and the three-part ADR bar. Artifact template: [templates.md](templates.md)
→ `02b-grill.md`. Stage prompt: [`../my-design-subflow/stages.md`](../my-design-subflow/stages.md)
→ **2g. Grill**.

## Goal

Reach a **shared understanding** of open design decisions, then capture durable
**domain language** (glossary) and **hard-to-reverse choices** (sparse ADRs).

**HITL:** Prefer **auto** (user-first picks on recommended answers). Honor
`00-run.md` **HITL Gate B** when present: `auto` / `async-notify` → settle
recommendations and continue; `blocking` → post frontier round and wait.

## Facts vs decisions

- **Facts** (repo paths, existing APIs, current behavior): look them up yourself
  or dispatch exploration. Never ask the user for look-up-able facts.
- **Decisions** (product/tech trade-offs): put on the frontier with a
  **Recommendation**, then settle per HITL.

## Design tree + frontier

Map the plan as a **design tree**: each decision branches into decisions that
depend on it.

- **Frontier** = every open decision whose prerequisites are already settled.
- Ask (or auto-settle) the **whole frontier** in one round — never a question
  that depends on another answer still open in the same round.
- After a round, recompute the frontier. Done when the frontier is **empty**.

### Round format (chat or `02b-grill.md`)

```markdown
❓ **Q1** — **<title>**: <body; include Option choices when 2+>

➡️ Recommended: <Option N or short answer> — user-first: <one line>

---

❓ **Q2** — **<title>**: …
➡️ Recommended: …
```

When presenting 2+ choices in chat, also use my-plan-flow **Decision N** shape
(What / Example / Pros / Cons / Recommendation).

### Scenario stress-test (required when domain boundaries matter)

Invent 1–3 concrete edge scenarios that force precise boundaries
(e.g. offline then reconnect; two caregivers; partial failure). Record outcomes
under Settled or Open in `02b-grill.md`.

### Code cross-check

When the user (or idea) states how something works, check the code. If they
disagree, surface it as a frontier question — do not silently pick one.

## Domain modeling (inline)

### Glossary

- If `GLOSSARY-MAP.md` exists at repo root, use it to find the right context
  `GLOSSARY.md`. Else use root `GLOSSARY.md` (create lazily on first term).
- When a term is resolved, **update the glossary immediately** — do not batch.
- Definitions: 1–2 sentences; what it **is**, not how it is implemented.
- Be opinionated: pick one canonical word; list aliases under `_Avoid_:`.
- Only project-specific terms — not generic programming vocabulary.

Example entry:

```markdown
**Offline mode**:
Care logging stored in the device iCloud container without a live API session.
_Avoid_: Sample mode, local mode
```

### ADRs (sparse)

Offer / write an ADR **only when all three** are true:

1. **Hard to reverse** — changing later is costly
2. **Surprising without context** — a future reader will wonder why
3. **Real trade-off** — genuine alternatives existed

Prefer a **short** ADR (1–3 sentences: context, decision, why). Match existing
repo ADR location (`docs/adr/`, `docs/decisions/`, …). If none, use
`docs/decisions/ADR-NNN-short-title.md`. See `documentation-and-adrs`.

Skip ADRs for easy-to-reverse or obvious choices. Record “ADR skipped — …” in
`02b-grill.md` when a tempting decision fails the three-part bar.

## When to run vs skip

| Run grill | Skip grill |
|-----------|------------|
| Mode **full** after Analyze | Mode **simple** and Analyze Design tree frontier is empty and no Build-critical open branches |
| Mode **simple** when Analyze lists open frontier / unsettled Decisions | Review profile **skip-review** copy/token-only with no behavior decisions |
| User says grill / stress-test the plan | Resume when `02b-grill.md` Result is already `frontier-empty` and artifacts unchanged |

On skip: parent Notes `grill skipped — <reason>`; do **not** invent empty theater rounds.

## Outputs (workflow slug)

Write `.my-docs/workflow/<slug>/02b-grill.md` (template in [templates.md](templates.md)).
Optionally update:

- Repo `GLOSSARY.md` (or mapped context glossary)
- ADR file when the three-part bar passes
- `02-analysis.md` Settled decisions + Design tree (mark frontier empty)

**Result values:** `frontier-empty` | `needs-round` | `skipped`

## Completion

- **frontier-empty** — every branch visited; no silent assumptions left for Design.
- Parent may **auto-approve** and continue to Design (default). Post a short
  **Grill digest** (≤4 bullets): settled picks, glossary/ADR touches, residual risk.
- **needs-round** only when HITL is **blocking** and human answers are required,
  or when facts are still loading from a subagent (unblock other frontier items).

## Do not

- Do not start Design while Result is `needs-round`.
- Do not re-litigate Gate A 80/20 (product day-to-day) — grill settles **design**
  branches under that lock.
- Do not put implementation paths or file lists in the glossary.
- Do not write production feature code in this stage.
