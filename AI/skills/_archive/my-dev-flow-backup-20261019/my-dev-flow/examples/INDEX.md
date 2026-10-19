# Golden path examples

Every golden path includes a fixed **Parent before each Task** block:

1. Clarity boundary + boundary-matched token ([parent-next.md](../parent-next.md))
2. `--next --derive` (or `preflight.py`)
3. `--snapshot-consent` before launch; `--check-consent-writes` after
4. `handoff-for.py` on exit 0

**After any parent consent/waiver write** (Gate B/C approved, Build armed, provenance, smoke-waive / smoke-pass-rerun / docs-only / card-override): append Run log `parent consent write — <kind>`, then re-snapshot (`--snapshot-consent`). Align: [simple-auth-gate-b-blocking.md](simple-auth-gate-b-blocking.md). SoT: [hitl.md](../hitl.md) · launch card [orchestrator-rules.md](../orchestrator-rules.md).

| Example | When |
|---------|------|
| [simple-bugfix.md](simple-bugfix.md) | Mode simple + lite happy path (non-auth helper) |
| [simple-api-gate-b-blocking.md](simple-api-gate-b-blocking.md) | Mode simple + Has API/DB yes → Gate B **blocking** + provenance |
| [simple-auth-gate-b-blocking.md](simple-auth-gate-b-blocking.md) | Mode simple + API=no DB=no **auth=yes** → Gate B **blocking** |
| [simple-skip-review.md](simple-skip-review.md) | Mode simple + legal skip-review → Gate C escape + provenance |
| [async-gate-b-build-armed.md](async-gate-b-build-armed.md) | Mode simple Gate B async-notify → one-turn gap → Build armed → Build |
| [full-lite-review.md](full-lite-review.md) | Mode full + Review profile lite |
| [full-api-db.md](full-api-db.md) | Mode full + API∥DB |
| [reclassify-simple-to-full.md](reclassify-simple-to-full.md) | Mid-run scope growth |
| [design-backloop-after-build.md](design-backloop-after-build.md) | Design invalid after Build |
| [drop-skip-review-api-flip.md](drop-skip-review-api-flip.md) | Has API/DB flips yes under skip-review |
| [max-round-decision-n.md](max-round-decision-n.md) | Round / Verify attempts ≥3 → Decision N (+ raise-cap) |
| [gate-a-escalate.md](gate-a-escalate.md) | Gate A Result **escalate** → Decision N (never invent ok) |
| [anti-patterns.md](anti-patterns.md) | Wrong → right pairs |
