# Design-backloop (design invalid after Build)

When Build/review proves design wrong (contracts/IA):

1. Notes `design-backloop`  
2. Bump Gate B settle gen; clear consent tokens  
3. Last Verify pending; clear verify-pass stamp + Last verify settle-gen  
4. Invalidate overall + isolated `03a*` clean → `pending`  
5. Keep `review-stale` / `test-stale`  
6. Selector: always **Pre-Build** while Notes set  

## Prefer (Expected Next = [derive-next.md](derive-next.md))

- Mode **full:** Prefer unpaid Isolated API/DB (even if files exist) → else `design-review`  
- Mode **simple:** Prefer `design-verify-phase` only (no isolated Prefer stages)  

Entry Prefer unpaid `design-update` when artifacts need rewrite.

## Clear Notes

Same turn as Gate B re-settle after fresh Design clean. Then Prefer `build`.

## Stale clear after rebuild

Lite/full and skip-review clear rules: [verify.md](verify.md) Stale.
