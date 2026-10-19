# Parent next (open 1–2 files)

Given card **Stage id** / **Next**, open the **Open** row + compose handoff. Do not re-read orchestrator SKILL.

**Habit:** [preflight.md](preflight.md) → [derive-next.md](derive-next.md) → handoff from [handoffs.md](handoffs.md) → `stages/<id>.md`.

**Parent-only carve:** when Next is `gate-b` or `gate-c`, stop after this table’s Open row (gate file + linked hitl) — **skip** handoff compose and `stages/<id>.md` ([step-0.md](step-0.md) Load budget · [preflight.md](preflight.md) Always).

**Round / Run metrics:** parent sole owner — bump rules in [decisions.md](decisions.md) only (this file maps Next → open paths; it does not define Round).

Clarity boundaries: design [clarity-check](../my-dev-flow-v2-design/stages/clarity-check.md); code [clarity-check](../my-dev-flow-v2-code/stages/clarity-check.md). Parent logs `clarity-check ok — <Next>`.

| Next | Open (1–2) |
|------|------------|
| Step 0 | [step-0.md](step-0.md) · [artifacts/00-run.md](artifacts/00-run.md) |
| `ideation` | [../my-dev-flow-v2-design/stages/ideation.md](../my-dev-flow-v2-design/stages/ideation.md) |
| `gate-a` | [../my-dev-flow-v2-design/stages/gate-a.md](../my-dev-flow-v2-design/stages/gate-a.md) |
| `ideation-update` | [../my-dev-flow-v2-design/stages/ideation-update.md](../my-dev-flow-v2-design/stages/ideation-update.md) |
| `skim` | [../my-dev-flow-v2-design/stages/skim.md](../my-dev-flow-v2-design/stages/skim.md) |
| `analyze` | [../my-dev-flow-v2-design/stages/analyze.md](../my-dev-flow-v2-design/stages/analyze.md) |
| `grill` | [grill.md](grill.md) · [../my-dev-flow-v2-design/stages/grill.md](../my-dev-flow-v2-design/stages/grill.md) |
| `design` | [../my-dev-flow-v2-design/stages/design.md](../my-dev-flow-v2-design/stages/design.md) |
| `design-phase` | [../my-dev-flow-v2-design/stages/design-phase.md](../my-dev-flow-v2-design/stages/design-phase.md) |
| `design-update` | [../my-dev-flow-v2-design/stages/design-update.md](../my-dev-flow-v2-design/stages/design-update.md) |
| `api-contract-review` | [../my-dev-flow-v2-design-review/stages/api-contract-review.md](../my-dev-flow-v2-design-review/stages/api-contract-review.md) |
| `db-design-review` | [../my-dev-flow-v2-design-review/stages/db-design-review.md](../my-dev-flow-v2-design-review/stages/db-design-review.md) |
| `api\|db` | both rows above (same-turn parallel while Pending parallel `api\|db` — [lenses.md](lenses.md)) |
| `design-review` | [../my-dev-flow-v2-design-review/stages/design-review.md](../my-dev-flow-v2-design-review/stages/design-review.md) |
| `design-verify-phase` | [../my-dev-flow-v2-design-review/stages/design-verify-phase.md](../my-dev-flow-v2-design-review/stages/design-verify-phase.md) |
| `tdd-review` | [../my-dev-flow-v2-code/stages/tdd-review.md](../my-dev-flow-v2-code/stages/tdd-review.md) · [verify.md](verify.md) |
| `gate-b` | [gate-b.md](gate-b.md) **Read before you decide** · [hitl.md](hitl.md) — blocking: paste reading guide + digest; parent sets approved. **auto:** write design-scoped `gate-b auto — <HH:MM>` (or digest) after current **Design clean** / **Verify clean** (Design-clean time) same turn, then Prefer `build` (no user wait). **async-notify:** digest this turn; arm next. No Task — [derive-next.md](derive-next.md) Settle freshness |
| `build` | [../my-dev-flow-v2-code/stages/build.md](../my-dev-flow-v2-code/stages/build.md) · [verify.md](verify.md) |
| `smoke` | [../my-dev-flow-v2-test/stages/smoke.md](../my-dev-flow-v2-test/stages/smoke.md) |
| `code-review-phase` | [../my-dev-flow-v2-review/stages/code-review-phase.md](../my-dev-flow-v2-review/stages/code-review-phase.md) |
| `adversarial` | [../my-dev-flow-v2-review/stages/adversarial.md](../my-dev-flow-v2-review/stages/adversarial.md) |
| `quality` | [../my-dev-flow-v2-review/stages/quality.md](../my-dev-flow-v2-review/stages/quality.md) |
| `lens-*` | matching file under [../my-dev-flow-v2-review/stages/](../my-dev-flow-v2-review/stages/) |
| `merge-findings` | [../my-dev-flow-v2-review/stages/merge-findings.md](../my-dev-flow-v2-review/stages/merge-findings.md) |
| `fix-review` | [../my-dev-flow-v2-review/stages/fix-review.md](../my-dev-flow-v2-review/stages/fix-review.md) |
| `test-full` | [../my-dev-flow-v2-test/stages/test-full.md](../my-dev-flow-v2-test/stages/test-full.md) |
| `test-lite` | [../my-dev-flow-v2-test/stages/test-lite.md](../my-dev-flow-v2-test/stages/test-lite.md) |
| `fix-tests` | [../my-dev-flow-v2-code/stages/fix-tests.md](../my-dev-flow-v2-code/stages/fix-tests.md) |
| `gate-c` | [gate-c.md](gate-c.md) **Read before you decide** — paste reading guide + blocking ask; no merge yet |
| `merge` | [../my-dev-flow-v2-merge/stages/merge.md](../my-dev-flow-v2-merge/stages/merge.md) · code [clarity-check Merge](../my-dev-flow-v2-code/stages/clarity-check.md#merge) |

Resume: [resume.md](resume.md).
