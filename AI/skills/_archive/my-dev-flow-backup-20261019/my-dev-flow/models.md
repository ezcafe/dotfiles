# Models + usage-limit

Canonical model resolution for [`my-dev-flow`](SKILL.md).  
**This file is SoT for:** model tiers + usage-limit fallback.  
Pipeline order: [stages.md](stages.md).

## Resolve once

Resolve from the **current Task model allowlist** (not a frozen hardcoded list). Soft preferred hints may go stale — allowlist wins.

| Tier | Used by | How to pick from allowlist |
|------|---------|----------------------------|
| **High** | Analyze; Design; Update from design review; **simple** `design-phase` | First slug matching high/thinking-high preference; else any High-tier; else Medium → Fast → `inherit` |
| **Medium** | Ideation; Mode **full** judgment stages when available | First Medium-tier slug; else Fast → `inherit` |
| **Fast** | Build/Fix/Smoke/Test/Merge; **Mode simple** mechanical + lite review; mechanical when Medium missing | First Fast-tier slug (hint: `composer-2.5-fast` if listed); else `inherit` |

**Soft preferred hints** (use only when present in allowlist): High `claude-sonnet-5-5-high` → `claude-fable-5-1-thinking-high`; Medium `claude-opus-5-5-medium`; Fast `composer-2.5-fast`.

**Mechanical stages:** Gate A, skim, grill, design-review, design-verify-phase, API/DB contract review, TDD review, Adversarial, Quality, Lite combined / code-review-phase, lenses, Merge findings.

**Fast-on-simple:** When Mode is **simple**, mechanical stages and lite review **prefer Fast** even if Medium is on the allowlist (cut latency). Mode **full** still prefers Medium for those stages when available; use Fast only when Medium is missing.

At start: resolve once; write slugs into `00-run.md`; note fallbacks. Re-resolve if allowlist changes mid-run. Only ask user if **no** Task can launch.

## Usage-limit fallback (per stage)

When a Task hits a usage limit / rate limit / quota / capacity error:

1. Do **not** stop the pipeline.
2. Wait **5 seconds** → retry **once** same model. Log `usage-limit retry — <stage> — waited 5s`.
3. If still limited → retry **once** with model **`inherit`** (same prompt/description). Log `usage-limit retry — <stage> — inherit model`.
4. If inherit succeeds → continue; later stages use resolved tier models again.
5. If inherit still fails → **main-thread** for **that stage only**. Log `main-thread fallback — <stage> — usage limit after inherit`.
6. Next stages still launch as Tasks. Do not permanently disable subagents.
