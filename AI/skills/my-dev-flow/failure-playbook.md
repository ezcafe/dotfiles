# Failure playbook (parent)

**This file is SoT for:** what the parent chats on hard stops and max-rounds.  
Decision shapes: [invariants.md](invariants.md). Pipeline: [stages.md](stages.md).  
Veto / Gate C: [hitl.md](hitl.md). Skip-review ban: [lenses.md](lenses.md).

## Quick map

| Situation | Parent action | Chat |
|-----------|---------------|------|
| **verify-fail** after 3 attempts | Pause; Decision N (verify-fail shape) | Options: narrow/waive · different Verify commands · Stop |
| **design-review / design-verify** after 3 Update rounds | Pause; Decision N | Raise cap · ship Enhancements-only if clean · Stop/reclassify |
| **review Fix** after 3 rounds | Pause; Decision N | Raise cap · defer Enhancements if clean · Stop / design-backloop |
| **test↔fix** after 3 rounds | Pause; Decision N | Raise cap · waive green tests → Gate C · Stop |
| **Design-backloop** (design invalid after Build) | Pause; Decision N | Amend design · Fix-only · Stop |
| **Gate B veto** before Build (`pending`) | Do **not** Build | Settle veto or re-open Gate B ([hitl.md](hitl.md)) |
| **Veto window open** without **Build armed** | Do **not** Build | Arm Build on this turn / resume, or settle veto ([hitl.md](hitl.md)) |
| **Gate B veto after Build** | Pause; Decision N | Discard draft · Keep + re-open Gate B · Stop |
| **Usage limit** on Task | Wait 5s → same model → `inherit` → main-thread that stage only | Log only; do not ask unless inherit fails and main-thread also blocked |
| **User reject / stop / abort** | Status `stopped` (not `done`) | Freeze stage + reason; require new Decision to resume |
| **Merge success** | Status `done` | Do not continue; new work → new slug |
| **Silence at blocking gate** | Stay paused | Do not invent approval |
| **Mid-run scope growth** (API/DB/auth) | Decision N (reclassify) | Stay simple · Upgrade full · New slug/stop — **never** keep `skip-review` if contracts appear |
| **Task count ≥ 20** (Mode full, running) | Decision N (soft budget) | Continue · Reclassify/slim · Stop ([invariants.md](invariants.md)) |
| **main-thread fallbacks ≥ 3** (running) | Decision N (soft pause) | Continue · Reclassify/model path · Stop ([invariants.md](invariants.md)) |
| **Gate C decline / silence** | Stay paused or `stopped` | No commit/push/PR/merge |
| **async-notify Gate B on Mode full** | Do not — use **blocking** | [hitl.md](hitl.md) Default Gate B (Option A) |

## Anti-loop rules

- Max **3** attempts per stage entry unless the user raises the cap in Decision N.
- Do **not** re-launch the same Fix/Verify loop without a new Decision after the cap.
- Do **not** silently rewrite `03-design` / `04-tasks` inside Build or Fix — use design-backloop.
- Do **not** treat Gate B auto/async as Gate C approval.

## After the user picks

1. Log the Decision N Option in Run log + Notes.
2. Update Orchestrator card **Next step**.
3. Resume only the chosen path (do not continue the old failing loop).
