# Solo subflow entry

Full pipeline: [stages.md](stages.md). Still honor Verify, severity, clarity-check, parent-only consent, and handoff R/W.

| Skill | Min state | Typical next |
|-------|-----------|--------------|
| [design](../my-dev-flow-v2-design/SKILL.md) | `00-run` + Mode + idea | design-review / design-verify |
| [design-review](../my-dev-flow-v2-design-review/SKILL.md) | `01`–`04`; Has API/DB yes\|no | Gate B |
| [code](../my-dev-flow-v2-code/SKILL.md) Build | Gate B settled; design clean; Verify commands | review / smoke / (skip-review ordered recovery) |
| [review](../my-dev-flow-v2-review/SKILL.md) | verify-pass + Smoke; profile ≠ skip-review. Mode **full** + profile **full** → E1 independent `smoke-pass (re-run)` before Adv ([verify.md](verify.md)) | Adv→Quality (full) or code-review-phase (lite) → lenses → merge-findings if 2+ → test-* |
| [test](../my-dev-flow-v2-test/SKILL.md) | review clean (unless skip-review) | Gate C |
| [merge](../my-dev-flow-v2-merge/SKILL.md) | Gate C approved + provenance; test bar | `done` |

Grill-only: [grill.md](grill.md).
