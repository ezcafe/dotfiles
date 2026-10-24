# Derive next — Pre-Build (first-match)

Load with Unsafe jumps from [derive-next.md](derive-next.md) + Definitions from [derive-next-defs-pre.md](derive-next-defs-pre.md). First-match wins among concrete Next cells; fall-through meta-rows do **not** consume first-match ([derive-next.md](derive-next.md)).

| State | Expected Next |
|-------|---------------|
| Status `done` \| `stopped` | Stop |
| **paused-wait** (Status `paused` ∧ (Build armed unpaid on async path ∨ Gate C approved non-empty without `merge` ∨ Notes `waiting — <reason>` — parent **or** labeled solo set+clear ([hitl.md](hitl.md) · [solo-entry.md](solo-entry.md); Stages return `candidate waiting — …` only))) | Stop — stay paused ([resume.md](resume.md)). Do **not** Prefer `gate-b` again while async-notify pause |
| Status `paused` ∧ ¬ **paused-wait** | *(fall-through — evaluate next Prefer row; re-derive next unpaid; do **not** invent Notes `waiting — <reason>` — parent **or** labeled solo only)* |
| Mode simple ∧ Notes `design-stale` | Decision N — Upgrade to Mode full required before design-stale Prefer ([step-0.md](step-0.md) · [hitl.md](hitl.md)); ban Prefer `design` / design-stale unpaid path on simple card |
| **ideation unpaid** (both Modes) | `ideation` — before Gate A / `design-phase` |
| Mode full, unpaid Gate A | `gate-a` |
| Mode full, unpaid skim | `skim` |
| Mode full ∧ (Notes `design-stale` / **design-stale unpaid**) | Prefer **Grill open** → `grill` first (close: Notes `grill-skip` **or** Result `frontier-empty` only); then first unpaid among **Analyze unpaid** → **Grill unpaid** → **design unpaid under design-stale** (checkable — [derive-next.md](derive-next.md); do **not** Prefer Isolated / design-review / design-verify / `design-update` / require design-update Run-log; ban `design` while Grill still open). Mode simple ∧ design-stale → row above (Decision N) — never this Prefer |
| Mode full, **Analyze unpaid** | `analyze` |
| Mode full, **Grill open** | `grill` — **before** ¬ Design present → `design` **and** before design-backloop → `design-update` |
| Mode simple, **Grill open** ∧ ¬ **cold-start carve** | `grill` — mid-open ≡ full **Grill open**; carve SoT [grill.md](grill.md) |
| Notes `design-backloop` + (design-update unpaid **or** design-review not clean) | Prefer unpaid `design-update` while unpaid **and** **Grill closed**; else (design-update paid) Mode full: unpaid Isolated → else `design-review`. Mode simple: `design-verify-phase` only. While **Grill open** → Prefer `grill` first (row above) |
| Mode simple, ¬ ideation unpaid, ¬ Design present (cold start carve — [grill.md](grill.md); also incomplete Design) | `design-phase` |
| Any `03a*` Result **`needs update`** **or** **backloop rewrite unpaid** | `design-update` — only when **Grill closed** (else Prefer `grill`) |
| Mode simple, Design present, design-review not clean | `design-verify-phase` |
| Mode full, ¬ Design present | `design` |
| Mode full, Design present, Isolated unpaid | Prefer unpaid `api-contract-review` / `db-design-review` (both unpaid → Next `api\|db`; Pending parallel) |
| Mode full, Design present, design-review not clean | `design-review` |
| Design clean, **04a unpaid / dirty** | `tdd-review` — only when unpaid/dirty (not when ¬ planned tests present) |
| Design clean ∧ **04a ok** (¬ unpaid / dirty), Gate B not settled | `gate-b` |
| Notes `design-backloop` + Design clean ∧ **04a ok** + **Gate B settled post-Notes** | Clear Notes same turn → Prefer `build` (settle Run-log **after** Notes — [gate-b.md](gate-b.md) · [design-backloop.md](design-backloop.md); auto Prefer must **not** Prefer `build` until this clear) |
| Notes `design-backloop` + Design clean ∧ **04a ok** (¬ **Gate B settled post-Notes** — even if an old settle still matches) | `gate-b` — do **not** Prefer `build` / clear Notes on pre-Notes settle ([gate-b.md](gate-b.md) Prefer after settle) |
| Design clean ∧ **04a ok**, Gate B settled (Notes cleared / no `design-backloop`) | `build` |
| *(unmatched — no Prefer row above)* | Decision N ([failure.md](failure.md) · [decisions.md](decisions.md)) — do **not** invent Next |
