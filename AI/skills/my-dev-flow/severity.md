# Severity exit (canonical)

All my-dev-flow subflows use this rule unless a stage says otherwise.

## Severities

| Level | Blocks **clean**? |
|-------|-------------------|
| **Critical** | Yes |
| **Major** | Yes |
| **Enhancement** | No — log and defer (see below) |
| **Nit / FYI** | No |

## Clean

**Clean** = zero open **Critical** and **Major** for that stage or round.

Enhancements and nits do **not** block clean. List them in the findings table and copy must-fix items into **Deferred** (in `03a`, `05-review-log`, or `00-run.md` Notes) when not fixing this round.

## Fix ask

Fix ask bullets include **Critical** and **Major** only (≤ cap in handoffs.md). Optional: one line “Deferred Enhancements: …” in Notes.

## Review profile

| Profile | Code review |
|---------|-------------|
| **full** | Adversarial → Quality → lenses → test |
| **lite** | Same sequence; parent **may** use one combined Task (`Lite combined review`) instead of separate Adversarial + Quality when Mode simple and Lens plan is none or single lens |
| **skip-review** | Skip this subflow entirely after smoke-pass |
