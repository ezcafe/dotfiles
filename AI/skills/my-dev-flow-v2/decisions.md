# Decisions + max rounds

**Option shape** (every Decision N): What / Example / Pros / Cons / Recommendation. Number Decision N and Option 1/2/3.

## Caps

| When | Option 1 | Option 2 | Option 3 | Prefer |
|------|----------|----------|----------|--------|
| Gate A escalate | Re-run Gate A | Override `ok` after explicit yes | Stop | Ask; never invent `ok` |
| Design-backloop | Amend → re-review → Gate B | Fix-only | Stop | 1 if contracts/IA change |
| Gate B veto after Build | Discard draft | Keep draft + re-open Gate B | Stop | Per user |
| verify-fail ×3 | Narrow / waive command | New Verify commands | Stop | Ask |
| design-review ×3 | Raise cap | Ship Enhancements only | Stop | 3 if Critical/Major remain |
| review Fix ×3 | Raise cap | Defer Enhancements | Stop / backloop | Ask |
| test↔fix ×3 | Raise cap / re-run test | Stop | — | Ask; **no** inventable lite/full waive → Gate C (skip-review escape+provenance only — [gate-c.md](gate-c.md)) |
| Mid-run reclassify | Stay simple | Upgrade full | New slug / stop | 2 when API/DB/auth |
| Task count ≥25 (Mode full) | Continue | Slim / reclassify | Stop | Ask |
| main-thread fallbacks ≥3 | Continue | Change model path | Stop | Ask |

## Run metrics (parent sole Round owner)

Required when section exists: Task count · verify-fail count · main-thread fallbacks.

Bump Round on `01a` / `03a-*` / review / test re-entry. Tasks must **not** invent Round.
