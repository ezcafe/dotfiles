---
name: code-review-and-quality
description: >-
  Conducts multi-axis code review before merge. Use when reviewing PRs or
  local changes written by you, another agent, or a human. Use when assessing
  correctness, security, architecture, readability, and performance.
---

# Code Review and Quality

Cursor-optimized adaptation of [addyosmani/agent-skills code-review-and-quality](https://github.com/addyosmani/agent-skills/tree/main/skills/code-review-and-quality). Approve when the change improves code health and fits project conventions — not only when it matches how you would have written it.

## Project first

Read `AGENTS.md` / `CLAUDE.md` and neighboring patterns. Flag deviations from project style as Required when they matter; Nit when preference-only.

## Boundaries

| Tier | Rule |
|------|------|
| **Always** | Review tests and intent before nitpicking style. Label severity. Lead with correctness and security. |
| **Ask first** | Delete listed dead code; bulk dependency bumps; merge despite open Critical items. |
| **Never** | Rubber-stamp LGTM. Accept “fix later” for known issues. Run `npm audit fix --force` (or equivalent). |

## Five axes (order)

1. **Correctness** — Matches spec? Edges and errors? Tests test the right thing? Races / off-by-one?
2. **Security** — Input bounds, authz, injection, secrets, untrusted externals. Deep dive → [security-and-hardening](../security-and-hardening/SKILL.md)
3. **Architecture** — Fits patterns? Boundaries clear? Complexity reduced or only moved? Feature logic out of shared modules?
4. **Readability** — Names, control flow, earned abstractions, no bolted conditionals on unrelated paths
5. **Performance** — N+1, unbounded fetch, missing pagination, hot-path waste. Deep dive → [performance-optimization](../performance-optimization/SKILL.md)

## Process

### 1. Context

What should change? Which spec/task? Expected behavior delta?

### 2. Tests first

Exist? Behavior over implementation? Edges? Would they catch a regression?

### 3. Implementation walk

Per file: five axes above. Prefer named structural remedies (see [reference.md](reference.md)).

### 4. Label findings

| Label | Meaning |
|-------|---------|
| **Critical:** | Blocks merge (vuln, data loss, broken behavior) |
| *(no prefix)* / **Required** | Must fix or explicitly defer with reason |
| **Optional:** / **Consider:** | Suggestion |
| **Nit:** | Style; author may ignore |
| **FYI** | Context only |

Order: Critical/Required → structure → nits.

### 5. Verification story

What was run (tests, build, manual, screenshots)? Trust green CI only as necessary, not sufficient.

## Size guidance

| Diff | Bar |
|------|-----|
| ~100 lines | Ideal |
| ~300 lines | OK if one logical change |
| ~1000+ lines | Ask to split |

Watch **file** size too: growing an already huge file without extraction is a structural finding. Separate refactor PRs from feature PRs.

## Dead code

List unreachable/unused items explicitly, then **ask** before deleting.

## Dependencies

Before adding: existing stack? Size? Maintained? Known vulns? License?

Upgrades: changelog (not just semver); prefer one package per change; review lockfile diff; never hand-edit lockfile; no force-audit. Triage → [security-and-hardening](../security-and-hardening/SKILL.md).

## Honesty

Do not soften production bugs. Quantify when possible. Push back on bad approaches; defer gracefully when the author has fuller context. Comment on code, not people.

## Checklist

Copy into the review reply:

```markdown
## Review: [title]
- [ ] Context understood
- [ ] Correctness + tests adequate
- [ ] Security (secrets, bounds, authz, injection)
- [ ] Architecture (patterns, size, no complexity relocate)
- [ ] Readability
- [ ] Performance (N+1, bounds, pagination)
- [ ] Deps/lockfile if touched
- [ ] Verdict: Approve | Request changes
```

## Related

- [reference.md](reference.md) — remedies, anti-rationalizations
- [code-simplification](../code-simplification/SKILL.md)
