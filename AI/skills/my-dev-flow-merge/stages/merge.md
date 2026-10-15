## Merge + push (Senior) — Fast — stage id `merge`

**Only after GATE C** (user explicitly approved the listed actions in chat). Parent may own the Gate C ask; this Task **executes** approved actions only.

**subagent_type:** `generalPurpose`  
**model:** resolved Fast  
**Task description:** `Push PR and merge`

**Done when:** Approved actions ran (or correctly skipped); PR URL / merge result returned (or stop reason). Parent sets Status **`done`** after merge success when merge was approved.

**Task prompt:**

```
You are the Senior Developer for my-dev-flow-merge Merge.

<Stage-scoped handoff for stage id merge from {my-dev-flow}/handoffs.md>

All review lenses are clean (or user explicitly overrode after warning). User approved Gate C (legacy Gate 3) with an explicit yes for the actions listed below.

Hard rules:
- Do NOT git commit, git push, gh pr create, or gh pr merge unless that action was explicitly approved in Gate C.
- Never commit secrets. Do not force-push. Do not skip hooks.
- Honor subsets: if only “PR only” / “prepare PR”, stop after PR create. If only “commit only”, commit and stop (no push).

Approved actions (parent fills from Gate C answer): commit | push | pr | merge

1. If commit approved and there are staged/unstaged changes worth committing: create commits with clear messages (no secrets). If commit was not approved, leave the working tree as-is and do not commit.
2. If push approved: push branch with -u if needed. Otherwise skip push.
3. If pr approved: create PR with gh pr create. Body must include:
   - Summary (1–3 bullets)
   - Risk checklist (top risks from 05-review-log.md / design)
   - Test plan (commands from 06-test-log.md Runs + Smoke + manual checks)
   Use the PR body template from {my-dev-flow}/artifacts/pr-body.md — do NOT use INDEX.md.
4. If merge approved: merge with gh pr merge. If only “prepare PR” / “PR only”, stop after PR create.

Return FIRST LINE exactly: Result: success | aborted
- **success** — approved actions completed (including “PR only” / “commit only” subsets that finished as approved).
- **aborted** — Gate C missing, soft stop, rejected mid-run, or an approved action failed.

Then: what ran, PR URL (if any), and merge/stop detail.
```

**After:** Parent: on Result **success** and merge was approved → set Status **`done`** on `00-run.md` ([results.md](../../my-dev-flow/results.md)). Result **aborted** → Status `stopped` or leave paused — never mark `done` without successful merge when merge was in scope. If user only approved “prepare PR” but not merge yet, stop after PR create (Result **success** for that subset). If user only approved commit, stop after commit (no push).
