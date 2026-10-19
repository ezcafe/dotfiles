# Handoffs (compose Task prompt — no Python)

**SoT for:** base block · stage R/W · Task description · Decision option shape.

Before launch: copy **base block** + this stage’s Read/Write row + **Description**. Paste into Orchestrator card Task description. Load `stages/<id>.md` only — do not load this whole file every launch after you know the row.

## Decision option shape

For every Decision N with 2+ options:

- **What it is** · **Example** · **Pros** · **Cons**
- Then **Recommendation**

Fixed Decision tables: [decisions.md](decisions.md).

## Base block (every Task)

```
Repo root: <absolute path>
Workflow slug: <slug>
Stage: <stage-id>
00-run.md: .my-docs/workflow/<slug>/00-run.md
Read only the artifacts listed for this stage.
Write only: <write cell>
Do not write Gate B/C approved, Build armed (set or clear), or provenance.
Do not write card-override, smoke-waive, clarity-check ok, or parent consent lines.
Use plain words. Fresh context — no prior chat memory.
Honor size-caps.md and skills-path.md.
Severity exit per severity.md (Critical/Major block clean).
```

## Stage id → read / write

Paths under `.my-docs/workflow/<slug>/` unless noted.

| Stage id | Read | Write |
|----------|------|-------|
| `ideation` | `00-run.md` | `01-idea.md` |
| `gate-a` | `00-run.md`, `01-idea.md` | `01a-gate-a.md` |
| `ideation-update` | `00-run.md`, `01-idea.md`, `01a-gate-a.md` | `01-idea.md` (+ append `01a` round notes) |
| `skim` | `00-run.md`, `01-idea.md`, `01a-gate-a.md` | `02-skim.md` |
| `analyze` | `00-run.md`, `01-idea.md`, `01a` if present, `02-skim` if present | `02-analysis.md` |
| `grill` | `00-run.md`, idea, analysis, skim if present; repo glossary/ADR if present | `02b-grill.md`; may update `02-analysis.md` Settled/Design tree; may update repo glossary/ADR |
| `design` | `00-run.md`, idea, 01a/skim if present, analysis, grill if present | `03-design.md`, `04-tasks.md` |
| `design-phase` | `00-run.md`, idea, 01a/skim if present — **Mode simple** | analysis, grill (or skip), design, tasks |
| `design-review` | `00-run.md`, idea→tasks + 03a-api/db if present | `03a-design-review-log.md` |
| `design-verify-phase` | same as design-review — **Mode simple** | `03a-design-review-log.md` (+ api/db when flagged, never invent empty) |
| `api-contract-review` | `00-run.md`, analysis, design API, tasks | `03a-api-contract-review.md` |
| `db-design-review` | `00-run.md`, analysis, design DB, tasks | `03a-db-design-review.md` |
| `design-update` | 03a* + idea→tasks | `03-design.md`, `04-tasks.md`, Notes (no consent fields) |
| `tdd-review` | run, design, tasks, 03a if present | `04a-tdd-test-review.md` |
| `build` | run, design, tasks, 04a if present, 06 for Smoke | code + Smoke section; Result verify-pass\|verify-fail |
| `smoke` | run, 06 | `06` Smoke section |
| `adversarial` | run, tasks, 05 + draft | `05` Adversarial |
| `quality` | run, idea, design, tasks, 05 + draft | `05` Quality |
| `code-review-phase` | run, idea, design, tasks, 05 + draft | `05` Adv+Quality |
| `lens-*` | run, design contracts, tasks + draft | matching `05-lens-*.md` |
| `merge-findings` | run, active lenses, 05 | `05` Merged lenses |
| `fix-review` | run, 05 Fix ask, design, tasks | code; may update `05` Fix notes; Result verify-pass\|verify-fail |
| `test-full` | run Verify, design, tasks, 06 | `06`; Test path `full` |
| `test-lite` | run Verify, tasks, 06 | `06`; Test path `lite` |
| `fix-tests` | run, 06 Fix ask, design, tasks | code; may append `06` Round notes; Result verify-pass\|verify-fail |
| `merge` | run, 06, 05 if present; [artifacts/pr-body.md](artifacts/pr-body.md) | PR/merge actions only — never Gate C approved |

## Task description map

| Stage id | description |
|----------|-------------|
| `ideation` | Ideation problem framing |
| `gate-a` | User day-to-day review |
| `ideation-update` | Update idea from review |
| `skim` | Light repo skim |
| `analyze` | Analyze codebase |
| `grill` | Grill design tree |
| `design` | Design and tasks |
| `design-phase` | Design phase bundle |
| `design-review` | Design review |
| `api-contract-review` | API contract review |
| `db-design-review` | DB design review |
| `design-verify-phase` | Design verify phase |
| `design-update` | Update design docs |
| `tdd-review` | Review TDD test cases |
| `build` | Build with TDD |
| `smoke` | Smoke build and unit |
| `adversarial` | Adversarial test review |
| `code-review-phase` | Lite combined review |
| `quality` | Quality review |
| `lens-security` | Security review |
| `lens-perf` | Performance review |
| `lens-memory` | Memory review |
| `lens-api` | API contract lens |
| `lens-db` | Database review |
| `merge-findings` | Merge review findings |
| `fix-review` | Fix review findings |
| `test-full` | Full test suite |
| `test-lite` | Run build and tests |
| `fix-tests` | Fix from test log |
| `merge` | Execute Gate C actions |
