# Solo subflow entry

Full pipeline: [stages.md](stages.md). Still honor Verify, severity, clarity-check, parent-only consent, and handoff R/W.

| Skill | Min state | Typical next |
|-------|-----------|--------------|
| [design](../my-dev-flow-v2-design/SKILL.md) | `00-run` + Mode + idea | design-review / design-verify |
| [design-review](../my-dev-flow-v2-design-review/SKILL.md) | `01`–`04`; Has API/DB yes\|no | unpaid `tdd-review` when `04-tasks` has planned tests; else Gate B |
| [code](../my-dev-flow-v2-code/SKILL.md) Build | Gate B settled; design clean; Verify commands | review / smoke / (skip-review ordered recovery) |
| [review](../my-dev-flow-v2-review/SKILL.md) | verify-pass + Smoke; profile ≠ skip-review. Mode **full** + profile **full** → E1 independent Smoke before Adv ([verify.md](verify.md) Independent Smoke (SoT)) | Adv→Quality (full) or code-review-phase (lite) → lenses → merge-findings if 2+ → test-* |
| [test](../my-dev-flow-v2-test/SKILL.md) **smoke** | Build verify-pass; Mode×profile needs independent Smoke (E1) or skip-review Prefer unpaid `smoke re-run` ([verify.md](verify.md)) | Adv / Prefer paid Gate C / continue table |
| [test](../my-dev-flow-v2-test/SKILL.md) **test-full** / **test-lite** | review clean + lenses clean (profile ≠ skip-review) | clear `test-stale` when Lite/full clear met → Prefer `merge` \| `gate-c` only when **Tests success** |
| [test](../my-dev-flow-v2-test/SKILL.md) **skip-review** | legal skip-review after Build | ordered recovery only — [verify.md](verify.md) Skip-review + Smoke (not a free jump to Gate C) |
| [merge](../my-dev-flow-v2-merge/SKILL.md) | Gate C approved + provenance; test bar | `done` |

Grill-only: [grill.md](grill.md).
