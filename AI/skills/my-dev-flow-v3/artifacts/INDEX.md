# Artifacts

**Step 0 seeds only** [00-run.md](00-run.md) into `.my-docs/workflow/<slug>/`.  
Other files are **templates** — create/copy when the owning stage writes (progressive writes). Do **not** pre-seed `pending` stubs. Paying predicates use Result tokens — e.g. Design present = `03`+`done`; Grill closed = Notes `grill-skip` **or** Result `frontier-empty` only (≠ `pending`/`skipped`); **04a unpaid / dirty** (when planned tests present) includes `pending`; ¬ planned tests → **04a ok** without `04a` ([../derive-next.md](../derive-next.md)).

| File | Role | Created by |
|------|------|------------|
| [00-run.md](00-run.md) | Card / consent / settle gen | Step 0 |
| [01-idea.md](01-idea.md) | Framing | `ideation` |
| [01a-gate-a.md](01a-gate-a.md) | Gate A | `gate-a` |
| [02-skim.md](02-skim.md) | Skim | `skim` |
| [02-analysis.md](02-analysis.md) | Analysis | `analyze` / `design-phase` |
| [02b-grill.md](02b-grill.md) | Grill log | `grill` / `design-phase` |
| [03-design.md](03-design.md) | Design options | `design` / `design-phase` |
| [03a-design-review-log.md](03a-design-review-log.md) | Overall design-review | `design-review` / `design-verify-phase` |
| [03a-api-contract-review.md](03a-api-contract-review.md) | Isolated API | Isolated stage **or** `design-verify-phase` when Has API ∈ {yes, unknown} (not tiny) |
| [03a-db-design-review.md](03a-db-design-review.md) | Isolated DB | Isolated stage **or** `design-verify-phase` when Has DB ∈ {yes, unknown} (not tiny) |
| [04-tasks.md](04-tasks.md) | TDD-ready tasks | `design` / `design-phase` |
| [04a-tdd-test-review.md](04a-tdd-test-review.md) | Optional TDD plan review | `tdd-review` |
| [05-review-log.md](05-review-log.md) | Adv / Quality / Merged | review stages |
| [05-lens.md](05-lens.md) | Lens template | copy → `05-lens-<id>.md` per lens |
| [06-test-log.md](06-test-log.md) | Smoke + tests | Build / Smoke / test-* |
| [pr-body.md](pr-body.md) | PR draft | merge path |
| [_calibration.md](_calibration.md) | After done | parent after `done` |
