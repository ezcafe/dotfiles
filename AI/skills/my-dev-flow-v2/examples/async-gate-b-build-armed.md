# Golden: async-notify Gate B → Build armed

**Ask:** Mode simple low-risk fix; user asks for a veto window before Build.  
**Classify:** Mode simple; Has API/DB/auth = no; HITL Gate B starts **auto**, then flips to **async-notify** only with Notes `async-notify requested — user: "…"`.

## Path

| Turn | Action |
|------|--------|
| N | Post digest; **Build armed: none**; Notes veto window open; Run log digest HH:MM; Status **`paused`**; Notes `async-gap-pending — <digest-HH:MM>`. Do **not** set **Build armed: yes**. Do **not** launch Build. End turn. |
| N+1 | No veto → set durable **`Build armed: yes`** + Run log arm with **later** HH:MM; keep `async-gap-pending`. Then launch Build if `Gate B veto` still `none`. |
| After verify-pass | **Parent** clears **Build armed: none** (+ veto-window / `async-gap-pending` Notes); Task must not write the field. Then review/test → Gate C |

## Do not

- Launch Build in the same parent turn as the async-notify digest
- Invent a same-turn gap substitute
- Let the Build Task clear or write **Build armed** (parent-only)
- Use **Gate B approved** as the arm token (async uses **Build armed**)
- Use async-notify on Mode **full** (always **blocking**)

SoT: [gate-b.md](../gate-b.md) · [hitl.md](../hitl.md).
