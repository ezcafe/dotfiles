# my-dev-flow handoffs

Stage-scoped handoffs, Decision options shape, and artifact size caps.
Artifact templates: [artifacts/INDEX.md](artifacts/INDEX.md) (one file per stage). Severity: [severity.md](severity.md). Paths: [skills-path.md](skills-path.md).

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

---

## Stage-scoped handoff (required)

Do **not** paste the full artifact catalog into every Task. Use the **base block** + only the paths for that **stage id**.

### Base block (every Task)

```
Repo root: <absolute path>
Workflow slug: <slug>
Stage: <stage-id>
00-run.md: .my-docs/workflow/<slug>/00-run.md
Read only the artifacts listed for this stage (do not open others unless a listed file links to them).
Write only: <write list for stage>
Use simple plain words. Fresh context — do not assume prior chat or other agents' memory.
Honor artifact size caps in my-dev-flow/handoffs.md.
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
| `design-review` | `00-run.md`, `01-idea.md`, `01a` (if present), `02-skim.md` (if present), `02-analysis.md`, `02b-grill.md` (if present), `03-design.md`, `04-tasks.md`, `03a-api-contract-review.md` (if Has API), `03a-db-design-review.md` (if Has DB) | `03a-design-review-log.md` |
| `api-contract-review` | `00-run.md`, `02-analysis.md`, `03-design.md` (API contracts), `04-tasks.md`, `02-skim.md` (if present), repo `AGENTS.md` / route patterns when present | `03a-api-contract-review.md` only |
| `db-design-review` | `00-run.md`, `02-analysis.md`, `03-design.md` (Database contracts + example queries), `04-tasks.md`, `02-skim.md` (if present), repo `AGENTS.md` / `db/schema` / migration patterns when present | `03a-db-design-review.md` only |
| `design-update` | `00-run.md`, `03a-design-review-log.md`, `03a-api-contract-review.md` (if present), `03a-db-design-review.md` (if present), `01-idea.md`, `02-skim.md` (if present), `02-analysis.md`, `02b-grill.md` (if present), `03-design.md`, `04-tasks.md` | Fix-ask targets + round notes in `03a*` files |
| `tdd-review` | `00-run.md`, `03-design.md`, `04-tasks.md`, `03a-design-review-log.md` (if present) — **only when planned tests exist** | `04a-tdd-test-review.md` |
| `build` | `00-run.md`, `03-design.md`, `04-tasks.md`, `04a-tdd-test-review.md` (if present) | code (after Gate B) |
| `smoke` | `00-run.md`, `06-test-log.md` | `06-test-log.md` (Smoke section) |
| `adversarial` | `00-run.md`, `04-tasks.md`, `05-review-log.md` + draft code/tests | `05-review-log.md` (Adversarial section) |
| `quality` | `00-run.md`, `01-idea.md`, `01a-idea-ui-review.md` (if present), `03-design.md`, `04-tasks.md`, `05-review-log.md` + draft code | `05-review-log.md` (Quality section) |
| `spm-api` | `00-run.md`, `03-design.md` (API contracts), `04-tasks.md` + draft API/route/validator code | `05-lens-api.md` only |
| `spm-db` | `00-run.md`, `03-design.md` (Database contracts + example queries), `04-tasks.md` + draft schema/migration/query code | `05-lens-db.md` only |
| `spm-security` | `00-run.md`, `03-design.md`, `04-tasks.md` + draft code | `05-lens-security.md` only |
| `spm-perf` | `00-run.md`, `03-design.md`, `04-tasks.md` + draft code | `05-lens-performance.md` only |
| `spm-memory` | `00-run.md`, `03-design.md`, `04-tasks.md` + draft code | `05-lens-memory.md` only |
| `merge-findings` | `00-run.md`, active `05-lens-*.md` for this round, `05-review-log.md` | `05-review-log.md` (Merged lenses section) |
| `fix-review` | `00-run.md`, `05-review-log.md` (Fix ask), `03-design.md`, `04-tasks.md` | code + fix notes in `05-review-log.md` |
| `test-full` | `00-run.md`, `04-tasks.md`, `06-test-log.md` | `06-test-log.md` |
| `test-lite` | `00-run.md`, `04-tasks.md`, `06-test-log.md` | `06-test-log.md` (smoke + targeted e2e only) |
| `fix-tests` | `00-run.md`, `06-test-log.md` (Fix ask), `03-design.md`, `04-tasks.md` | code |
| `merge` | `00-run.md`, `06-test-log.md` | PR / merge (no secret files) |

**Prompt tip:** After the base block, paste only the concrete paths for that stage (expand `<slug>`). Example for `design-review`:

```
Read:
- .my-docs/workflow/<slug>/01-idea.md
- .my-docs/workflow/<slug>/02-analysis.md
- .my-docs/workflow/<slug>/03-design.md
- .my-docs/workflow/<slug>/04-tasks.md
(and 01a / 02-skim when present per table; see LEGACY.md for old 01b/ui-refs)
Write: .my-docs/workflow/<slug>/03a-design-review-log.md
```

Legacy name: “Shared handoff block” in older stage prompts means **stage-scoped handoff** for that stage id — never the full catalog.

---

## Artifact size caps (required)

Keep artifacts short so later Tasks stay cheap. Soft caps (body content; headings OK):

| Artifact | Cap | Rule |
|----------|-----|------|
| `02-skim.md` | ≤ ~40 lines | Project shape 1–3 sentences; ≤5 rows per table |
| `01-idea.md` | Problem map ≤ ~25 lines (full); stub OK in simple | 3–5 bullets per WHAT branch; mind map ≤15 lines |
| `02-analysis.md` | Overall What/Why/How short; ≤5 solution pieces | Prefer bullets; Spike ≤5 rows; Design tree ≤15 lines; Solution branches ≤12 lines |
| `02b-grill.md` | ≤ ~60 lines | Frontier rounds + settled; glossary/ADR pointers only |
| `03-design.md` | See Mode | **full:** two Decision options; **simple:** one recommended design + ≤3-line rejected alternative. **System design** Overview ≤ ~12 bullets (or `N/A`); ≤3 Concept N; each Pattern ≤ ~8 lines; ≤3 patterns — point to sequence/contracts instead of restating; cut prose elsewhere if needed |
| `03a` / `04a` Fix ask | ≤10 bullets | Critical/Major first |
| `05-review-log` Fix ask | ≤15 bullets | Critical/Major only; Enhancements → Deferred section (severity.md) |
| Parent post-step check | First ~40 lines | Read **Result** / Fix ask header only — do not re-read full design docs |

If a cap would hide a Critical risk, keep the risk and cut prose elsewhere.

---

