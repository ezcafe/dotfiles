# Parent-next — Open 1–2

After derive Expected Next, open **at most two** files from this table’s **Open 1–2** column. Do not open full handoffs or orchestrator SKILL.

**Habit:** routing pack ([preflight.md](preflight.md) → [derive-next.md](derive-next.md) + matching half) → handoff **row only** → this table’s **Open 1–2** + **Skill** for Expected Next ([step-0.md](step-0.md) Load budget) → if Skill ≠ `parent-inline`, open [spawn-contract.md](spawn-contract.md) only → **spawn** Task (Skill map also inlined there; not full [subagents.md](subagents.md) every turn — After = step-0 After Task); Open 1–2 are for the Task prompt, not parent inline execution.

**Row-only:** read **only** the matching Expected Next row in this table (and in [handoffs.md](handoffs.md)) — not the whole file ([step-0.md](step-0.md) Load budget).

**Parent-inline / labeled-solo carve:** Next `gate-b` / `gate-c` / `finalize-lens-plan` → Skill = `parent-inline` — Open 1–2 from **this table** (skip handoff compose; parent-inline **or** labeled solo as orchestrator — no skill Task). Aligns [step-0.md](step-0.md) Load budget: `gate-b`/`gate-c` open gate + hitl; `finalize-lens-plan` opens lenses.

**Clarity-check (extra, not a slot):** when Next ∈ the set in [clarity-check.md](clarity-check.md), open that file **before** the stage; log `clarity-check ok — <Next>`. This is **in addition to** Open 1–2 — it does **not** compete for the two-file slot ([preflight.md](preflight.md) Always §6 · [step-0.md](step-0.md) Load budget §4).

