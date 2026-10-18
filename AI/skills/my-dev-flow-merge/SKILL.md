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
| Gate C (always blocking) + test bar + **Gate C approved** + Provenance | [`../my-dev-flow/hitl.md`](../my-dev-flow/hitl.md) |
| Stage handoffs | **Required** `python3 {my-dev-flow}/scripts/handoff-for.py <stage-id>` ([`skills-path.md`](../my-dev-flow/skills-path.md)) · [`handoffs.md`](../my-dev-flow/handoffs.md) = edit SoT / debug only |
| Models (Merge = Fast) | [`../my-dev-flow/models.md`](../my-dev-flow/models.md) |
| Launch-time checklist | [`../my-dev-flow/orchestrator-rules.md`](../my-dev-flow/orchestrator-rules.md) |
| Decision shapes / detailed checklist body | [`../my-dev-flow/invariants.md`](../my-dev-flow/invariants.md) |
| PR body template | [`../my-dev-flow/artifacts/pr-body.md`](../my-dev-flow/artifacts/pr-body.md) |
| Result first-line tokens | [`../my-dev-flow/results.md`](../my-dev-flow/results.md) (`success` \| `aborted`) |
| Merge Task hard rules (execution SoT) | [`stages/merge.md`](stages/merge.md) |

## When to run

`run my-dev-flow-merge`, merge the workflow, or when parent reaches merge after the **Gate C test bar** for this Review profile ([`hitl.md`](../my-dev-flow/hitl.md)).

## Principles

- Accountability, not rubber stamp. **Gate C** is **always blocking**.
- **Name each action** in the Gate C ask: commit / push / PR / merge. Never run those without an **explicit user yes** naming them in this chat.
- After yes: set durable **`Gate C approved:`** on `00-run.md` to the named subset (`commit,push,pr,merge`) **and** Notes `provenance — gate-c-approved — user: "…"` — [`hitl.md`](../my-dev-flow/hitl.md) Provenance. Prefer Notes `Gate C yes — …`. Then run `lint-run.py --before-merge`.
- Honor **Gate C test bar** in [`hitl.md`](../my-dev-flow/hitl.md) by Review profile. Waivers (`gate-c-test-override` / `smoke-waive` / `docs-only` / `smoke-pass (re-run)`) require matching Notes kind **plus** `provenance — <kind> — user: "…"`. skip-review legality: [`lenses.md`](../my-dev-flow/lenses.md).
- PR body from [`artifacts/pr-body.md`](../my-dev-flow/artifacts/pr-body.md) — **not** INDEX.md.
- Never commit secrets; never force-push; do not skip hooks.
- Honor subsets: “PR only” → stop after `gh pr create`; “commit only” → commit and stop (no push).
- Merge Task returns first line `Result: success | aborted` ([results.md](../my-dev-flow/results.md)). Parent sets Status **`done`** only when Result **success** **and** `merge` ∈ **Gate C approved**. Subset without merge → stay `paused`. **aborted** / reject → `stopped`, not `done`.
- Load one `stages/merge.md` per Task; plain words in PR body. **Execution hard rules** live only in that file — do not restate here.

## Models

[`models.md`](../my-dev-flow/models.md) — Merge = Fast.

## Prerequisites

- Check `06-test-log.md` / Build result against Gate C test bar for this Review profile ([`hitl.md`](../my-dev-flow/hitl.md)). If below bar: **stop** and run the missing test mode or fix via `my-dev-flow-code`. Override only with Notes kind (`gate-c-test-override` / `smoke-waive` / `docs-only` / `smoke-pass (re-run)`) **plus** `provenance — <kind> — user: "…"` ([`hitl.md`](../my-dev-flow/hitl.md) Provenance).
- Prefer all review lenses clean (`05-review-log.md`). If not clean: **warn** and only continue if the user explicitly overrides **with** matching provenance kind.
- **Gate C yes** for the listed actions — durable **`Gate C approved`** on `00-run.md` (not `none`) **with** `provenance — gate-c-approved — user: "…"` ([`hitl.md`](../my-dev-flow/hitl.md) Provenance). Silence / “continue pipeline” / Gate B auto ≠ approval.
- **Required before launch:** `scripts/lint-run.py <run-dir> --before-merge` (enforces approved-actions + provenance + Gate C test bar).

Reject Gate C → stop.

## Pipeline

```
GATE C (blocking user yes — parent may ask) → Merge Task (only approved: commit | push | PR | merge)
→ parent sets Status done on success
```

## Orchestrator rules

- If Gate C not yet asked: ask with short risk summary (`05-review-log` / design), note test Result vs Gate C bar, list pending actions: commit? push? PR? merge?
- After yes: write **`Gate C approved:`** subset + provenance `gate-c-approved` on `00-run.md`; run `lint-run.py --before-merge`; launch Merge Task ([`stages/merge.md`](stages/merge.md) — **execution hard rules**) with **`description`** `Execute Gate C actions`. Pass only approved actions.
- If user says “PR only” / not merge yet: stop after `gh pr create`.
- If user says “commit only”: commit and stop (no push).
- Expect first line `Result: success | aborted`; then PR URL / detail. Parent marks Status `done` only after Result **success** and `merge` ∈ Gate C approved.

## Start checklist

1. Confirm Gate C test bar ([`hitl.md`](../my-dev-flow/hitl.md)) — or Notes waiver kind **+** matching `provenance — <kind> — user: "…"`; summarize top risks; ensure **Gate C approved** + provenance `gate-c-approved` set (ask if needed).
2. Open code [clarity-check.md](../my-dev-flow-code/stages/clarity-check.md) **Merge** section; log `clarity-check ok — merge` before launch ([parent-next.md](../my-dev-flow/parent-next.md)).
3. Run `lint-run.py --before-merge` (required; fail-closed on missing provenance / bar).
4. Resolve Fast model.
5. Run merge stage only for actions in **Gate C approved**; re-check field + provenance + chat. Hard rules: [`stages/merge.md`](stages/merge.md).
