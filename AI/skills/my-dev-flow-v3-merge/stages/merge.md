# Merge

## Hard rules

0. Abort (`Result: aborted`) if ¬ Tests success (incl. unpaid stale Notes) or `merge` ∉ Gate C approved when performing merge.  
1. Only perform actions named in Gate C approved.  
2. Never force-push. Never invent approval.  
3. Status `done` only after merge success **and** `merge` ∈ approved. PR-only → stay `paused`.
