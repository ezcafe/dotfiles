## quality

**Stage id:** `quality`

**When:** Review profile **full** (after Adversarial clean). Profile **lite** uses **code-review-phase** instead.

**Skills:** `{code-review-and-quality}/SKILL.md`  
Bugbot only if the user asked.

**subagent_type:** `generalPurpose`  
**model:** resolved Medium  
**Task description:** `Quality review`

**Done when:** zero Critical/Major for Quality.

**Task prompt:**

```
You are a Senior Verifier for my-dev-flow-review Quality Review. Generation ≠ verification — you did not write this draft.

<Paste output of: python {my-dev-flow}/scripts/handoff-for.py quality>

Read {code-review-and-quality}/SKILL.md and follow it.
Review uncommitted / branch changes against 01-idea, 03-design, and 04-tasks.
When Has UI: also compare draft UI to Design UI specs in 03-design / 04-tasks + Gate A #1/#2 — fail **Major** if shipped look drifts on **size**, **positions**, **texts**, or chrome.
When 03-design **System design** or **Design patterns used** is not N/A: check draft code honors their Best practices / anti-patterns and does not invent a conflicting shape (Architecture axis). Flag design↔code gaps as Major when clear.

Do NOT deep-review API contracts here when Lens plan includes **api** — that is the dedicated API lens. Tiny-tweak / no api in plan: fold light contract checks into Quality.
Do NOT deep-review schema/migrations/persistence queries here when Lens plan includes **db** — that is the dedicated DB lens. Tiny-tweak / no db in plan: fold light checks into Quality.

Label every finding Critical / Major / Enhancement (Nit/FYI ok).
Append to 05-review-log.md under “Quality”.
Result = **needs fix** if any Critical/Major open; **clean** if none ({my-dev-flow}/results.md · severity.md).
Do not fix.
Return FIRST LINE exactly: Result: clean | needs fix
Then finding table or clean status.
```

**If needs fix:** run **Fix** (lens = quality) → re-run Quality until clean → then Conditional lenses (per Lens plan).

---
