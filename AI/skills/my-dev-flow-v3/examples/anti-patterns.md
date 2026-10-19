# Anti-patterns

| Wrong | Right |
|-------|-------|
| Mode full + skip-review via Decision N | Forbidden — reclassify |
| Prefer merge from non-empty Gate C without `merge` ∈ set | Prefer gate-c or stay paused |
| Unlock Adv with Notes/Run-log alone | Require `Smoke source: Smoke-Task` (E1/skip-review) |
| Fake user quote for smoke-pass-rerun | Evidence provenance after Smoke Task |
| Build while design-stale | Pre-Build first-match rewrite first |
| Keep pre-flip Gate B settle | Bump settle gen; Prefer gate-b after Design clean |
| Prefer gate-c/merge under lite/full while ¬Tests success | Prefer unpaid test-* / clear stale first |
| Unilateral drop skip-review (Prefer-paid Else) | Named yes — Has flip mandatory drop is different |
| Design while Grill open + artifacts present | Settle grill; Next=`grill` |
