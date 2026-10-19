# Handoffs (compose Task prompt — no Python)

**SoT for:** base block · stage R/W · Task description · Decision option shape.

Before launch: copy **base block** + this stage’s Read/Write row + **Description**. Paste into Orchestrator card Task description. Load `stages/<id>.md` only — do not load this whole file every launch after you know the row.

**Mode simple bootstrap `01-idea` (parent, not a Task):** when derive expects bootstrap before `design-phase` and `01-idea.md` is missing, parent **either** writes a minimal stub from [artifacts/01-idea.md](artifacts/01-idea.md) (Core problem line / Mode-simple stub OK) **or** launches stage `ideation` — then Next=`design-phase` ([step-0.md](step-0.md) · [derive-next.md](derive-next.md)). Mode full never bootstraps this way — use `ideation`.

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
Do not write card-override, smoke-waive, Notes `smoke re-run`, Notes `smoke-pass (re-run)`, clarity-check ok, or parent consent lines.
Use plain words. Fresh context — no prior chat memory.
Follow size-caps / skills-path / severity already pasted in this handoff (parent inlines or pastes rules). Do not open size-caps.md, skills-path.md, or severity.md unless a needed rule is missing from the paste.
```

**Parent-only Notes (`smoke re-run`):** Parent sets Notes `smoke re-run` once before Prefer unpaid independent Smoke; clears it when writing Notes `smoke-pass (re-run)` ([verify.md](verify.md) Independent Smoke). Tasks must not write either token.

## Stage id → read / write

Paths under `.my-docs/workflow/<slug>/` unless noted.

| Stage id | Read | Write |
|----------|------|-------|
| `ideation` | `00-run.md` | `01-idea.md` |
| `gate-a` | `00-run.md`, `01-idea.md` | `01a-gate-a.md` |
| `ideation-update` | `00-run.md`, `01-idea.md`, `01a-gate-a.md` | `01-idea.md` (+ append `01a` round notes) |
| `skim` | `00-run.md`, `01-idea.md`, `01a-gate-a.md` | `02-skim.md` |
| `analyze` | `00-run.md`, `01-idea.md`, `01a-gate-a.md` if present, `02-skim.md` if present | `02-analysis.md` |
| `grill` | `00-run.md`, `01-idea.md`, `02-analysis.md`, `02-skim.md` if present; repo glossary/ADR if present | `02b-grill.md`; may update `02-analysis.md` Settled/Design tree; may update repo glossary/ADR |
| `design` | `00-run.md`, `01-idea.md`, `01a-gate-a.md`/`02-skim.md` if present, `02-analysis.md`, `02b-grill.md` if present | `03-design.md`, `04-tasks.md` — **After (parent):** clear Notes `design-stale` only after Last stage `design` **and** `03-design.md` rewrite for Mode full; then Prefer re-run API∥DB while Isolated API/DB unpaid (**even if files exist**); **Design clean** still unpaid until Mode-full `design-review` (or API∥DB → `design-review`) **clean**. **Has flip:** drop skip-review → lite\|reclassify → HITL Gate B **blocking** → settle clear (**Gate B approved: none** / **Build armed: none** / veto-window / `async-gap-pending` / `gate-b auto`) → Notes `has-flip — <flags> — <HH:MM>` → invalidate-or-Prefer-re-run when API/DB newly yes ([lenses.md](lenses.md) Has flip · [derive-next.md](derive-next.md) Settle freshness) |
| `design-phase` | `00-run.md`, `01-idea.md`, `01a-gate-a.md`/`02-skim.md` if present — **Mode simple** | `02-analysis.md`, `02b-grill.md` (or Notes skip), `03-design.md`, `04-tasks.md` — **After (parent):** **Has flip:** drop skip-review → lite\|reclassify → HITL Gate B **blocking** → settle clear (**Gate B approved: none** / **Build armed: none** / veto-window / `async-gap-pending` / `gate-b auto`) → Notes `has-flip — <flags> — <HH:MM>` → invalidate-or-Prefer-re-run when API/DB newly yes ([lenses.md](lenses.md) Has flip · [derive-next.md](derive-next.md) Settle freshness) |
| `design-review` | `00-run.md`, `01-idea.md`→`04-tasks.md` + `03a-api-*`/`03a-db-*` if present | `03a-design-review-log.md` |
| `design-verify-phase` | same as design-review — **Mode simple** | `03a-design-review-log.md` (+ `03a-api-*`/`03a-db-*` when flagged, never invent empty) |
| `api-contract-review` | `00-run.md`, `02-analysis.md`, `03-design.md` (API), `04-tasks.md` | `03a-api-contract-review.md` |
| `db-design-review` | `00-run.md`, `02-analysis.md`, `03-design.md` (DB), `04-tasks.md` | `03a-db-design-review.md` |
| `design-update` | `03a*` + `01-idea.md`→`04-tasks.md` | `03-design.md`, `04-tasks.md`, Notes (no consent fields) — **After (parent):** Mode **full:** Prefer unpaid `api-contract-review` / `db-design-review` while **Isolated API/DB unpaid** (Has yes, not tiny; Prefer even if files exist) → else `design-review`. Mode **simple:** Prefer `design-verify-phase` only (do **not** Prefer isolated stages). ([derive-next-pre.md](derive-next-pre.md) · [design-backloop.md](design-backloop.md)). **Has flip:** drop skip-review → lite\|reclassify → HITL Gate B **blocking** → settle clear (**Gate B approved: none** / **Build armed: none** / veto-window / `async-gap-pending` / `gate-b auto`) → Notes `has-flip — <flags> — <HH:MM>` → invalidate-or-Prefer-re-run when API/DB newly yes ([lenses.md](lenses.md) Has flip · [derive-next.md](derive-next.md) Settle freshness) |
| `tdd-review` | `00-run.md`, `03-design.md`, `04-tasks.md`, `03a*` if present | `04a-tdd-test-review.md` |
| `build` | `00-run.md`, `03-design.md`, `04-tasks.md`, `04a` if present, `06-test-log.md` for Smoke | code + Smoke section + **Smoke source: Build-verify**; Result verify-pass\|verify-fail |
| `smoke` | `00-run.md`, `06-test-log.md` | `06-test-log.md` Smoke section + **Smoke source: Smoke-Task** (no Notes) |
| `adversarial` | `00-run.md`, `04-tasks.md`, `05-review-log.md` + draft | `05-review-log.md` Adversarial |
| `quality` | `00-run.md`, `01-idea.md`, `03-design.md`, `04-tasks.md`, `05-review-log.md` + draft | `05-review-log.md` Quality |
| `code-review-phase` | `00-run.md`, `01-idea.md`, `03-design.md`, `04-tasks.md`, `05-review-log.md` + draft | `05-review-log.md` Adv+Quality |
| `lens-*` | `00-run.md`, `03-design.md` contracts, `04-tasks.md` + draft | matching `05-lens-*.md` |
| `merge-findings` | `00-run.md`, active `05-lens-*.md`, `05-review-log.md` | `05-review-log.md` Merged lenses |
| `fix-review` | `00-run.md`, `05-review-log.md` Fix ask, `03-design.md`, `04-tasks.md` | code; may update `05-review-log.md` Fix notes; Result verify-pass\|verify-fail |
| `test-full` | `00-run.md` Verify, `03-design.md`, `04-tasks.md`, `06-test-log.md` | `06-test-log.md`; Test path `full` |
| `test-lite` | `00-run.md` Verify, `04-tasks.md`, `06-test-log.md` | `06-test-log.md`; Test path `lite` |
| `fix-tests` | `00-run.md`, `06-test-log.md` Fix ask, `03-design.md`, `04-tasks.md` | code; may append `06-test-log.md` Round notes; Result verify-pass\|verify-fail |
| `merge` | `00-run.md`, `06-test-log.md`, `05-review-log.md` if present; [artifacts/pr-body.md](artifacts/pr-body.md) | PR/merge actions only — never Gate C approved |

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
