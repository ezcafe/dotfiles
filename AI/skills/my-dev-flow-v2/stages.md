# Stage index (canonical)

**SoT for:** Happy path, Mode × Review profile post-Build, Status vs stage, Slug, Cheap path, Gates.

| Concern | File |
|---------|------|
| Step 0 / Mode / profile | [step-0.md](step-0.md) |
| Resume / abort | [resume.md](resume.md) |
| Design-backloop | [design-backloop.md](design-backloop.md) |
| Preflight / derive | [preflight.md](preflight.md) · [derive-next.md](derive-next.md) · [derive-next-pre.md](derive-next-pre.md) · [derive-next-post.md](derive-next-post.md) |
| HITL / Gate B / Gate C | [hitl.md](hitl.md) · [gate-b.md](gate-b.md) · [gate-c.md](gate-c.md) |
| Results / Verify / Lenses | [results.md](results.md) · [verify.md](verify.md) · [lenses.md](lenses.md) |
| Next → open files | [parent-next.md](parent-next.md) |

**Progress:** ≤5 lines + path after each step; Result header ~40 lines; update card.

## Status vs stage id

| Field | Allowed | Role |
|-------|---------|------|
| **Status** | `running` \| `paused` \| `stopped` \| `done` | Lifecycle only |
| **Last stage** / card **Stage id** | handoffs ids (+ `gate-b` / `gate-c`) | Pipeline position |

**Done:** Status `done` only after Merge Result **success** and `merge` ∈ **Gate C approved**. Abort → `stopped`. PR-only subset → stay `paused`.

**Paused → running:** async Gate B digest, Gate A escalate, Gate B/C AskQuestion, **Grill blocking** (open frontier / Decision N), and other Decision N waits set Status `paused`. Parent restores Status **`running`** on resume / Build arm / post-Decision continue / Grill answers settled — unless still waiting on the user ([resume.md](resume.md) · [grill.md](grill.md) · [gate-b.md](gate-b.md) · [gate-a After](../my-dev-flow-v2-design/stages/gate-a.md)).

**Calibration (after `done`):** append ≤3 lines to `.my-docs/workflow/_calibration.md`: Mode OK? · Review profile OK? · Biggest friction stage?

## Happy path

```mermaid
flowchart LR
  subgraph full [Mode full]
    F0[Step 0] --> F1[Ideation→Gate A→skim]
    F1 --> F2[Analyze→Grill→Design]
    F2 --> F3[design-review API∥DB]
    F3 --> F4[Gate B→Build]
    F4 --> F5{Review profile}
    F5 -->|full| F6[independent Smoke→Adv→Quality→lenses→merge-findings if 2+→test-full→Gate C]
    F5 -->|lite| F7[code-review-phase→lenses→merge-findings if 2+→test-lite→Gate C]
  end
  subgraph simple [Mode simple]
    S0[Step 0] --> S1[design-phase]
    S1 --> S2[design-verify-phase]
    S2 --> S3[Gate B→Build]
    S3 --> S4{Review profile}
    S4 -->|lite| S5[code-review-phase→lenses→merge-findings if 2+→test-lite→Gate C]
    S4 -->|skip-review| S6[Prefer-unpaid→Prefer-paid→else Decision N]
  end
```

### Mode × Review profile → post-Build

| Mode | Review profile | After Build verify-pass + Smoke section |
|------|----------------|------------------------------------------|
| **full** | **full** | independent Smoke Task → `Smoke source: Smoke-Task` → parent Notes companion → Adv → Quality → lenses → `merge-findings` if 2+ → `test-full` → Gate C |
| **full** | **lite** | Skip Smoke Task (Build-writes-Smoke) when `06` matching smoke-pass from Build → `code-review-phase` → lenses per plan → `merge-findings` if 2+ → `test-lite` → Gate C |
| **simple** | **lite** | Same as full+lite |
| **simple** | **skip-review** | Legal only per [lenses.md](lenses.md); ordered recovery ([verify.md](verify.md) Skip-review + Smoke): Prefer-unpaid → Prefer-paid (bar met + `merge` ∈ approved → `merge`; else → `gate-c` — [verify.md](verify.md) Prefer paid); else Decision N ([decisions.md](decisions.md) Skip-review else). Gate C bar: [gate-c.md](gate-c.md) |

