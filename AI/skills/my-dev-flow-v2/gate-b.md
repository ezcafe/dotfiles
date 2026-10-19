# Gate B

**SoT for:** Default tiers, async-notify, Build armed, Gate B approved. Shared provenance: [hitl.md](hitl.md).

## Read before you decide (show to user)

When posting the Gate B digest / AskQuestion (blocking or async-notify), the **parent** pastes this reading guide to the user. Paths under `.my-docs/workflow/<slug>/`.

**Must read (decision):**

1. `03-design.md` — options, Recommendation, System design, contracts, UI locks
2. `04-tasks.md` — acceptance + planned tests
3. `03a-design-review-log.md` — overall design-review Result (must be **clean**)
4. `03a-api-contract-review.md` / `03a-db-design-review.md` — when present (Has API/DB)
5. `00-run.md` — Has API/DB/auth/PII/schema, HITL Gate B tier, Verify commands

**Skim if open issues:**

- `02b-grill.md` — Settled decisions (do not re-open without evidence)
- `04a-tdd-test-review.md` — when TDD review ran
- `01-idea.md` / `01a-gate-a.md` — only if UI locks or Core problem feel wrong

**Decide:** approve Build (named yes / Option N) · reject / change pick · stop. Blocking → parent records **Gate B approved** + provenance. Async → digest only this turn; arm **Build armed** next turn if no veto.

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
