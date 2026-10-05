---
name: my-dev-flow-merge
description: >-
  After explicit user Gate C approval, commits (if approved), pushes the branch,
  opens a PR, then merges. Never commit or push without that yes. Use when the
  user says run my-dev-flow-merge, merge the workflow, or after my-dev-flow-test
  full succeeds.
---

# my-dev-flow-merge

Merge subflow of [`my-dev-flow`](../my-dev-flow/SKILL.md). Human owns top risks.

**Details:** [stages.md](stages.md) · PR body in [`../my-dev-flow/artifacts.md`](../my-dev-flow/artifacts.md)

## When to run

`run my-dev-flow-merge`, merge the workflow, or when `my-dev-flow` reaches merge
after **my-dev-flow-test** success.

## Principles

- Accountability, not rubber stamp. **Gate C** (legacy Gate 3) is **always blocking**.
- Prefer green full test (`06-test-log.md` Result **success**) before Gate C. Smoke-pass alone is not enough to merge.
- **Never** `git commit`, `git push`, `gh pr create`, or `gh pr merge` without an **explicit user yes** in this chat. Name each action in the Gate C ask.
- Never commit secrets; never force-push.
- Plain words in PR body.

## Models

| Tier | Stages | Preferred slug |
|------|--------|----------------|
| **Fast** | Merge | `composer-2.5-fast` |

### Model availability

Follow [`my-dev-flow/stages.md`](../my-dev-flow/stages.md) → **Models**.  
Fast → `inherit`. Record the resolved slug (and any fallback) in `00-run.md`. Do not stop to ask unless no Task can run.

## Prerequisites

- Prefer `06-test-log.md` Result **success** (full mode). If not success: **stop** and tell the user to run `my-dev-flow-test` full (or fix via `my-dev-flow-code`). Only continue without green tests if the user **explicitly overrides**.
- Prefer all `my-dev-flow-review` lenses clean (check `05-review-log.md`). If not clean: **warn** and only continue if the user explicitly overrides.
- **Gate C** — user confirms **commit** (if needed), **push**, **PR**, and **merge** (or a subset they name). No git/remote actions before this.

Reject Gate C → stop. Silence / “continue pipeline” / Gate B auto ≠ approval.

## Pipeline

```
GATE C (blocking user yes) → Commit (only if approved) → Push + PR + merge (Fast; only approved steps)
```

## Orchestrator rules

- Ask Gate C with a short risk summary from `05-review-log.md` / design, note full test Result from `06-test-log.md`, and list pending actions: commit? push? PR? merge?
- After yes: launch Merge Task ([stages.md](stages.md)) with Task **`description`** `Push PR and merge` (see [`my-dev-flow`](../my-dev-flow/SKILL.md) → Task description map) so the Cursor subagent card shows live status. Pass only the actions the user approved.
- If user says “PR only” / not merge yet: stop after `gh pr create`.
- If user says “commit only”: commit and stop (no push).
- Return PR URL and merge result (or stop reason).

## Start checklist

1. Confirm full test success (or explicit override); summarize top risks; ask Gate C (commit / push / PR / merge).
2. Resolve Fast model.
3. Run merge stage only for approved actions; check Gate C yes in `00-run.md`.
