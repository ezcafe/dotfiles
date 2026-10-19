# HITL — human in the loop

**SoT for:** Parent-only consent, Notes↔provenance pairs, honesty residual. `card-override` → Unsafe jumps SoT only ([derive-next.md](derive-next.md)).

## Parent-only (Tasks must never write)

- Gate B approved / veto / Build armed / `gate-b auto — gen:<N>`  
- Gate C approved (named actions)  
- Waiver / escape / consent Notes: `docs-only`, `smoke-waive`, `gate-c-test-override`, `smoke-pass` (alias `smoke-pass (re-run)`), `smoke re-run`, `has-flip — …`, `tiny-contract-tweak`, `ideation-skip` / preferred `ideation skipped — <reason>`, `ideation-confirmed`, `grill-skip` / preferred `grill skipped — <reason>`, `04a skipped` / `04a skipped — <reason>`  
- **Lifecycle Notes (set + clear):** `design-stale`, `design-backloop`, `review-stale`, `test-stale`, `waiting — <reason>` — Stages return `candidate …` only; parent alone sets and clears ([step-0.md](step-0.md) Upgrade · [design-backloop.md](design-backloop.md) · [verify.md](verify.md) Stale · [resume.md](resume.md))  
- Card **Has** flags (`Has UI` / `Has API` / `Has DB` / `Has auth/PII/schema`) — stage returns `proposed Has: …` only; parent applies ([lenses.md](lenses.md) · [preflight.md](preflight.md) Always §4)  
- Provenance lines on `00-run.md`  
- Round bumps, Status lifecycle, **Gate B settle gen** bumps  
- Profile drop (e.g. skip-review → lite on Has flip)  
- **Verify stamp fields:** `Last Verify`, `Last verify-pass at`, `Last verify settle-gen` — parent alone on stage `Result: verify-pass` ([verify.md](verify.md) · [preflight.md](preflight.md) Always §7); stages return Result only  

**Ownership rule:** parent alone writes the Notes / settle / provenance / profile-drop / card Has / verify stamp fields above. Stage **After** returns a signal only (`proposed Has: …`, `Has flip detected`, `candidate tiny-contract-tweak`, `candidate ideation-skip`, `candidate ideation-confirmed`, `candidate grill-skip`, `candidate 04a skipped`, `candidate design-stale`, `candidate design-backloop`, `candidate review-stale`, `candidate test-stale`, `candidate waiting — <reason>`, `candidate clear design-stale`, `candidate clear review-stale`, `candidate clear test-stale`, `candidate clear waiting`, …) — Tasks never write those Notes, card Has, or clear lifecycle Notes.

### Lifecycle clear predicates (parent-only)

| Notes | Clear only when |
|-------|-----------------|
| `design-stale` | Mode-full `design` + `03` rewrite Result `done` ([step-0.md](step-0.md) Upgrade). While set: Prefer **Grill open** → `grill` first, then unpaid among **Analyze unpaid** → **Grill unpaid** → **design unpaid under design-stale** ([derive-next.md](derive-next.md) · [derive-next-pre.md](derive-next-pre.md)) |
| `design-backloop` | Design clean ∧ **04a ok** ∧ **Gate B settled post-Notes** ([design-backloop.md](design-backloop.md) · [derive-next.md](derive-next.md)) |
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
| `ideation-confirmed` | `ideation-confirmed` | `user: "<exact words ≥12 chars>"` — parent stamp after shared understanding; Stages return `candidate ideation-confirmed` only ([brainstorm.md](brainstorm.md)) |
| `grill-skip` / `grill skipped — <reason>` | `grill-skip` | `user: "<exact words ≥12 chars>"` **or** evidence of user skip grill — Stages return `candidate grill-skip` only ([grill.md](grill.md)) |
| `04a skipped` / `04a skipped — <reason>` | `04a-skipped` | `user: "<exact words ≥12 chars>"` (named yes) — Stages return `candidate 04a skipped` only |
| `gate-b auto — gen:<N>` | *(token itself)* | Notes **or** Run-log line with **current** settle gen — no user quote |
| Build armed (async settle) | *(card field)* | `**Build armed:** yes` + Run-log arm for current settle gen after veto window — no user quote |

Do **not** invent quotes. Honesty residual: markdown shape ≠ cryptographic proof.

## Tiers

| Gate | Default |
|------|---------|
| Gate A | Soft (escalate Decision N) |
| Grill | Async-notify → stay running; settle frontier same turn — do **not** advance to Design while Grill open ([grill.md](grill.md)) |
| Gate B | Mode full = **blocking**; Mode simple = **auto** only when API=no ∧ DB=no ∧ auth/PII/schema=no (explicit `no`); else **blocking** (yes **or** unknown). Async-notify only when user asks for a veto window on the low-risk auto path ([gate-b.md](gate-b.md)) |
| Gate C | Always **blocking** |

## card-override

Allowed only for Next↔derive mismatch. **Cannot** waive Unsafe jumps — full non-waive set is SoT in [derive-next.md](derive-next.md) (do not restate here).
