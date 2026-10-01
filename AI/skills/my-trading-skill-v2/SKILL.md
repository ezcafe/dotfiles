---
name: my-trading-skill-v2
description: >-
  Modular Elliott Wave skill for fast, memory-friendly wave detection and scenario analysis:
  hard-rule validation, pattern classification, indicator-assisted confluence, entry/exit and
  expected SL/TP zones, market psychology mapping, and explicit input/output contracts.
---

# My Trading Skill V2

## When to Use

Use this skill when the user asks for:

- Elliott Wave counting or relabeling
- Pattern identification (impulse, zigzag, flat, triangle, W-X-Y, W-X-Y-X-Z)
- Entry/exit planning with invalidation and target zones
- Scenario branching (primary vs alternate)
- Performance-aware detection workflows for coding or automation

## First Principles

1. Hard rules first. If violated, invalidate and relabel.
2. Structure before indicators.
3. Indicators confirm; they do not define Elliott labels.
4. Always provide invalidation and alternate scenario.
5. Keep output educational and non-prescriptive.

## Required Workflow

1. Build wave hypothesis from pivots.
2. Apply hard-rule checks.
3. Classify pattern family.
4. Add confluence (fib/channel/indicator/psychology).
5. Emit primary and alternate scenarios with switch triggers.
6. Provide entry/SL/TP zones as probabilistic ranges.

## Module Map

- Core rules: `core-rules.md`
- Pattern taxonomy: `pattern-library.md`
- Detection architecture and pseudocode: `detection-engine.md`
- Entry/exit and expected SL/TP logic: `entries-exits-sltp.md`
- Input/output schema: `io-contract.md`
- Psychology and scenario transitions: `market-psychology-and-scenarios.md`
- Source links: `references.md`

## Minimal Response Template

1. Working count (primary + alternate)
2. Rule checks (pass/fail)
3. Entry zone + confirmation
4. Expected SL and TP1/TP2/TP3 zones
5. Invalidation and scenario-switch triggers
6. Confidence rationale and source-backed notes

## Coding Strategy Summary (Fast/Efficient)

- Prefer O(n) streaming indicators and pivot extraction.
- Cap candidate branching to avoid combinatorial blow-up.
- Use rolling windows and bounded pivot history for memory control.
- Cache shared calculations across scenarios.

## Constraints

- Do not present outputs as financial advice.
- Do not hide uncertainty: explicitly mark tentative vs confirmed structure.
- If data is insufficient or contradictory, return best two scenarios and required confirmation signals.
