# Anti-patterns

| Wrong | Right |
|-------|-------|
| Mode full + skip-review via Decision N | Forbidden — reclassify |
| Prefer merge from non-empty Gate C without `merge` ∈ set | Prefer gate-c or stay paused |
| Unlock Adv with Notes/Run-log alone (E1) | E1: require `Smoke source: Smoke-Task` **before** Adv |
| Treat skip-review Smoke as Adv unlock | skip-review: unpaid Smoke for Gate C / Prefer paid only — no Adv path |
| Fake user quote for smoke-pass-rerun | Evidence provenance after Smoke Task |
| Build while design-stale | Pre-Build first-match: Gate A → skim → Prefer **Grill open** → `grill` first, then Analyze unpaid → Grill unpaid → design unpaid under design-stale (**design-stale unpaid** — no design-update Run-log) |
| Prefer Isolated / design-review / design-verify / design-update while Notes `design-stale` | Unsafe-jump — Prefer **Grill open** → `grill` first, then unpaid among Analyze → Grill → design unpaid under design-stale until Mode-full `design` + `03` rewrite clears Notes |
| Prefer `design` under design-stale while **Grill open** (e.g. `02b` `pending`/`needs-round`) | Deadlock ban — Prefer `grill` until Notes `grill-skip` **or** Result `frontier-empty`; only then **design unpaid under design-stale** |
| Treat analyze/design paid under design-stale from file alone / prior `done` | Upgrade invalidates `03` → `pending`; **design unpaid under design-stale** Prefer rewrite only when ¬ Grill open until Notes clear ([../step-0.md](../step-0.md) · [../derive-next.md](../derive-next.md)) |
| Prefer design-review / Isolated / `design-verify-phase` while ¬ Design present (`03` missing or Result ≠ `done`) | Mode full Prefer `design`; Mode simple Prefer `design-phase` on cold start (Design present = file **and** Result `done`) |
| Step 0 copy all templates / treat `pending` stubs as Design present or Grill closed | Seed **only** `00-run.md`; `02b`/`03` `pending` alone stays unpaid/open; `04a` `pending` unpaid only when planned tests present (Notes `grill-skip` still closes Grill) |
| Treat Notes `grill-skip` as open while `02b` is `pending`/`needs-round` | Notes `grill-skip` closes Grill — Prefer must not match Grill-open rows |
| Task Result `skipped` as Grill waive / treat `skipped` as Grill closed | Grill closed = Notes `grill-skip` **or** Result `frontier-empty` only — invent-waive ban ([../grill.md](../grill.md)) |
| Mode simple Prefer Isolated Prefer stages after Has flip | Prefer `design-verify-phase` (writes Isolated when Has ∈ {yes, unknown} not tiny) |
| Gate B auto when Has auth/PII/schema=yes **or** API/DB/auth `unknown` (API=DB=no); treat Has UI `unknown` as blocking auto | Blocking only for API/DB/auth yes\|`unknown` — auto iff API=no ∧ DB=no ∧ auth/PII/schema=no (explicit `no`); **Has UI not in Gate B auto** (UI `unknown`\|yes fail-closes skip-review only — [../lenses.md](../lenses.md) · [../gate-b.md](../gate-b.md)) |
| Task writes Notes `ideation-skip` / `ideation-confirmed` / `grill-skip` / `04a skipped` / lifecycle stale/backloop / `waiting — <reason>` / card Has | Parent-only — stage returns `candidate …` / `proposed Has` only ([../hitl.md](../hitl.md)) |
| Prefer Gate A / skim / Analyze / design / `design-phase` while **ideation unpaid** | Prefer `ideation` first; stages FIRST `blocked — ideation unpaid` ([../brainstorm.md](../brainstorm.md) · [../derive-next.md](../derive-next.md)) |
| Treat bare chat skip / `(or skip)` / `01-idea` alone as ideation Done | Parent Notes `ideation-confirmed` + provenance **or** `ideation-skip` — Stages return candidates only ([../brainstorm.md](../brainstorm.md)) |
| Seed Has all-`no` to unlock Gate B auto / skip-review | Template defaults `unknown`; require explicit `yes`\|`no` first ([../artifacts/00-run.md](../artifacts/00-run.md) · [../step-0.md](../step-0.md)) |
| Prefer Isolated / design-review while `03a*` needs update or **backloop rewrite unpaid** | Prefer **Grill open** → `grill` first; else Prefer unpaid `design-update` first when **Grill closed**; pay Run-log + set **ALL** `03a*` → `pending` |
| Prefer `design-update` while **Grill open** (Notes `design-backloop` / `needs update`) | Unsafe-jump — Prefer `grill` until Notes `grill-skip` **or** Result `frontier-empty` ([../design-backloop.md](../design-backloop.md) · [../derive-next-pre.md](../derive-next-pre.md)) |
| Mode simple: Prefer `design-phase` / treat mid-open as only artifacts∨`needs-round`|`pending` (miss Result `skipped`) | Mid-open ≡ **Grill open** ∧ ¬ cold-start carve — Prefer `grill` for full open ([../grill.md](../grill.md)) |
| Clear Notes `design-backloop` → Prefer `build` on pre-Notes / uncleared Gate B settle (gen match alone) | Clear only with **Gate B settled post-Notes** (Run-log settle line **after** Notes `design-backloop`); else Prefer `gate-b` while Notes set ([../design-backloop.md](../design-backloop.md) · [../derive-next-pre.md](../derive-next-pre.md)) |
| Mode simple auto Prefer `build` same turn while Notes `design-backloop` still set | Write auto settle + post-Notes Run-log; Prefer `gate-b` until **Gate B settled post-Notes** then clear→`build` ([../gate-b.md](../gate-b.md)) |
| Mid-run Upgrade without card **Mode = full** (or keep skip-review) | Upgrade must write Mode=full + drop skip-review → lite\|full ([../step-0.md](../step-0.md) · F11) |
| Treat `06` Result `smoke-pass` / success alone as Prefer paid / Gate C escape | Need Notes↔provenance escape pair ([../verify.md](../verify.md) · [../gate-c.md](../gate-c.md)) |
| Drop Open 1–2 stage file to “fit” clarity-check | Clarity-check is **extra** — does not spend the Open 1–2 slot ([../parent-next.md](../parent-next.md)) |
| Mode full: Prefer `design` while **Grill unpaid** / Grill open (incl. `02b` `pending`) | Prefer `grill` first (before ¬ Design present → `design`) |
| Prefer re-smoke / re-test while smoke-fail unpaid (pre-fix) | Prefer `fix-tests` first; after fix-tests verify-pass Prefer smoke if Smoke unpaid/fail |
| Prefer merge-findings / test-* while lens `needs fix` | Prefer `fix-review`; merge-findings only when planned lenses clean |
| Keep pre-flip Gate B settle | Bump settle gen; Prefer gate-b after Design clean ∧ **04a ok** |
| Soft-re-run overall `03a` after API/DB (¬tiny) **or** UI **or** auth/PII/schema Has flip to **yes** without invalidate | Parent **must** set overall `03a` → `pending` same turn as Always §4; then Prefer re-verify — Mode full Prefer unpaid Isolated when required → `design-review`; Mode simple Prefer `design-verify-phase` ([../lenses.md](../lenses.md) Has flip §5) |
| Treat `unknown` → `no` resolve as Has flip (bump settle gen) | Resolve only — parent writes Has=`no`; **no** settle bump / no `has-flip` (flip is toward **yes** only) — [../lenses.md](../lenses.md) |
| Prefer gate-c/merge under lite/full while ¬Tests success | Prefer unpaid test-* / clear stale first |
| Prefer gate-c/merge / test-* while ¬ **Lenses clean** (Merged unpaid dual-false) | Prefer `merge-findings` (plan 2+ planned clean + Merged unpaid); Prefer `finalize-lens-plan` when missing required |
| Prefer gate-b while **04a unpaid / dirty** (planned tests present ∧ missing/`pending`/`needs more tests`) | Prefer `tdd-review` only while unpaid/dirty; Prefer `gate-b` when **04a ok** (incl. ¬ planned tests present) |
| Unilateral drop skip-review (Prefer-paid Else) | Named yes — Has flip mandatory drop is different |
| Design / design-review / design-update / gate-b / build while Grill open; `design-phase` while **Grill open** ∧ ¬carve | Settle grill; Next=`grill`. Cold start carve — [../grill.md](../grill.md) |
| Brainstorm only when Has UI | Hard-gate always; Prefer `ideation` while **ideation unpaid** (both Modes) before Gate A / `design-phase` |
| Prefer Adv / Prefer-re-smoke / unpaid Smoke while Lens plan=`none` and missing required api/db | Prefer `finalize-lens-plan` first — before Smoke **and** before Adv ([../verify.md](../verify.md) Prefer order vs finalize-lens-plan) |
| Status `paused` alone as waiting / invent Notes `waiting — <reason>` | Stay paused only when **paused-wait**; Notes `waiting` parent-only set+clear (Stages `candidate waiting — …` only); else Prefer continue ([../resume.md](../resume.md) · [../hitl.md](../hitl.md)) |
