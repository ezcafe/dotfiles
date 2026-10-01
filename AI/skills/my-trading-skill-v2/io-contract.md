# I/O Contract

## Required Inputs

## Market Data

- `ohlcv`: array of candles with:
  - `time`, `open`, `high`, `low`, `close`, `volume`
- `timeframe`: e.g. `15m`, `1h`, `4h`, `1d`
- `lookbackBars`: minimum recommended 300+

## Optional Context

- `symbol` and `marketType` (`spot`, `futures`, `fx`, etc.)
- `sessionFilter` or trading-hours constraints

## Detection Parameters

- `pivotMethod`: `percent` | `atr` | `hybrid`
- `minSwingPct`
- `atrPeriod` (default 14)
- `minSwingAtrMult`
- `fractalConfirmBars` (optional)
- `maxPivots`
- `maxCandidatesPerDegree`

## Indicator Parameters

- `maFast`, `maSlow`
- `rsiPeriod`
- `macdFast`, `macdSlow`, `macdSignal`

## Risk and Projection Parameters

- `riskUnit` (R or % or absolute value)
- `maxRiskPct` (optional)
- `tpMode`: `conservative` | `balanced` | `extended`

## Expected Outputs

- `primaryScenario`
  - `patternFamily`
  - `waveLabels`
  - `confidence`
  - `invalidation`
  - `entryZone`
  - `slZone`
  - `tpLadder`
  - `evidence`
- `alternateScenarios[]` (same structure, lower rank)
- `switchTriggers[]` for scenario transitions
- `analysisNotes`

## Machine-Friendly Example

```json
{
  "primaryScenario": {
    "patternFamily": "impulse",
    "waveLabels": "1-2-3-4-5 (active: wave 3)",
    "confidence": "medium",
    "invalidation": {
      "type": "rule_break",
      "condition": "wave2_below_wave1_start",
      "price": 42150.0
    },
    "entryZone": {"low": 42800.0, "high": 43120.0, "trigger": "bullish_reclaim_after_pullback"},
    "slZone": {"low": 42080.0, "high": 42220.0, "basis": "structural_plus_atr"},
    "tpLadder": [
      {"name": "TP1", "low": 43800.0, "high": 44100.0, "confidence": "high"},
      {"name": "TP2", "low": 44750.0, "high": 45200.0, "confidence": "medium"},
      {"name": "TP3", "low": 46200.0, "high": 47000.0, "confidence": "low"}
    ],
    "evidence": {
      "rulesPass": true,
      "fibFit": "0.62 retrace in wave2",
      "channelFit": "wave4 near lower rail",
      "indicatorConfluence": ["ma_alignment", "rsi_recovery"]
    }
  },
  "alternateScenarios": [],
  "switchTriggers": [
    "close_below_42150_invalidates_primary",
    "triangle_breakout_upgrades_alternate"
  ],
  "analysisNotes": "Educational output only."
}
```

## Human-Readable Output Shape

1. Working count (primary + alternate)
2. Rule checks (pass/fail)
3. Entry/SL/TP zones
4. Invalidation and switch triggers
5. Confidence rationale
