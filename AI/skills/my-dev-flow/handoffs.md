# my-dev-flow handoffs

Stage-scoped handoffs, Decision options shape, progress paths, and Task `description` map.  
**This file is SoT for:** stage R/W maps · progress path / stage-id aliases · Task descriptions.  
Artifact size caps: [size-caps.md](size-caps.md). Tiny-tweak / never invent empty `03a-api` / `03a-db`: [lenses.md](lenses.md) (do not treat this file as second SoT for that rule).  
Templates: [artifacts/INDEX.md](artifacts/INDEX.md). Severity: [severity.md](severity.md). Paths: [skills-path.md](skills-path.md). Verify/Fix: [verify-and-fix.md](verify-and-fix.md). Parent checklist: [invariants.md](invariants.md). HITL / veto: [hitl.md](hitl.md). Pipeline order: [stages.md](stages.md).

**Required for Task launch:** `python {my-dev-flow}/scripts/handoff-for.py <stage-id>` → prints base block template + that stage’s R/W row (resolve `{my-dev-flow}` per [skills-path.md](skills-path.md); optional `--skill-root` / `--slug`).  
**This file (handoffs.md):** edit SoT / debug only — do **not** load the whole file for every launch.

## Decision options (required for every choice list)

Use this shape in chat **and** in docs whenever there are 2+ options:

- Number the decision: **Decision 1**, **Decision 2**, … (sequential for the run)
- Number each option: **Option 1**, **Option 2**, … (not A/B letters)

For each option:

- **What it is:** plain-words explanation
- **Example:** one concrete example
- **Pros:** …
- **Cons:** …

Then:

- **Recommendation:** which option number to pick and why

Do not list bare names without these fields.

**Built-in Decision shapes** (still use Decision N numbering in the run) — full tables in [invariants.md](invariants.md) and [hitl.md](hitl.md):

| When | Options (fixed) | Where |
|------|-----------------|-------|
| Design invalid after Build / Fix | Amend design → re-review → Gate B · Fix-only · Stop | [stages.md](stages.md) Design-backloop / [invariants.md](invariants.md) |
| async-notify Gate B veto after Build | Discard draft · Keep draft + re-open Gate B · Stop | [hitl.md](hitl.md) |
| verify-fail / review / test max rounds | Narrow or raise cap · Proceed if clean / waive · Stop | [invariants.md](invariants.md) |

---

## Stage-scoped handoff (required)

Do **not** paste the full artifact catalog into every Task. Use the **base block** + only the paths for that **stage id**.

### Base block (every Task)

Printed by `python {my-dev-flow}/scripts/handoff-for.py <stage-id>`. With `--skill-root <abs>`, paths below become absolute under that root.

```
Repo root: <absolute path>
Workflow slug: <slug>
Stage: <stage-id>
00-run.md: .my-docs/workflow/<slug>/00-run.md
Read only the artifacts listed for this stage (do not open others unless a listed file links to them).
Write only: <write list for stage>
Use simple plain words. Fresh context — do not assume prior chat or other agents' memory.
Honor artifact size caps in my-dev-flow/size-caps.md.
Resolve skill paths per my-dev-flow/skills-path.md ({my-dev-flow}, {myplan}, etc.).
Severity exit per my-dev-flow/severity.md (Critical/Major block clean; defer Enhancement).
```

### Stage id → read / write

