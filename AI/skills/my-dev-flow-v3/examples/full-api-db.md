# Golden: full API+DB

**Prefer checkpoints:** ideation (`ideation-confirmed`) → Gate A → skim → Analyze → Grill `frontier-empty` → Design → Isolated API∥DB → design-review clean → Prefer `tdd-review` if **04a unpaid / dirty**; else Prefer `gate-b` when **04a ok**; `finalize-lens-plan` if missing required api/db; Smoke-Task before Adv.

**Isolation (Option B):**

- Spawn `my-dev-flow-v3-design` Task for unpaid design stages; HITL → hard-stop → Parent-relay → After Task → re-derive → re-spawn (same pattern as [simple-bugfix.md](simple-bugfix.md) · [isolation-spawn-hardstop.md](isolation-spawn-hardstop.md)).
- Isolated API∥DB = **two** design-review Tasks **same turn**; then spawn design-review for general `design-review` after Isolated paid.

1. Step 0 → Mode full, profile full  
2. Spawn design Task → Brainstorm hard-gate → Parent-relay → Notes `ideation-confirmed` + provenance → re-derive → Gate A → skim → Analyze → Grill frontier-empty → Design (re-spawn across hard stops)  
3. Both Isolated unpaid → same-turn two Tasks API∥DB → design-review clean  
4. Prefer `tdd-review` if **04a unpaid / dirty**; else Prefer `gate-b` when **04a ok** → Gate B blocking → settle gen token → spawn code Task → Build (TDD)  
5. `finalize-lens-plan` if needed (**before Smoke and before Adv**) → Independent Smoke (`Smoke-Task`) **before** Adv → Quality → lenses (clean before test-*) → test-full → Gate C → merge
