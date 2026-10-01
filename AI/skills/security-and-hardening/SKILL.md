---
name: security-and-hardening
description: >-
  Hardens code against vulnerabilities and supply-chain risk. Use when handling
  user input, auth, sessions, file uploads, webhooks, PII, payments, dependency
  audits, or LLM/tool features. Use when auditing or changing security-sensitive
  surfaces.
---

# Security and Hardening

Cursor-optimized adaptation of [addyosmani/agent-skills security-and-hardening](https://github.com/addyosmani/agent-skills/tree/main/skills/security-and-hardening). Treat external input as hostile, secrets as sacred, and authz as mandatory.

## Project first

Follow existing auth, cookie, and header patterns in the repo. Prefer project primitives over new ad-hoc security middleware.

## Boundaries

| Tier | Rule |
|------|------|
| **Always** | Validate at edges. Parameterize queries. Encode output. HTTPS externally. Hash passwords (argon2/scrypt/bcrypt). httpOnly + secure + sameSite session cookies. Run package-manager audit against the lockfile before release. |
| **Ask first** | New/changed auth flows; storing new PII/payment categories; new external integrations; CORS changes; file uploads; rate-limit changes; elevated roles; destructive FS cleanup logic. |
| **Never** | Commit or log secrets. Trust client-only validation. Disable security headers for convenience. `eval` / `innerHTML` with untrusted data. Auth tokens in `localStorage`. Expose stack traces to clients. `npm audit fix --force` (or equivalent) without human review. |

## Threat model (5 minutes)

1. **Trust boundaries** — HTTP, forms, uploads, webhooks, third-party APIs, queues, LLM output, paths/env from other processes. Trust follows who *wrote* the value.
2. **Assets** — Credentials, PII, payments, admin actions, money movement.
3. **STRIDE lens** — Spoofing, Tampering, Repudiation, Info disclosure, DoS, Elevation.
4. **Abuse cases** — Write “how would I misuse this?” next to the happy path; test those first.

If you cannot name boundaries, you are not ready to harden (insecure design).

## Priority controls

- **Injection** — Parameterized SQL/ORM only; never shell with user strings
- **Authn** — Strong password hash; session cookies hardened; rate-limit login
- **Authz** — Check ownership/role on every mutating and sensitive read
- **XSS** — Framework escaping; sanitize only if HTML is required
- **SSRF** — Allowlist host + https; reject private/reserved IPs; `redirect: 'error'`; know DNS rebinding TOCTOU (pin IP or filtering agent for high risk)
- **Config** — Helmet/CSP/HSTS/frame/options; CORS allowlist (no `*`)
- **Secrets** — Env only; `.env` gitignored; rotate if ever committed
- **Uploads** — Type allowlist, size cap, prefer magic-byte checks
- **Destructive paths** — After symlink resolve: under allowlisted root, ≥1 level below root, ownership evidence *before* delete; no fallback to a wider path
- **Rate limits** — Shared store if >1 process (Redis/HTTP limiter); memory counters fail open under scale
- **Supply chain** — One lockfile; frozen install in CI; block install scripts until approved; triage audit by reachability; review new deps + lockfile + script policy together
- **Privacy** — Minimize PII; purpose + retention + real deletion path; consent before vendor share
- **LLM** — Model output = untrusted (no eval/SQL/shell/innerHTML/paths); permissions in code not prompts; no secrets/cross-tenant data in context; constrain tools; cap tokens/loops; partition RAG per tenant

Patterns: [reference.md](reference.md).

## OWASP Top 10 (required in design + code security review)

Use the current [OWASP Top 10](https://owasp.org/www-project-top-ten/) categories. For each **relevant** item, say pass / fail / N/A with one plain-words note. Do not skip a category silently — mark N/A when the change cannot hit it.

| ID | Name | Look for |
|----|------|----------|
| **A01** | Broken Access Control | Missing ownership/role checks; IDOR; privilege escalation; workspace/tenant bleed |
| **A02** | Cryptographic Failures | Secrets in logs/client; weak hashing; sensitive data in URLs; cleartext at rest/transit when it must be protected |
| **A03** | Injection | SQL/ORM raw concat; command/shell; XSS via unescaped HTML; LDAP/NoSQL injection |
| **A04** | Insecure Design | No threat model; trust client-only rules; missing rate limits / abuse cases; unsafe defaults |
| **A05** | Security Misconfiguration | Open CORS `*`; missing security headers; verbose errors to clients; debug left on |
| **A06** | Vulnerable Components | New deps without triage; known CVEs in reach; unreviewed install scripts |
| **A07** | Auth Failures | Weak session cookies; credential stuffing gaps; broken logout; predictable tokens |
| **A08** | Software / Data Integrity | Unsigned webhooks; unsafe deserialization; CI/CD tamper; integrity of updates |
| **A09** | Logging / Monitoring Failures | No audit for sensitive actions; secrets in logs; no alert path for authz failures |
| **A10** | SSRF | Server fetch of user URLs; missing host allowlist; private IP / redirect abuse |

Primary source: https://owasp.org/Top10/

## Checklist

```markdown
### OWASP Top 10 (relevant items)
- [ ] A01 Broken Access Control
- [ ] A02 Cryptographic Failures
- [ ] A03 Injection
- [ ] A04 Insecure Design
- [ ] A05 Security Misconfiguration
- [ ] A06 Vulnerable Components
- [ ] A07 Auth Failures
- [ ] A08 Software / Data Integrity
- [ ] A09 Logging / Monitoring Failures
- [ ] A10 SSRF

### Authn / Authz
- [ ] Passwords hashed (salt rounds ≥ 12 for bcrypt if used)
- [ ] Session cookies httpOnly, secure, sameSite
- [ ] Login rate-limited (shared store if multi-instance)
- [ ] Every sensitive endpoint checks permission + ownership

### Input / Output
- [ ] Boundary validation
- [ ] Parameterized queries
- [ ] Encoded HTML output
- [ ] SSRF allowlist on server-side fetches
- [ ] Destructive FS targets: root + depth + ownership

### Data
- [ ] No secrets in repo or logs
- [ ] Sensitive fields stripped from API responses
- [ ] PII classified, minimized, retention + delete path

### Supply chain / AI
- [ ] Audit triaged; no unreviewed install scripts
- [ ] LLM output validated/encoded; tools scoped
```

## Related

- [reference.md](reference.md) — BAD/GOOD snippets, audit triage, LLM checks
- Review gate: [code-review-and-quality](../code-review-and-quality/SKILL.md)
- API contracts: [api-and-interface-design](../api-and-interface-design/SKILL.md)
- Design + code security reviews in my-plan-flow must use the OWASP table above
