# HITL Gate C

**SoT for:** Gate C test bar, **Gate C approved** actions.  
Index + shared Provenance / Tiers / Git: [hitl.md](hitl.md). Gate B: [hitl-gate-b.md](hitl-gate-b.md). Pipeline: [stages.md](stages.md).

**Parent-only write (hard):** Parent writes **Gate C approved** and matching provenance — never from Task returns. See [hitl.md](hitl.md) Parent-only consent.

**Preferred collection:** When the IDE exposes **AskQuestion** / decision UI, prefer it for the Gate C commit/push/PR/merge ask. After an explicit user yes in **this** parent turn, the **parent** writes **Gate C approved** + provenance in that same turn — never from Merge Task output. Residual: preferred channel, not machine-proof of chat speech ([hitl.md](hitl.md) Honesty).

## Gate C test bar (before merge subflow)

| Review profile | Required |
|----------------|----------|
| **skip-review** | **Fail-closed:** legal only per [lenses.md](lenses.md) **and** Build **verify-pass** + Smoke smoke-pass **and** one escape **with provenance**: Notes `smoke-pass (re-run)` + `smoke-pass-rerun`, Complexity/Notes `docs-only` + `docs-only`, or `smoke-waive` / `gate-c-test-override` with their kinds. Free-text Notes alone are **rejected**. Relying on Build-writes-Smoke alone → lint `--before-merge` **error** / `--next` → `do-not-launch` (exit **1**). Recovery: [verify-and-fix.md](verify-and-fix.md) |
| **lite** | `06-test-log.md` Result **success** **and** **Test path last run:** `lite` (missing → fail closed; LEGACY alias `Mode last run`) |
| **full** | `06-test-log.md` Result **success** **and** **Test path last run:** `full` (missing → fail closed; LEGACY alias `Mode last run`) |

Explicit user override may waive green tests **only** with Notes `gate-c-test-override` **plus** provenance `gate-c-test-override`. Does **not** waive Notes `review-stale` / `test-stale` (or unpaid clean/success vs `Last verify-pass at` — [verify-and-fix.md](verify-and-fix.md) Stale).

**Lint:** `scripts/lint-run.py <run-dir> --before-merge` (also when `--next` and card Next=`merge`) enforces this bar from `00-run.md` + `06-test-log.md` unless Notes override **with provenance** is present; **errors** on `review-stale` / `test-stale` and on unpaid `05`/`06` vs `Last verify-pass at`; skip-review Build-only smoke → **error** unless the fail-closed escape above; also runs `--check-results` (warn-only).

After Merge Result **success** **and** `merge` ∈ **Gate C approved** → set Status **`done`**. Subset without `merge` (e.g. PR only) → stay `paused`; leave Next for remaining actions. Abort/reject → `stopped`, not `done` ([results.md](results.md) · [stages.md](stages.md) Done criteria).

## Gate C approved actions (durable)

**Required when at Gate C / before merge:** parent records the user’s explicit yes as a durable field on `00-run.md` **and** provenance ([hitl.md](hitl.md) Provenance):

```markdown
**Gate C approved:** commit,push,pr,merge

### Notes
- provenance — gate-c-approved — user: "commit push PR and merge"
```

| Value | Meaning |
|-------|---------|
| `none` | No Gate C yes yet (default until ask settles) |
| comma-separated subset of `commit` \| `push` \| `pr` \| `merge` | Actions the user named in this chat |

**Rules:**

- Do **not** invent actions. Subset only what the user named (“PR only” → `pr` or `commit,push,pr` as said).
- Provenance quote must match the user’s words (see [hitl.md](hitl.md) Provenance).
- Merge Task / parent must re-read **Gate C approved** before git/remote actions.
- Lint: default `scripts/lint-run.py <run-dir>` errors when card Next=`merge` and **Gate C approved** is missing / `none` / empty **or** provenance missing. `--before-merge` enforces approved-actions + provenance + Gate C test bar and runs `--check-results` warn-only (prefer before launching Merge).
