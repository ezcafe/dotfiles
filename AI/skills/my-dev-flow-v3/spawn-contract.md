# Spawn contract (parent → Task) — SoT

**Load budget §5:** open **this file only** when Next maps to a subflow skill (not full [subagents.md](subagents.md) every turn). **Skill map is inlined below.** After Task checklist SoT = [step-0.md](step-0.md) After Task + [preflight.md](preflight.md) Always §8 — open [subagents.md](subagents.md) only if that checklist is missing (optional narrative). **Hard stop list is inlined below** (must paste into every Task prompt).

Use Cursor **Task** tool: `subagent_type=generalPurpose`, **local** (not cloud / not `best-of-n-runner` unless user asks). **Fresh** Task each time parent enters a skill (or re-enters after a hard stop). Do **not** dump prior stage transcripts into the prompt.

## Skill map (Expected Next → skill)

| Skill | Stage ids |
|-------|-----------|
| [`my-dev-flow-v3-design`](../my-dev-flow-v3-design/SKILL.md) | `ideation` / brainstorm, `gate-a`, `skim`, `analyze`, `grill`, `design`, `design-phase`, `design-update` |
| [`my-dev-flow-v3-design-review`](../my-dev-flow-v3-design-review/SKILL.md) | `api-contract-review`, `db-design-review`, `design-review`, `design-verify-phase` |
| [`my-dev-flow-v3-code`](../my-dev-flow-v3-code/SKILL.md) | `tdd-review`, `build`, `fix-tests` |
| [`my-dev-flow-v3-review`](../my-dev-flow-v3-review/SKILL.md) | `adversarial`, `quality`, `code-review-phase`, `lens-*`, `merge-findings`, `fix-review` |
| [`my-dev-flow-v3-test`](../my-dev-flow-v3-test/SKILL.md) | `smoke`, `test-full`, `test-lite` |
| [`my-dev-flow-v3-merge`](../my-dev-flow-v3-merge/SKILL.md) | `merge` |

**Parent-inline only (never map to a skill Task):** Step 0, `gate-b`, `gate-c`, `finalize-lens-plan`.

`api|db` both unpaid → spawn **two** design-review Tasks **same turn** (parallel Isolated) — same Prefer rule as today.

Prompt **must** include:

1. Skill name + absolute/repo path to that skill’s `SKILL.md`
2. Workflow slug path: `.my-docs/workflow/<slug>/`
3. Card snapshot: Mode, profile, Has flags, settle gen, Status, relevant Notes tokens (not full history)
4. **Expected Next** (first stage to run) + “continue unpaid stages **in this skill only** until Hard stop”
5. Ban list pointer: [hitl.md](hitl.md) Parent-only — Tasks never write parent-only fields. Same Ownership rule as [hitl.md](hitl.md) (paste or open).
6. **HITL ban:** Task must **not** AskQuestion (or otherwise chat the user) for HITL / consent / frontier answers. Put questions in the artifact **and** Return shape `Blocked / questions for user`. Hard-stop; parent presents; parent re-spawns after answers ([hitl.md](hitl.md) Parent-relay)
7. Open 1–2 paths for Expected Next ([parent-next.md](parent-next.md)) — Task reads those; parent already opened them for compose
8. **Hard stop list** (paste verbatim — Task must return when **any**):

```text
Hard stop — return to parent when any of:
1. Parent-only Next — derive would Prefer gate-b / gate-c / finalize-lens-plan
2. Skill boundary — next unpaid Prefer maps to a different skill
3. HITL / consent — need named user yes or parent Notes before Prefer continues
   (ideation confirm/skip, grill frontier answers or grill-skip, 04a skipped,
   Decision N, Gate B/C, escape Notes, Build arm, any candidate waiting — …)
4. Candidate that parent must apply before continue — proposed Has / Has flip,
   lifecycle candidate …, candidate Status: done|paused
5. Verify / failure cap — verify-fail at max, hard-stop, or candidate Status: paused
6. Skill unpaid empty — no further unpaid stage in this skill
Do not cross into another skill. Do not write parent-only fields
(Status / Last stage / Next / lifecycle Notes / card Has / consent / verify stamps).
Do not AskQuestion for HITL.
```

9. **Return shape** (required) — `Last stage:` here is a **report** only; parent stamps card Last stage / Next:

```text
Last stage: <id>
Results: <paths + Result tokens>
After signals: <proposed Has / candidate Status / candidate … / none>
Stop reason: <parent-only Next | skill-boundary:<next-skill|id> | hitl:<kind> | candidate-apply | verify-cap | skill-idle | …>
Blocked / questions for user: <if any — full Q text; parent presents>
```

**After apply:** follow [step-0.md](step-0.md) After Task checklist + [preflight.md](preflight.md) Always §8. Open [subagents.md](subagents.md) only if the checklist is missing (optional narrative).

## HITL re-entry (parent checklist)

After Stop reason `hitl:*` or non-empty `Blocked / questions for user`:

1. Apply After signals ([hitl.md](hitl.md)) — do **not** invent consent Notes yet  
2. Present questions to the user (parent chat / AskQuestion)  
3. On answers: parent stamps Notes + provenance when required ([hitl.md](hitl.md))  
4. Re-run routing pack → **re-derive** Expected Next — do **not** force the prior Next:  
   - answers without pay / frontier still open → often still `ideation` / `grill`  
   - after paid ideation confirm/skip → Prefer `gate-a` (Mode full) or `design-phase` (Mode simple) — **never** re-force `ideation` ([examples/simple-bugfix.md](examples/simple-bugfix.md))  
5. Spawn a **fresh** Task for the **mapped** skill with that Expected Next + card snapshot reflecting new Notes  

**Solo:** agent may AskQuestion / settle frontier same turn — labeled solo only ([solo-entry.md](solo-entry.md) · [grill.md](grill.md) · [brainstorm.md](brainstorm.md)).
