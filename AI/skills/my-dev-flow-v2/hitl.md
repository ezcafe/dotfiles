# HITL (index)

| Concern | SoT |
|---------|-----|
| Gate B tiers / Build armed / Gate B approved | [gate-b.md](gate-b.md) |
| Gate C test bar / Gate C approved | [gate-c.md](gate-c.md) |
| Grill domain | [grill.md](grill.md) |
| Tiers / Provenance / Parent-only / Git | **this file** |

## Tiers

| Tier | Behavior | Allowed for |
|------|----------|-------------|
| **auto** | Approve without waiting | Gate B (Mode simple low-risk); Grill |
| **async-notify** | Post digest; Gate B: end turn, Build next turn after **Build armed**; Grill: continue | Gate B (narrow); Grill |
| **blocking** | Pause for approve/reject | Gate B (required Mode full); **required** Gate C |

## Parent-only consent (hard)

**Parent** writes on `00-run.md` — never from Task returns:

- Gate B approved · Gate C approved · **Build armed** (`none`\|`yes` — [gate-b.md](gate-b.md))
- Notes waiver tokens (table below) + matching **provenance** kinds
- `clarity-check ok — <Next>` lines

**Build armed read:** Build / preflight / resume treat durable `**Build armed:** yes` plus Run log arm HH:MM + Notes `async-gap-pending` as the async settle token (not Gate B approved).

**Build armed clear:** parent-only after Build **verify-pass** ([gate-b.md](gate-b.md) step 5). Tasks never set or clear **Build armed**.

After explicit user yes **in this parent turn**, parent records consent **same turn**. Prefer AskQuestion when available.

## Notes tokens vs provenance kinds

Notes strings and provenance `kind` values are **different**. Escape/waiver needs **both** sides of a required pair:

| Notes token (literal) | Provenance kind | Used for |
|-----------------------|-----------------|----------|
| `smoke-pass (re-run)` | `smoke-pass-rerun` | Independent Smoke paid (E1 / skip-review escape) |
| `docs-only` | `docs-only` | Skip-review Gate C escape |
| `smoke-waive` | `smoke-waive` | Skip-review Gate C escape |
| `gate-c-test-override` | `gate-c-test-override` | Skip-review Gate C escape |
| `card-override` | `card-override` | Card Next vs derive mismatch only — never unpaid lite/full tests or illegal Mode×profile |

Do **not** write provenance kind `smoke-pass-rerun` as a Notes line, or Notes `smoke-pass (re-run)` as a provenance kind.

## Provenance

```markdown
- provenance — <kind> — user: "<exact user words ≥12 chars, non-filler>"
```

| kind | When |
|------|------|
| `gate-b-approved` | Blocking Gate B settled |
| `gate-c-approved` | Gate C approved non-empty |
| `smoke-pass-rerun` / `docs-only` / `smoke-waive` / `gate-c-test-override` / `card-override` | Matching Notes token from table above |

Do not invent quotes. Short fillers (`yes`, `ok`, `lgtm`) alone are invalid.

## Honesty / residual

Soft checklists ([preflight.md](preflight.md)) and handoff bans raise the cost of cheating; they do **not** cryptographically prove consent.

- Provenance quotes check **shape + quality** only — they do **not** prove the user uttered those words.
- Notes `smoke-pass (re-run)` plus forged Run-log / `06` evidence do **not** prove an independent Smoke Task ran.
- Gate C still needs an **explicit named yes** in the **parent** turn (commit / push / PR / merge) before recording **Gate C approved**.

Parent-only consent remains a **process rule**: Tasks must not write approved / armed / waiver / clarity fields. Soft enforcement only — stop and fix when a check fails; do not invent approvals to pass.

## Git

Never force-push. Never commit secrets (`.env`, `*.pem`, `credentials.json`, `*secret*`).
