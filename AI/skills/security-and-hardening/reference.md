# Security reference

Copy **GOOD** patterns only. BAD blocks are anti-examples.

## SQL

```typescript
// BAD
const query = `SELECT * FROM users WHERE id = '${userId}'`;

// GOOD
const user = await db.query('SELECT * FROM users WHERE id = $1', [userId]);
```

## XSS

```typescript
// BAD
element.innerHTML = userInput;

// GOOD — framework text binding (e.g. React children)
return <div>{userInput}</div>;

// GOOD — if HTML required
const clean = DOMPurify.sanitize(userInput);
```

## Authz

```typescript
// Always check resource ownership after authenticate
if (task.ownerId !== req.user.id) {
  return res.status(403).json({
    error: { code: 'FORBIDDEN', message: 'Not authorized' },
  });
}
```

## SSRF sketch (GOOD direction)

```typescript
// Allowlist host + https only; resolve ALL addrs; reject non-unicast;
// fetch with redirect: 'error'. For high risk: pin IP or use an SSRF filter
// agent — DNS can rebind between check and connect (TOCTOU).
```

## File upload

```typescript
const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/webp'];
const MAX_SIZE = 5 * 1024 * 1024;

// Reject non-allowlisted mimetype and oversize; verify magic bytes when critical
```

## Rate limit (multi-instance)

Prefer Redis / HTTP-based limiter shared across instances. In-process counters under-count behind a load balancer.

## Secrets layout

```
.env.example  → commit (placeholders)
.env          → never commit
.gitignore    → .env, .env.local, *.pem, *.key
```

If a secret hits a remote: **rotate first**, then purge history.

## Audit triage

```
critical/high + reachable → fix now (update/patch/replace)
critical/high + unused across runtime/build/test/deploy → fix soon; document
moderate + prod reachable → next release
moderate + dev-only → backlog
low → regular update cycle
```

Never treat “audit clean” as “package is trustworthy.”

## LLM output (GOOD direction)

```typescript
// BAD: db.query(await llm.generate(`SQL for: ${userQuestion}`))
// BAD: el.innerHTML = await llm.reply(msg)

// GOOD: parse → schema-validate → allowlisted action / textContent only
const intent = CommandSchema.parse(JSON.parse(await llm.replyJson(msg)));
await runAllowlistedAction(intent.action, intent.params);
```

## Destructive path ops

Before delete/move/overwrite of a derived path:

1. Resolve symlinks
2. Target under allowlisted root
3. At least one directory below that root
4. Ownership/authorization evidence read *before* the op
5. On refusal: log and stop — never widen the path

## Privacy classes

| Class | Handle |
|-------|--------|
| Non-personal | Normal |
| PII | Minimize, ACL, include in export/delete |
| Sensitive (health/finance/minors/…) | Stricter basis, encryption/audit often required |
