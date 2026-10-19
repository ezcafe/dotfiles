## code-review-phase

**Stage id:** `code-review-phase`

**When:** Review profile **lite** (any Mode, including Mode full). **Required** (not optional). Covers Adversarial + Quality in one Task. Review profile **full** uses `adversarial` then `quality` instead. Never launch separate Adv+Quality under lite.

**subagent_type:** `generalPurpose`  
**model:** Fast preferred (Fast-on-simple)  
**Task description:** `Lite combined review`

**Done when:** `05-review-log.md` Adversarial + Quality sections clean (zero Critical/Major), or Fix ask listed.

**Task prompt:**

```
You are the Senior Verifier for my-dev-flow-v2-review **Lite combined review** (code-review-phase). Fresh context only. Generation ≠ verification — you did not write this draft. Do not fix code in this Task.

<Paste output of: compose handoff from {my-dev-flow-v2}/handoffs.md for code-review-phase>

Read 00-run.md (Lens plan — default none), 01-idea, 03-design, 04-tasks, draft code/tests.
Read {code-review-and-quality}/SKILL.md for the Quality pass.

### Pass A — Adversarial tests
Check mock theater, missing edges/negatives, flaky patterns, missing failure-mode coverage vs 04-tasks. Append heading “Adversarial test review” to 05-review-log.md with **Result:** clean | needs fix under that heading.

### Pass B — Quality
Multi-axis quality vs idea/design/tasks. Has UI → fail Major on Design UI / Gate A #1/#2 drift. Defer deep API/DB contract issues to lenses when Lens plan includes api/db. Append heading “Quality” with **Result:** clean | needs fix under that heading.

### Lenses — parent owns (do not pay in-band)
Parent **always** launches isolated `lens-*` Tasks for every unpaid entry on Lens plan ([lenses-overview.md](lenses-overview.md) · `{my-dev-flow-v2}/lenses.md` · `{my-dev-flow-v2}/derive-next.md`). This Task must **not** write `05-lens-*.md` and must **not** mark any lens paid. You may note lens signals / deferrals in Adv or Quality prose only. **api/db:** When Lens plan includes api/db and Notes are **not** `tiny-contract-tweak`, do **not** deep-fold contracts here. Tiny-tweak: fold light contract checks into Quality (no forced api/db lens; still no `05-lens-*` write).

Clean only if zero Critical/Major in Adv + Quality ({my-dev-flow-v2}/severity.md). Else Fix ask ≤15 bullets Critical/Major only.
Keep / update file-top **Result:** clean | needs fix to match worst-of Adv+Quality section Results (lite convenience only — file-top alone never pays **Review clean**; file-top here does **not** include Merged; **overall Result** may also include Merged when Lens plan **2+** — [artifacts/05-review-log.md](../../my-dev-flow-v2/artifacts/05-review-log.md) · `{my-dev-flow-v2}/derive-next.md` Definitions). **Review clean** = Adv + Quality section Results both **`clean`**; missing or **`pending`** section Result = unpaid (**code-review unpaid**). **Round:** do **not** invent or bump — parent increments on re-entry (`{my-dev-flow-v2}/decisions.md`). max-round Decision N uses derived **overall Result** / worst-section (may include Merged).
Return FIRST LINE exactly: Result: clean | needs fix
Then path to 05-review-log.md.
```

**After:** SoT → [derive-next.md](../../my-dev-flow-v2/derive-next.md) · [parent-loop-hint.md](parent-loop-hint.md). clean → parent launches unpaid `lens-*` per Lens plan (never in-band; 2+ → parallel → `merge-findings`) → `test-lite`. needs fix → Next=`fix-review` (Fix Mode code-review-phase); then Prefer re-run this dirty stage.

---
