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

Mode full + both API+DB yes: Pending parallel `api|db` until both `03a-*` exist, then `none`. Prefer same-turn parallel when both missing.

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

2+ lenses → `merge-findings` before test. After all planned `05-lens-*` exist, Merged lenses unpaid/pending → Prefer `merge-findings` ([derive-next.md](derive-next.md)).

**Lenses paid** (unpaid-check only — blocks re-launch while Fix is pending):

| Lens plan | Paid when |
|-----------|-----------|
| **2+** | `05` Merged lenses Result **`clean`** \| **`needs fix`** recorded |
| **1** | that planned `05-lens-*` Result **`clean`** \| **`needs fix`** (parent may copy into Merged lenses; no Merge Task) |
| **`none`** | N/A |

**`needs fix` is paid** for unpaid-check. **Exception:** after `fix-review` **verify-pass** for Fix Mode `merged-lenses` or plan-1 lens Fix, treat planned `05-lens-*` + Merged as **unpaid** until Result is **`clean`** again ([derive-next.md](derive-next.md) Prefer re-lens).

**Lenses clean** (required before `test-*` / `gate-c`): Merged (plan **2+**) or planned `05-lens-*` (plan **1**) Result **`clean`** only — [preflight.md](preflight.md).

## skip-review legality

Mode **simple** only. Drop when Has API or Has DB or Has auth/PII/schema becomes **yes** (same ban as API/DB). Gate C fail-closed: [gate-c.md](gate-c.md).
