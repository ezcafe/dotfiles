Copy into `.my-docs/workflow/<slug>/`. [handoffs.md](../handoffs.md) · [LEGACY.md](../LEGACY.md).

# 00-run.md

```markdown
# Workflow run: <slug>

**Status:** ideation | gate-a | skim | analyze | grill | design | design-review | tdd-review | gate-b | build | smoke | review | test | gate-c | done | stopped

**Mode:** full | simple — set after complexity check (or override/resume); see my-dev-flow **Mode selection**

**Complexity:** simple | complex — one-line reason (e.g. `simple — clear bug fix` / `complex — new multi-surface feature`)

**Slug:** `YYYYMMDD-feature-x` (UTC date + short kebab feature; e.g. `20261005-offline-care-log`)

**Review profile:** full | lite | skip-review — set at Step 0 (see my-dev-flow **Review profile**)

**Lens plan:** none | api | db | security | perf | memory | api+db | api+security | … — set before code review (see stages.md **Conditional lenses**). Include **api** when **Has API = yes**. Include **db** when **Has DB = yes**. (Legacy field name **SPM plan** — see LEGACY.md.)

**Run metrics (optional — copy to Notes at end or increment during run):**

| Metric | Value |
|--------|-------|
| design-review rounds | |
| Gate B tier used | auto \| async-notify \| blocking |
| usage-limit inherit retries | |
| main-thread fallbacks | |
| deferred Enhancements count | |

**Last stage:** (e.g. `Gate A done`, `skim done`, `Gate B auto`) — resume from the next incomplete step; do not redo completed gates unless artifacts changed

## Resolved models

| Tier | Slug | Notes |
|------|------|-------|
| High | | Analyze, Design, Update |
| Medium | | Creative/judgment Medium stages when available (incl. Grill) |
| Fast | | Build, Fix, Smoke, Test, Merge; **also mechanical Medium stages when Medium unavailable** |

**Preferred defaults (pick first present in Task allowlist):** High `claude-sonnet-5-5-high` · Medium `claude-opus-5-5-medium` · Fast `composer-2.5-fast`. Also try `claude-fable-5-1-thinking-high` for High when listed.

**Fallback:** High → Medium → Fast → `inherit` · Medium → Fast → `inherit` · Fast → `inherit`.

**Mechanical → Fast:** If preferred Medium is missing, mechanical stages (Gate A, skim, grill, design-review, API contract review, DB design review, TDD review, Adversarial, Quality, Lens/API/DB lenses, Merge findings) **must use Fast when Fast is available** — do not jump to `inherit` while Fast works. On **usage limit**, see stages.md (retry → **inherit** → main thread). Note fallbacks in Notes.

## Repo

- **Root:**
- **Branch:**
- **Started:**
- **Last stage:**
- **Has UI:** yes | no — set in Ideation (or simple bootstrap). UI specs go in Design (see LEGACY.md — no UI concept step).
- **Has API:** yes | no — set when contracts are clear; **must be yes|no before design-review** (if still unknown and Design has API contracts → yes). When yes: isolated API contract review + **api** lens.
- **Has DB:** yes | no — set when schema/migrations/persistence are clear; **must be yes|no before design-review** (if still unknown and Design has DB contracts → yes). When yes: isolated DB design review + **db** lens.
- **HITL Gate B:** auto | async-notify | blocking — see my-dev-flow **HITL tiers**
- **HITL Gate C:** blocking — **always**. Never auto/async. No commit/push/PR/merge without explicit user yes.
- **04a:** run | skipped — reason (skipped when no planned test cases):

## Orchestrator card (parent — avoid re-ingest)

Update after each step. Parent reads **this card + one stages.md section** for the next Task. Do **not** re-read full subflow `SKILL.md` every step (load once per phase, or when Mode/profile changes).

| Field | Value |
|-------|-------|
| Phase | design \| code \| review \| test \| merge |
| Next step | (e.g. Step 4a TDD review) |
| Task description | (card title) |
| Stage id | (handoff table id) |
| stages.md section | path + heading only |
| Model tier | High \| Medium \| Fast (mechanical→Fast rule if Medium missing) |
| Prereq Result | (e.g. design-review clean) |
| Artifact to check | path — read first ~40 lines / Result only |
| Main-thread fallback | none \| `<stage>` (usage limit after wait 5s + retry + inherit retry) — only that stage; next stages still Task |

## Gates

Canonical names (legacy aliases in parentheses):

- [ ] Gate A — Day-to-day + 80/20 (auto when `01a` Result ok) *(legacy: Gate 1 + Gate 2-UI)*
- [ ] Gate B — Design + tasks (+ tests if planned) approved *(legacy: Gate 2)* — HITL tier: auto | async-notify | blocking; user-first when auto; skim **System design** + **Design patterns used** when blocking
- [ ] Gate C — Commit / push / PR / merge approved *(legacy: Gate 3)* — **always blocking**; ask for each action explicitly

## Notes

- Abort / scope-change: Status `stopped` + frozen stage + reason (see stages.md)
-

## Run log

Newest at the bottom. Format: `- **HH:MM** · running|done|paused|stopped · Step … · note`

Example usage-limit lines:
`- **HH:MM** · done · Step 2 — Analyze · usage-limit retry — waited 5s`
`- **HH:MM** · done · Step 2 — Analyze · usage-limit retry — inherit model`
`- **HH:MM** · done · Step 2 — Analyze · main-thread fallback — usage limit after inherit`

-
```
---
