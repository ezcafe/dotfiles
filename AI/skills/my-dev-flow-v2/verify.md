# Verify + Fix + Smoke

**SoT for:** Verify gate, Build-writes-Smoke, Fix rules.

## Verify commands (`00-run.md`)

```markdown
**Verify commands:**
- **cwd:** <repo or package>
- **build:** `<command>` | N/A — <reason>
- **unit:** `<command>` | N/A — <reason>
- **e2e:** `<command>` | N/A — <reason>
```

Prefer project scripts. Do not invent a new test stack. Monorepo: set cwd to the touched package.

## Gate B check (Build first action)

Read durable fields on `00-run.md`: **Gate B veto**, **Gate B approved**, **Build armed** (`none`\|`yes` — [gate-b.md](gate-b.md)).

| Condition | Action |
|-----------|--------|
| `Gate B veto: pending` | `Result: blocked — Gate B veto` |
| Blocking + approved missing/weak provenance | `Result: blocked — Gate B approved` |
| Auto + missing design-scoped `gate-b auto — <HH:MM>` (or digest after current **Design clean** / **Verify clean**) | `Result: blocked — Gate B auto not settled` |
| Settle fails freshness (token earlier than Design-clean minute, or earlier than has-flip minute when a flip Note exists; **or** Design-clean time unresolved — [derive-next.md](derive-next.md) Settle freshness) | `Result: blocked — Gate B settle stale` |
| Veto window open and **Build armed** ≠ `yes` (including `none`) | `Result: blocked — Build armed not yes` |
| Async-notify + Notes `async-gap-pending` but gap incomplete (no **Build armed: yes** / arm HH:MM not later than digest) | `Result: blocked — async gap incomplete` |
| Notes `design-backloop` | `Result: blocked — design-backloop` |
| Notes `design-stale` | `Result: blocked — design-stale` |
| Else veto `none` + settled | Continue |

## Verify gate

- **Pass:** listed build+unit (non-N/A) exit 0 → `Result: verify-pass`
- **Fail:** still red after attempt budget → `Result: verify-fail`
- **Budget:** max 3 attempts per stage entry
- Parent advances **only** on verify-pass

## Build-writes-Smoke

On verify-pass, Build writes `06-test-log.md` Smoke section (`smoke-pass`) and sets **Smoke source: Build-verify** ([artifacts/06-test-log.md](artifacts/06-test-log.md)).

Parent may skip the post-Build Smoke Task when `06` already records matching **smoke-pass** from Build, **except**:

