# Failure playbook (parent)

**This file is SoT for:** what the parent chats on hard stops and max-rounds.  
Decision shapes: [invariants.md](invariants.md). Pipeline: [stages.md](stages.md). Design-backloop: [design-backloop.md](design-backloop.md).  
Veto / Gate B: [hitl-gate-b.md](hitl-gate-b.md). Gate C: [hitl-gate-c.md](hitl-gate-c.md). Provenance / parent-only: [hitl.md](hitl.md). Skip-review ban: [lenses.md](lenses.md).

## Quick map

| Situation | Parent action | Chat |
|-----------|---------------|------|
| **Gate A escalate** (`01a` Result escalate) | Pause; Decision N | Re-run Gate A · human override Result `ok` + Notes **only after explicit user yes** · Stop — never invent `ok` ([results.md](results.md) · [invariants.md](invariants.md)) |
| **verify-fail** after 3 attempts | Pause; Decision N (verify-fail shape) | Options: narrow/waive · different Verify commands · Stop |
| **design-review / design-verify** after 3 Update rounds | Pause; Decision N | Raise cap · ship Enhancements-only if clean · Stop/reclassify |
| **review Fix** after 3 rounds | Pause; Decision N | Raise cap · defer Enhancements if clean · Stop / design-backloop |
| **test↔fix** after 3 rounds | Pause; Decision N | Raise cap · waive green tests → Gate C · Stop |
| **Design-backloop** (design invalid after Build) | Pause; Decision N | Amend → Notes `design-backloop`, **Gate B approved: none**, clear Build armed / veto-window; if prior `05`/`06` Results exist → Notes `- review-stale` / `- test-stale` (or clear Results) ([verify-and-fix.md](verify-and-fix.md) Stale); Next `design-update` (Decision N is entry — no prior `03a` Fix ask); Fix-only · Stop ([design-backloop.md](design-backloop.md)) |
| **Gate B veto** before Build (`pending`) | Do **not** Build | Settle veto or re-open Gate B ([hitl-gate-b.md](hitl-gate-b.md)) |
| **Veto window open** without **Build armed** / incomplete async gap | Do **not** Build | Run `--next` → copy `async-gap-pending`; arm with later HH:MM; or settle veto ([hitl-gate-b.md](hitl-gate-b.md)) |
| **Missing provenance** (Gate B/C approved, waivers, docs-only, smoke-pass-rerun, card-override) | Do **not** Build / Merge / unlock unsafe Next | **Parent** copies verbatim quote from latest user message (≥12 chars) into `provenance — <kind> — user: "…"` ([hitl.md](hitl.md)) |
| **Gate B veto after Build** | Pause; Decision N | Discard · Keep + re-open → **Gate B approved: none**, clear armed/window, Next `gate-b` · Stop ([hitl-gate-b.md](hitl-gate-b.md) · [invariants.md](invariants.md)) |
| **Max-round cap** (Round ≥3 / Verify attempts ≥3 / metrics) | `--next` → `do-not-launch` | Decision N ([invariants.md](invariants.md)); parent must have incremented Round / metrics. To raise cap: Notes `- max-round-cap — <domain> — <N> — user: "…"` (domains: `design-review` \| `gate-a` \| `verify` \| `review-fix` \| `test-fix`) |
| **Usage limit** on Task | Wait 5s → same model → `inherit` → main-thread that stage only | Log only; do not ask unless inherit fails and main-thread also blocked |
| **User reject / stop / abort** | Status `stopped` (not `done`) | Freeze stage + reason; require new Decision to resume |
| **Merge success** + `merge` ∈ Gate C approved | Status `done` | Do not continue; new work → new slug |
| **Silence at blocking gate** | Stay paused | Do not invent approval |
| **Mid-run scope growth** (API/DB/auth) | Decision N (reclassify) | Stay simple · Upgrade full · New slug/stop — **never** keep `skip-review` if contracts appear |
| **Has API/DB flips yes under skip-review** | Drop skip-review → **lite** (or reclassify) | One-liner: set Has API/DB **yes**, Review profile **lite**, re-lint — [examples/drop-skip-review-api-flip.md](examples/drop-skip-review-api-flip.md) |
| **Smoke gap under skip-review** | Ordered recovery | (1) Prefer Notes `smoke re-run` once → (2) re-Build → (3) drop skip-review → lite → (4) waivers last ([verify-and-fix.md](verify-and-fix.md) Skip-review + Smoke ordered recovery) |
| **review-stale / test-stale** (Notes) | Do **not** merge | Re-enter review / test-full|test-lite; clear token only after fresh clean/success — lint `--before-merge` errors; `--next` do-not-launch ([verify-and-fix.md](verify-and-fix.md)) |
| **Task count ≥ 25** (Mode full, running) | Decision N (soft budget) | Continue · Reclassify/slim · Stop ([invariants.md](invariants.md)) |
| **Missing clarity-check token** | Do **not** launch; `--next` → `do-not-launch` | Exact `clarity-check ok — <Next>` for every clarity boundary. Open the boundary file ([parent-next.md](parent-next.md)); re-run `--next` |
| **main-thread fallbacks ≥ 3** (running) | Decision N (soft pause) | Continue · Reclassify/model path · Stop ([invariants.md](invariants.md)) |
| **Gate C decline / silence** | Stay paused or `stopped` | No commit/push/PR/merge |
| **Merge success without `merge` in Gate C approved** | Stay `paused` | Leave Next for remaining actions — do not set `done` ([results.md](results.md)) |
| **async-notify Gate B on Mode full** | Do not — use **blocking** | [hitl-gate-b.md](hitl-gate-b.md) |
| **Blocking Gate B without Gate B approved** | Do **not** Build | **Parent** sets **Gate B approved** `yes` (or named pick) **+** provenance `gate-b-approved` — [hitl-gate-b.md](hitl-gate-b.md) |

## Anti-loop rules

- Max **3** attempts per stage entry unless the user raises the cap in Decision N **and** parent writes `max-round-cap — <domain> — <N> — user: "…"` ([invariants.md](invariants.md)).
- Do **not** re-launch the same Fix/Verify loop without a new Decision after the cap.
- Do **not** silently rewrite `03-design` / `04-tasks` inside Build or Fix — use design-backloop.
- Do **not** treat Gate B auto/async as Gate C approval.

## After the user picks

1. Log the Decision N Option in Run log + Notes.
2. Update Orchestrator card **Next step**.
3. Resume only the chosen path (do not continue the old failing loop).