| Next | Skill | Open (1–2) |
|------|-------|------------|
| Step 0 | `parent-inline` | [step-0.md](step-0.md) · [artifacts/00-run.md](artifacts/00-run.md) |
| `ideation` / brainstorm | `my-dev-flow-v3-design` | [../my-dev-flow-v3-design/stages/ideation.md](../my-dev-flow-v3-design/stages/ideation.md) · [brainstorm.md](brainstorm.md) |
| `gate-a` | `my-dev-flow-v3-design` | [../my-dev-flow-v3-design/stages/gate-a.md](../my-dev-flow-v3-design/stages/gate-a.md) |
| `skim` | `my-dev-flow-v3-design` | [../my-dev-flow-v3-design/stages/skim.md](../my-dev-flow-v3-design/stages/skim.md) |
| `analyze` | `my-dev-flow-v3-design` | [../my-dev-flow-v3-design/stages/analyze.md](../my-dev-flow-v3-design/stages/analyze.md) |
| `grill` | `my-dev-flow-v3-design` | [grill.md](grill.md) · [../my-dev-flow-v3-design/stages/grill.md](../my-dev-flow-v3-design/stages/grill.md) |
| `design` | `my-dev-flow-v3-design` | [../my-dev-flow-v3-design/stages/design.md](../my-dev-flow-v3-design/stages/design.md) |
| `design-phase` | `my-dev-flow-v3-design` | [../my-dev-flow-v3-design/stages/design-phase.md](../my-dev-flow-v3-design/stages/design-phase.md) |
| `design-update` | `my-dev-flow-v3-design` | [../my-dev-flow-v3-design/stages/design-update.md](../my-dev-flow-v3-design/stages/design-update.md) |
| `api-contract-review` | `my-dev-flow-v3-design-review` | [../my-dev-flow-v3-design-review/stages/api-contract-review.md](../my-dev-flow-v3-design-review/stages/api-contract-review.md) |
| `db-design-review` | `my-dev-flow-v3-design-review` | [../my-dev-flow-v3-design-review/stages/db-design-review.md](../my-dev-flow-v3-design-review/stages/db-design-review.md) |
| `api\|db` | `my-dev-flow-v3-design-review` ×2 parallel | [../my-dev-flow-v3-design-review/stages/api-contract-review.md](../my-dev-flow-v3-design-review/stages/api-contract-review.md) · [../my-dev-flow-v3-design-review/stages/db-design-review.md](../my-dev-flow-v3-design-review/stages/db-design-review.md) (Pending parallel — both Open) |
| `design-review` | `my-dev-flow-v3-design-review` | [../my-dev-flow-v3-design-review/stages/design-review.md](../my-dev-flow-v3-design-review/stages/design-review.md) |
| `design-verify-phase` | `my-dev-flow-v3-design-review` | [../my-dev-flow-v3-design-review/stages/design-verify-phase.md](../my-dev-flow-v3-design-review/stages/design-verify-phase.md) |
| `tdd-review` | `my-dev-flow-v3-code` | [../my-dev-flow-v3-code/stages/tdd-review.md](../my-dev-flow-v3-code/stages/tdd-review.md) · [results.md](results.md) |
| `gate-b` | `parent-inline` | [gate-b.md](gate-b.md) · [hitl.md](hitl.md) |
| `finalize-lens-plan` | `parent-inline` | [lenses.md](lenses.md) (parent-inline **or** labeled solo as orchestrator — not a Task; set Lens plan api/db; then re-derive) |
| `build` | `my-dev-flow-v3-code` | [../my-dev-flow-v3-code/stages/build.md](../my-dev-flow-v3-code/stages/build.md) · [verify.md](verify.md) |
| `smoke` | `my-dev-flow-v3-test` | [../my-dev-flow-v3-test/stages/smoke.md](../my-dev-flow-v3-test/stages/smoke.md) |
| `code-review-phase` | `my-dev-flow-v3-review` | [../my-dev-flow-v3-review/stages/code-review-phase.md](../my-dev-flow-v3-review/stages/code-review-phase.md) (E1 FIRST if launched under E1) |
| `adversarial` | `my-dev-flow-v3-review` | [../my-dev-flow-v3-review/stages/adversarial.md](../my-dev-flow-v3-review/stages/adversarial.md) (E1 FIRST: Smoke-Task or `blocked — Smoke unpaid`) |
| `quality` | `my-dev-flow-v3-review` | [../my-dev-flow-v3-review/stages/quality.md](../my-dev-flow-v3-review/stages/quality.md) (same E1 FIRST) |
| `lens-api` | `my-dev-flow-v3-review` | [../my-dev-flow-v3-review/stages/lens-api.md](../my-dev-flow-v3-review/stages/lens-api.md) |
| `lens-db` | `my-dev-flow-v3-review` | [../my-dev-flow-v3-review/stages/lens-db.md](../my-dev-flow-v3-review/stages/lens-db.md) |
| `lens-security` | `my-dev-flow-v3-review` | [../my-dev-flow-v3-review/stages/lens-security.md](../my-dev-flow-v3-review/stages/lens-security.md) |
| `lens-perf` | `my-dev-flow-v3-review` | [../my-dev-flow-v3-review/stages/lens-perf.md](../my-dev-flow-v3-review/stages/lens-perf.md) |
| `lens-memory` | `my-dev-flow-v3-review` | [../my-dev-flow-v3-review/stages/lens-memory.md](../my-dev-flow-v3-review/stages/lens-memory.md) |
| `lens-*` | `my-dev-flow-v3-review` | matching `lens-*.md` under [../my-dev-flow-v3-review/stages/](../my-dev-flow-v3-review/stages/) · overview [lenses-overview.md](../my-dev-flow-v3-review/stages/lenses-overview.md) |
| `merge-findings` | `my-dev-flow-v3-review` | [../my-dev-flow-v3-review/stages/merge-findings.md](../my-dev-flow-v3-review/stages/merge-findings.md) |
| `fix-review` | `my-dev-flow-v3-review` | [../my-dev-flow-v3-review/stages/fix-review.md](../my-dev-flow-v3-review/stages/fix-review.md) |
| `test-full` | `my-dev-flow-v3-test` | [../my-dev-flow-v3-test/stages/test-full.md](../my-dev-flow-v3-test/stages/test-full.md) |
| `test-lite` | `my-dev-flow-v3-test` | [../my-dev-flow-v3-test/stages/test-lite.md](../my-dev-flow-v3-test/stages/test-lite.md) |
| `fix-tests` | `my-dev-flow-v3-code` | [../my-dev-flow-v3-code/stages/fix-tests.md](../my-dev-flow-v3-code/stages/fix-tests.md) |
| `gate-c` | `parent-inline` | [gate-c.md](gate-c.md) · [hitl.md](hitl.md) |
| `merge` | `my-dev-flow-v3-merge` | [../my-dev-flow-v3-merge/stages/merge.md](../my-dev-flow-v3-merge/stages/merge.md) · [gate-c.md](gate-c.md) (optional) |

Resume: [resume.md](resume.md).