| Stage id | Read (under `.my-docs/workflow/<slug>/`) | Write |
|----------|------------------------------------------|-------|
| `ideation` | `00-run.md` | `01-idea.md` |
| `gate-a` | `00-run.md`, `01-idea.md` | `01a-idea-ui-review.md` |
| `ideation-update` | `00-run.md`, `01-idea.md`, `01a-idea-ui-review.md` | `01-idea.md` (+ `01a` round notes) |
| `skim` | `00-run.md`, `01-idea.md`, `01a-idea-ui-review.md` | `02-skim.md` |
| `analyze` | `00-run.md`, `01-idea.md`, `01a-idea-ui-review.md` (if present), `02-skim.md` (if present) | `02-analysis.md` |
| `grill` | `00-run.md`, `01-idea.md`, `02-skim.md` (if present), `02-analysis.md`; also repo `GLOSSARY.md` / `GLOSSARY-MAP.md` / ADR dir when present | `02b-grill.md`; may update `02-analysis.md` Settled/Design tree; may update repo `GLOSSARY.md` and/or one ADR |
| `design` | `00-run.md`, `01-idea.md`, `01a-idea-ui-review.md` (if present), `02-skim.md` (if present), `02-analysis.md`, `02b-grill.md` (if present) | `03-design.md`, `04-tasks.md` |
| `design-phase` | `00-run.md`, `01-idea.md`, `01a` (if present), `02-skim.md` (if present) — **Mode simple only** | `02-analysis.md`, `02b-grill.md` (or Notes skip), `03-design.md`, `04-tasks.md` |
| `design-review` | `00-run.md`, `01-idea.md`, `01a` (if present), `02-skim.md` (if present), `02-analysis.md`, `02b-grill.md` (if present), `03-design.md`, `04-tasks.md`, `03a-api-contract-review.md` (if Has API **and** not Notes `tiny-contract-tweak` / if present), `03a-db-design-review.md` (if Has DB **and** not Notes `tiny-contract-tweak` / if present) | `03a-design-review-log.md` |
| `design-verify-phase` | same reads as `design-review` — **Mode simple only** | `03a-design-review-log.md` + `03a-api-contract-review.md` when Has API **and** not Notes `tiny-contract-tweak` + `03a-db-design-review.md` when Has DB **and** not Notes `tiny-contract-tweak` — **never** invent empty `03a-api` / `03a-db` |
| `api-contract-review` | `00-run.md`, `02-analysis.md`, `03-design.md` (API contracts), `04-tasks.md`, `02-skim.md` (if present), repo `AGENTS.md` / route patterns when present — stage N/A when Has API = no or Notes `tiny-contract-tweak` | `03a-api-contract-review.md` only (do not invent if skipped) |
| `db-design-review` | `00-run.md`, `02-analysis.md`, `03-design.md` (Database contracts + example queries), `04-tasks.md`, `02-skim.md` (if present), repo `AGENTS.md` / `db/schema` / migration patterns when present — stage N/A when Has DB = no or Notes `tiny-contract-tweak` | `03a-db-design-review.md` only (do not invent if skipped) |
| `design-update` | `00-run.md`, `03a-design-review-log.md` (if present), `03a-api-contract-review.md` (if present — not Notes `tiny-contract-tweak` / skipped), `03a-db-design-review.md` (if present — not Notes `tiny-contract-tweak` / skipped), `01-idea.md`, `02-skim.md` (if present), `02-analysis.md`, `02b-grill.md` (if present), `03-design.md`, `04-tasks.md` | `03-design.md`, `04-tasks.md`, `00-run.md` Notes (backloop rounds), plus `03a*` round notes when present (no empty `03a-api` / `03a-db`) |
| `tdd-review` | `00-run.md`, `03-design.md`, `04-tasks.md`, `03a-design-review-log.md` (if present) — **only when planned tests exist** | `04a-tdd-test-review.md` |
| `build` | `00-run.md` (Verify commands + **Gate B veto** must be `none`; when HITL Gate B is **blocking** → **Gate B approved** `yes`/named pick; if Notes veto window open → **Build armed** required — [hitl.md](hitl.md) · [verify-and-fix.md](verify-and-fix.md)), `03-design.md`, `04-tasks.md`, `04a-tdd-test-review.md` (if present), when **Has UI**: Design UI specs in `03-design` / acceptance in `04-tasks` (+ `01a-idea-ui-review.md` if present for Gate A #1/#2), `06-test-log.md` (create/update Smoke) | code + Smoke section; first line Result **verify-pass** \| **verify-fail**; if veto `pending`, (blocking without **Gate B approved**), (veto window open without **Build armed**), or Notes `design-backloop` → stop without coding (`blocked — …`); parent skips Smoke Task on verify-pass |
| `smoke` | `00-run.md`, `06-test-log.md` | `06-test-log.md` (Smoke section) — only when Smoke re-run needed |
| `adversarial` | `00-run.md`, `04-tasks.md`, `05-review-log.md` + draft code/tests | `05-review-log.md` (Adversarial section) |
| `quality` | `00-run.md`, `01-idea.md`, `01a-idea-ui-review.md` (if present), `03-design.md`, `04-tasks.md`, `05-review-log.md` + draft code | `05-review-log.md` (Quality section) |
| `code-review-phase` | `00-run.md`, `01-idea.md`, `01a` (if present), `03-design.md`, `04-tasks.md`, `05-review-log.md` + draft code/tests — **Review profile lite** (alias: Lite combined) | `05-review-log.md` (Adversarial + Quality; optional single-lens notes when Lens plan has one lens) |
| `lens-api` | `00-run.md`, `03-design.md` (API contracts), `04-tasks.md` + draft API/route/validator code | `05-lens-api.md` only |
| `lens-db` | `00-run.md`, `03-design.md` (Database contracts + example queries), `04-tasks.md` + draft schema/migration/query code | `05-lens-db.md` only |
| `lens-security` | `00-run.md`, `03-design.md`, `04-tasks.md` + draft code | `05-lens-security.md` only |
| `lens-perf` | `00-run.md`, `03-design.md`, `04-tasks.md` + draft code | `05-lens-performance.md` only |
| `lens-memory` | `00-run.md`, `03-design.md`, `04-tasks.md` + draft code | `05-lens-memory.md` only |
| `merge-findings` | `00-run.md`, active `05-lens-*.md` for this round, `05-review-log.md` | `05-review-log.md` (Merged lenses section) |
| `fix-review` | `00-run.md` (Verify commands), `05-review-log.md` (Fix ask), `03-design.md`, `04-tasks.md` | code + fix notes; first line Result **verify-pass** \| **verify-fail** |
| `test-full` | `00-run.md` (Verify commands), `03-design.md`, `04-tasks.md`, `06-test-log.md` — **one Task:** coverage + add missing e2e + run suite | `06-test-log.md` (Coverage + Runs + Result; **Mode last run:** `full`) |
| `test-lite` | `00-run.md` (Verify commands), `04-tasks.md`, `06-test-log.md` | `06-test-log.md` (targeted e2e; unit if needed; **Mode last run:** `lite`) |
| `fix-tests` | `00-run.md` (Verify commands), `06-test-log.md` (Fix ask), `03-design.md`, `04-tasks.md` | code; first line Result **verify-pass** \| **verify-fail** |
| `merge` | `00-run.md` (**Gate C approved** — abort if missing/`none`), `06-test-log.md`, `05-review-log.md` (if present), skim `03-design.md` (optional for PR risk summary); template `{my-dev-flow}/artifacts/pr-body.md` | PR body from template + merge (no secret files) |

**Prompt tip:** After the base block, paste only the concrete paths for that stage (expand `<slug>`). Example for `design-review`:

```
Read:
- .my-docs/workflow/<slug>/01-idea.md
- .my-docs/workflow/<slug>/02-analysis.md
- .my-docs/workflow/<slug>/03-design.md
- .my-docs/workflow/<slug>/04-tasks.md
(and 01a / 02-skim when present per table)
Write: .my-docs/workflow/<slug>/03a-design-review-log.md
```

---

## Artifact size caps

Soft caps SoT: [size-caps.md](size-caps.md) (do not load this file for caps).

---

## Progress path / Stage id aliases

Orchestrator card uses **stage ids**. Alias column is for chat only.

| Stage id (prefer) | Alias | Path |
|-------------------|-------|------|
| (classify) | Step 0 | `00-run.md` (Status `running`) |
| `ideation` | Step 1 | `01-idea.md` |
| `gate-a` | Gate A | `01a-idea-ui-review.md` |
| `skim` | Step 1s | `02-skim.md` |
| `analyze` / `design-phase` | Step 2 | `02-analysis.md` (+ design bundle on simple) |
| `grill` | Step 2g | `02b-grill.md` or skip note |
| `design` / `design-phase` | Step 3 | `03-design.md` + `04-tasks.md` |
| `design-review` / `api-contract-review` / `db-design-review` / `design-verify-phase` | — | `03a-*` |
| `tdd-review` | Step 4a | `04a-tdd-test-review.md` or skip note |
| Gate B | — | digest + HITL |
| `build` | Step 4 | key code paths |
| `smoke` | — | `06-test-log.md` Smoke (re-run only; usually skipped) |
| `adversarial` / `quality` / `code-review-phase` / `lens-*` / `merge-findings` | Steps 5–9 | `05-review-log.md` (+ `05-lens-*.md`) |
| `test-full` / `test-lite` | — | `06-test-log.md` (after review clean) |
| `merge` | Gate C | PR URL / result |

### File log examples (`00-run.md` only)

```markdown
- **HH:MM** · done · analyze · usage-limit retry — waited 5s
- **HH:MM** · done · Gate B — async-notify · Gate B veto: none
- **HH:MM** · paused · gate-b · Build armed · parent turn gap observed
- **HH:MM** · done · build · Result verify-pass · Smoke section written · Smoke Task skipped
- **HH:MM** · paused · Gate C — blocking — Approve commit + push + PR + merge?
- **HH:MM** · stopped · Gate B veto pending — frozen before Build
- **HH:MM** · done · merge · Mode was right because clear bug fix stayed simple
```

---

## Task `description` map (by stage id)

Use as Task `description` / Orchestrator card **Task description**.

| Stage id | description |
|----------|-------------|
| (classify) | `Classify and resolve models` |
| `ideation` | `Ideation problem framing` |
| `gate-a` | `User day-to-day review` |
| `ideation-update` | `Update idea from review` |
| `skim` | `Light repo skim` |
| `analyze` | `Analyze codebase` (Mode full) |
| `grill` | `Grill design tree` (Mode full) |
| `design` | `Design and tasks` (Mode full) |
| `design-phase` | `Design phase bundle` (Mode simple — Analyze+Grill+Design) |
| `design-review` | `Design review` (Mode full general) |
| `api-contract-review` | `API contract review` (Mode full; parallel with DB when both) |
| `db-design-review` | `DB design review` (Mode full; parallel with API when both) |
| `design-verify-phase` | `Design verify phase` (Mode simple — general + API/DB when flagged) |
| `design-update` | `Update design docs` |
| `tdd-review` | `Review TDD test cases` |
| `build` | `Build with TDD` |
| `smoke` | `Smoke build and unit` (re-run only; usually skipped) |
| `adversarial` | `Adversarial test review` (Review profile **full**) |
| `code-review-phase` | `Lite combined review` (**required** when profile lite) |
| `quality` | `Quality review` (Review profile **full**) |
| `lens-security` | `Security review` |
| `lens-perf` | `Performance review` |
| `lens-memory` | `Memory review` |
| `lens-api` | `API contract lens` |
| `lens-db` | `Database review` |
| `merge-findings` | `Merge review findings` |
| `fix-review` | `Fix review findings` |
| `test-full` | `Full test suite` (coverage + e2e gaps + run — one Task) |
| `test-lite` | `Run build and tests` |
| `fix-tests` | `Fix from test log` |
| `merge` | `Push PR and merge` |
