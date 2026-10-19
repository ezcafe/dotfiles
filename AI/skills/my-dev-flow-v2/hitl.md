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
| **auto** | Approve without waiting — Gate B: durable `gate-b auto — <HH:MM>` (or digest) after current **Design clean** / **Verify clean** (Design-clean time — [derive-next.md](derive-next.md) Settle freshness · [gate-b.md](gate-b.md)) | Gate B (Mode simple low-risk); Grill |
| **async-notify** | Post digest; Gate B: end turn, Build next turn after **Build armed**; Grill: stay running; settle frontier same turn (do not advance to Design while Grill open) — [grill.md](grill.md) After | Gate B (narrow); Grill |
| **blocking** | Pause for approve/reject | Gate B (required Mode full); **required** Gate C |

## Parent-only consent (hard)

**Parent** writes on `00-run.md` — never from Task returns:

- Gate B approved · Gate C approved · **Build armed** (`none`\|`yes` — [gate-b.md](gate-b.md))
- Gate B auto settle token `gate-b auto — <HH:MM>` (or digest) after current **Design clean** / **Verify clean** (Design-clean time — [derive-next.md](derive-next.md) Settle freshness · [gate-b.md](gate-b.md))
- Notes waiver tokens (table below) + matching **provenance** kinds
- `clarity-check ok — <Next>` lines

**Build armed read:** Build / preflight / resume treat durable `**Build armed:** yes` plus Run log arm HH:MM + Notes `async-gap-pending` as the async settle token (not Gate B approved).

**Build armed clear:** parent-only after Build **verify-pass** ([gate-b.md](gate-b.md) step 5). Tasks never set or clear **Build armed**.

After explicit user yes **in this parent turn**, parent records consent **same turn**. Prefer AskQuestion when available.

**Gate pauses:** when asking the user at Gate A (escalate / Decision N), Gate B (blocking / async digest), or Gate C, paste that gate’s **Read before you decide** block ([gate-a After](../my-dev-flow-v2-design/stages/gate-a.md) · [gate-b.md](gate-b.md) · [gate-c.md](gate-c.md)) before or with the digest / AskQuestion. Set Status **`paused`**.

**Grill blocking pause:** when HITL Grill is **blocking** and frontier is open (`needs-round` / Decision N), set Status **`paused`**, Next=`grill`; do **not** advance to Design. Restore **`running`** only after human answers and re-run / parent apply — [grill.md](grill.md).

## Notes tokens vs provenance kinds

Notes strings and provenance `kind` values are **different**. Escape/waiver needs **both** sides of a required pair:

| Notes token (literal) | Provenance kind | Used for |
|-----------------------|-----------------|----------|
| `smoke-pass (re-run)` | `smoke-pass-rerun` | Companion provenance after Smoke-Task (E1 / skip-review escape) — not an alternate unlock ([verify.md](verify.md) Independent Smoke (SoT)) |
| `docs-only` | `docs-only` | Skip-review Gate C escape |
| `smoke-waive` | `smoke-waive` | Skip-review Gate C escape |
| `gate-c-test-override` | `gate-c-test-override` | Skip-review Gate C escape |
| `card-override` | `card-override` | Card Next vs derive mismatch only — never unpaid lite/full tests or illegal Mode×profile |

Do **not** write provenance kind `smoke-pass-rerun` as a Notes line, or Notes `smoke-pass (re-run)` as a provenance kind.

## Provenance

**Default (user consent):**

```markdown
- provenance — <kind> — user: "<exact user words ≥12 chars, non-filler>"
```

**Evidence-backed carve (`smoke-pass-rerun` only):** after Prefer unpaid → independent Smoke → Prefer paid, when there is no user utterance, parent may record:

```markdown
- provenance — smoke-pass-rerun — evidence: smoke Task + 06 Smoke section after Last verify-pass at <ISO-8601>
```

`<ISO-8601>` must match `00-run.md` **Last verify-pass at** (Run-log local wall time — [artifacts/00-run.md](artifacts/00-run.md) · [derive-next.md](derive-next.md) Freshness). Require real Smoke Task + `06` Smoke section updated **after** that timestamp. Do **not** invent a fake user quote. Other escape kinds (`docs-only`, `smoke-waive`, `gate-c-test-override`) and Gate B/C approved still need the user form.

| kind | When |
|------|------|
| `gate-b-approved` | Blocking Gate B settled |
| `gate-c-approved` | Gate C approved non-empty |
| `smoke-pass-rerun` | Matching Notes `smoke-pass (re-run)` — user form **or** evidence-backed carve above |
| `docs-only` / `smoke-waive` / `gate-c-test-override` / `card-override` | Matching Notes token from table above — user form only |

Do not invent quotes. Short fillers (`yes`, `ok`, `lgtm`) alone are invalid.

## Honesty / residual

Soft checklists ([preflight.md](preflight.md)) and handoff bans raise the cost of cheating; they do **not** cryptographically prove consent.

- Provenance quotes check **shape + quality** only — they do **not** prove the user uttered those words.
- Notes `smoke-pass (re-run)` alone (or plus forged Run-log / `06` evidence) do **not** pay Smoke unpaid, Prefer paid, Gate C independent Smoke, or Adv/Quality FIRST — only `Smoke source: Smoke-Task` does ([verify.md](verify.md) Independent Smoke (SoT)).
- Gate C still needs an **explicit named yes** in the **parent** turn (commit / push / PR / merge) before recording **Gate C approved**.

Parent-only consent remains a **process rule**: Tasks must not write approved / armed / waiver / clarity fields. Soft enforcement only — stop and fix when a check fails; do not invent approvals to pass.

## Git

Never force-push. Never commit secrets (`.env`, `*.pem`, `credentials.json`, `*secret*`).
