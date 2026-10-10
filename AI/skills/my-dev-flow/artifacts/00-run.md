Copy into `.my-docs/workflow/<slug>/`. [handoffs.md](../handoffs.md) · [LEGACY.md](../LEGACY.md) · [verify-and-fix.md](../verify-and-fix.md).

# 00-run.md

```markdown
# Workflow run: <slug>

**Status:** ideation | gate-a | skim | analyze | grill | design | design-review | tdd-review | gate-b | build | smoke | review | test | gate-c | done | stopped

**Mode:** full | simple — set after complexity check (or override/resume); see my-dev-flow **Mode selection**

**Complexity:** simple | complex — one-line reason (e.g. `simple — clear bug fix` / `complex — new multi-surface feature`)

**Slug:** `YYYYMMDD-feature-x` (UTC date + short kebab feature; e.g. `20261005-offline-care-log`)

**Review profile:** full | lite | skip-review — set at Step 0 (see my-dev-flow **Review profile**)

**Lens plan:** none | api | db | security | perf | memory | api+db | api+security | … — **default `none`** at Step 0; add lenses only on clear signals before code review (see stages.md **Conditional lenses**). Include **api** when **Has API = yes**. Include **db** when **Has DB = yes**. (Legacy: **SPM plan** — see LEGACY.md.)

**Verify commands:** (set by skim/Analyze; required before Build — see verify-and-fix.md)
- **cwd:**
- **build:** `<command>` | N/A — <reason>
- **unit:** `<command>` | N/A — <reason>
- **e2e:** `<command>` | N/A — <reason>

**Last Verify:** pending | verify-pass | verify-fail
**Verify attempts:** 0 (reset per Build/Fix stage entry; max 3)

**Run metrics (optional — copy to Notes at end or increment during run):**

| Metric | Value |
|--------|-------|
| Task count | (increment each launched Task) |
| design-review rounds | |
| Gate B tier used | auto \| async-notify \| blocking |
| Grill HITL tier used | auto \| async-notify \| blocking |
| verify-fail count | |
| smoke↔fix rounds | |
| review Fix rounds | |
| usage-limit inherit retries | |
| main-thread fallbacks | |
| deferred Enhancements count | |
| phase bundles used | design-phase \| design-verify-phase \| code-review-phase \| test-full \| none |

**Last stage:** (e.g. `Gate A done`, `Build verify-pass`, `Gate B auto`) — resume from the next incomplete step; do not redo completed gates unless artifacts changed

## Resolved models

| Tier | Slug | Notes |
|------|------|-------|
| High | | Analyze, Design, Update |
| Medium | | Mode **full** judgment stages when available (incl. Grill) |
| Fast | | Build, Fix, Smoke, Test, Merge; Mode **simple** mechanical + lite review; mechanical when Medium unavailable |

**Resolve:** From the current Task model allowlist, pick the **first** slug that matches the tier (see stages.md **Models**). Soft preferred hints (not sole truth): High `claude-sonnet-5-5-high` or `claude-fable-5-1-thinking-high` · Medium `claude-opus-5-5-medium` · Fast `composer-2.5-fast`. If none match, use tier fallbacks below.

**Fallback:** High → Medium → Fast → `inherit` · Medium → Fast → `inherit` · Fast → `inherit`.

**Fast-on-simple:** Mode **simple** → mechanical + lite review prefer **Fast** even if Medium is listed. Mode **full** → Medium when available for mechanical; if Medium missing, mechanical **must use Fast** when available — do not jump to `inherit` while Fast works. On **usage limit**, see stages.md (retry → **inherit** → main thread). Note fallbacks in Notes.

**Simple phase bundles:** Mode simple uses stage ids `design-phase`, `design-verify-phase`, `code-review-phase` (see stages.md **Speed defaults**).

## Repo

- **Root:**
- **Branch:**
- **Started:**
- **Last stage:**
- **Has UI:** yes | no — set in Ideation (or simple bootstrap). UI specs go in Design (see LEGACY.md — no UI concept step).
- **Has API:** yes | no — set when contracts are clear; **must be yes|no before design-review** (if still unknown and Design has API contracts → yes). When yes: isolated API contract review + **api** lens.
- **Has DB:** yes | no — set when schema/migrations/persistence are clear; **must be yes|no before design-review** (if still unknown and Design has DB contracts → yes). When yes: isolated DB design review + **db** lens.
- **HITL Gate B:** auto | async-notify | blocking — see my-dev-flow **HITL tiers**
- **HITL Grill:** auto | async-notify | blocking — **independent of Gate B**. Default: Mode full → async-notify; Mode simple → auto. See grill.md.
- **HITL Gate C:** blocking — **always**. Never auto/async. No commit/push/PR/merge without explicit user yes.
- **04a:** run | skipped — reason (skipped when no planned test cases):
- **Smoke:** pending | smoke-pass (from Build) | smoke-pass (re-run) | smoke-fail | skipped-verify-bar (skip-review)

## Orchestrator card (parent — avoid re-ingest)

Update after each step. Parent reads **this card + one stages.md section** for the next Task. Do **not** re-read full subflow `SKILL.md` every step (load once per phase, or when Mode/profile changes).

After Build/Fix: read Task return **first line** for `Result: verify-pass | verify-fail` (see verify-and-fix.md).

| Field | Value |
|-------|-------|
| Phase | design \| code \| review \| test \| merge |
| Next step | (e.g. Step 4a TDD review) |
| Task description | (card title) |
| Stage id | (handoff table id) |
| stages.md section | path + heading only |
| Model tier | High \| Medium \| Fast (mechanical→Fast rule if Medium missing) |
| Prereq Result | (e.g. design-review clean, verify-pass) |
| Last Verify | pending \| verify-pass \| verify-fail |
| Verify attempts | 0–3 |
| Artifact to check | path — read first ~40 lines / Result only |
| Main-thread fallback | none \| `<stage>` (usage limit after wait 5s + retry + inherit retry) — only that stage; next stages still Task |

## Gates

Canonical names (legacy aliases in parentheses):

- [ ] Gate A — Day-to-day + 80/20 (auto when `01a` Result ok) *(legacy: Gate 1 + Gate 2-UI)*
- [ ] Gate B — Design + tasks (+ tests if planned) approved *(legacy: Gate 2)* — HITL tier: auto | async-notify | blocking; user-first when auto; skim **System design** + **Design patterns used** when blocking
- [ ] Gate C — Commit / push / PR / merge approved *(legacy: Gate 3)* — **always blocking**; ask for each action explicitly

## Notes

- Abort / scope-change: Status `stopped` + frozen stage + reason (see stages.md)
- async-notify veto after Build started: Decision N (discard draft / keep draft + re-open Gate B / stop) — see stages.md
-

## Run log

Newest at the bottom. Format: `- **HH:MM** · running|done|paused|stopped · Step … · note`

Example usage-limit lines:
`- **HH:MM** · done · Step 2 — Analyze · usage-limit retry — waited 5s`
`- **HH:MM** · done · Step 2 — Analyze · usage-limit retry — inherit model`
`- **HH:MM** · done · Step 2 — Analyze · main-thread fallback — usage limit after inherit`
`- **HH:MM** · done · Step 4 — Build · Result verify-pass · Smoke section written · Smoke Task skipped`
`- **HH:MM** · paused · Build verify-fail after 3 attempts — Decision N`

-
```
---
