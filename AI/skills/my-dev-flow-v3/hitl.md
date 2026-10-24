# HITL — human in the loop

**SoT for:** Parent-only consent, Notes↔provenance pairs, honesty residual, **Parent-relay** (orchestrated) vs solo conversational HITL. `card-override` → Unsafe jumps SoT only ([derive-next.md](derive-next.md)).

## Parent-relay (orchestrated Option B) — SoT

When the parent spawns an isolated skill Task ([spawn-contract.md](spawn-contract.md); [subagents.md](subagents.md) optional narrative only):

1. **Task never AskQuestion** (or otherwise chat the user) for HITL / consent / frontier answers.  
2. Task writes questions into the artifact **and** Return shape `Blocked / questions for user`.  
3. Task **hard-stops** (Stop reason `hitl:<kind>`).  
4. **Parent** presents questions to the user; stamps Notes + provenance when required.  
5. Parent re-spawns a **fresh** Task after answers ([spawn-contract.md](spawn-contract.md) HITL re-entry).

**Orchestrated Task** = `candidate …` only + Parent-relay — never stamps Notes / provenance / Status / Last stage / Next / verify.

## Labeled solo carve — SoT

When the user runs a subflow **alone** ([solo-entry.md](solo-entry.md)):

1. Solo **may** AskQuestion / settle frontier same turn.  
2. After answers: solo stamps **Notes+provenance** (consent / waiver / ideation-confirmed / ideation-skip / grill-skip / `tiny-contract-tweak` / Gate B·C / escape tokens) — same pairs as Notes↔provenance below.  
3. Solo acting as orchestrator also stamps Status / Last stage / Next / verify / lifecycle / card Has per Always §8 ([preflight.md](preflight.md)).  
4. Do **not** invent quotes. Honesty residual still applies.

“Stay running / settle frontier same turn” applies to **solo** only — **not** orchestrated Task runs.

## Parent-only (Tasks must never write)

- Gate B approved / veto / Build armed / `gate-b auto — gen:<N>`  
- Gate C approved (named actions)  
- Waiver / escape / consent Notes: `docs-only`, `smoke-waive`, `gate-c-test-override`, `smoke-pass` (alias `smoke-pass (re-run)`), `smoke re-run`, `has-flip — …`, `tiny-contract-tweak`, `ideation-skip` / preferred `ideation skipped — <reason>`, `ideation-confirmed`, `grill-skip` / preferred `grill skipped — <reason>`, `04a skipped` / `04a skipped — <reason>`  
- **Lifecycle Notes (set + clear):** `design-stale`, `design-backloop`, `review-stale`, `test-stale`, `waiting — <reason>` — **Orchestrated Task:** return `candidate …` only; parent sets and clears. **Labeled solo** acting as orchestrator may set/clear ([step-0.md](step-0.md) Upgrade · [design-backloop.md](design-backloop.md) · [verify.md](verify.md) Stale · [resume.md](resume.md) · [solo-entry.md](solo-entry.md))  
- Card **Has** flags (`Has UI` / `Has API` / `Has DB` / `Has auth/PII/schema`) — **Orchestrated Task:** return `proposed Has: …` only; parent applies. **Labeled solo** applies when acting as orchestrator ([lenses.md](lenses.md) · [preflight.md](preflight.md) Always §4 · [solo-entry.md](solo-entry.md))  
- Provenance lines on `00-run.md`  
- Round bumps, **Status lifecycle** (stamp from `candidate Status: done|paused` after merge / pause signals — **Orchestrated Task** never writes Status; parent **or** labeled solo stamps), **Gate B settle gen** bumps  
- Profile drop (e.g. skip-review → lite on Has flip)  
- **Card pipeline fields:** **Last stage**, card **Next** — **Orchestrated:** parent after Task ([preflight.md](preflight.md) Always §8 · [step-0.md](step-0.md) After Task); Return shape may *report* `Last stage: <id>` — Tasks never write those card fields. **Labeled solo** stamps when acting as orchestrator ([solo-entry.md](solo-entry.md))  
- **Verify stamp fields:** `Last Verify`, `Last verify-pass at`, `Last verify settle-gen` — **Orchestrated:** parent on stage `Result: verify-pass` ([verify.md](verify.md) · [preflight.md](preflight.md) Always §8); stages return Result only. **Labeled solo** stamps when acting as orchestrator ([solo-entry.md](solo-entry.md))  

**Ownership rule:** **Orchestrated Task** → return signal only (`proposed Has: …`, `Has flip detected`, `candidate Status: done|paused`, `candidate tiny-contract-tweak`, `candidate ideation-skip`, `candidate ideation-confirmed`, `candidate grill-skip`, `candidate 04a skipped`, `candidate design-stale`, `candidate design-backloop`, `candidate review-stale`, `candidate test-stale`, `candidate waiting — <reason>`, `candidate clear design-stale`, `candidate clear review-stale`, `candidate clear test-stale`, `candidate clear waiting`, …) + Parent-relay — never write those Notes, card Has, Status, Last stage, Next, verify stamps, or clear lifecycle Notes. **Parent** (after Parent-relay / applying After signals) **or labeled solo** (acting as orchestrator — after AskQuestion / when applying After signals) writes the Notes / settle / provenance / profile-drop / card Has / Status / **Last stage** / card **Next** / verify stamp fields above ([solo-entry.md](solo-entry.md) · labeled solo carve).

