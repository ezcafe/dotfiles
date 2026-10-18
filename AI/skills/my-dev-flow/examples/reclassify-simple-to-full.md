# Golden path — mid-run reclassify simple → full

Short recovery. Parent follows [step-0.md](../step-0.md) Mid-run reclassify + [invariants.md](../invariants.md). Drop skip-review when contracts appear ([lenses.md](../lenses.md)).

## Ask started as

> Tiny copy tweak on settings label.

## What changed mid-run

Design discovers a new public route + persistence. Has API → **yes**, Has DB → **yes**.

## Parent actions

1. Pause; **Decision N** (reclassify): Stay simple · Upgrade to **full** · New slug/stop.
2. Prefer Option **Upgrade to full**.
3. Set Mode **full**; Review profile **full** or **lite** (never keep **skip-review**).
4. Notes: `reclassify simple→full — API+DB appeared`; clear skip-review if set.
5. Resume Full pipeline from incomplete step (usually Analyze/Design → design-review with Pending parallel `api|db` when both yes).
6. Gate B → **blocking** ([hitl.md](../hitl.md) Default Gate B narrow async — Mode full never async-notify default).

## Do not

- Keep Mode simple + skip-review after Has API/DB yes
- Invent Ideation redo unless Decision N / Fix ask requires it
