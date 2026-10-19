# Build

## FIRST

Stop with blocked Result if: `design-stale` / `design-backloop` / Gate B auto not settled / Gate B settle stale / veto / missing Build armed when async.

## Do

1. TDD per task in `04-tasks.md`.  
2. Verify commands → `verify-pass` or `verify-fail`.  
3. On verify-pass: set `Smoke source: Build-verify` on `06` when writing Smoke section.

## After (parent)

Stamp Last Verify, Last verify-pass at (ISO-8601 Run-log local wall time), Last verify settle-gen. Mark stale Notes if rebuild ([../../my-dev-flow-v3/verify.md](../../my-dev-flow-v3/verify.md)).