**`candidate design-stale` ban:** parent applies Notes `design-stale` **only** with card **Mode = full** (same turn as Mid-run Upgrade — [step-0.md](step-0.md)). Mode simple ∧ `candidate design-stale` → Decision N / Upgrade first; never set Notes `design-stale` on a simple card.

### Lifecycle clear predicates (parent / labeled solo as orchestrator)

| Notes | Clear only when |
|-------|-----------------|
| `design-stale` | Mode-full `design` + `03` rewrite Result `done` ([step-0.md](step-0.md) Upgrade). While set: Prefer **Grill open** → `grill` first, then unpaid among **Analyze unpaid** → **Grill unpaid** → **design unpaid under design-stale** ([derive-next-defs-pre.md](derive-next-defs-pre.md) · [derive-next-pre.md](derive-next-pre.md)) |
| `design-backloop` | Design clean ∧ **04a ok** ∧ **Gate B settled post-Notes** ([design-backloop.md](design-backloop.md) · [derive-next-defs-pre.md](derive-next-defs-pre.md)) |
| `review-stale` | [verify.md](verify.md) Stale lite/full clear (skip-review: N/A clear) |
| `test-stale` | [verify.md](verify.md) Stale clear rules met |
| `waiting — <reason>` | Wait reason resolved (user answer / Build arm / remaining Gate C named yes) — Stages return `candidate waiting — …` / `candidate clear waiting` only ([resume.md](resume.md) · [derive-next-post.md](derive-next-post.md)) |

## Notes ↔ provenance

Every escape / approval Note that unlocks a Prefer path needs a matching provenance entry:

| Notes token | Provenance key | Form |
|-------------|----------------|------|
| Gate B approved (blocking settle) | `gate-b-approved` | `user: "<exact words ≥12 chars>"` |
| Gate C named yes | `gate-c-approved` | `user: "<exact words ≥12 chars>"` |
| `docs-only` / `smoke-waive` / `gate-c-test-override` | same id | `user: "…"` |
| `smoke-pass` (alias `smoke-pass (re-run)`) | `smoke-pass-rerun` | **Evidence** after Smoke Task: `evidence: Smoke-Task + 06 Smoke after verify-pass settle-gen=<N>` — **no fake user quote**. Used on **first-pass and Prefer-re-smoke** independent Smoke success. Canonical Notes token = `smoke-pass`; alias `(re-run)` only ([verify.md](verify.md)) |
| `ideation-skip` / `ideation skipped — <reason>` | `ideation-skip` | `user: "<exact words ≥12 chars>"` **or** evidence of user skip ideation / approved throwaway — Stages return `candidate ideation-skip` only ([brainstorm.md](brainstorm.md)) |
| `ideation-confirmed` | `ideation-confirmed` | `user: "<exact words ≥12 chars>"` — parent after Parent-relay **or** labeled solo after AskQuestion; Stages return `candidate ideation-confirmed` only ([brainstorm.md](brainstorm.md) · [solo-entry.md](solo-entry.md)) |
| `grill-skip` / `grill skipped — <reason>` | `grill-skip` | `user: "<exact words ≥12 chars>"` **or** evidence of user skip grill — Stages return `candidate grill-skip` only ([grill.md](grill.md)) |
| `04a skipped` / `04a skipped — <reason>` | `04a-skipped` | `user: "<exact words ≥12 chars>"` (named yes) — Stages return `candidate 04a skipped` only |
| `tiny-contract-tweak` / `tiny-contract-tweak — <reason>` | `tiny-contract-tweak` | `user: "<exact words ≥12 chars>"` **or** evidence of user tiny-approve — Stages return `candidate tiny-contract-tweak` only ([lenses.md](lenses.md) Tiny) |
| `gate-b auto — gen:<N>` | *(token itself)* | Notes **or** Run-log line with **current** settle gen — no user quote |
| Build armed (async settle) | *(card field)* | `**Build armed:** yes` + Run-log arm for current settle gen after veto window — no user quote |

Do **not** invent quotes. Honesty residual: markdown shape ≠ cryptographic proof.

## Tiers

| Gate | Default |
|------|---------|
| Gate A | Soft (escalate Decision N) |
| Grill | **Orchestrated:** Parent-relay — Task hard-stops each frontier round; parent presents; re-spawn ([spawn-contract.md](spawn-contract.md)). **Solo:** async-notify → stay running; settle frontier same turn — do **not** advance to Design while Grill open ([grill.md](grill.md)) |
| Gate B | Mode full = **blocking**; Mode simple = **auto** only when API=no ∧ DB=no ∧ auth/PII/schema=no (explicit `no`); else **blocking** (yes **or** unknown). Async-notify only when user asks for a veto window on the low-risk auto path ([gate-b.md](gate-b.md)) |
| Gate C | Always **blocking** |

## card-override

Allowed only for Next↔derive mismatch. **Cannot** waive Unsafe jumps — full non-waive set is SoT in [derive-next.md](derive-next.md) (do not restate here).
