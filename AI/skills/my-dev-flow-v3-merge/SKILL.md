---
name: my-dev-flow-v3-merge
description: >-
  After explicit Gate C approval, commits (if approved), pushes, opens PR, then
  merges. Never commit/push without named user yes. Use when run
  my-dev-flow-v3-merge or after Gate C test bar is met.
---

# my-dev-flow-v3-merge

## Start

Confirm **Tests success** ≡ Gate C bar ([../my-dev-flow-v3/gate-c.md](../my-dev-flow-v3/gate-c.md)) including unpaid stale Notes cleared.  
Confirm each named action ∈ Gate C approved (+ provenance).  
Skip-review: independent Smoke (`Smoke-Task`) required; Build-writes-Smoke alone fails closed.  
Abort if unpaid stale Notes remain.

## Stages

| Id | File |
|----|------|
| merge | [stages/merge.md](stages/merge.md) |
