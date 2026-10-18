---
name: my-dev-flow-merge
description: >-
  After explicit user Gate C approval, commits (if approved), pushes the branch,
  opens a PR, then merges. Never commit or push without that yes. Use when the
  user says run my-dev-flow-merge, merge the workflow, or after the Gate C test
  bar for this Review profile is met (hitl.md).
---

# my-dev-flow-merge

Merge subflow of [`my-dev-flow`](../my-dev-flow/SKILL.md). Human owns top risks.

**Owns:** `merge` — [stages.md](stages.md) index; load **`stages/merge.md` only** via parent-next / handoff.  
**Gate C ask** may be the **parent**; this skill’s Merge Task **executes** only the approved actions.

**Shared SoT (do not restate Happy path):**

| Concern | File |
|---------|------|
| Pipeline order / Status `done` | [`../my-dev-flow/stages.md`](../my-dev-flow/stages.md) |
| Gate C (always blocking) + test bar + **Gate C approved** | [`../my-dev-flow/hitl.md`](../my-dev-flow/hitl.md) |
| Stage handoffs | **Required** `scripts/handoff-for.py <stage-id>` · [`handoffs.md`](../my-dev-flow/handoffs.md) = edit SoT / debug only |
| Models (Merge = Fast) | [`../my-dev-flow/models.md`](../my-dev-flow/models.md) |
| Parent checklist | [`../my-dev-flow/invariants.md`](../my-dev-flow/invariants.md) |
| PR body template | [`../my-dev-flow/artifacts/pr-body.md`](../my-dev-flow/artifacts/pr-body.md) |
| Result first-line tokens | [`../my-dev-flow/results.md`](../my-dev-flow/results.md) (`success` \| `aborted`) |

## When to run

`run my-dev-flow-merge`, merge the workflow, or when parent reaches merge after the **Gate C test bar** for this Review profile ([`hitl.md`](../my-dev-flow/hitl.md)).

## Principles

- Accountability, not rubber stamp. **Gate C** is **always blocking**.
- **Name each action** in the Gate C ask: commit / push / PR / merge. Never run those without an **explicit user yes** naming them in this chat.
- After yes: set durable **`Gate C approved:`** on `00-run.md` to the named subset (`commit,push,pr,merge`) — [`hitl.md`](../my-dev-flow/hitl.md). Prefer Notes `Gate C yes — …`. Lint: `lint-run.py --before-merge`.
- Honor **Gate C test bar** in [`hitl.md`](../my-dev-flow/hitl.md) by Review profile. skip-review legality: [`lenses.md`](../my-dev-flow/lenses.md).
- PR body from [`artifacts/pr-body.md`](../my-dev-flow/artifacts/pr-body.md) — **not** INDEX.md.
- Never commit secrets; never force-push; do not skip hooks.
- Honor subsets: “PR only” → stop after `gh pr create`; “commit only” → commit and stop (no push).
- Merge Task returns first line `Result: success | aborted` ([results.md](../my-dev-flow/results.md)). Parent sets Status **`done`** only when Result **success** **and** `merge` ∈ **Gate C approved**. Subset without merge → stay `paused`. **aborted** / reject → `stopped`, not `done`.
- Load one `stages/merge.md` per Task; plain words in PR body.

## Models

[`models.md`](../my-dev-flow/models.md) — Merge = Fast.

## Prerequisites

- Check `06-test-log.md` / Build result against Gate C test bar for this Review profile. If below bar: **stop** and run the missing test mode or fix via `my-dev-flow-code`. Only continue if the user **explicitly overrides** (log in Notes).
- Prefer all review lenses clean (`05-review-log.md`). If not clean: **warn** and only continue if the user explicitly overrides.
- **Gate C yes** for the listed actions — durable **`Gate C approved`** on `00-run.md` (not `none`) **with** matching provenance (`provenance — gate-c-approved — user: "…"` — [`hitl.md`](../my-dev-flow/hitl.md) Provenance). Silence / “continue pipeline” / Gate B auto ≠ approval.

Reject Gate C → stop.

## Pipeline

```
GATE C (blocking user yes — parent may ask) → Merge Task (only approved: commit | push | PR | merge)
→ parent sets Status done on success
```

## Orchestrator rules

- If Gate C not yet asked: ask with short risk summary (`05-review-log` / design), note test Result vs Gate C bar, list pending actions: commit? push? PR? merge?
- After yes: write **`Gate C approved:`** subset on `00-run.md`; launch Merge Task ([`stages/merge.md`](stages/merge.md)) with **`description`** `Push PR and merge`. Pass only approved actions.
- If user says “PR only” / not merge yet: stop after `gh pr create`.
- If user says “commit only”: commit and stop (no push).
- Expect first line `Result: success | aborted`; then PR URL / detail. Parent marks Status `done` only after Result **success** and `merge` ∈ Gate C approved.

## Start checklist

1. Confirm Gate C test bar ([`hitl.md`](../my-dev-flow/hitl.md)) — or explicit override; summarize top risks; ensure **Gate C approved** set (ask if needed); prefer `lint-run.py --before-merge`.
2. Resolve Fast model.
3. Run merge stage only for actions in **Gate C approved**; re-check field + chat.
