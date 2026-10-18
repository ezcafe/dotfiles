# Result first-line vocabulary (canonical)

**This file is SoT for:** Task / stage **Result** first-line tokens and when the parent advances.  
Severity (Critical/Major vs Enhancement): [severity.md](severity.md).  
Verify gate details: [verify-and-fix.md](verify-and-fix.md).  
Pipeline order: [stages.md](stages.md).

## Convention

Return line 1 as:

```
Result: <token>
```

Optional short note after an em dash: `Result: blocked — Gate B veto`.  
Parent reads the first ~40 lines; do not bury the token.

## Token table

| Domain | Tokens | Parent advances when | Do not advance when |
|--------|--------|----------------------|---------------------|
| **Verify** (Build / Fix) | `verify-pass` \| `verify-fail` | `verify-pass` | `verify-fail` (retry ≤3 or Decision N) |
| **Blocked** (pre-code stop) | `blocked — <reason>` | — (settle reason) | Always stay; e.g. Gate B veto, Gate B approved, Build armed missing, design-backloop |
| **Design review** (`03a*`) | `clean` \| `needs update` \| `skipped` | overall `clean` (API/DB `clean`\|`skipped`) | `needs update` → Update → re-review |
| **Gate A** (`01a`) | `ok` \| `needs update` \| `escalate` | `ok` (auto-check Gate A) | `needs update` → ideation-update ↔ gate-a until ok or round=3 (pause human only at max 3); `escalate` → hold (`--derive` / `--next` stay fail-closed — not skim). Resume only after **Decision N** + **explicit user yes**: re-run Gate A, or set Result `ok` + Notes — never invent Result `ok` ([invariants.md](invariants.md) · [failure-playbook.md](failure-playbook.md)) |
| **Grill** (`02b`) | `frontier-empty` \| `needs-round` \| `skipped` | `frontier-empty` or `skipped` | `needs-round` |
| **Skim** | `done` \| `skipped` | either | — |
| **TDD review** (`04a`) | `clean` \| `needs more tests` | `clean` or Notes skip | `needs more tests` |
| **Code review** (`05*` — Adv, Quality, Lite combined, lenses, Merge findings) | `clean` \| `needs fix` | `clean` | `needs fix` → Fix → re-review (legacy lens text `has findings` → `needs fix`) |
| **Test / Smoke** (`06`) | `success` \| `failure` \| `smoke-pass` \| `smoke-fail` | `success` / `smoke-pass` | `failure` / `smoke-fail` → Fix |
| **Merge** | `success` \| `aborted` | `success` **and** `merge` ∈ **Gate C approved** → Status `done` | `aborted` → `stopped`; `success` without `merge` in approved → stay `paused`, leave Next for remaining actions |

**Clean** for review stages = zero open Critical/Major ([severity.md](severity.md)).

## Parent habit

1. Read Result first line.
2. Update Orchestrator card + Last Verify when Verify applies.
3. Advance only per table above.
4. Max 3 attempts → Decision N ([invariants.md](invariants.md)).

**Lint (optional):** `scripts/lint-run.py <run-dir> --check-results` scans known artifact Result headers for valid tokens and soft-warns on oversize bodies ([size-caps.md](size-caps.md)). Also runs automatically (warn-only) with `--before-merge` or when card Next=`merge`.
