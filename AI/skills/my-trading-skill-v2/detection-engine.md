# Detection Engine (Fast + Memory-Friendly)

## Objective

Detect Elliott structures with low latency and bounded memory, then rank scenarios using rule validity first and confluence second.

## Pipeline

1. Pivot extraction (O(n))
2. Rule-first pruning
3. Pattern-family classification
4. Confluence scoring
5. Scenario emission (primary + alternate)

## Layer 1: Pivot Extraction (O(n))

- Input: OHLCV stream, lookback window, sensitivity parameters.
- Primary method: volatility-adaptive ZigZag/pivot extraction:
  - `minSwingPct` OR `minSwingAtrMult * ATR(period)`
  - Optional fractal confirmation to reduce noise.
- Output: ordered pivot list with fields:
  - `idx`, `time`, `price`, `type` (`H`/`L`), `swingSize`, `swingAtrNorm`

### Performance Notes

- One pass over candles.
- ATR and moving stats use rolling windows.
- Keep only recent pivots up to `maxPivots` (default 300) to cap memory.

## Layer 2: Rule-First Pruning

Generate candidate wave segmentations from pivots and reject invalid structures early.

### Hard Impulse Invalidations

- Wave 2 cannot retrace past Wave 1 start.
- Wave 3 cannot be shortest among Waves 1, 3, 5.
- Wave 4 cannot overlap Wave 1 territory in a standard impulse.

### Corrective Family Gates

- ZigZag: 5-3-5
- Flat variants: 3-3-5
- Triangle variants: 3-3-3-3-3 (A-B-C-D-E)
- Combination families: W-X-Y, W-X-Y-X-Z with connector X waves

### Complexity Control

- Evaluate only local pivot windows (for example 7-21 pivots).
- Cap candidate count per degree (`maxCandidatesPerDegree`).
- Drop candidates after first hard-rule violation.

## Layer 3: Confluence Scoring

After validity, compute confidence via weighted confluence.

### Scoring Features

- Fibonacci proximity score (retracement/extension fit).
- Channel score (temporary/complete impulse channel behavior).
- Alternation score (Wave 2 vs Wave 4 character).
- Indicator score:
  - trend alignment (MA slope/alignment),
  - momentum exhaustion/divergence (RSI/MACD),
  - volatility state (ATR normalization).
- Psychology consistency score (wave-position narrative coherence).

### Confidence Tiers

- High: valid rules + strong multi-factor confluence.
- Medium: valid rules + partial confluence.
- Low: valid rules + weak confluence or conflicting indicators.

## Computational Profile

- Pivot extraction: O(n)
- Candidate generation: O(k * w), where:
  - `k` = pivot count cap
  - `w` = bounded local window size
- Scoring: O(c), `c` = surviving candidate count (bounded by cap)
- Memory: O(k + rollingIndicators)

## Streaming Pseudocode

```python
def analyze(candles, cfg):
    atr = rolling_atr(candles, cfg.atr_period)                # O(n)
    pivots = extract_pivots(candles, atr, cfg)                # O(n)
    candidates = build_candidates(pivots, cfg.max_window)     # bounded

    valid = []
    for cand in candidates:
        if violates_hard_rules(cand):
            continue
        fam = classify_family(cand)                            # impulse/flat/triangle/combination
        if fam is None:
            continue
        score = confluence_score(cand, candles, atr, cfg)
        valid.append((cand, fam, score))

    ranked = rank(valid, key=lambda x: x.score, desc=True)
    primary = ranked[0] if ranked else None
    alternate = ranked[1] if len(ranked) > 1 else None
    return build_output(primary, alternate, cfg)
```

## Practical Defaults

- `atr_period = 14`
- `minSwingAtrMult = 1.2`
- `ma_fast = 20`, `ma_slow = 50`
- `rsi_period = 14`
- `macd = (12, 26, 9)`
- `maxPivots = 300`
- `maxCandidatesPerDegree = 50`

Tune by timeframe and asset volatility.