1. **E1** (Mode **full** × profile **full**) — always Prefer unpaid independent Smoke ([Independent Smoke](#independent-smoke-e1)); Build-writes-Smoke never waives E1 (**Smoke unpaid** until Smoke Task — [derive-next.md](derive-next.md)).
2. **skip-review unpaid** — When profile is **skip-review** and Smoke is unpaid/fail ([derive-next.md](derive-next.md) **Smoke unpaid**), Prefer unpaid independent Smoke first ([Skip-review + Smoke](#skip-review--smoke-ordered-recovery)); Build-writes-Smoke does **not** pay and does **not** waive Prefer unpaid. **If an escape pair exists but Smoke is still unpaid/fail:** Prefer unpaid Smoke anyway (do **not** softlock). Gate C under skip-review requires independent Smoke for **every** escape kind ([gate-c.md](gate-c.md)).

Lite paths (Mode **simple** / Mode **full** + profile **lite**) may skip when the Build Smoke section matches Verify commands and neither exception applies (Build-writes-Smoke may pay — [derive-next.md](derive-next.md) **Smoke unpaid**).

## Independent Smoke (SoT)

**Independent Smoke** = `Smoke source: Smoke-Task` (required); Notes `smoke-pass (re-run)` + evidence is the companion provenance for Prefer paid / Gate C escape pair, not an alternate unlock. Optionally ALSO Run log / `06` after **Last verify-pass at** (never Run-log alone). Do **not** pay Smoke unpaid, Prefer paid, Gate C independent Smoke, or Adv/Quality FIRST from Notes alone or Run-log alone. **Reject** `Smoke source: Build-verify` or `pending` even when Notes `smoke-pass (re-run)` + evidence exist. Copies point here — do not restate an (A)|(B) alternate unlock.

## Independent Smoke (E1)

**When:** Mode **full** + Review profile **full**. Build-writes-Smoke alone is **blocked** before Adv / Quality / lenses; Prefer unpaid independent Smoke always. Bar: [Independent Smoke (SoT)](#independent-smoke-sot).

**Ordered path:**

1. Parent sets Notes `smoke re-run` once (after Build verify-pass) before Prefer unpaid — Task must **not** write this token ([handoffs.md](handoffs.md)).
2. Launch independent Smoke Task (`smoke`).
3. On smoke-pass: Smoke Task sets **Smoke source: Smoke-Task** on `06` only. Parent writes Notes `smoke-pass (re-run)`, clears `smoke re-run`, and records provenance kind `smoke-pass-rerun` when needed for Gate C escape — evidence-backed form OK ([hitl.md](hitl.md) Notes↔provenance pairs). Task must **not** write Notes.
4. Evidence required: Run log stage `smoke` and/or `06-test-log.md` Smoke section updated **after** `Last verify-pass at`.

Do **not** unlock Adv / Quality / lenses from Notes alone (companion only — SoT). On **smoke-fail**: Next `fix-tests` ([derive-next.md](derive-next.md)); re-smoke only after verify-pass — do **not** re-match “Smoke unpaid” while fail is unpaid. **E1 dual-forge** (invent Notes + evidence without a Smoke Task) is an anti-pattern ([examples/anti-patterns.md](examples/anti-patterns.md)).

## Skip-review + Smoke ordered recovery

Under legal **skip-review** ([lenses.md](lenses.md) · [gate-c.md](gate-c.md)):

1. **Prefer unpaid:** Parent sets Notes `smoke re-run` once → independent Smoke Task when Smoke is unpaid/fail, Notes `test-stale`, **or** an escape Notes↔provenance pair exists but Smoke is still unpaid/fail (Prefer unpaid Smoke anyway — do **not** softlock on Prefer paid / Decision N). Build-writes-Smoke does **not** pay (**Smoke unpaid** until Smoke Task — [derive-next.md](derive-next.md)). Prefer unpaid Smoke first for **every** escape kind (including `docs-only` / `smoke-waive` / `gate-c-test-override`). **Stale:** `test-stale` → Prefer unpaid Smoke (not `test-full` / `test-lite`); clear `test-stale` when `Smoke source: Smoke-Task` is fresh after **Last verify-pass at**. `review-stale` is N/A under skip-review — clear; do not Prefer review ([Stale after rebuild](#stale-after-rebuild)).
2. **Prefer paid:** Build **verify-pass** + independent Smoke **smoke-pass** per [Independent Smoke (SoT)](#independent-smoke-sot) (`Smoke source: Smoke-Task` required; Notes `smoke-pass (re-run)` + evidence = companion for escape pair only) + **any one** escape Notes↔provenance pair from [hitl.md](hitl.md) (`smoke-pass (re-run)` ↔ `smoke-pass-rerun` — evidence-backed form OK, no fake user quote; or `docs-only` ↔ `docs-only`; or `smoke-waive` / `gate-c-test-override` with same-kind provenance) — **only when** unpaid stale Notes cleared (`review-stale` N/A cleared; `test-stale` cleared) (**Tests success** under skip-review — [derive-next.md](derive-next.md)). Destination: bar met **and** `merge` ∈ **Gate C approved** (+ provenance `gate-c-approved`) → Prefer **`merge`**; else → Prefer **`gate-c`** ([derive-next-post.md](derive-next-post.md)). Independent Smoke required for **every** escape kind. Do **not** else-drop to lite once that pair exists. Prefer-paid lands on the skip-review bar (independent smoke-pass + escape), **not** lite/full **success**. Escape alone with unpaid/fail Smoke does **not** Prefer paid. Notes alone does **not** Prefer paid. Stale Notes still set → Prefer unpaid Smoke (step 1), not Prefer paid.
3. **Else — Decision N** ([decisions.md](decisions.md) Skip-review else): Prefer stay skip-review + ask escape **or run Smoke** vs drop → lite. Do **not** drop profile or write escape Notes (`docs-only`, `smoke-waive`, `gate-c-test-override`) without named user yes. Escape alone is **not** enough ([gate-c.md](gate-c.md)).

On **smoke-fail** (or later test fail): Expected Next is **`fix-tests`** first ([derive-next.md](derive-next.md) · [derive-next-post.md](derive-next-post.md)) — do **not** re-match Prefer unpaid / Decision N drop while fail is unpaid. Re-smoke only after Fix returns **verify-pass**.

Build-writes-Smoke alone is **not** enough for Gate C under skip-review and does **not** waive Prefer unpaid. Do **not** launch `test-full` / `test-lite` while skip-review stays legal. **Skip-review dual-forge** (invent Notes + evidence without a Smoke Task) is a separate anti-pattern — do **not** call it E1 ([examples/anti-patterns.md](examples/anti-patterns.md)).

See also [stages.md](stages.md) Simple path (a).

## Fix

- Fix-from-tests: repair from `06` Fix ask only; verify-pass before re-test / re-smoke.
- Fix-from-review: repair from `05` Fix ask; verify-pass before re-review. After Last stage `fix-review` + Last Verify **verify-pass**, Expected Next is Prefer re-run **dirty** verifier by Fix Mode / profile ([derive-next.md](derive-next.md)) — lite Mode `code-review-phase` → `code-review-phase`; full Mode `adversarial-tests` \| `quality` → that section (both dirty/unclear → Adv then Quality); Mode `merged-lenses` \| `plan-1-lens` → mark planned `05-lens-*` + Merged unpaid → Prefer re-run dirty `lens-*` (or all planned) → `merge-findings` if 2+; already clean → continue table — not another `fix-review` while Prefer re-verify/re-lens is unpaid.
- Max 3 Fix rounds → Decision N ([decisions.md](decisions.md)).
- Design invalid → [design-backloop.md](design-backloop.md); never silently rewrite `03`/`04`.
- After smoke-fail → `fix-tests`: re-launch `smoke` only once Fix Result is **verify-pass** (never re-smoke on a red verify).

## Stale after rebuild

When Build rewrites a previously reviewed draft, mark Notes `review-stale` / `test-stale` and re-run review/test. Do not treat old clean Results as paid.

**Lite/full clear (SoT — operational):** Compare evidence timestamps to **Last verify-pass at** (ISO-8601 Run-log local wall time — [derive-next.md](derive-next.md) Freshness). Clear `review-stale` **only when** Run-log records Adv+Quality (profile **full**) or `code-review-phase` (profile **lite**) **after** that timestamp **and** **Review clean**. Clear `test-stale` **only when** `06` **Updated** (or Run-log `test-full` / `test-lite`) is **after** that timestamp **and** Result **success** + matching **Test path last run**. Prefer `merge` / `gate-c` only when stale Notes are cleared ([derive-next-post.md](derive-next-post.md) · [gate-c.md](gate-c.md)).

**Skip-review carve (approach a):** `review-stale` is N/A (no review path) — clear on Amend / do not Prefer review. `test-stale` → Prefer unpaid independent Smoke (not `test-full` / `test-lite`); clear `test-stale` when `Smoke source: Smoke-Task` is fresh after **Last verify-pass at**. Prefer paid (→ `merge` \| `gate-c`) only when stale Notes are cleared ([derive-next-post.md](derive-next-post.md) · [derive-next.md](derive-next.md) Unsafe).
