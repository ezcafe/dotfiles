# my-dev-flow-v3-review stages (index)

**Load one file only:** `stages/<stage-id>.md` for the current Task.

**Owned stage ids:** `code-review-phase` · `adversarial` · `quality` · `lens-api` · `lens-db` · `lens-security` · `lens-perf` · `lens-memory` · `merge-findings` · `fix-review`

Happy path (profile-qualified):

- **E1 (Mode full + profile full):** independent Smoke (`Smoke source: Smoke-Task`) **before** Adv → Quality → lenses → …  
- **Lite (Mode full|simple + profile lite):** Build-writes-Smoke may pay → Prefer `code-review-phase` → lenses → …  

Notes `smoke-pass` (alias `smoke-pass (re-run)`) = companion only. SoT: [../my-dev-flow-v3/stages.md](../my-dev-flow-v3/stages.md) · [../my-dev-flow-v3/verify.md](../my-dev-flow-v3/verify.md).

| Stage id | File |
|----------|------|
| `code-review-phase` | [stages/code-review-phase.md](stages/code-review-phase.md) |
| `adversarial` | [stages/adversarial.md](stages/adversarial.md) |
| `quality` | [stages/quality.md](stages/quality.md) |
| lenses overview | [stages/lenses-overview.md](stages/lenses-overview.md) |
| `lens-api` | [stages/lens-api.md](stages/lens-api.md) |
| `lens-db` | [stages/lens-db.md](stages/lens-db.md) |
| `lens-security` | [stages/lens-security.md](stages/lens-security.md) |
| `lens-perf` | [stages/lens-perf.md](stages/lens-perf.md) |
| `lens-memory` | [stages/lens-memory.md](stages/lens-memory.md) |
| `merge-findings` | [stages/merge-findings.md](stages/merge-findings.md) |
| `fix-review` | [stages/fix-review.md](stages/fix-review.md) |
