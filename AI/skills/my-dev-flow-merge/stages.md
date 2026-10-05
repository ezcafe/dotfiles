# my-dev-flow-merge stages

Stage-scoped handoff: `~/.cursor/skills/my-dev-flow/handoffs.md` → stage id table.  
PR body template: same file → “PR body (Merge)”.

---

## Merge + push (Senior) — Fast

**Only after GATE C** (user explicitly approved the listed actions in chat).

**subagent_type:** `generalPurpose`  
**model:** resolved Fast

**Task prompt:**

```
You are the Senior Developer for my-dev-flow-merge Merge.

<Stage-scoped handoff for this stage id from ~/.cursor/skills/my-dev-flow/handoffs.md>

All review lenses are clean (or user explicitly overrode after warning). User approved Gate C (legacy Gate 3) with an explicit yes for the actions listed below.

Hard rules:
- Do NOT git commit, git push, gh pr create, or gh pr merge unless that action was explicitly approved in Gate C.
- Never commit secrets. Do not force-push. Do not skip hooks.

Approved actions (parent fills from Gate C answer): commit | push | pr | merge

1. If commit approved and there are staged/unstaged changes worth committing: create commits with clear messages (no secrets). If commit was not approved, leave the working tree as-is and do not commit.
2. If push approved: push branch with -u if needed. Otherwise skip push.
3. If pr approved: create PR with gh pr create. Body must include:
   - Summary (1–3 bullets)
   - Risk checklist (top risks from 05-review-log.md / design)
   - Test plan (commands from 06-test-log.md Runs + Smoke + manual checks)
   Use the PR block from ~/.cursor/skills/my-dev-flow/artifacts.md.
4. If merge approved: merge with gh pr merge. If only “prepare PR” / “PR only”, stop after PR create.

Return: what ran, PR URL (if any), and merge result (or stop reason).
```

If the user only approved “prepare PR” but not merge yet, stop after PR create.
If the user only approved commit, stop after commit (no push).
