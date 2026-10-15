# Golden path — design-backloop after Build

Short recovery. SoT: [stages.md](../stages.md) Design-backloop · [invariants.md](../invariants.md) · [failure-playbook.md](../failure-playbook.md).

## Trigger

Build/Fix verify-fail (or review Critical/Major) cannot stay aligned with `03`/`04` without contract or IA change.

## Parent actions

1. Pause; **Decision N**: Amend design · Fix-only · Stop.
2. Prefer **Amend design** when contracts/IA must change.
3. Log Notes `design-backloop`; prior Gate B **invalid**.
4. Set **`Gate B approved: none`**; clear Notes **Build armed** and veto-window tokens; card Next = `design-update`. Decision N Option 1 is enough entry — no prior `03a` Fix ask required.
5. Do **not** silently rewrite `03`/`04` inside Build/Fix.
6. Resume: `design-update` → design-review / design-verify-phase → **Gate B** (Next=`gate-b` while token still present) → Fix/Build.
7. After Gate B re-settle, clear Notes `design-backloop` by HITL tier: **blocking** → clear + approved yes/named pick; **auto** → clear (approved may stay `none`); **async-notify** → clear + Build armed rules. Then Build when armed.
8. Advance only on Result tokens in [results.md](../results.md) (`clean`, then `verify-pass`).

## Do not

- Launch Build while Notes still say `design-backloop` (lint error — including soft Gate B / approved `none`; `--next` redirects `build` only)
- Set Next `build` before design-update + re-review; after re-review, Next=`gate-b` with token still present is correct until settle
- Go to Gate C with a known design mismatch
- Treat Gate B veto-after-Build as the same Decision (that shape is in [hitl.md](../hitl.md))
