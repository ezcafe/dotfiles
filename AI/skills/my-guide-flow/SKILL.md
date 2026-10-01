---
name: my-guide-flow
description: >-
  Teaches a topic over multiple sessions in a durable guide workspace under
  .my-docs/guide/{topic-slug}/. Builds mission, trusted resources, HTML lessons
  with shared assets, reference docs, glossary, and learning records; targets
  zone of proximal development and long-term retention (retrieval, spacing,
  interleaving). Use when the user says run my-guide-flow, teach me,
  guide me through, start a learning workspace, or wants a stateful lesson
  series grounded in primary sources.
disable-model-invocation: true
argument-hint: "What would you like to learn about?"
---

# my-guide-flow

Stateful teaching workflow adapted from
[mattpocock/skills · teach](https://github.com/mattpocock/skills/tree/main/skills/productivity/teach).
Does not ship product code. Artifacts live under `.my-docs/guide/`, not the cwd root.

**Details:** [stages.md](stages.md) · formats below

## Package files

| File | Role |
|------|------|
| [SKILL.md](SKILL.md) | Rules, philosophy, workspace layout |
| [stages.md](stages.md) | Step order: Mission → Resources → Lesson loop |
| [MISSION-FORMAT.md](MISSION-FORMAT.md) | `MISSION.md` template |
| [RESOURCES-FORMAT.md](RESOURCES-FORMAT.md) | `RESOURCES.md` template |
| [LEARNING-RECORD-FORMAT.md](LEARNING-RECORD-FORMAT.md) | `learning-records/` template |
| [GLOSSARY-FORMAT.md](GLOSSARY-FORMAT.md) | `reference/glossary` / `GLOSSARY.md` template |

## When to run

- `run my-guide-flow`, `teach me`, `guide me through`, `start a learning workspace`
- Resume: workspace already has `MISSION.md` → continue from [stages.md](stages.md) next incomplete step
- Topic argument: use `{topic}` / argument-hint to pick or create `{topic-slug}`

## Guide workspace root

```text
.my-docs/guide/{topic-slug}/
```

**Slug rules:** lowercase, hyphens, short (e.g. `swift-concurrency`, `cloudkit-offline`). One mission per slug. Unrelated topics → new slug.

**If missing:** create the directory tree lazily as stages need files. Do **not** put guide state in the repo root or inside app source trees.

### Files in the workspace

| Path | Role |
|------|------|
| `00-run.md` | Run card: topic, slug, Last stage, Notes |
| `MISSION.md` | Why they learn — grounds every lesson ([MISSION-FORMAT.md](MISSION-FORMAT.md)) |
| `RESOURCES.md` | High-trust knowledge + communities ([RESOURCES-FORMAT.md](RESOURCES-FORMAT.md)) |
| `NOTES.md` | Teaching preferences / scratchpad |
| `GLOSSARY.md` | Canonical terms once understood ([GLOSSARY-FORMAT.md](GLOSSARY-FORMAT.md)) |
| `learning-records/NNNN-slug.md` | Decision-grade insights (ZPD) ([LEARNING-RECORD-FORMAT.md](LEARNING-RECORD-FORMAT.md)) |
| `lessons/NNNN-slug.html` | One short self-contained lesson each |
| `reference/*.html` | Cheat sheets / algorithms / compressed units for revisit |
| `assets/*` | Shared CSS, quiz widgets, diagrams — reuse by default |

## Philosophy

Deep learning needs:

1. **Knowledge** — from high-trust resources in `RESOURCES.md` (never trust parametric memory alone)
2. **Skills** — interactive lessons with tight feedback loops
3. **Wisdom** — real practice with people/communities (when the user allows)

### Fluency vs storage strength

- **Fluency:** in-the-moment recall (can feel like mastery)
- **Storage strength:** long-term retention — the real goal

Prefer desirable difficulty: retrieval practice, spacing, interleaving (skills practice only).

Before `RESOURCES.md` is solid, prioritize finding primary sources. Cite claims in lessons.

## Mission first

If `MISSION.md` is empty or vague, interview for Why / Success / Constraints / Out of scope before teaching. Confirm with the user before changing an existing mission; then add a learning record.

## Zone of proximal development (ZPD)

Each lesson should challenge “just enough.”

If the user did not name the next topic:

1. Read `learning-records/` + `MISSION.md` + `NOTES.md`
2. Pick the most mission-relevant thing still in ZPD
3. Prefer one tangible win per lesson

## Lessons

Primary teaching unit: one HTML file in `lessons/`, numbered `0001-slug.html`, then increment.

**Requirements:**

- Short; completable quickly; one tightly scoped win tied to the mission
- Beautiful, print-friendly typography (Tufte-leaning); shared stylesheet from `assets/`
- Link via anchors to other lessons and `reference/` docs
- Recommend one primary source (highest-trust resource found)
- Remind the user they can ask follow-up questions to the agent (teacher)
- Open the lesson for the user when a sensible CLI exists (`open path` on macOS)

**Build order inside a lesson:** teach only the knowledge needed for the skill → practice via interactive feedback (quiz / guided steps). For quizzes: equal word/character length per choice so formatting does not leak the answer.

### Assets

Before authoring a lesson, read `assets/`. Reuse components. New reusable pieces go in `assets/` — do not inline duplicates. First reusable piece every workspace earns: a shared stylesheet linked by every lesson.

## Knowledge / skills / wisdom

| Mode | Difficulty | Agent focus |
|------|------------|-------------|
| Knowledge | Enemy (protect working memory) | Cite `RESOURCES.md`; explain only what the skill needs |
| Skills | Tool (effortful retrieval) | Quizzes, in-browser tasks, real-world step lists + immediate feedback |
| Wisdom | Delegate to community | Answer briefly, then point to high-reputation communities unless user opted out (record in `RESOURCES.md` / `NOTES.md`) |

## Reference documents

While writing lessons, also write `reference/*.html` (and keep `GLOSSARY.md` current). Lessons are rarely revisited; references are. Glossaries, once present, bind terminology in every lesson.

## Run card (`00-run.md`)

Create/update on every session:

```md
# Guide run: {Topic}

- **Slug:** {topic-slug}
- **Root:** `.my-docs/guide/{topic-slug}/`
- **Last stage:** Mission | Resources | Lesson | Reference | Record
- **Notes:** {preferences, community opt-out, blockers}
```

## Decision options

When 2+ teaching paths exist (next lesson topic, resource set, community), present Decision N with What / Example / Pros / Cons / Recommendation. Prefer user-first picks when auto-settling.

## Plain language

Simple words in chat and all guide docs. Short paragraphs. Bold lead labels on bullets when scannable lists help.

## Do not

- Put guide artifacts outside `.my-docs/guide/{topic-slug}/`
- Teach from parametric knowledge when primary sources are missing
- Write long lessons that overload working memory
- Log every session as a learning record (records = decision-grade only)
- Change `MISSION.md` without user confirmation
- Ship product/feature code under this skill

## Source

Upstream behavior and formats adapted from
[teach](https://github.com/mattpocock/skills/tree/main/skills/productivity/teach)
(MISSION / RESOURCES / LEARNING-RECORD / GLOSSARY formats included in this package).
