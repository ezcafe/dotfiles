# Preflight (agent checklist — replaces Python lint)

Run **before every Task**. Soft enforcement: stop and fix `00-run.md` / ask user when a check fails. Do **not** invent approvals to pass.

## Always

1. Card **Mode** / **Review profile** / **Status** match `00-run.md` body.
2. **Status** ∈ `running|paused|stopped|done` (not a stage id).
3. Mode × profile legal ([stages.md](stages.md) Forbidden).
4. Card **Next** matches [derive-next.md](derive-next.md) expected next — else fix card or Notes `card-override — <reason>` + provenance `card-override` (**mismatch carve only** — never waives unpaid lite/full test bar / illegal Mode×profile).
5. Compose handoff from [handoffs.md](handoffs.md) for `<stage-id>`; load only `stages/<id>.md`.
6. Soft-cap Open paths ≤2 ([parent-next.md](parent-next.md)).
7. After Task: read Result first line ([results.md](results.md)); update card; bump Round / Run metrics ([decisions.md](decisions.md)). Parent-only consent fields unchanged by Task.

## Clarity boundaries

When Next ∈ `design-phase|analyze|grill|design|tdd-review|build|fix-review|fix-tests|merge`:

1. Open the matching clarity-check file (design or code subflow).
2. On pass, parent Notes: `clarity-check ok — <exact Next>`.
3. Fail → ask user; do not launch.

## Before design-review / design-verify / api|db-review

- Has API / Has DB / Has auth/PII/schema each `yes|no`.
- skip-review forbidden if Has API or Has DB or Has auth/PII/schema = yes ([lenses.md](lenses.md)).
- Mode full + both API+DB yes (not tiny): Pending parallel `api|db` until both `03a-*` exist.

## Before Build

- Design-review or design-verify Result **clean**.
- `Gate B veto: none`.
- **Fail-closed tier:** if Has API or Has DB or Has auth/PII/schema = **yes**, HITL Gate B **MUST** be `blocking` (not `auto` / `async-notify`); else do-not-launch ([gate-b.md](gate-b.md)).
- Blocking Gate B → **Gate B approved** set + provenance `gate-b-approved` ([gate-b.md](gate-b.md)).
- Async-notify → durable **`Build armed: yes`** + Run log arm HH:MM later than digest + Notes `async-gap-pending — <digest-HH:MM>` (veto window open and **Build armed** ≠ `yes` → do-not-launch).
- No Notes `design-backloop`.
- Verify commands set ([verify.md](verify.md)).

## Before Adv / code-review-phase

- Lens plan includes api/db when Has API/DB yes (unless tiny-tweak).
- Mode full + profile full → independent Smoke done (Notes `smoke-pass (re-run)` + Smoke evidence; provenance `smoke-pass-rerun` when Gate C escape needs it — [hitl.md](hitl.md)).

## Before test-* / gate-c

- Lens plan **2+**: Merged lenses Result must be **`clean`**. Unpaid/pending → do-not-launch; Expected Next `merge-findings`. **`needs fix`** → do-not-launch; Expected Next `fix-review` (or Prefer re-lens after Fix verify-pass — [derive-next.md](derive-next.md)).
- Lens plan **1**: that planned `05-lens-*` (or Merged if parent copied) Result must be **`clean`**. Unpaid/pending → do-not-launch; Prefer that `lens-*`. **`needs fix`** → do-not-launch; Expected Next `fix-review` (or Prefer re-lens after Fix verify-pass).
- Plan `none`: no lens gate.

## Before Merge

- **Gate C approved** non-empty subset of `commit,push,pr,merge` + provenance `gate-c-approved`.
- Gate C test bar met ([gate-c.md](gate-c.md)):
  - Profile **lite** / **full** → `06` Result **success** + Test path last run matching profile. Notes waiver / escape kinds are **invalid** here.
  - Profile **skip-review** only → escape kinds (`smoke-pass-rerun` / `docs-only` / `smoke-waive` / `gate-c-test-override`) with matching Notes↔provenance ([hitl.md](hitl.md)).
- No unpaid review/test stale Notes.

## Consent habit (parent-only)

Before Task: note current Gate B/C approved, **Build armed** (`none`\|`yes`), and waiver Notes.

After Task: confirm Task did **not** change those fields. Only parent writes them after explicit user yes — [hitl.md](hitl.md). After Build **verify-pass**, parent clears **Build armed** to `none` ([gate-b.md](gate-b.md) step 5); Task must not.
