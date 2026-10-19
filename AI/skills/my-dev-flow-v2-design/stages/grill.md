## grill — Grill + domain modeling (Medium)

**When:** After Analyze. Mode **full** — always (unless `02b` already `frontier-empty` and artifacts unchanged). Mode **simple** — when Analyze Design tree has open frontier / unsettled Decisions, or Has API/DB; else skip. (Mode simple inside **design-phase** uses the same grill rules.)

**Rules:** `{my-dev-flow-v2}/grill.md` + `documentation-and-adrs`.

**subagent_type:** `generalPurpose`  
**model:** resolved Medium  
**Task description:** `Grill design tree`

**Done when:** `02b-grill.md` Result **frontier-empty** or **skipped**; glossary/ADR updated when terms/decisions qualify.

**HITL:** Honor **HITL Grill** in `00-run.md` (independent of Gate B). Default tier by Mode: `{my-dev-flow-v2}/grill.md` (HITL Grill default). **auto** / **async-notify** → apply user-first recommendations and settle the frontier in this Task (do not wait). **blocking** → write open frontier with recommendations; parent pauses for human answers, then re-run or parent applies answers. See `{my-dev-flow-v2}/grill.md` · `{my-dev-flow-v2}/hitl.md`.

**Task prompt:**

```
You are grilling the design tree for my-dev-flow-v2-design. Fresh context only. Follow {my-dev-flow-v2}/grill.md and documentation-and-adrs.

<Paste output of: compose handoff from {my-dev-flow-v2}/handoffs.md for grill>

Read 00-run.md (Mode, HITL Grill, Has API/DB), 01-idea.md, 02-skim.md (if present), 02-analysis.md (especially Design tree + Blocking questions + Settled decisions).
Read repo GLOSSARY.md or GLOSSARY-MAP.md if present. Cross-check claims against code when needed — look up facts yourself; do not ask the user for look-up-able facts.

Build the design tree. Work the frontier in rounds:
- List only questions whose prerequisites are settled
- Each question: title, body, choices when 2+, Recommended answer with user-first one-liner
- Invent 1–3 concrete edge scenarios that stress domain boundaries; record outcomes
- If HITL is auto or async-notify (default): settle each recommended answer now; log auto-pick rationale
- If HITL is blocking: leave frontier open with recommendations; Result needs-round

Domain modeling:
- When a term resolves, update GLOSSARY.md (or mapped context glossary) immediately — definitions only, _Avoid_ aliases
- Offer/write an ADR only if hard-to-reverse AND surprising AND real trade-off (short 1–3 sentence form preferred). Else note ADR skipped.

Write .my-docs/workflow/<slug>/02b-grill.md using the template.
Also update 02-analysis.md Design tree + Settled decisions so frontier is empty when settled.

Do not write production feature code. Do not write 03-design yet. Do not re-litigate Gate A 80/20.
Return FIRST LINE exactly: Result: frontier-empty | needs-round | skipped
Then Grill digest (≤4 bullets) + paths touched (02b, glossary, ADR) ({my-dev-flow-v2}/results.md).
```

**After (parent):**

1. If **skipped** → Notes `grill skipped — <reason>`; continue to Design.
2. If **frontier-empty** → post Grill digest; Run log `done · Grill · frontier-empty · auto` (or blocking settled); continue to Design.
3. If **needs-round** and HITL **blocking** → pause with digest; after human answers, re-run Grill or parent applies answers into `02b` then Design.
4. If **needs-round** under auto (should be rare) → parent user-first settles remaining frontier into `02b`, then Design.

---
