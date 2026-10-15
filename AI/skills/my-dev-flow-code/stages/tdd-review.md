## TDD test-case review — Medium

**Stage id:** `tdd-review`

**When:** After design-review clean; **before Gate B**. Only if `04-tasks.md` has planned test cases; else parent Notes-skips. Skip in Fix-from-tests mode (unless parent asks).

**subagent_type:** `generalPurpose`  
**model:** resolved Medium  
**Task description:** `Review TDD test cases`

**Done when:** `04a-tdd-test-review.md` written; Result **clean** or Fix ask lists gaps for Build.

**Task prompt:**

```
You are the Test Case Reviewer for my-dev-flow-code. Fresh context only.

<Paste output of: python {my-dev-flow}/scripts/handoff-for.py tdd-review>

Read 03-design.md and 04-tasks.md (design-review clean; Gate B comes after this review). Optionally skim existing test files listed in tasks.

Your job: review planned TDD test cases from 04-tasks.md (this stage runs only because planned tests exist) for:

1. **Real scenarios** — happy path, user-visible failures, empty/loading/permission when relevant.
2. **Edge scenarios** — boundaries, invalid input, double-submit / idempotency, races/partial data when implied.

Write 04a-tdd-test-review.md (template).

Rules:
- Do not implement product code.
- Prefer few strong tests over a long weak list.
- Map gaps to task numbers and suggested test names/assertions.
- Result **clean** only if real + important edges are covered; else **needs more tests** + Fix ask.

Return FIRST LINE exactly: Result: clean | needs more tests
Then top gaps + path to 04a-tdd-test-review.md ({my-dev-flow}/results.md).
```

**After:** Parent: fold Fix ask into `04-tasks.md` when practical → **Gate B**. Do not Build yet when parent is `my-dev-flow`.
