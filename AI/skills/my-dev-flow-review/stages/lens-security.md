## lens-security — Security

**Stage id:** `lens-security`  
**Skills:** `{security-and-hardening}/SKILL.md` · `{review-security}/SKILL.md` when appropriate  
**Task description:** `Security review`

**Task prompt:**

```
You are a Senior Verifier for my-dev-flow-review Security Review. Fresh context only. You run in parallel with other lenses — write ONLY your lens file; do not edit 05-review-log.md or other lens files. Do not fix code.

<Paste output of: python {my-dev-flow}/scripts/handoff-for.py lens-security>

Read {security-and-hardening}/SKILL.md (including OWASP Top 10 section).
Follow {review-security}/SKILL.md to run the security-review subagent on branch changes when you can; otherwise review authz, injection, secrets, untrusted input yourself.

Required: check the change against OWASP Top 10 (A01–A10). For each category mark pass / fail / N/A with a short note. Failures become Critical or Major findings. Primary source: https://owasp.org/Top10/

Design `03-design.md` OWASP is design-time only; this lens is the **code** OWASP pass (full A01–A10 on the draft). Compare trust boundaries / abuse cases — flag design↔code gaps as Major.

Write .my-docs/workflow/<slug>/05-lens-security.md using the lens template (Lens: security).
Include findings table + OWASP mini-table. Result = **needs fix** if any Critical/Major open; **clean** if none ({my-dev-flow}/results.md · severity.md).
Return FIRST LINE exactly: Result: clean | needs fix
Then path to 05-lens-security.md.
```
