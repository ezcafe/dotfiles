# Golden: Fix (merged-lenses / plan-1) → Prefer re-lens

**Setup:** Profile **full** or **lite**; Lens plan **2+** (or **1**); Merge findings (or plan-1 lens) wrote Fix ask → `fix-review` Mode `merged-lenses` (or plan-1 lens Fix) returned **verify-pass**. Adv/Quality / `code-review-phase` already **clean**.

**Path:**

1. Derive Next: Last stage `fix-review` + Last Verify = **verify-pass** → Prefer Mode `merged-lenses` / plan-1 branch — **not** “already clean → continue” into `test-*` while Merged / `05-lens-*` still says `needs fix`.
2. Parent marks planned `05-lens-*` + Merged **unpaid**/pending (`needs fix` no longer counts as paid until re-clean).
3. Prefer re-run dirty `lens-*` (or all planned; parallel when 2+) → `merge-findings` if 2+.
4. Merge / plan-1 Result **clean** → Prefer else continue table (`test-full` / `test-lite`). Still `needs fix` → `fix-review` again (max rounds → Decision N).

**Do not:** Treat lenses as paid on `needs fix` after this Fix verify-pass; launch `test-*` / `gate-c` while Merged / plan-1 Result ≠ **clean**; Prefer only Adv/Quality when Fix Mode was lens/merged.

See [derive-next.md](../derive-next.md) Post-Build · [lenses.md](../lenses.md) · [preflight.md](../preflight.md) Before test-*/gate-c · [fix-review.md](../../my-dev-flow-v2-review/stages/fix-review.md).
