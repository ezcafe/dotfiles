## Merge + push (Senior) — Fast — stage id `merge`

**Only after GATE C** (user explicitly approved the listed actions in chat). Parent may own the Gate C ask; this Task **executes** approved actions only.

**subagent_type:** `generalPurpose`  
**model:** resolved Fast  
**Task description:** `Execute Gate C actions`

**Done when:** Approved actions ran (or correctly skipped); PR URL / merge result returned (or stop reason). Parent sets Status **`done`** after merge success when merge was approved.

**Task prompt:**

```
You are the Senior Developer for my-dev-flow-merge Merge.

<Paste output of: python3 {my-dev-flow}/scripts/handoff-for.py merge>

All review lenses are clean (or user explicitly overrode after warning).

Hard rules:
- FIRST: re-read durable **Gate C approved:** on `00-run.md` **and** Notes/Run log provenance `gate-c-approved` with a quality user quote (verbatim, ≥12 chars, non-filler — [`hitl.md`](../../my-dev-flow/hitl.md) Provenance). If approved missing/`none`/empty **or** provenance missing/weak → stop immediately with Result: aborted (do not git/remote). Parent must ask Gate C and set both.
- Gate C test bar: honor [`hitl.md`](../../my-dev-flow/hitl.md) for this Review profile (parent should run `lint-run.py --before-merge` first). Notes `gate-c-test-override` / `smoke-waive` / `docs-only` / `smoke-pass (re-run)` may waive **only** with matching provenance kinds.
- Do NOT git commit, git push, gh pr create, or gh pr merge unless that action is listed in **Gate C approved**.
- Never commit secrets. Do not force-push. Do not skip hooks.
- **Refuse to commit** (stop / unstage / warn parent) when any path matches: `.env`, `.env.*`, `*.pem`, `credentials.json`, or `*secret*` (case-insensitive basename). Prefer abort over shipping secrets. PR body still includes “No secrets in diff” checklist.
- Honor subsets: if only “PR only” / “prepare PR”, stop after PR create. If only “commit only”, commit and stop (no push).

Approved actions = parse **Gate C approved** (commit | push | pr | merge subset). Parent may also pass the same list; the durable field wins if they disagree.

0. Read **Gate C approved** + provenance on `00-run.md`. Abort if none/empty/missing or provenance weak. Confirm Gate C test bar (or Notes override **with provenance**).
1. If commit approved and there are staged/unstaged changes worth committing: scan paths for secret patterns above; if any hit → Result: aborted (do not commit). Else create commits with clear messages. If commit was not approved, leave the working tree as-is and do not commit.
2. If push approved: push branch with -u if needed. Otherwise skip push.
3. If pr approved: create PR with gh pr create. Body must include:
   - Summary (1–3 bullets)
   - Risk checklist (top risks from 05-review-log.md / design)
   - Test plan (commands from 06-test-log.md Runs + Smoke + manual checks)
   Use the PR body template from {my-dev-flow}/artifacts/pr-body.md — do NOT use INDEX.md.
4. If merge approved: merge with gh pr merge. If only “prepare PR” / “PR only”, stop after PR create.

Return FIRST LINE exactly: Result: success | aborted
- **success** — approved actions completed (including “PR only” / “commit only” subsets that finished as approved).
- **aborted** — Gate C approved missing/none, soft stop, rejected mid-run, or an approved action failed.

Then: what ran, PR URL (if any), and merge/stop detail.
```

**After:** Parent: on Result **success** **and** `merge` ∈ **Gate C approved** → set Status **`done`** on `00-run.md` ([results.md](../../my-dev-flow/results.md)). Result **success** without `merge` in approved (commit / push / PR only) → stay **`paused`**; leave card Next for remaining Gate C actions — do **not** mark `done`. Result **aborted** → Status `stopped` or leave paused — never mark `done` without successful merge when merge was in scope. If user only approved “prepare PR” but not merge yet, stop after PR create (Result **success** for that subset). If user only approved commit, stop after commit (no push).
