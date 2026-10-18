Copy into `.my-docs/workflow/<slug>/`. [handoffs.md](../handoffs.md) · [LEGACY.md](../LEGACY.md) · [verify-and-fix.md](../verify-and-fix.md) · [hitl.md](../hitl.md) · [invariants.md](../invariants.md) · [failure-playbook.md](../failure-playbook.md).

# 00-run.md

Fill **Required** at Step 0. Fill **Optional** when known.  
**Lint (required):** `scripts/lint-run.py <run-dir>` at Step 0; `--before-design-review` before design-review; `--before-build` before Build; `--before-code-review` before Adv / code-review-phase; `--before-merge` before merge when Next=`merge`.

**Enums (exact single token — no `|` templates in filled runs):**

| Field | Allowed |
|-------|---------|
| Status | `running` \| `paused` \| `stopped` \| `done` |
| Mode | `full` \| `simple` |
| Review profile | `full` \| `lite` \| `skip-review` |
| Gate B veto | `none` \| `pending` |
| Gate B approved | `none` \| `yes` \| named pick (e.g. `Option 2`) |
| Pending parallel | `none` \| `api` \| `db` \| `api\|db` |
| Has UI / API / DB | `yes` \| `no` |
| Last Verify | `pending` \| `verify-pass` \| `verify-fail` |
| Last verify-pass at | `none` \| ISO-8601 (set on verify-pass — [verify-and-fix.md](../verify-and-fix.md) Stale) |
| Gate C approved | `none` \| comma-separated subset of `commit`,`push`,`pr`,`merge` |

