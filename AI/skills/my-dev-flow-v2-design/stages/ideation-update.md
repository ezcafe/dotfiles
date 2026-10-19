## ideation-update — Ideation update from Gate A (Medium)

**When:** `01a` Result is **needs update**.

**subagent_type:** `generalPurpose`  
**model:** resolved Medium  
**Task description:** `Update idea from review`

**Done when:** Fix-ask items addressed in `01-idea.md`.

**Task prompt:**

```
You are the Product Owner updating ideation from the user-role day-to-day review (Gate A). Fresh context only.

<Paste output of: compose handoff from {my-dev-flow-v2}/handoffs.md for ideation-update>

Read 01a-gate-a.md (Findings + Fix ask; LEGACY fallback `01a-idea-ui-review.md` on resume only). Read 01-idea.md.

Rules:
- Update only listed Fix-ask items in 01-idea.md.
- Keep full **80/20 UI** when UI applies; keep **Has UI** accurate.
- Append a short note under 01a → Round notes.
- No production code. Simple plain words.

Return: what you updated in 01-idea.md.
```

**After:** Parent re-runs Gate A. Do not claim Gate A approved yet.

---