**Forbidden:** Mode simple + profile full; Mode full + skip-review; **skip-review** when Has API or Has DB or Has auth/PII/schema = **yes** (drop → lite\|reclassify + Gate B blocking — [lenses.md](lenses.md) · [preflight.md](preflight.md)). Illegal combos are **never** unlocked by `card-override` **or** Decision N (Decision N **cannot** legalize Mode full + skip-review) — reclassify Mode/profile instead. `card-override` is only for Next↔derive mismatch ([derive-next.md](derive-next.md) · [hitl.md](hitl.md)).

### Full pipeline order

1. Step 0 — Mode full; profile full|lite; seed `00-run.md`; [preflight.md](preflight.md#seed-checklist)
2. Ideation (set Has UI)
3. Gate A → `01a` (auto when ok; max 3 rounds)
4. Light skim → `02-skim.md` (fail-closed until `01a` = `ok`)
5. Analyze → Grill → Design (two options); set Has API/DB
6. Design ↔ review until clean — both Has API+DB → same-turn parallel API∥DB when both Isolated API/DB unpaid (missing or Result unpaid/pending)
7. Optional TDD review (`04a`) if planned tests
8. Gate B — [gate-b.md](gate-b.md) (Mode full = blocking)
9. Build → verify-pass + Smoke section (max 3)
10. Post-Build per table above
11. Review ⇄ Fix (max 3) → Test ⇄ Fix (max 3)
12. Gate C blocking → merge → `done`

### Simple pipeline order

1. Step 0 — Mode simple; profile lite|skip-review; bootstrap `01-idea` if needed ([step-0.md](step-0.md) · [handoffs.md](handoffs.md))
2. `design-phase` (Analyze+Grill+Design)
3. `design-verify-phase` until clean (max 3)
4. Optional 04a → Gate B → Build (Gate B: auto only if API=no DB=no auth/PII/schema=no; else blocking)
5. After Build verify-pass + Smoke section:
   - **(a) skip-review** — ordered recovery per [verify.md](verify.md) Skip-review + Smoke: Prefer-unpaid → Prefer-paid (bar met + `merge` ∈ approved → `merge`; else → `gate-c` — [verify.md](verify.md) Prefer paid); else Decision N ([decisions.md](decisions.md) Skip-review else). Gate C bar: [gate-c.md](gate-c.md)
   - **(b) lite** — Skip Smoke Task when Build-writes-Smoke matching smoke-pass → `code-review-phase` → lenses per plan → `merge-findings` if 2+ → `test-lite` → Gate C
6. Merge → `done` + calibration

## Slug

`YYYYMMDD-feature-x` (UTC + kebab). Folder: `.my-docs/workflow/<slug>/`.

## Cheap path

| Ask looks like | Mode | Review profile |
|----------------|------|----------------|
| Copy / token / docs-only | simple | skip-review |
| Bug fix / one helper / tiny UI | simple | lite |
| Clear small feature, no new auth/schema | simple | lite |
| New/changed public API or persistence | **full** (unless [tiny tweak](lenses.md)) | never skip-review |
| Ambiguous / invent *what* | full or [myplan / invent-*what*](step-0.md) first | full |

## Gates

| Gate | When | Who | User reading guide (parent pastes when asking) |
|------|------|-----|------------------------------------------------|
| **A** | After Ideation (full) | Auto when `01a` ok; human on escalate / max-3 | [gate-a.md](../my-dev-flow-v2-design/stages/gate-a.md) **Read before you decide** |
| **B** | After design clean (+04a Result **clean** or Notes `04a skipped`; **not** on `needs more tests` alone); before Build | HITL ([gate-b.md](gate-b.md)) | [gate-b.md](gate-b.md) **Read before you decide** |
| **C** | Before commit/push/PR/merge | Always blocking ([gate-c.md](gate-c.md)) | [gate-c.md](gate-c.md) **Read before you decide** |
