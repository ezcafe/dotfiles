# Models + usage-limit

Resolve from the **current Task model allowlist** (allowlist wins over soft hints).

| Tier | Used by | Pick |
|------|---------|------|
| **High** | Analyze; Design; Update; simple `design-phase` | High → Medium → Fast → `inherit` |
| **Medium** | Ideation; Mode full judgment (incl. Grill) | Medium → Fast → `inherit` |
| **Fast** | Build/Fix/Smoke/Test/Merge; Mode simple mechanical + lite review | Fast → `inherit` |

**Soft hints** (if in allowlist): High `claude-sonnet-5-5-high` / `claude-fable-5-1-thinking-high`; Medium `claude-opus-5-5-medium`; Fast `composer-2.5-fast`.

**Fast-on-simple:** Mode simple prefers Fast for mechanical + lite review.

## Usage-limit

1. Wait 5s → retry once same model.
2. Still limited → retry once with `inherit`.
3. Still fails → main-thread for **that stage only**; continue Tasks for later stages.
4. Log each fallback on Run log. ≥3 main-thread fallbacks → Decision N ([decisions.md](decisions.md)).
