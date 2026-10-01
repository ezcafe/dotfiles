# Code review reference

## Structural remedies (propose the move)

- Replace long conditional chains with a typed model or dispatcher
- Collapse duplicate branches into one flow
- Separate orchestration from business logic
- Move feature-specific logic out of shared modules
- Reuse the canonical helper instead of a near-duplicate
- Make type boundaries explicit so downstream branching disappears
- Delete pass-through wrappers that add no API clarity
- Extract helpers or split oversized files

Prefer remedies that **remove** concepts a reader must hold, not relocate them.

## Change description bar

**First line:** Short imperative (“Delete the FizzBuzz RPC”).

**Body:** Why, decisions, links to bugs/benchmarks/docs. Acknowledge known shortcomings.

**Anti-patterns:** “Fix bug”, “Phase 1”, “Moving code from A to B” with no why.

## Multi-model pattern (optional)

```
Model A implements → Model B reviews correctness/architecture
  → A addresses → Human final call
```

Example review prompt:

> Review this change for correctness, security, and project conventions. Spec: [X]. Expected: [Y]. Label Critical / Required / Optional / Nit.

## Dependency upgrade checklist

1. Read changelog / migration notes
2. One package (or small related group) per change
3. Tests green before and after
4. Review lockfile transitive diff
5. Commit lockfile; never hand-edit

## Common rationalizations

| Claim | Reality |
|-------|---------|
| “It works” | Unreadable / insecure / wrong architecture still ships debt |
| “I wrote it” | Authors miss their own assumptions |
| “Clean up later” | Later rarely comes — gate at review |
| “AI code is fine” | Needs more scrutiny, not less |
| “Tests pass” | Necessary, not sufficient |
| “Refactor is cleaner” | Relocating complexity ≠ reducing it |
| “Just a version bump” | Behavior change you did not write — read the changelog |
| “Bump everything in one PR” | Hides which package broke the build |

## Presumptive structural blockers

Escalate to Required when the change makes structure worse:

- Refactor that relocates complexity without reducing concept count
- Grows a large file with no decomposition plan
- Feature logic dumped into a shared module
- Near-duplicate of an existing canonical helper
- Silent fallback hiding an unclear invariant
