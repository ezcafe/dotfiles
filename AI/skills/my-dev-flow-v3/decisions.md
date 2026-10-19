# Decisions + max rounds

**Option shape:** What / Example / Pros / Cons / Recommendation. Number Decision N and Option 1/2/3.

## Caps

| When | Prefer |
|------|--------|
| Gate A escalate | Ask; never invent `ok` |
| Design-backloop | Amend → re-review → Gate B if contracts/IA change. On Amend: Notes `design-backloop`; bump settle gen; clear Gate B consent; Last Verify pending; invalidate overall + isolated `03a` clean; keep stale Notes ([design-backloop.md](design-backloop.md)) |
| verify-fail ×3 | Ask |
| design-review / review Fix / test↔fix ×3 | Ask; no inventable lite/full waive → Gate C |
| Mid-run reclassify → full | Upgrade path in [step-0.md](step-0.md) |
| User override `skip-review` while Mode full or profile lite/full | Prefer Ask — stay stronger bar **or** switch simple+skip-review if legal. **Cannot** legalize Mode full + skip-review |
| Skip-review else (Prefer unpaid unmatched + Prefer-paid bar unmet, incl. Smoke-done/escape-missing) | Prefer stay + ask escape **or run Smoke** vs drop → lite; named user yes required |
| Task count ≥25 (Mode full) | Ask slim / reclassify |

## Round owner

Parent sole Round owner. Tasks must not invent Round.
