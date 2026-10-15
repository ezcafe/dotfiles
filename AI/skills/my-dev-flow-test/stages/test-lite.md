## Lite test (Fast) — stage id `test-lite`

**When:** Review profile **lite** after review clean (or parent asks lite).

**subagent_type:** `generalPurpose`  
**model:** resolved Fast  
**Task description:** `Run build and tests`

**Done when:** targeted e2e (and unit if needed) green; Result success|failure in `06-test-log.md`.

**Task prompt:**

```
You run lite verification for my-dev-flow-test. Fresh context only.

<Paste output of: python {my-dev-flow}/scripts/handoff-for.py test-lite>
Read {my-dev-flow}/verify-and-fix.md for Verify commands rules.

Read 00-run.md **Verify commands** (required). Use those cwd/build/unit/e2e only — do not invent a different stack. N/A → skip with note.
Read 04-tasks.md for required e2e. Run the repo’s unit (if not already smoke-pass and unit not N/A) and only e2e that match this change / tasks (when e2e not N/A).
Do NOT run a coverage Task. Do NOT add broad missing e2e unless 04-tasks explicitly requires a new e2e file.
Write results into 06-test-log.md. Result: success | failure. On failure include Fix ask.
Do not fix product code. Do not merge, push, or open Gate C.

Return FIRST LINE exactly: Result: success | failure
Then short summary + path to 06-test-log.md ({my-dev-flow}/results.md).
```
