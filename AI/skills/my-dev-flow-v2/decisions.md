# Decisions + max rounds

**Option shape** (every Decision N): What / Example / Pros / Cons / Recommendation. Number Decision N and Option 1/2/3.

## Caps

| When | Option 1 | Option 2 | Option 3 | Prefer |
|------|----------|----------|----------|--------|
| Gate A escalate | Re-run Gate A | Override `ok` after explicit yes | Stop | Ask; never invent `ok` |
| Design-backloop | Amend → re-review → Gate B | Fix-only | Stop | 1 if contracts/IA change. On Amend: Notes `design-backloop`; clear Gate B settle; set **Last Verify: pending** + **Last verify-pass at: none**; **Invalidate prior overall `03a` clean** **and** isolated `03a-api` / `03a-db` **clean** when present (pending / drop clean); keep `review-stale` / `test-stale` ([design-backloop.md](design-backloop.md)) |
| Gate B veto after Build | Discard draft | Keep draft + re-open Gate B | Stop | Per user |
| verify-fail ×3 | Narrow / waive command | New Verify commands | Stop | Ask |
| design-review ×3 | Raise cap | Ship Enhancements only | Stop | 3 if Critical/Major remain |
| review Fix ×3 | Raise cap | Defer Enhancements | Stop / backloop | Ask |
| test↔fix ×3 | Raise cap / re-run test | Stop | — | Ask; **no** inventable lite/full waive → Gate C (skip-review only with verify-pass + smoke-pass + escape Notes↔provenance — [gate-c.md](gate-c.md)) |
| Mid-run reclassify | Stay simple | Upgrade full | New slug / stop | 2 when API/DB/auth. **After Upgrade full:** set Notes `design-stale` — Mode-simple `analyze`/`grill`/`03`/`03a*` unpaid until Mode-full rewrite; **Invalidate prior overall `03a` clean** **and** isolated `03a-api` / `03a-db` **clean** when present (set each Result **pending** or remove **clean** — same as Amend); **Gate B approved: none**; **Build armed: none**; clear veto-window tokens **and** `gate-b auto — <HH:MM>` (or digest) if present; set **Last Verify: pending**; **Last verify-pass at: none**; keep `review-stale` / `test-stale` when set (skip-review: clear `review-stale` as N/A) (mirror [design-backloop.md](design-backloop.md) Amend); run derive Pre-Build (Mode full) first-match — Gate A / skim if unpaid, then Notes `design-stale` Prefer first unpaid among `analyze` → `grill` → `design` (before Grill open / No `02-analysis`) — before Design-review/API∥DB; keep `01-idea` unless this Decision requires Ideation redo; **never** keep skip-review (Decision N cannot legalize Mode full + skip-review); do **not** Build / Post-Build while Notes `design-stale`; after Notes clear, Prefer re-run API∥DB when Has=yes **and** isolated unpaid/pending (**even if files exist**) until Mode-full isolated Last stage is paid; **Design clean** only after Mode-full `design-review` (or API∥DB → `design-review`) **clean** ([step-0.md](step-0.md) Mid-run · [reclassify-simple-to-full.md](examples/reclassify-simple-to-full.md)) |
| User override `skip-review` while Mode full or profile lite/full | Switch to Mode **simple** + profile **skip-review** | Stay current Mode + profile (**lite**/**full**; no skip-review) | Stop | Prefer Ask — never auto-downgrade Mode or auto-set skip-review from this state; Decision N **cannot** legalize Mode **full** + skip-review ([stages.md](stages.md) Forbidden · [step-0.md](step-0.md)) |
| Skip-review else (when Prefer unpaid does not match and Prefer-paid bar unmet — Smoke-done/escape-missing included; [verify.md](verify.md) Skip-review + Smoke § Else) | Stay skip-review + ask escape Notes↔provenance **or run Smoke** | Drop skip-review → **lite** (`code-review-phase` → lenses → `merge-findings` if 2+ → `test-lite`) | Stop | Prefer stay + ask escape **or run Smoke** vs drop → lite; do **not** drop profile or write escape Notes without named user yes ([verify.md](verify.md) Skip-review + Smoke § Else · [gate-c.md](gate-c.md)) |
| Task count ≥25 (Mode full) | Continue | Slim / reclassify | Stop | Ask |
| main-thread fallbacks ≥3 | Continue | Change model path | Stop | Ask |

## Run metrics (parent sole Round owner)

**SoT for Round bumps** — stage prompts point here only (not [parent-next.md](parent-next.md)).

Required when section exists: Task count · verify-fail count · main-thread fallbacks.

Bump Round on `01a` / `03a-*` / review / test re-entry. Tasks must **not** invent Round.