```markdown
# Workflow run: <slug>

## Required

**Status:** running
<!-- Exact one of: running | paused | stopped | done. Pipeline position = Orchestrator card Stage id / Last stage — not Status. -->

**Mode:** simple
<!-- Exact one of: full | simple — after complexity check (or override/resume); stages.md Mode selection -->

**Complexity:** one-line reason only (not a second classifier). e.g. `clear bug fix` / `new multi-surface feature`

**Slug:** `YYYYMMDD-feature-x` (UTC date + short kebab feature)

**Review profile:** lite
<!-- Exact one of: full | lite | skip-review. Profile full requires Mode full (simple+full forbidden). Never keep skip-review when Mode full or Has API/DB = yes (lenses.md · stages.md). -->

**Lens plan:** none
<!-- Default none. Add api|db|security|perf|memory only on signals — lenses.md -->

**Pending parallel:** none
<!-- Exact one of: none | api | db | api|db. When Has API=yes AND Has DB=yes AND Notes do NOT say tiny-contract-tweak: set api|db until both 03a-api-contract-review.md and 03a-db-design-review.md exist, then none. Mode simple / tiny-tweak / single flag → none. -->

**Verify commands:** (required before Build — verify-and-fix.md)
- **cwd:**
- **build:** `<command>` | N/A — <reason>
- **unit:** `<command>` | N/A — <reason>
- **e2e:** `<command>` | N/A — <reason>

**Last Verify:** pending
**Last verify-pass at:** none
<!-- ISO-8601 when Last Verify becomes verify-pass (Build After). Lint compares 05/06 mtimes for unpaid clean/success — verify-and-fix.md Stale. none until first verify-pass. -->
**Verify attempts:** 0
<!-- Reset per Build/Fix stage entry; max 3 -->

**Gate B veto:** none
<!-- Exact one of: none | pending — hitl.md. Must be none before Build. -->

**Gate B approved:** none
<!-- none until Gate B settles. HITL Gate B blocking → yes (or named pick) before Build. auto → may stay none. async-notify → Build armed + gap (not this field) — hitl.md. -->

**Gate C approved:** none
<!-- Required default none. At Gate C / before merge: none until user yes; then comma-separated subset of commit,push,pr,merge naming what the user approved (hitl.md). -->

**Last stage:** stage id + short note (e.g. `build verify-pass`, `gate-b async-notify`) — resume from next incomplete stage id

**Run metrics:** (Task count, verify-fail count, main-thread fallbacks **required** when present; rest optional — invariants.md)
- Task count:
- verify-fail count:
- main-thread fallbacks:
- design-review rounds:
- smoke↔fix / test↔fix rounds:
- Gate B HITL / Grill HITL:
- inherit retries:

## Optional / when known

### Resolved models

| Tier | Slug | Notes |
|------|------|-------|
| High | | Analyze, Design, Update |
| Medium | | Mode **full** judgment stages when available (incl. Grill) |
| Fast | | Build, Fix, Smoke, Test, Merge; Mode **simple** mechanical + lite review |

**Resolve:** From the current Task model allowlist — [models.md](../models.md) is SoT for soft hints. Do not hardcode slugs here.

**Fallback:** High → Medium → Fast → `inherit` · Medium → Fast → `inherit` · Fast → `inherit`.

**Fast-on-simple:** Mode **simple** → mechanical + lite review prefer **Fast**. Mode **full** → Medium when available for mechanical.

**Simple phase bundles:** `design-phase`, `design-verify-phase`, `code-review-phase` (stages.md Speed defaults).

### Repo

- **Root:**
- **Branch:**
- **Started:**
- **Has UI:** no
- **Has API:** no
- **Has DB:** no
<!-- Has API/DB must be exact yes|no before design-review (not unknown; not "yes | no" template). -->
- **HITL Gate B:** auto
- **HITL Grill:** auto
- **HITL Gate C:** blocking
<!-- Gate C always blocking. Gate B: Mode full → blocking (never auto/async-notify); Mode simple → auto|async-notify only when Has API/DB=no + no auth/PII/schema (hitl.md Default Gate B narrow async). HITL Grill independent of Gate B. Soft HITL = Grill + simple Gate B only. -->
- **04a:** skipped — reason:
- **Smoke:** pending
<!-- pending | smoke-pass (from Build) | smoke-pass (re-run) | smoke-fail | skipped-verify-bar (skip-review) -->

### Orchestrator card (parent — avoid re-ingest)

Update after each step. Parent reads **this card + one** stages/hitl/models/lenses/invariants section. Load subflow `SKILL.md` once per phase.

| Field | Value |
|-------|-------|
| Phase | design |
| Stage id | |
| Next step | |
| Task description | handoff-for.py <stage-id> output (required) |
| stages.md section | path + heading only (or hitl/models/lenses/invariants) |
| Model tier | Fast |
| Prereq Result | |
| Last Verify | pending |
| Verify attempts | 0 |
| Gate B veto | none |
| Artifact to check | |
| Design backloop | none |
| Main-thread fallback | none |

### Gates

- [ ] Gate A — Day-to-day + 80/20 (auto when `01a` Result ok)
- [ ] Gate B — Design + tasks (+ tests if planned) — HITL: Mode full → blocking; Mode simple → auto | async-notify | blocking per hitl.md
- [ ] Gate C — Commit / push / PR / merge — **always blocking** (record **Gate C approved** on yes)

### Notes

- Abort / scope-change: Status `stopped` + frozen stage + reason
- async-notify Gate B tokens: write live lines only when posting / arming — see hitl.md (do not paste example tokens into Notes at seed time)
- Gate C yes: set **Gate C approved:** commit,push,pr,merge (subset as named); optional Notes `Gate C yes — … (chat HH:MM)` — hitl.md
- Design backloop path: failure-playbook.md / invariants.md / stages.md
- tiny-contract-tweak — Notes fold into Quality / code-review-phase (optional)
- Status `done` only after Merge Result success **and** `merge` ∈ Gate C approved; subset without merge → stay paused; abort → `stopped`
- Calibration (required after `done`, ≤3 lines): Mode OK? · Review profile OK? · Biggest friction stage? — append same lines to `.my-docs/workflow/_calibration.md` (stages.md Done criteria)

### Run log

Newest at the bottom: `- **HH:MM** · running|done|paused|stopped · <stage-id> · note`

-
```
---
