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
| Veto window open and **Build armed** ≠ `yes` (including `none`) | `Result: blocked — Build armed not yes` |
| Async-notify + Notes `async-gap-pending` but gap incomplete (no **Build armed: yes** / arm HH:MM not later than digest) | `Result: blocked — async gap incomplete` |
| Notes `design-backloop` | `Result: blocked — design-backloop` |
| Else veto `none` + settled | Continue |

## Verify gate

- **Pass:** listed build+unit (non-N/A) exit 0 → `Result: verify-pass`
- **Fail:** still red after attempt budget → `Result: verify-fail`
- **Budget:** max 3 attempts per stage entry
- Parent advances **only** on verify-pass

## Build-writes-Smoke

On verify-pass, Build writes `06-test-log.md` Smoke section (`smoke-pass`). Parent may skip Smoke Task except when Independent Smoke (E1) applies.

## Independent Smoke (E1)

**When:** Mode **full** + Review profile **full**. Build-writes-Smoke alone is **blocked** before Adv / Quality / lenses.

**Ordered path:**

1. Notes `smoke re-run` once (after Build verify-pass).
2. Launch independent Smoke Task (`smoke`).
3. On smoke-pass: Notes `smoke-pass (re-run)`; clear `smoke re-run`. Record provenance kind `smoke-pass-rerun` when needed for Gate C escape ([hitl.md](hitl.md) Notes↔provenance pairs).
4. Evidence required: Run log stage `smoke` and/or `06-test-log.md` Smoke section updated **after** `Last verify-pass at`.

Do **not** unlock Adv / Quality / lenses from Notes or Run-log DONE alone. On **smoke-fail**: Next `fix-tests` ([derive-next.md](derive-next.md)); re-smoke only after verify-pass — do **not** re-match “Smoke unpaid” while fail is unpaid. **E1 dual-forge** (invent Notes + evidence without a Smoke Task) is an anti-pattern ([examples/anti-patterns.md](examples/anti-patterns.md)).

## Skip-review + Smoke ordered recovery

Under legal **skip-review** ([lenses.md](lenses.md) · [gate-c.md](gate-c.md)):

1. **Prefer unpaid:** Notes `smoke re-run` once → independent Smoke Task.
2. **Prefer paid:** Notes `smoke-pass (re-run)` ↔ provenance `smoke-pass-rerun` ([hitl.md](hitl.md)) → **`gate-c`**. Do **not** else-drop to lite once that pair exists.
3. **Else (peer alternatives — either):**
   - drop skip-review → lite (`code-review-phase` → lenses per plan → `merge-findings` if 2+ → `test-lite`), **or**
   - Gate C escape + matching provenance (`docs-only`, `smoke-waive`, or `gate-c-test-override`).

On **smoke-fail** (or later test fail): Expected Next is **`fix-tests`** first ([derive-next.md](derive-next.md)) — do **not** re-match Prefer unpaid / drop-lite while fail is unpaid. Re-smoke only after Fix returns **verify-pass**.

Build-writes-Smoke alone is **not** enough for Gate C under skip-review. Do **not** launch `test-full` / `test-lite` while skip-review stays legal. **Skip-review dual-forge** (invent Notes + evidence without a Smoke Task) is a separate anti-pattern — do **not** call it E1 ([examples/anti-patterns.md](examples/anti-patterns.md)).

See also [stages.md](stages.md) Simple path (a).

## Fix

- Fix-from-tests: repair from `06` Fix ask only; verify-pass before re-test / re-smoke.
- Fix-from-review: repair from `05` Fix ask; verify-pass before re-review. After Last stage `fix-review` + Last Verify **verify-pass**, Expected Next is Prefer re-run **dirty** verifier by Fix Mode / profile ([derive-next.md](derive-next.md)) — lite Mode `code-review-phase` → `code-review-phase`; full Mode `adversarial-tests` \| `quality` → that section (both dirty/unclear → Adv then Quality); Mode `merged-lenses` or plan-1 lens Fix → mark planned `05-lens-*` + Merged unpaid → Prefer re-run dirty `lens-*` (or all planned) → `merge-findings` if 2+; already clean → continue table — not another `fix-review` while Prefer re-verify/re-lens is unpaid.
- Max 3 Fix rounds → Decision N ([decisions.md](decisions.md)).
- Design invalid → [design-backloop.md](design-backloop.md); never silently rewrite `03`/`04`.
- After smoke-fail → `fix-tests`: re-launch `smoke` only once Fix Result is **verify-pass** (never re-smoke on a red verify).

## Stale after rebuild

When Build rewrites a previously reviewed draft, mark Notes `review-stale` / `test-stale` and re-run review/test. Do not treat old clean Results as paid.
