## adversarial

**Stage id:** `adversarial`

**When:** Review profile **full**. Profile **lite** uses **code-review-phase** instead.

**Generation ≠ verification:** different pass from Build.

**subagent_type:** `generalPurpose`  
**model:** resolved Medium  
**Task description:** `Adversarial test review`

**Done when:** zero Critical/Major on test quality.

**Task prompt:**

```
You are a Senior Verifier for my-dev-flow-review Adversarial Test Review. You did NOT write this code. Do not rewrite features unless needed to describe a finding.

<Paste output of: python {my-dev-flow}/scripts/handoff-for.py adversarial>

Review tests and how they map to 04-tasks.md and the behavior in the draft.

Check:
- Tests that only assert mocks are mocks (“mock theater”)
- Missing edge cases and negative cases
- Non-deterministic or flaky patterns
- Missing failure-mode coverage for critical paths
- Prefer readable, deterministic tests tied to real failure modes

Append findings to 05-review-log.md under heading “Adversarial test review” with severity Critical / Major / Enhancement (and Nit/FYI if useful).
Under that same heading write **Result:** clean | needs fix (section Result is SoT for parent derive on Review profile full — do not rely on a file-top Result alone).

Section Result = **needs fix** if any Critical/Major open; **clean** if none ({my-dev-flow}/results.md · severity.md).
If not clean: list findings with file:line when possible. Do not fix them yourself.
Return FIRST LINE exactly: Result: clean | needs fix
Then finding table or clean status.
```

**If needs fix:** run **Fix** (lens = adversarial-tests) → re-run this lens until clean → then Quality.

---
