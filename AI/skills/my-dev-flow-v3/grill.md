# Grill — stress-test the plan

Adapted from [mattpocock grilling](https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md): design tree + frontier rounds.

## Goal

Interview until shared understanding. Map decisions as a **design tree**. Work in **rounds**. The **frontier** is every decision whose prerequisites are settled.

## Round format

```
❓ **Q1** - **<title>**: <body; choices OK>

➡️ <recommended answer>

---

❓ **Q2** - ...
```

Word questions so **"yes" accepts the recommendation**. Ask the **whole frontier** in one round; wait for answers before the next.

Finding **facts** is the agent's job (dispatch explore). Finding **decisions** is the user's.

## Done when

Frontier empty (`02b` Result `frontier-empty` or Notes grill-skip / Result `skipped`).

## Prefer / fail-closed

- Grill open + design artifacts present (or `02b` needs-round) → Expected Next `grill`. Execution: Task `grill` **or** parent apply into `02b`; card Next stays `grill` until closed.  
- Prefer `design-phase` on Grill open **only** for cold start (no artifacts, no `02b` needs-round).  
- Do **not** start Design / design-review / gate-b / build while Grill open and artifacts present.  
- Async-notify tier: stay `running`; settle frontier same turn — do **not** treat “continue” as advance to Design.
