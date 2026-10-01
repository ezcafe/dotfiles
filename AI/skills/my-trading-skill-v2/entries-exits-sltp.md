# Entries, Exits, SL, and TP Framework

## Important Framing

- Educational analysis only.
- Output probabilities and scenario ranges, not certainty.
- Always report invalidation.

## Entry Framework

## 1) Structure-Confirmed Entry

- Wait for pattern completion signal:
  - Wave 2 completes in valid retracement zone.
  - Triangle E completes and breakout confirms continuation.
  - ABC completion with C exhaustion + reversal confirmation.

## 2) Confluence-Confirmed Entry

Require at least 2-3 from:

- Rule-valid count
- Fibonacci reaction zone
- Channel boundary reaction
- Momentum confirmation (RSI/MACD turn/divergence)
- Trend filter alignment (MA slope/alignment)

## 3) Breakout Entry

- For triangle/combination exits, prefer close-based breakout confirmation.
- Avoid mid-structure entries inside choppy consolidation.

## Exit Framework

- Partial exits at TP ladder zones.
- Full exit on:
  - structural invalidation,
  - opposite high-confidence scenario trigger,
  - clear momentum failure near target zones.

## Expected SL Zone Logic

- Structural stop basis:
  - beyond count invalidation point (preferred).
- Volatility buffer:
  - optional ATR multiplier buffer to avoid noise stop-outs.
- Combined formula:
  - `stop = invalidation +/- max(structuralBuffer, atrMult * ATR)`

## Expected TP Zone Logic

Build TP zones from scenario family:

- Motive continuation:
  - Wave 3/5 fib projections + channel rails.
- Corrective completion:
  - C vs A multiples (0.618, 1.0, 1.618) and prior pivot zones.
- Use TP ladder:
  - TP1 = conservative confluence
  - TP2 = base-case confluence
  - TP3 = extended case

## Output Template

- Entry zone: `price_low -> price_high`
- Confirmation trigger: plain language condition
- SL zone: `sl_low -> sl_high` + rationale
- TP ladder:
  - TP1, TP2, TP3 with scenario confidence labels
- Invalidation trigger:
  - exact structural condition
