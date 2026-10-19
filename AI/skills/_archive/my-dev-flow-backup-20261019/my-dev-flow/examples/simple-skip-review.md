# Golden path — Mode simple + skip-review

Minimal walkthrough for legal **skip-review**. Parent follows [stages.md](../stages.md) Simple (a). Do not invent Ideation / Gate A / skim.

## Ask

> Update button copy on settings screen — docs/copy only, no API or schema.

## Step 0

- Status **`running`**; Mode **simple**, Review profile **skip-review**, Lens plan **none**, Pending parallel **none**, Gate B veto **none**
- Has API **no**, Has DB **no**, no auth/PII/schema
- Slug e.g. `20261018-settings-copy-tweak`
- Bootstrap thin `01-idea.md` (Core problem one line)
- HITL Gate B prefer **auto**; Gate C **blocking**
- **Lint:** `scripts/lint-run.py .my-docs/workflow/<slug>/` (optional `preflight.py`)

## Parent before each Task (fixed)

1. Clarity boundary when Next ∈ clarity stages; log `clarity-check ok — <Next>`.
2. `python3 {my-dev-flow}/scripts/lint-run.py <run-dir> --next --derive` (or `preflight.py` launch pack)
3. `--snapshot-consent` before launch; `--check-consent-writes` after ([hitl.md](../hitl.md))
4. After any parent consent/waiver write: Run log `parent consent write — <kind>` → re-snapshot
5. On handoff (exit 0): `python3 {my-dev-flow}/scripts/handoff-for.py <stage-id>`

## Pipeline

| # | Stage id | Result |
|---|----------|--------|
| 1 | `design-phase` | Writes analysis + design + tasks; Verify commands; Has API/DB **no** |
| 2 | `design-verify-phase` | `03a` Result **clean** |
| 3 | (04a) | Notes `04a skipped` unless planned tests |
| 4 | Gate B | Prefer **auto** (low-risk); parent-only consent ([hitl.md](../hitl.md)) |
| 5 | `build` | verify-pass + Smoke section smoke-pass (Build-writes-Smoke) |
| 6 | Smoke Task | Prefer Notes `smoke re-run` **once** before Gate C escapes ([verify-and-fix.md](../verify-and-fix.md)); else skip if escape + provenance ready |
| 7 | Gate C | Fail-closed escape **+ provenance** — e.g. Notes `smoke-pass (re-run)` + `provenance — smoke-pass-rerun — user: "…"` **or** `smoke-waive` / `docs-only` / `gate-c-test-override` with matching kinds ([hitl-gate-c.md](../hitl-gate-c.md)). **Parent** sets **Gate C approved** + provenance from latest user message + Run log `parent consent write — gate-c-approved` (and waiver kind) → re-snapshot |
| 8 | `merge` | Only approved actions → Status **`done`** when `merge` ∈ Gate C approved |

## Illegal

- Has API or Has DB flips to **yes** → drop skip-review ([lenses.md](../lenses.md) · [drop-skip-review-api-flip.md](drop-skip-review-api-flip.md))
- Gate C with only Build-writes-Smoke and no escape + provenance → lint `--before-merge` **errors**
- Invent provenance / paste tokens to unlock merge ([anti-patterns.md](anti-patterns.md))

## Parent habits

- Consent / waivers / provenance = **parent-only** ([hitl.md](../hitl.md))
- Increment Round / Run metrics after each cycle ([parent-next.md](../parent-next.md))
- SoT: [stages.md](../stages.md) Simple (a) · [hitl-gate-c.md](../hitl-gate-c.md) · [verify-and-fix.md](../verify-and-fix.md)
