# Orchestrator rules (short)

**SoT for:** parent habits across stages.  
Happy path: [stages.md](stages.md). Load budget: [step-0.md](step-0.md#load-budget). Design invalid: [design-backloop.md](design-backloop.md).

- Honor Full/Simple order in [stages.md](stages.md); one subflow at a time. Honor [Load budget](step-0.md#load-budget).
- Before each Task: [invariants.md](invariants.md); `lint-run.py --next --derive`; **required** `python3 {my-dev-flow}/scripts/handoff-for.py <stage-id>`.
- Design-review update → re-review. Smoke/test fail → Fix (verify-pass) → re-run.
- No advance on verify-fail; max 3 → Decision N. Design invalid → [design-backloop.md](design-backloop.md).
- Card Next step = stage id (+ Description from `handoff-for.py` output). Unsafe card vs derive → Notes `card-override — <reason>` **+** `provenance — card-override — user: "…"` ([hitl.md](hitl.md)), or fix card.
- Mode full Task count ≥25 → Decision N ([invariants.md](invariants.md)).
