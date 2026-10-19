# HITL — human in the loop

**SoT for:** Parent-only consent, Notes↔provenance pairs, honesty residual, `card-override`.

## Parent-only (Tasks must never write)

- Gate B approved / veto / Build armed / `gate-b auto — gen:<N>`  
- Gate C approved (named actions)  
- Waiver / escape Notes: `docs-only`, `smoke-waive`, `gate-c-test-override`, `smoke-pass (re-run)`, `smoke re-run`, `has-flip — …`  
- Provenance lines on `00-run.md`  
- Round bumps, Status lifecycle, settle gen bumps  

## Notes ↔ provenance

Every escape / approval Note that unlocks a Prefer path needs a matching provenance entry:

| Notes token | Provenance key | Form |
|-------------|----------------|------|
| Gate C named yes | `gate-c-approved` | `user: "<exact words ≥12 chars>"` |
| `docs-only` / `smoke-waive` / `gate-c-test-override` | same id | `user: "…"` |
| `smoke-pass (re-run)` | `smoke-pass-rerun` | **Evidence** after Smoke Task: `evidence: Smoke-Task + 06 Smoke after verify-pass settle-gen=<N>` — **no fake user quote** |

Do **not** invent quotes. Honesty residual: markdown shape ≠ cryptographic proof.

## Tiers

| Gate | Default |
|------|---------|
| Gate A | Soft (escalate Decision N) |
| Grill | Async-notify → stay running; settle frontier same turn — do **not** advance to Design while Grill open ([grill.md](grill.md)) |
| Gate B | Mode full = **blocking**; Mode simple = **auto** only when API=no DB=no auth=no; else **blocking**. Async-notify only when user asks for a veto window on the low-risk auto path |
| Gate C | Always **blocking** |

## card-override

Allowed only for Next↔derive mismatch. **Cannot** waive unpaid tests, illegal Mode×profile, design-stale Build, or Gate C named-yes.
