# Handoffs R/W

**Base ban (every Task):** never write Gate B/C approved, Build armed, settle gen, provenance, waiver Notes (`smoke-waive`, `smoke-pass (re-run)`, `smoke re-run`, `docs-only`, `gate-c-test-override`, `has-flip`), Status, Round.

Compose **one row** after you know Next — do not re-read this whole file every turn.

| Stage id | Read | Write | After (parent) |
|----------|------|-------|----------------|
| brainstorm / ideation | idea draft | `01-idea.md` | Shared understanding confirmed → Gate A or design-phase |
| gate-a | idea | `01a-gate-a.md` | |
| skim | idea + 01a | `02-skim.md` | |
| analyze | idea + skim | `02-analysis.md` | |
| grill | analysis | `02b-grill.md` | Next stays `grill` until frontier-empty |
| design | analysis + grill | `03-design.md` (+ options) | Clear `design-stale` only after Mode-full design + 03 rewrite; Has flip checklist ([lenses.md](lenses.md)) |
| design-phase | idea | 02+03+04 (+ grill) | Grill closed; Has flip checklist |
| design-update | prior 03 + findings | 03 (+ tasks) | Mode full: Prefer unpaid Isolated then design-review. Mode simple: design-verify-phase only. Has flip checklist |
| design-verify-phase / design-review | 03 (+ contracts) | `03a-*.md` | |
| api-contract-review / db-design-review | 03 | matching `03a-*` | Prefer unpaid sibling; then design-review when both paid |
| tdd-review | `04` / `04a` | `04a` | |
| build | Design clean + Gate B settled | code + `06` Smoke section + Build-verify | Stamp verify fields; mark stale if rebuild |
| smoke | 06 | Smoke source Smoke-Task | Parent Notes companion |
| adversarial / quality / code-review-phase | draft + 05 | `05-review-log.md` sections | |
| lens-* | draft + plan | `05-lens-*.md` | |
| merge-findings | lenses | Merged section | |
| fix-review / fix-tests | findings | code + verify | Stamp verify fields |
| test-full / test-lite | 06 | 06 Result + path | Clear test-stale when Lite/full clear met; Prefer merge\|gate-c only when Tests success |
| merge | Gate C approved | git/PR | done only if merge ∈ approved + success |

Description map: `lens-api` `lens-db` `lens-security` `lens-perf` `lens-memory` expand from `lens-*`.
