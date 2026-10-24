# Solo subflow entry

When user runs a subflow alone:

1. Require min-state on `00-run.md` (Mode, profile, settle gen, Has flags).  
2. Preflight → derive still apply if orchestrating multi-step.  
3. Respect Gate B/C consent — labeled solo stamps Notes+provenance after AskQuestion (same pairs as [hitl.md](hitl.md)); never invent quotes.  
4. E1: independent Smoke with `Smoke source: Smoke-Task` before Adv (Notes companion only).  
5. **skip-review:** Prefer unpaid independent Smoke (`Smoke source: Smoke-Task`); Build-writes-Smoke does **not** waive. Prefer-re-smoke order + Prefer paid escape Notes↔provenance — [verify.md](verify.md) · [../my-dev-flow-v3-test/SKILL.md](../my-dev-flow-v3-test/SKILL.md).  
6. Gate B: `unknown` ≠ `no` (blocking / no auto until explicit `no`) — [lenses.md](lenses.md) · [gate-b.md](gate-b.md).  
7. test-full/lite: on success clear `test-stale` when Lite/full clear met ([hitl.md](hitl.md) · [verify.md](verify.md)); Prefer `merge`\|`gate-c` only when **Tests success** **and** **Lenses clean**.
8. **Consent Notes carve (labeled solo):** after AskQuestion answers, solo stamps Notes+provenance (`ideation-confirmed` / `ideation-skip` / `grill-skip` / `tiny-contract-tweak` / Gate B/C / escape tokens as required) — pays ideation/grill / tiny without a separate parent. **Orchestrated Task:** return `candidate …` only + Parent-relay — never AskQuestion, never stamp Notes ([hitl.md](hitl.md) · [brainstorm.md](brainstorm.md) · [grill.md](grill.md) · [lenses.md](lenses.md)).  
9. **Lifecycle / Has (orchestrated Task):** never write lifecycle Notes (`design-stale` / `design-backloop` / `review-stale` / `test-stale` / `waiting — <reason>`), card Has, or provenance — return `candidate …` / `proposed Has` / `candidate clear …` only; parent applies ([hitl.md](hitl.md)). Labeled solo acting as orchestrator applies lifecycle / Has / Status / Last stage / Next / verify stamps per [hitl.md](hitl.md) · [preflight.md](preflight.md) Always §8.  
10. **Isolation:** solo agent **is** the skill runner — no nested Task required; solo may AskQuestion / settle frontier same turn. Orchestrator parent **must** spawn per [spawn-contract.md](spawn-contract.md) (Skill map + Hard stop / Return shape SoT); After = [step-0.md](step-0.md) After Task. Parent-relay HITL (Task never AskQuestion); hard-stop back to parent on HITL / parent-only Next / skill boundary ([hitl.md](hitl.md)).
11. **Skill-boundary (labeled solo):** if derived Next is **outside** the invoked skill’s stage ids ([spawn-contract.md](spawn-contract.md) Skill map) → open that skill’s stage file(s) from [parent-next.md](parent-next.md) Open 1–2 **or** hard-stop with `skill-boundary:<id>` (mirror Hard stop #2). Do **not** improvise cross-skill procedure without loading the owning stage. Parent-inline Next (`gate-b` / `gate-c` / `finalize-lens-plan`) → Open 1–2 from parent-next; no skill Task.
