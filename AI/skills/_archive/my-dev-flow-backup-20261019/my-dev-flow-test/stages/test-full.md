## Full test suite — Fast — stage id `test-full` (one Task)

**When:** Review profile **full** after review clean. **One Task** covers coverage check + add missing e2e + run suite. Do **not** launch separate coverage / add-e2e / run Tasks on new runs (legacy names accepted on resume — see `{my-dev-flow}/LEGACY.md`).

**subagent_type:** `generalPurpose`  
**model:** resolved Fast  
**Task description:** `Full test suite`

**Done when:** `06-test-log.md` has Coverage + Runs filled; Result **success** | **failure** and **Test path last run:** `full` (LEGACY alias **Mode last run** on resume only).

**Task prompt:**

```
You run **full** verification for my-dev-flow-test in **one** Task (coverage + gaps + suite). Fresh context only. Do not fix product behavior here (except adding e2e for MISSING flows). Do not merge or push.

<Paste output of: python3 {my-dev-flow}/scripts/handoff-for.py test-full>
Read {my-dev-flow}/verify-and-fix.md for Verify commands rules.

### 1 — Coverage
Read 03-design.md (success criteria, flows) and 04-tasks.md. Scan existing e2e + how to run them.
Map each main flow → covered (file + test name) or MISSING. Note stack or “no e2e stack”.
Write 06-test-log.md Coverage section. Test path last run: full.

### 2 — Add missing e2e
If MISSING items exist **and** an e2e stack exists: add tests only for those flows using repo patterns. Do not change product behavior. If a gap cannot be automated safely, mark blocked with why.
If no e2e stack: skip add; note in Coverage; parent may mark failure if e2e was required.

### 3 — Run suite
Read 00-run.md **Verify commands**. Use those cwd/build/unit/e2e only (N/A → skip with note). Do not invent a different stack.
Run in order: build → unit → e2e (when not N/A).
Capture exit codes + short failure excerpts.
Result = **success** only if all non-N/A Verify steps are green AND no open required MISSING/blocked gaps.
Else Result = **failure** + Fix ask for my-dev-flow-code.
Update 06-test-log.md Runs + Result.

Return FIRST LINE exactly: Result: success | failure
Then short summary + path to 06-test-log.md ({my-dev-flow}/results.md).
```

**After:** success → parent Gate C (not this skill). failure → Fix-from-tests (verify-pass) → re-run `test-full`. Max 3 test↔fix rounds → Decision N (`{my-dev-flow}/invariants.md`).
