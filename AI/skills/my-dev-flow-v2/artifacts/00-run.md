Copy into `.my-docs/workflow/<slug>/`. Companions: [handoffs.md](../handoffs.md) · [verify.md](../verify.md) · [hitl.md](../hitl.md) · [gate-b.md](../gate-b.md) · [gate-c.md](../gate-c.md) · [decisions.md](../decisions.md) · [preflight.md](../preflight.md) · [derive-next.md](../derive-next.md) · [models.md](../models.md) · [lenses.md](../lenses.md) · [failure.md](../failure.md).

# 00-run.md

**Step 0:** fill Required; set HITL from Mode (below). Enums must be exact single tokens (no `|` leftovers).

| Field | Allowed |
|-------|---------|
| Status | `running` \| `paused` \| `stopped` \| `done` |
| Mode | `full` \| `simple` |
| Review profile | `full` \| `lite` \| `skip-review` |
| Gate B veto | `none` \| `pending` |
| Gate B approved | `none` \| `yes` \| named pick |
| Build armed | `none` \| `yes` |
| Pending parallel | `none` \| `api` \| `db` \| `api\|db` |
| Has UI / API / DB / auth/PII/schema | `yes` \| `no` |
| Last Verify | `pending` \| `verify-pass` \| `verify-fail` |
| Last verify-pass at | `none` \| ISO-8601 |
| Gate C approved | `none` \| subset of `commit`,`push`,`pr`,`merge` |
| HITL Gate B | full → `blocking`; simple low-risk → `auto` else `blocking` ([gate-b.md](../gate-b.md)) |
| HITL Grill | full → `async-notify`; simple → `auto` ([grill.md](../grill.md)) |
| HITL Gate C | always `blocking` |

```markdown
# Workflow run: <slug>

## Required

**Status:** running
**Mode:** <full|simple>
**Complexity:** <one-line reason>
**Slug:** `YYYYMMDD-feature-x`
**Review profile:** <full|lite|skip-review>
**Lens plan:** none
**Pending parallel:** none

**Verify commands:**
- **cwd:**
- **build:** `<command>` | N/A — <reason>
- **unit:** `<command>` | N/A — <reason>
- **e2e:** `<command>` | N/A — <reason>

**Last Verify:** pending
**Last verify-pass at:** none
**Verify attempts:** 0

**Gate B veto:** none
**Gate B approved:** none
**Build armed:** none
**Gate C approved:** none

**Last stage:**

**Run metrics:**
- Task count:
- verify-fail count:
- main-thread fallbacks:

## Optional / when known

### Resolved models

| Tier | Slug | Notes |
|------|------|-------|
| High | | Analyze, Design, Update |
| Medium | | Mode full judgment (incl. Grill) |
| Fast | | Build, Fix, Smoke, Test, Merge; Mode simple mechanical + lite review |

**Resolve:** [models.md](../models.md). Fallback: High→Medium→Fast→`inherit`.

### Repo

- **Root:**
- **Branch:**
- **Started:**
- **Has UI:** no
- **Has API:** no
- **Has DB:** no
- **Has auth/PII/schema:** no
- **HITL Gate B:** <Step 0: full→blocking; simple low-risk→auto else blocking>
- **HITL Grill:** <Step 0: full→async-notify; simple→auto>
- **HITL Gate C:** blocking
- **04a:** skipped — reason:
- **Smoke:** pending

### Orchestrator card (parent)

| Field | Value |
|-------|-------|
| Phase | design |
| Stage id | |
| Next | |
| Task description | |
| stages.md section | |
| Model tier | Fast |
| Prereq Result | |
| Last Verify | pending |
| Verify attempts | 0 |
| Gate B veto | none |
| Artifact to check | |
| Design backloop | none |
| Main-thread fallback | none |

### Gates

- [ ] Gate A — Day-to-day + 80/20 (auto when `01a` Result ok)
- [ ] Gate B — Design + tasks — HITL per field above ([gate-b.md](../gate-b.md))
- [ ] Gate C — Commit / push / PR / merge — always blocking

### Notes

- Write live consent / waiver / async tokens only when posting — [hitl.md](../hitl.md)
- Status `done` only after Merge success **and** `merge` ∈ Gate C approved

### Run log

Newest at bottom: `- **HH:MM** · running|done|paused|stopped · <stage-id> · note`

-
```
---
