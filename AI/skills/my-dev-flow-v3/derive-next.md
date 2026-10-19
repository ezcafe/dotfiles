# Derive next (Expected Next SoT)

**Load:** this whole file before each Task (kept short on purpose). First-match wins.

## Selector Pre vs Post

| Condition | Half |
|-----------|------|
| Notes `design-backloop` or `design-stale` | **Pre-Build** (always) |
| No Build verify-pass for **current** Gate B settle gen | **Pre-Build** |
| Build verify-pass with **Last verify settle-gen** == current settle gen | **Post-Build** |

On verify-pass, parent sets **Last verify settle-gen** = current **Gate B settle gen**.

## Definitions

| Term | Meaning |
|------|---------|
| **Design clean** / **Verify clean** | Overall `03a` **clean** **and** Isolated API/DB paid when required (`clean`\|`skipped`; Has=yes not tiny → file required) |
| **design-review not clean** | ¬ Design clean (incl. Isolated unpaid) |
| **Isolated API/DB unpaid** | Has yes (not tiny) and file missing **or** Result ≠ `clean` (incl. `pending`) — Prefer re-run **even if files exist** |
| **Grill open** | `02b` Result `needs-round` **or** Grill unpaid with no grill-skip |
| **design artifacts** | `02-analysis` + `03` + `04` present (ignore Grill) |
| **Review clean** | Adv + Quality section Results both **clean** (file-top alone never pays) |
| **code-review unpaid** | Planned Adv/Quality missing **or** section Result missing/`pending` (not `needs fix`) |
| **Review needs fix** | Adv and/or Quality section Result = `needs fix` |
| **Lens plan unpaid** | Planned `05-lens-*` missing **or** Result missing/`pending`. Result-bearing = `clean`\|`needs fix` only |
| **Smoke unpaid** | E1 or skip-review: unpaid until `Smoke source: Smoke-Task`. Lite: Build-writes-Smoke may pay |
| **Tests success** | ≡ Gate C test bar ([gate-c.md](gate-c.md)) |
| **Tests unpaid** | Profile ≠ skip-review **and** ¬(`06` success **and** path matches profile) |
| **Gate C unpaid** | approved `none`/empty **or** remaining named actions unpaid |
| **Gate B settled** | Token gen == current settle gen ([gate-b.md](gate-b.md)) |

## Unsafe jumps (never Prefer / launch)

- Illegal Mode×profile  
- Build / Post-Build while `design-stale` or `design-backloop` (until clear rules met)  
- Design family / gate-b / build while Grill open **and** design artifacts present (cold start carve: artifacts missing → Prefer `design-phase` allowed)  
- `gate-c` / `merge` while ¬ Tests success or unpaid stale Notes  
- `merge` unless Tests success **and** `merge` ∈ Gate C approved  
- Stages while Status `done` \| `stopped`  
- Post-Build while verify settle-gen ≠ current Gate B settle gen  

`card-override` cannot waive these.

## Pre-Build (first-match)

| State | Expected Next |
|-------|---------------|
| Mode full, unpaid Gate A | `gate-a` |
| Mode full, unpaid skim | `skim` |
| Notes `design-stale` | Prefer first unpaid `analyze` → `grill` → `design` (do not match Grill-open / paid Mode-simple analysis) |
| Notes `design-backloop` + design-update unpaid / design-review not clean | Mode full: Prefer unpaid Isolated → else `design-review`. Mode simple: `design-verify-phase` only |
| Notes `design-backloop` + Design clean + Gate B settled | Clear Notes same turn → Prefer `build` |
| Mode full, no `02-analysis` | `analyze` |
| Grill open + design artifacts present (or `02b` needs-round) | `grill` |
| Mode simple, no design artifacts + Grill unpaid (cold start) | `design-phase` |
| Mode simple, design-review not clean | `design-verify-phase` |
| Mode full, Isolated unpaid | Prefer unpaid `api-contract-review` / `db-design-review` (both unpaid → Next `api\|db`; Pending parallel) |
| Mode full, design-review not clean | `design-review` |
| Design clean, Gate B not settled | `gate-b` |
| Design clean, Gate B settled | `build` |

## Post-Build (first-match)

| State | Expected Next |
|-------|---------------|
| Status `done` \| `stopped` | Stop |
| Status `paused` + waiting on user | Stop — stay paused ([resume.md](resume.md)) |
| Last Verify ≠ verify-pass at Build/Fix | re-`build` / same Fix if attempts &lt; 3 else Decision N |
| verify-pass + Last verify-pass at none | Stop — stamp ISO local ([results.md](results.md)) |
| Lens plan missing required api/db | Stop — parent finalize Lens plan |
| E1 or skip-review Smoke unpaid/fail | Prefer unpaid `smoke` (even if escape exists; Build-writes-Smoke does not waive) |
| Review needs fix | `fix-review` |
| code-review unpaid (profile full) | Prefer unpaid Adv then Quality |
| code-review unpaid (profile lite) | `code-review-phase` |
| Review clean, Lens plan unpaid | Prefer unpaid `lens-*` |
| Plan 2+, all lenses Result-bearing, Merged unpaid | `merge-findings` |
| Notes `review-stale` (not skip-review) | Prefer unpaid review ([verify.md](verify.md) clear duty) |
| Notes `test-stale` | skip-review → Prefer unpaid Smoke; else Prefer unpaid `test-*` |
| Legal skip-review Prefer paid | bar met + `merge` ∈ approved → `merge`; else → `gate-c`; else Decision N |
| Tests unpaid (lite/full) | Prefer unpaid `test-full` / `test-lite` |
| Tests success + `merge` ∈ approved | `merge` |
| Tests success + Gate C unpaid | `gate-c` |
