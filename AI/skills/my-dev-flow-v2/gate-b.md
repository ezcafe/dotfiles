# Gate B

**SoT for:** Default tiers, async-notify, Build armed, Gate B approved. Shared provenance: [hitl.md](hitl.md).

## Default tier

| Mode / scope | Prefer |
|--------------|--------|
| Mode **full** | Always **blocking** |
| Mode **simple** + API=no + DB=no + no auth/PII/schema + design clean | **auto** |
| Mode **simple** + API/DB/auth/PII/schema yes or open Critical/Major | **blocking** |

**async-notify:** only Mode simple low-risk row **and** user asks for a veto window. Record:

```markdown
- async-notify requested — user: "<verbatim ≥12 chars>"
```

## Blocking settle

Parent sets before Build:

```markdown
**Gate B approved:** yes
- provenance — gate-b-approved — user: "…"
```

## async-notify + Build armed

Durable field on `00-run.md` (parent-only write/read):

```markdown
**Build armed:** none | yes
```

| Value | Meaning |
|-------|---------|
| `none` | Not armed (default; also after parent clear on verify-pass or veto) |
| `yes` | Parent armed Build on a turn **after** the async digest |

1. Post digest; set `Gate B veto: none`; **Build armed: none**; Notes veto window open; Run log digest HH:MM; Status `paused`; do **not** launch Build same turn.
2. Notes: `async-gap-pending — <digest-HH:MM>`.
3. **Next parent turn:** set **`Build armed: yes`**; Run log arm HH:MM **later** than digest; then launch Build if veto still `none`.
4. User veto → `Gate B veto: pending`; set **Build armed: none**; do not Build.
5. Build Task first action: re-read veto / approved / **Build armed** — stop with `blocked — …` if unsettled (veto window open and **Build armed** ≠ `yes`, including `none` → `blocked — Build armed not yes`). **Parent-only clear (chosen habit):** after Build returns **verify-pass**, parent sets **Build armed: none** and clears veto-window / `async-gap-pending` Notes as needed. Build Task must **not** write **Build armed**.

## Veto after Build

Decision N ([decisions.md](decisions.md)): discard draft · keep draft + re-open Gate B · stop.
