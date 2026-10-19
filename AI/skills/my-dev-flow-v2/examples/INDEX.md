# Examples (golden paths)

Short narratives for Mode × profile. Read one when classifying or stuck.

| Example | Mode | Profile | Notes |
|---------|------|---------|-------|
| [simple-bugfix.md](simple-bugfix.md) | simple | lite | design-phase → verify → Build → review → test-lite → Gate C |
| [simple-skip-review.md](simple-skip-review.md) | simple | skip-review | ordered recovery: Prefer paid → Gate C; else drop lite; else escape |
| [drop-skip-review-api-flip.md](drop-skip-review-api-flip.md) | simple | skip→lite | Has API/DB/auth flips yes → drop skip-review immediately |
| [lite-with-lenses.md](lite-with-lenses.md) | simple\|full | lite | code-review-phase → lenses per plan → merge-findings if 2+ → test-lite |
| [full-lite-review.md](full-lite-review.md) | full | lite | Full design path; post-Build lite (not Adv→test-full) |
| [simple-api-gate-b-blocking.md](simple-api-gate-b-blocking.md) | simple | lite | Has API=yes → Gate B blocking (not auto) |
| [simple-auth-gate-b-blocking.md](simple-auth-gate-b-blocking.md) | simple | lite | API=no DB=no auth=yes → Gate B blocking |
| [full-api-db.md](full-api-db.md) | full | full | Ideation→…→ parallel API∥DB → independent Smoke → Adv→test-full |
| [reclassify-simple-to-full.md](reclassify-simple-to-full.md) | simple→full | full\|lite | Mid-run API+DB → Decision N upgrade |
| [design-backloop-after-build.md](design-backloop-after-build.md) | any | any | Design invalid after Build → amend → Gate B again |
| [gate-a-escalate.md](gate-a-escalate.md) | full | full\|lite | escalate → Decision N → re-run or override ok after explicit yes |
| [async-gate-b-build-armed.md](async-gate-b-build-armed.md) | simple | lite | async-notify → next-turn Build armed → Build |
| [smoke-fail-fix-resmoke.md](smoke-fail-fix-resmoke.md) | any | any | smoke-fail → fix-tests verify-pass → re-smoke (not stay on fix-tests) |
| [fix-review-rereview.md](fix-review-rereview.md) | any | full\|lite | Fix → Prefer re-verify dirty Adv/Quality / code-review-phase |
| [fix-review-relens.md](fix-review-relens.md) | any | full\|lite | Fix Mode merged-lenses / plan-1 → Prefer re-unpay lenses → re-lens → merge if 2+ |

Anti-patterns (incl. skip-review dual-forge): [anti-patterns.md](anti-patterns.md).

Also: inventing Gate C yes; Build without Gate B approved; skip-review with Has API/DB/auth/PII/schema=yes; relying on Build-writes-Smoke alone under skip-review; launching `test-lite` while profile stays skip-review.
