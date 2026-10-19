# my-dev-flow-v2-review stages (index)

**Progressive disclosure:** Principles live in [SKILL.md](SKILL.md).  
**Load one file only:** `stages/<stage-id>.md` for the current Task.

**Shared SoT:** Stage-scoped handoff: compose from `{my-dev-flow-v2}/handoffs.md` (base block + R/W + Description). Paths: `{my-dev-flow-v2}/skills-path.md`.

**Owned stage ids:** `code-review-phase` · `adversarial` · `quality` · `lens-api` · `lens-db` · `lens-security` · `lens-perf` · `lens-memory` · `merge-findings` · `fix-review`

## Happy-path pointers

Order keys off **Review profile**, not Mode (Mode full + profile lite → lite row).

| Review profile | Order |
|----------------|-------|
| **lite** | `code-review-phase` ⇄ Fix → lenses per plan → Merge if 2+ → `test-lite` |
| **full** | independent Smoke (`Smoke source: Smoke-Task`) → `adversarial` ⇄ Fix → `quality` ⇄ Fix → lenses → Merge if 2+ → Fix loop → `test-full` |

> Notes `smoke-pass (re-run)` is companion provenance only (not the path unlock) — [verify.md](../my-dev-flow-v2/verify.md) Independent Smoke (SoT).

Lens routing (when Lens plan ≠ none): [stages/lenses-overview.md](stages/lenses-overview.md).  
Parent loop hint: [stages/parent-loop-hint.md](stages/parent-loop-hint.md).  
Parent SoT: [`../my-dev-flow-v2/stages.md`](../my-dev-flow-v2/stages.md) Mode × Review profile table.

## Per-stage prompts

| Stage id | File |
|----------|------|
| `code-review-phase` | [stages/code-review-phase.md](stages/code-review-phase.md) |
| `adversarial` | [stages/adversarial.md](stages/adversarial.md) |
| `quality` | [stages/quality.md](stages/quality.md) |
| lenses overview | [stages/lenses-overview.md](stages/lenses-overview.md) |
| `lens-api` | [stages/lens-api.md](stages/lens-api.md) |
| `lens-db` | [stages/lens-db.md](stages/lens-db.md) |
| `lens-security` | [stages/lens-security.md](stages/lens-security.md) |
| `lens-perf` | [stages/lens-perf.md](stages/lens-perf.md) |
| `lens-memory` | [stages/lens-memory.md](stages/lens-memory.md) |
| `merge-findings` | [stages/merge-findings.md](stages/merge-findings.md) |
| `fix-review` | [stages/fix-review.md](stages/fix-review.md) |
