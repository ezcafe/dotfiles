# Conditional lenses — API / DB / Security / Performance / Memory

**When:** After Quality / Lite combined (`code-review-phase`) is clean **and** `00-run.md` **Lens plan** is not `none`. **Parent always owns** lenses: launch **only** lenses listed in Lens plan as isolated `lens-*` Tasks (parallel when 2+). `code-review-phase` / Quality may note lens signals but must **not** write `05-lens-*.md` or mark lenses paid.

**Plan=`none` / forced api/db:** When Has API/DB ∈ {yes, unknown} ∧ ¬tiny ∧ (plan=`none` **or** missing required `api`/`db`) → Prefer `finalize-lens-plan` (parent-inline **or** labeled solo as orchestrator — not a Task) **before Smoke and before Adv** — **not** Prefer-re-smoke / unpaid Smoke / Adv / lenses / `test-*` ([derive-next-post.md](../../my-dev-flow-v3/derive-next-post.md) · [lenses.md](../../my-dev-flow-v3/lenses.md) · [solo-entry.md](../../my-dev-flow-v3/solo-entry.md) · [hitl.md](../../my-dev-flow-v3/hitl.md)). Only go to test when **Lenses clean** vacuous: plan=`none` **and** no required api/db (Has API/DB = no, or Notes `tiny-contract-tweak` — [lenses.md](../../my-dev-flow-v3/lenses.md)).

Auto-add **api** / **db** only per `{my-dev-flow-v3}/lenses.md` — **not** when Notes `tiny-contract-tweak`. Missing required api/db → Prefer `finalize-lens-plan` (parent-inline **or** labeled solo as orchestrator — not a Task) before Smoke **and** Adv.

**R/W:** each lens writes **only** its own `05-lens-*.md` (never `05-review-log.md` — avoids parallel write races). Handoff row: `{my-dev-flow-v3}/handoffs.md` `lens-*`.

**After (parent):**

| Plan | After |
|------|-------|
| **2+** (parallel) | Wait all siblings. Any planned lens **`needs fix`** → Prefer `fix-review` Mode `merged-lenses`. Prefer `merge-findings` only when planned lenses **clean** **and** Merged unpaid |
| **1** | Parent copies lens Result into `05-review-log.md` Merged lenses as `clean` \| `needs fix`; needs fix → `fix-review` Mode `plan-1-lens` |
| Serial | Next unpaid `lens-*` only when parent chose serial |

**FIRST-LINE Result** (every lens Task): `Result: clean | needs fix` then path to `05-lens-*.md`.

Prefer / dirty / clean predicates: `{my-dev-flow-v3}/derive-next.md` · `{my-dev-flow-v3}/lenses.md` (do not contradict).

### Ban-when (Task / solo cheat — shared for all `lens-*`)

Not Prefer Next lookup. After Result → **Hard stop**; parent re-derives ([derive-next-post.md](../../my-dev-flow-v3/derive-next-post.md)).

| Ban when | Do not Prefer |
|----------|---------------|
| any planned lens **`needs fix`** | `merge-findings` / `test-*` / `gate-c` / `merge` |
| planned lenses not all **clean** (plan 2+) | `merge-findings` |
| plan **1** | invent Merged — parent copies Result into Merged |

| Lens | Stage id | Open | Output file |
|------|----------|------|-------------|
| API | `lens-api` | [lens-api.md](lens-api.md) | `.my-docs/workflow/<slug>/05-lens-api.md` |
| DB | `lens-db` | [lens-db.md](lens-db.md) | `.my-docs/workflow/<slug>/05-lens-db.md` |
| Security | `lens-security` | [lens-security.md](lens-security.md) | `.my-docs/workflow/<slug>/05-lens-security.md` |
| Performance | `lens-perf` | [lens-perf.md](lens-perf.md) | `.my-docs/workflow/<slug>/05-lens-perf.md` |
| Memory | `lens-memory` | [lens-memory.md](lens-memory.md) | `.my-docs/workflow/<slug>/05-lens-memory.md` |

Overwrite the lens file each round. Template: `{my-dev-flow-v3}/artifacts/05-lens.md`.

When Has UI, also apply interface craft (a11y, layout, writing, type, color, polish) if project UI skills are installed.
