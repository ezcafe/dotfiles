# Golden: Fix lenses → Prefer re-lens

**Setup:** Lens plan 2+ (or 1); `fix-review` Mode `merged-lenses` / `plan-1-lens` returned **verify-pass**. Adv/Quality already clean.

**Path:**

1. Re-unpay planned `05-lens-*` + Merged.  
2. Prefer re-lens → `merge-findings` if 2+ **only when planned lenses clean**.  
3. Still `needs fix` → `fix-review` again.

**Do not:** Prefer `test-*` / `gate-c` / `merge` while Lenses dirty or ¬ **Lenses clean** (incl. Merged unpaid); Prefer `merge-findings` on `needs fix`.
