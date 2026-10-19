# Has API/DB + Lens plan + skip-review

**SoT for:** Has API/DB, Has auth/PII/schema, tiny-tweak, Lens plan, skip-review ban.

## Has API / Has DB / Has auth/PII/schema

Set each `yes|no` before design-review (not unknown).

| Flag | Yes when |
|------|----------|
| **Has API** | New/changed REST/GraphQL/routes/server actions, edge validators, public types |
| **Has DB** | New/changed tables/columns/indexes/migrations/ORM, notable writes/SQL |
| **Has auth/PII/schema** | Auth, sessions, roles, PII, or schema/migration risk in scope |

When **Has API** or **Has DB** or **Has auth/PII/schema** is **yes**:

1. Never keep Review profile **skip-review**.
2. Mode full → isolated API/DB review Tasks when Has API/DB yes (unless tiny tweak); Mode simple → fold into design-verify-phase. Auth/PII alone does not force isolated 03a.
3. **Finalize deadline (SoT):** when Has API/DB yes, parent must finalize matching **api**/**db** on Lens plan **before code review** (unless tiny tweak). Parent may set earlier (e.g. before Gate B); late finalize after Adv / code-review-phase starts is forbidden.

Mode full + both API+DB yes (not tiny):

- **Both Isolated API/DB unpaid** (missing **or** Result unpaid/pending — Prefer re-run even if files exist after Upgrade/Amend invalidate): set Pending parallel `api|db`. Card **Next** may be literal `api|db` **or** the first Prefer stage id (`api-contract-review`); Pending parallel authorizes launching both same turn. Prefer same-turn parallel.
- **Resume:** Prefer only the unpaid/pending sibling; set Pending parallel to `api` or `db` for that sibling.
- **Both paid** (`clean`\|`skipped`): clear Pending parallel to `none`.

## Tiny tweak

All must hold — then fold contracts (no isolated 03a; no forced lenses):

- One field / column / validator / docs-only contract note
- No new auth, PII, or cross-service boundary
- Blast radius one package
- Notes: `tiny-contract-tweak — Notes fold light checks into Quality / code-review-phase prose (no 05-lens-* / not paid)`
Never invent empty `03a-api` / `03a-db` when skipped.

## Lens plan

Default **`none`**. Add only on clear signal:

| Lens | Stage | When |
|------|-------|------|
| api | `lens-api` | Has API yes (not tiny) |
| db | `lens-db` | Has DB yes (not tiny) |
| security | `lens-security` | Auth, secrets, trust boundaries |
| perf | `lens-perf` | Latency/CWV/hot path |
| memory | `lens-memory` | Leaks / large payloads |

2+ lenses → `merge-findings` before test. **Result-bearing** = `clean` \| `needs fix` only. **Lens plan unpaid** = some planned `05-lens-*` missing or Result missing/**`pending`** — **excludes Merged** ([derive-next.md](derive-next.md) Definitions). Prefer `merge-findings` only when every planned `05-lens-*` is Result-bearing **and** Merged unpaid/pending (**above** launch-lens — do not rematch launch); dirty **`needs fix`** → Prefer `fix-review` Mode `merged-lenses` (plan **2+**) or Mode `plan-1-lens` (plan **1**) — **not** Prefer `merge-findings` while Fix is pending ([derive-next-post.md](derive-next-post.md)).

**Lenses paid** (unpaid-check only — blocks re-launch while Fix is pending):

| Lens plan | Paid when |
|-----------|-----------|
| **2+** | `05` Merged lenses Result **`clean`** \| **`needs fix`** recorded |
| **1** | that planned `05-lens-*` Result **`clean`** \| **`needs fix`** (parent may copy into Merged lenses; no Merge Task) |
| **`none`** | N/A |

**`needs fix` is paid** for unpaid-check (do not re-launch lenses / Prefer `merge-findings` while Fix is pending — Expected Next `fix-review`). **Exception:** after `fix-review` **verify-pass** for Fix Mode `merged-lenses` or Mode `plan-1-lens`, treat planned `05-lens-*` + Merged as **unpaid** until Result is **`clean`** again ([derive-next.md](derive-next.md) Prefer re-lens).

**Lenses clean** (required before `test-*` / `gate-c`): Merged (plan **2+**) or planned `05-lens-*` (plan **1**) Result **`clean`** only — not unpaid/pending and not `needs fix` — [preflight.md](preflight.md).

## skip-review legality

Mode **simple** only. Legal only while Has API=no **and** Has DB=no **and** Has auth/PII/schema=no.

**Has flip (fail-closed):** when any of those becomes **yes**, parent **MUST** immediately drop Review profile skip-review → **lite** (or Decision N reclassify to **full** if not tiny) **and** set HITL Gate B **blocking**. **Mirror Amend settle clear:** **Gate B approved: none**; **Build armed: none**; clear veto-window / `async-gap-pending`; **clear** design-scoped `gate-b auto — <HH:MM>` (or digest) if present; write Notes `has-flip — <flags> — <HH:MM>` — [design-backloop.md](design-backloop.md) · [gate-b.md](gate-b.md) · [derive-next.md](derive-next.md) Settle freshness. Keep API/DB invalidate-or-Prefer-re-run below. Checked on Always #4–5 + Before Build ([preflight.md](preflight.md)); Forbidden in [stages.md](stages.md). Design / design-phase / design-update After must apply the same drop + settle clear + has-flip Notes. Gate C fail-closed: [gate-c.md](gate-c.md).

**Has flip → Design/Verify unpaid (API/DB newly yes, not tiny):** when Has API or Has DB flips **no→yes** (not Notes `tiny-contract-tweak`), prior overall `03a` **`clean`** no longer pays **Design clean** / **Verify clean** while **Isolated API/DB unpaid**. Parent **MUST** either invalidate overall `03a` Result to **`pending`** (same habit as Amend / Upgrade) **or** Prefer re-run `design-verify-phase` (Mode simple) / API∥DB then `design-review` (Mode full) until **Design clean** / **Verify clean**. Do **not** advance on overall token alone — [derive-next.md](derive-next.md) · [examples/drop-skip-review-api-flip.md](examples/drop-skip-review-api-flip.md).
