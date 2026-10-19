## 3. Conditional lenses — API / DB / Security / Performance / Memory (Medium|Fast)

**When:** After Quality / Lite combined is clean **and** `00-run.md` **Lens plan** is not `none`. Parent launches **only** lenses listed in Lens plan (parallel when 2+). If plan is `none` or tiny-tweak fold, skip section 3–4 and go to test.

Auto-add **api** / **db** only per `{my-dev-flow}/lenses.md` — **not** when Notes `tiny-contract-tweak` or Lens plan folds into Quality / code-review-phase.

**api/db isolation:** When Lens plan includes **api** or **db** (not tiny-tweak), always launch isolated Tasks — even under lite, even if only one lens.

Wait for launched lenses. Merge findings only if **2+** lenses; if **1** lens, parent copies into Merged lenses (no Merge Task).

**Result tokens (all `05*` including lenses):** `clean` \| `needs fix` per `{my-dev-flow}/results.md`. Parent advances only on `clean`. Legacy artifact text `has findings` → treat as `needs fix` when Critical/Major open.

**1 lens (parent copy):** copy lens file Result into `05-review-log.md` Merged lenses as `clean` \| `needs fix` (same advance rule as Merge findings). **2+ lenses:** Merge findings Result is SoT for advance ([stages/merge-findings.md](merge-findings.md)).

Each lens writes **only** its own file (do not edit `05-review-log.md` here — avoids parallel write races):

| Lens | Stage id | Output file |
|------|----------|-------------|
| API | `lens-api` | `.my-docs/workflow/<slug>/05-lens-api.md` |
| DB | `lens-db` | `.my-docs/workflow/<slug>/05-lens-db.md` |
| Security | `lens-security` | `.my-docs/workflow/<slug>/05-lens-security.md` |
| Performance | `lens-perf` | `.my-docs/workflow/<slug>/05-lens-performance.md` |
| Memory | `lens-memory` | `.my-docs/workflow/<slug>/05-lens-memory.md` |

Overwrite the lens file each round. Use the lens template in `{my-dev-flow}/artifacts/INDEX.md` → “05-lens-*.md”.
