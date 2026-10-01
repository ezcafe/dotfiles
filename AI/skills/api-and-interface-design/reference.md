# API design reference

BAD/GOOD examples for agents. Prefer copying **GOOD** only.

## Error body

```typescript
interface APIError {
  error: {
    code: string;      // e.g. VALIDATION_ERROR
    message: string;   // human-readable
    details?: unknown;
  };
}
```

## Contract sketch

```typescript
interface TaskAPI {
  createTask(input: CreateTaskInput): Promise<Task>;
  listTasks(params: ListTasksParams): Promise<PaginatedResult<Task>>;
  getTask(id: string): Promise<Task>; // throws NotFoundError
  updateTask(id: string, input: UpdateTaskInput): Promise<Task>;
  deleteTask(id: string): Promise<void>; // idempotent
}

interface CreateTaskInput {
  title: string;
  description?: string;
}

interface Task {
  id: string;
  title: string;
  description: string | null;
  createdAt: Date;
  updatedAt: Date;
}
```

## Pagination response

```json
{
  "data": [],
  "pagination": {
    "page": 1,
    "pageSize": 20,
    "totalItems": 142,
    "totalPages": 8
  }
}
```

## Idempotency pitfalls

| BAD key / pattern | Why |
|-------------------|-----|
| `crypto.randomUUID()` per attempt | Every retry is a new intent |
| `` `${userId}:${amount}` `` | Collapses distinct legitimate charges |
| `` `${orderId}:${Date.now()}` `` | Timestamp ≈ random |
| Check exists then insert | Race under concurrent retries |
| Replay first response when body hash differs | Silent wrong outcome |
| TTL shorter than DLQ replay window | Duplicate after “expiry” |

### Atomic claim (GOOD idea)

```typescript
// Claim with unique constraint; on conflict → replay or 409
try {
  await db.insert({ key, state: 'in_progress', requestHash });
} catch (e) {
  if (isUniqueViolation(e)) return replayOrReject(key);
  throw e;
}
```

### Payload guard (GOOD idea)

```typescript
if (existing.requestHash !== hash(req.body)) {
  // 422 — key reused with different payload
}
```

## Discriminated status (GOOD)

```typescript
type TaskStatus =
  | { type: 'pending' }
  | { type: 'in_progress'; assignee: string; startedAt: Date }
  | { type: 'completed'; completedAt: Date }
  | { type: 'cancelled'; reason: string };
```

## Optional branded IDs

```typescript
type TaskId = string & { readonly __brand: 'TaskId' };
type UserId = string & { readonly __brand: 'UserId' };
```

Use only if the project already uses branded IDs — do not introduce a second ID style.
