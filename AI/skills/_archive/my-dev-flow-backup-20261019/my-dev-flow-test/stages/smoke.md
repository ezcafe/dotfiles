## Smoke — build + unit only — Fast

**Stage id:** `smoke`

**When:** Smoke **re-run** when Build did not leave smoke-pass, commands mismatch Verify commands, Notes `smoke re-run`, **or** Mode **full** + Review profile **full** (E1 — independent Smoke required before Adv; Build-writes-Smoke alone blocked — `{my-dev-flow}/verify-and-fix.md`). Mode **simple** / Mode **full** + profile **lite**: after Build verify-pass with matching Smoke section, **parent may skip** this Task (Build-writes-Smoke). Under **skip-review**: do **not** launch `test-full` / `test-lite`; allow this Task **only** with Notes `smoke re-run` (ordered recovery: prefer Notes `smoke re-run` once before re-Build / drop → lite / waivers — [verify-and-fix.md](../../my-dev-flow/verify-and-fix.md) Skip-review + Smoke ordered recovery); else Gate C when escape + provenance met ([hitl-gate-c.md](../../my-dev-flow/hitl-gate-c.md) · [hitl.md](../../my-dev-flow/hitl.md)) or drop skip-review → lite.

**subagent_type:** `generalPurpose`  
**model:** resolved Fast  
**Task description:** `Smoke build and unit`

**Done when:** Smoke section filled; Result **smoke-pass** or **smoke-fail**.

**Task prompt:**

```
You are the runner for my-dev-flow-test Smoke (build + unit only). Fresh context only. Do not run e2e. Do not start code review here.

<Paste output of: python3 {my-dev-flow}/scripts/handoff-for.py smoke>

Read 00-run.md **Verify commands** (required). Use those commands and cwd only — do not invent a different stack. N/A unit → run build only (see verify-and-fix.md).

Run in order:
1. Build (if not N/A)
2. Unit tests (if not N/A)

Rules:
- Update 06-test-log.md → Smoke section + Test path last run: smoke (LEGACY alias Mode last run on resume only).
- Result = smoke-pass only if all non-N/A Verify build/unit steps are green.
- Otherwise Result = smoke-fail and fill Fix ask for my-dev-flow-code.
- Do not fix product code. Do not merge or push.
- Simple plain words.

Return FIRST LINE exactly: Result: smoke-pass | smoke-fail
Then short summary + path to 06-test-log.md ({my-dev-flow}/results.md).
```

**After:** Parent: on smoke-pass, when Mode **full** + profile **full**, write Notes `smoke-pass (re-run)` (and clear Notes `smoke re-run`) — Run log already has stage `smoke` / 06 updated after Last verify-pass at ([verify-and-fix.md](../../my-dev-flow/verify-and-fix.md) E1). Because consent fingerprint includes Notes `smoke-pass (re-run)` as waiver kind `smoke-pass-rerun`, also append Run log `parent consent write` ack (e.g. `parent consent write — smoke-pass-rerun`) then re-snapshot / pass `--check-consent-writes` ([hitl.md](../../my-dev-flow/hitl.md) · [parent-next.md](../../my-dev-flow/parent-next.md)). Then → `my-dev-flow-review`. Under legal skip-review: record `smoke-pass (re-run)` **plus** provenance `smoke-pass-rerun` **plus** the same `parent consent write` ack before Gate C escape ([hitl-gate-c.md](../../my-dev-flow/hitl-gate-c.md) · [hitl.md](../../my-dev-flow/hitl.md)). Else (Mode simple / profile lite Build-writes-Smoke skip path) → review or Gate C if escape + provenance. smoke-fail → Fix-from-tests (`--derive` → `fix-tests`) → verify-pass → re-smoke. Do not open Gate C/merge from this skill.
