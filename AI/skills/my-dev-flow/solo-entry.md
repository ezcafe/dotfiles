# Subflow solo entry

Run a subflow **alone** when its prerequisites are met. Full pipeline order: [stages.md](stages.md).

| Skill | Min artifacts / state | Typical next after solo |
|-------|----------------------|-------------------------|
| [`my-dev-flow-design`](../my-dev-flow-design/SKILL.md) | `00-run.md` + Mode; idea (or bootstrap); Gate A/skim if Mode full | design-review / design-verify-phase |
| [`my-dev-flow-design-review`](../my-dev-flow-design-review/SKILL.md) | `03-design.md`, `04-tasks.md`; Has API/DB yes\|no | Gate B (or Update → re-review) |
| [`my-dev-flow-code`](../my-dev-flow-code/SKILL.md) TDD | `03`+`04` with planned tests; code clarity-check + `clarity-check ok — tdd-review` | Gate B → Build |
| [`my-dev-flow-code`](../my-dev-flow-code/SKILL.md) Build | Gate B settled ([hitl.md](hitl.md): **blocking** → **Gate B approved** `yes`/named pick; **async-notify** → **Build armed** + one-turn gap; **auto** may leave approved `none`); `Gate B veto: none`; Verify commands set; design-review **or** design-verify-phase Result **clean** (by Mode); skip-review legality: [lenses.md](lenses.md); code clarity-check + `clarity-check ok — build` | Smoke skip → review (or Gate C if legal skip-review — [lenses.md](lenses.md)) |
| [`my-dev-flow-code`](../my-dev-flow-code/SKILL.md) Fix | Fix ask in `05-review-log` or `06-test-log`; Verify commands; code clarity-check + `clarity-check ok — fix-review|fix-tests` | Re-review or re-test that mode |
| [`my-dev-flow-review`](../my-dev-flow-review/SKILL.md) | Build verify-pass + Smoke section; Review profile ≠ skip-review | test-full (profile full) / test-lite (profile lite) |
| [`my-dev-flow-test`](../my-dev-flow-test/SKILL.md) smoke | Only when Build-writes-Smoke incomplete / mismatch | review or Fix |
| [`my-dev-flow-test`](../my-dev-flow-test/SKILL.md) full/lite | Review clean (unless skip-review) | Gate C |
| [`my-dev-flow-merge`](../my-dev-flow-merge/SKILL.md) | Gate C **explicit yes** naming each action; test bar per [hitl.md](hitl.md); code clarity-check Merge + `clarity-check ok — merge` | Status `done` only when Merge Result **success** **and** `merge` ∈ Gate C approved |

**Grill-only:** [grill.md](grill.md) needs Analyze / idea (or `02-analysis.md`); not a substitute for Design.

When solo: still honor Verify gate, severity exit, and **required** `scripts/handoff-for.py <stage-id>` ([handoffs.md](handoffs.md) = edit SoT / debug only). Update `00-run.md` Orchestrator card.
