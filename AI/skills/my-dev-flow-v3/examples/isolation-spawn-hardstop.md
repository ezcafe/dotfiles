# Golden: isolation spawn + hard stop

**SoT:** [../spawn-contract.md](../spawn-contract.md) (Skill map + Hard stop) · [../step-0.md](../step-0.md) Load budget §5 + After Task checklist · [../subagents.md](../subagents.md) optional narrative.

## Happy path (orchestrator)

1. Derive Expected Next → skill-mapped (e.g. `design`).  
2. Open [../spawn-contract.md](../spawn-contract.md) only → spawn **fresh** local `Task` for `my-dev-flow-v3-design` (Hard stop list inlined in prompt).  
3. Task continues unpaid stages **in that skill only** until Hard stop.  
4. Return shape includes After signals (never Status / Last stage / Next / Notes / card Has / verify-stamp writes; never AskQuestion).  
5. Parent After Task: follow [../step-0.md](../step-0.md) After Task checklist (+ Always §8) — open [../hitl.md](../hitl.md) as needed → apply signals → stamp Status / Last stage / Next / verify fields → re-derive.

## Hard stops (Task must return)

| Stop | Example |
|------|---------|
| Parent-only Next | Prefer would be `gate-b` / `gate-c` / `finalize-lens-plan` |
| Skill boundary | design unpaid empty → next Prefer is design-review skill |
| HITL / consent | ideation confirm, grill frontier, Gate C named yes |
| Candidate-apply | `proposed Has`, `candidate design-stale`, `candidate Status: done\|paused` |
| Verify / failure cap | verify-fail at max → parent Decision N / pause |

## HITL re-entry — golden turn transcript

**Ideation (2 relays):**

```text
Parent: spawn design Task, Expected Next=ideation
Task: writes Q1 into 01-idea; Return Stop reason=hitl:ideation;
      Blocked / questions for user: <Q1>
Parent: presents Q1 → user answers → stamps ideation-confirmed + provenance
Parent: re-derive → Expected Next=design-phase (simple) or gate-a (full)
      — never force ideation after paid ([simple-bugfix.md](simple-bugfix.md))
Parent: re-spawn design Task with that Expected Next
```

**Grill (one frontier round):**

```text
Parent: spawn design Task, Expected Next=grill
Task: writes frontier Q1–Qn into 02b; Result=needs-round;
      Return Stop reason=hitl:grill-frontier; Blocked / questions: <frontier>
Parent: presents frontier → user answers → (optional) Task re-spawn applies answers → frontier-empty
      or candidate grill-skip → parent Notes grill-skip (labeled solo may stamp after AskQuestion — [../solo-entry.md](../solo-entry.md))
```

Checklist: [../spawn-contract.md](../spawn-contract.md) HITL re-entry.

## Anti (Wrong → Right)

| Wrong | Right |
|-------|-------|
| Parent runs `build` inline while orchestrating | Spawn `my-dev-flow-v3-code` Task |
| One Task continues into design-review after design idle | Hard stop → parent re-derives → new Task |
| Merge Task writes Status `done` | Return `Result: success` + `candidate Status: done`; parent stamps |
| Task writes card Last stage / Next | Return shape reports `Last stage:` only; parent stamps card |
| Task AskQuestion for grill / ideation | Return `Blocked / questions`; parent presents |
| Load full [../subagents.md](../subagents.md) every turn for spawn | Load budget §5 → [../spawn-contract.md](../spawn-contract.md) only (map inlined); After = step-0 checklist |
