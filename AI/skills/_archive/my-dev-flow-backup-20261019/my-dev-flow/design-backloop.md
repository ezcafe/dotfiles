# Design-backloop after Build

**SoT for:** design invalid after Build / Fix that cannot stay aligned with `03`/`04`.  
Decision shapes: [invariants.md](invariants.md). Stale tokens: [verify-and-fix.md](verify-and-fix.md). Gate B re-open: [hitl-gate-b.md](hitl-gate-b.md).

**When:** Fix/verify-fail cannot stay aligned with `03`/`04` without contract/IA change; review Major/Critical needs design change; parent/user says design wrong after Build.

**Do not:** silently amend `03`/`04` in Build/Fix; do not go to Gate C.

**Decision N** ([invariants.md](invariants.md)): Amend design / Fix-only / Stop. After **Option 1**:

1. Log Notes bullet `- design-backloop`; prior Gate B **invalid**.
2. Set **`Gate B approved: none`**; clear Notes **Build armed** and veto-window tokens.
3. If prior `05-review-log` / `06-test-log` Results exist: add Notes `- review-stale` and `- test-stale` (or clear those Results) so derive / `--before-merge` will not treat old clean/success as paid before Gate C ([verify-and-fix.md](verify-and-fix.md)).
4. Card Next = `design-update` (not `build`). Decision N Option 1 is the entry — design-update accepts Notes `design-backloop` without a prior `03a` Fix ask ([design-update.md](../my-dev-flow-design/stages/design-update.md)).
5. Resume design-update → design-review / design-verify-phase → **Gate B** (Next=`gate-b` while token still present) → Fix/Build.
6. After fresh Gate B settle, clear Notes `- design-backloop` by HITL tier (same parent turn as settle):
   - **blocking** — clear token + set **Gate B approved** `yes` / named pick **+** quality provenance `provenance — gate-b-approved — user: "…"` ([hitl.md](hitl.md) Provenance)
   - **auto** — clear token after digest settle; approved may stay `none`
   - **async-notify** — clear token + **Build armed** rules ([hitl-gate-b.md](hitl-gate-b.md))
   Then Build when armed. Lint still errors while token present (blocks Build for all tiers). Clear `review-stale` / `test-stale` only after fresh review clean / test success.

Lint: Notes `- design-backloop` → **error** on `--before-build` or Next=`build` until cleared (blocks Build even when Gate B is soft); default lint with Next in recovery (`design-update` / design-review / `design-verify-phase` / `gate-b` / …) → **warn** recovery in progress. `--next` redirects **`build`** only (not `gate-b`); Next=`gate-b` + token → normal Gate B digest / settle path. `--next --derive` mirrors this (token + `gate-b` / review clean → derive `gate-b`, not `design-update`).

Gate B veto after Build is separate ([hitl-gate-b.md](hitl-gate-b.md) re-open Gate B).
