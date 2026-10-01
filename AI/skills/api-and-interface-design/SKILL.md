---
name: api-and-interface-design
description: >-
  Designs stable APIs and module boundaries that are hard to misuse. Use when
  creating REST endpoints, type contracts between modules, GraphQL schemas, or
  frontend/backend interfaces. Use when changing public interfaces.
---

# API and Interface Design

Cursor-optimized adaptation of [addyosmani/agent-skills api-and-interface-design](https://github.com/addyosmani/agent-skills/tree/main/skills/api-and-interface-design). Make the right thing easy and the wrong thing hard.

## Project first

Follow `AGENTS.md` / existing route and error patterns in the repo before inventing a new shape.

## Boundaries

| Tier | Rule |
|------|------|
| **Always** | Define contract (types/schemas) before implementation. One error shape. Validate at system edges only. |
| **Ask first** | Breaking field changes; new auth surfaces; changing CORS; public API versioning strategy. |
| **Never** | Leak internals in errors. Mix null / throw / `{ error }` styles. Accept `Idempotency-Key` without honouring it. |

## Core rules

1. **Contract first** — Typed input/output before code. Separate create-input from full entity (server fields on output only).
2. **Hyrum’s Law** — Observable behavior becomes a contract. Be intentional about what you expose.
3. **One-version rule** — Prefer extend-in-place over parallel API versions.
4. **Addition over modification** — New fields optional; do not remove or retype existing fields without a migration plan.
5. **Predictable naming** — Plural nouns for REST resources; camelCase fields/params; `is`/`has`/`can` for booleans.

## Workflow

### 1. Write the contract

Define operations, inputs, outputs, and failure modes in types or OpenAPI-equivalent. Prefer discriminated unions for status variants.

### 2. Errors (one strategy)

REST default:

- `400` bad request shape
- `401` unauthenticated
- `403` authenticated but forbidden
- `404` missing
- `409` conflict / in-flight duplicate
- `422` validation failed
- `500` server (no stack traces to clients)

Stable body: `{ error: { code, message, details? } }`. See [reference.md](reference.md).

### 3. Validate at boundaries

Validate: route bodies/params, forms, third-party responses, env config.

Do **not** re-validate between trusted internal functions that already share types.

Treat third-party and LLM output as untrusted (see [security-and-hardening](../security-and-hardening/SKILL.md)).

### 4. Lists

Paginate from day one (`page` / `pageSize` or cursor). Filter via query params. Prefer `PATCH` for partial updates.

### 5. Idempotency (state-changing)

If you accept `Idempotency-Key`:

- Key from client or immutable intent id — never regenerate per retry
- Claim with one atomic insert + unique constraint (no check-then-act)
- Same key + different body → fail loudly (`422`)
- In-flight duplicate → default **`409`** (or wait / `202` if product requires it)
- Retention ≥ longest retry / DLQ path

Details: [reference.md](reference.md).

## Checklist

- [ ] Typed input and output for every endpoint / public function
- [ ] Single error format
- [ ] Validation only at edges
- [ ] List endpoints paginated
- [ ] New fields additive
- [ ] Naming consistent with the project
- [ ] Mutating endpoints: idempotent or documented unsafe-to-retry

## Related

- Hardening patterns: [security-and-hardening](../security-and-hardening/SKILL.md)
- Examples and pitfalls: [reference.md](reference.md)
