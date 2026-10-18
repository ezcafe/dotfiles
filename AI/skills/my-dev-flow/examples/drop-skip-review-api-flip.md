# Golden path — drop skip-review when Has API flips yes

Short recovery. SoT: [lenses.md](../lenses.md) · [hitl.md](../hitl.md) Gate C bar · [step-0.md](../step-0.md) Mid-run reclassify.

## Start

Mode **simple**, Review profile **skip-review**, Has API=no, Has DB=no (legal).

## Flip

Analyze/Design sets **Has API: yes** (or Has DB yes).

## Parent actions

1. Immediately drop Review profile **skip-review** → **lite** (or reclassify to full if not tiny).
2. Decision N if scope grew beyond tiny tweak ([invariants.md](../invariants.md)).
3. Lint: default `scripts/lint-run.py <run-dir>` errors while skip-review + Has API/DB yes remain; after drop, default lint must pass. `--check-skip-review` / `--before-build` are optional explicit checks.
4. After Build verify-pass: run `code-review-phase` → `test-lite` → Gate C (skip-review path **forbidden**).
5. Gate B: if auth/schema in scope or API/DB yes → prefer **blocking** ([hitl.md](../hitl.md)).

## Do not

- Keep skip-review to “save time”
- Mode full + skip-review (always illegal)
