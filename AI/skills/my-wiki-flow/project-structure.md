# Canonical project structure

Every project under `projects/{slug}/` uses the pages below. Distill from **real
code** (sources, handlers, schemas, build/run config, tests) — **not** from
README/docs/ADRs. Repo Markdown is a pointer only; confirm every claim in code
at the validation SHA.

Aligned with [ADS](https://archstandard.org/v1/standard/overview/) and
[Google tech writing — large docs](https://developers.google.com/tech-writing/two/large-docs).
[Diátaxis](https://diataxis.fr/) informs optional **how-to** pages and
`entity_type` labels — this is **not** a four-quadrant Diátaxis site (see
[philosophy.md](philosophy.md)).

Frontmatter, lint rules, and Karpathy layers: [content-contract.md](content-contract.md).
Operations: [stages.md](stages.md).

```text
projects/{slug}/
  architecture.md          # 1. Architecture
  topic-index.md           # 2. Topic index (agent routing)
  solution-design.md       # 3. Solution design hub
  solution-design/         #    one page per feature
    {feature-slug}.md
  decisions.md             # 4. Decisions (judgment layer)
  glossary.md              # 5. Glossary
  how-to/                  #    optional ops / task guides
    {task-slug}.md
  references/              # overflow / prose fold-in (article.template.md)

concepts/                  # cross-project evergreen notes (optional)
  {concept-slug}.md
  topic-index.md           # optional vault-wide concept map
```

Scaffold: `wiki-scaffold-project.sh {slug} [workspace]`  
Feature page: `wiki-add-feature.sh {slug} {feature} [master-feature]`  
How-to: `wiki-add-howto.sh {slug} {task-slug}`  
Concept: `wiki-add-concept.sh {concept-slug}`

## Page roles and required sections

Agents **must** use these H2 headings (exact titles). Do not invent alternate top-level names.

### 1. Architecture — `architecture.md`

Project-wide only. **No** feature sequence diagrams.

| Section | Content |
|---------|---------|
| Purpose and quality goals | Boundaries + top quality goals (metric/signal + `workspace:` source) |
| Building block view | Mermaid **`C4Container`** (or **`C4Component`**) + responsibilities table |
| Interaction diagram | Mermaid **`C4Dynamic`** — 1–2 architecturally relevant scenarios |
| Communication and data | From/To/Protocol/Sync-async/Data owned (no diagram re-narration) |
| Cross-cutting concerns | Security, observability, errors, resilience (project-wide) |
| Deployment view | Environments; optional deployment Mermaid if >1 deployable |
| Risks and technical debt | Risk/debt, impact, mitigation, source |
| Key decisions and constraints | ADR-lite: Status (`proposed`/`accepted`/`superseded`/`deprecated`), Date, Summary, Consequences — **append-only**; supersede with a new row |
| Related solution designs | Links to feature pages |

### 2. Topic index — `topic-index.md`

Thin **topic → page** map. Agents load this before opening full pages.

| Section | Content |
|---------|---------|
| Topic map | GFM table: Topic \| Page (`[[wikilink]]`) \| Notes. Synonym rows OK. One row per confirmed feature. Include how-to and concept links when relevant. |

Keep short. No diagrams. No essay prose.

### 3. Solution design — hub + features

**Hub** (`solution-design.md`): master feature index (Owner + Status columns).
Optional frontmatter `nav_group:` / `master_feature:` groups features in the HTML sidebar.

**Feature page** — required H2s:

| Section | Content |
|---------|---------|
| Summary | Short problem/goal/owner/status (outcomes live under Business requirements) |
| Scope and requirements | **Business requirements** + in-scope/exclusions + **Given/When/Then** acceptance |
| Design overview | Affected components (table only) |
| Sequence diagram | Mermaid **`sequenceDiagram` only**; include `alt`/`opt` for a failure/edge path |
| API contracts | **Progressive:** Spec summary always (`Owns contract?` + `workspace:`). Full field tables + curl success/error only when Owns=`yes` (or shared + non-obvious). Arrays ≥1 item |
| Data and state changes | Entities, storage, migrations |
| Complex logic | Rules + `workspace:` + code fence; or `N/A` + `workspace:` cite |
| Failure and retry behavior | Timeouts, retries, idempotency; or `N/A` + cite |
| Cross-cutting deltas | Only deltas vs Architecture; or `N/A — inherits Architecture` |
| Testing and rollout | Separate lists: Key tests / Release / Rollback |
| Decisions and open questions | Decisions / open items |

Ops procedures that a competent person runs repeatedly belong in **`how-to/`**, not as a substitute for this design page. Link them from Topic index and from Testing and rollout when useful.

### 4. Decisions — `decisions.md`

Practitioner judgment layer (not ADR dump). Voice: **Use X when Y**.

| Section | Content |
|---------|---------|
| Decision rules | Rule / Use when / Avoid when / `workspace:` source |
| Anti-patterns | Anti-pattern / Why / Prefer instead / source |
| Trade-offs | Choice A / B / Pick A when / Pick B when / source |
| Related architecture decisions | Links to Architecture ADR-lite (do not duplicate full tables) |

Architecture owns Status/Date records. Decisions owns actionable rules. Both cite code.

### 5. Glossary — `glossary.md`

| Term | Definition | Related link |
|------|------------|--------------|
| … | Project-specific meaning | `[[wikilink]]` |

### 6. How-to — `how-to/{task}.md` (optional)

Task guides for competent operators (`entity_type: how-to`). One goal per page.

| Section | Content |
|---------|---------|
| Prerequisites | Tools, access, assumptions |
| Steps | Numbered procedure (no Architecture re-narration) |
| Verify | How to confirm success |
| Rollback | Optional; how to undo |
| Related | Links to Architecture / feature / Decisions |

Scaffold: `wiki-add-howto.sh {slug} {task}`. Add a Topic map row.

### 7. Concepts — `concepts/{slug}.md` (optional, vault-wide)

Cross-project evergreen notes (`entity_type: explanation` or `reference`).
One idea per page. Dense wikilinks to projects that apply the concept.

| Section | Content |
|---------|---------|
| Definition | What it means in *your* practice |
| When to use | Short rules |
| Related projects | Links into Architecture / Decisions / features |
| Key claims | Prefer `confidence: high` with `workspace:`; else `confidence: low` + source |

Optional `concepts/topic-index.md` Topic map for vault-wide routing.
Set `reviewed:` on distill/fold-in; lint warns after 90 days.
Scaffold: `wiki-add-concept.sh {concept-slug}`.

## Feature discovery (before writing feature pages)

Do **not** invent dozens of shallow pages. Propose a list, then **confirm with the user**.

**Candidate sources (code only):**

1. Top-level route / RPC / event handlers under `src/`, `app/`, `cmd/`, `internal/`.
2. Packages or modules with non-trivial branching (multiple call sites or tests).
3. Deployable services / workers named in compose, Helm, or CI.
4. User-named list (always allowed; overrides heuristics).

**Selection rules:**

| Include | Skip |
|---------|------|
| User-confirmed names | Pure CRUD with no branches |
| Handlers with complex logic / multi-step flows | Generated clients, fixtures |
| Cross-service orchestration | One-line wrappers |
| Cap default proposal at **8** features; ask to add more | Duplicate pages for the same flow |

After confirmation: `wiki-add-feature.sh` for each; fill from code; link from hub;
add Topic map rows on `topic-index.md`.

## Codebase validation (mandatory on distill / update)

1. Resolve workspace from `config.yaml` → `projects.{slug}.workspace`.
2. Inspect code: entrypoints, handlers, schemas-as-code, manifests/Makefile/CI, tests.
3. Do not treat README/`docs/**`/ADRs as source of truth.
4. Set `validated_against: workspace:{path}@{sha}` and `updated`.
5. Every Key claims bullet maps to a code path or runnable command (`confidence: high`), or is marked `confidence: low`.
6. If code and wiki disagree → update the wiki (or mark superseded).
7. Append `log.md`.

## Prose fold-in (code stays primary)

Books, Confluence, papers, brand docs under `raw/` or `inbox/`:

- Fold synthesized notes into `references/` (and optional Glossary / Decisions / concepts).
- Set `confidence: low` and `reviewed:` until code-confirmed.
- **Never** use prose alone as evidence for Architecture building blocks, Interaction
  diagrams, feature sequences, or high-confidence Key claims — confirm in code first.
- See [stages.md](stages.md) Stage 3e.

## Diagrams and tables

- Architecture building blocks: **`C4Container`** or **`C4Component`**.
- Architecture interaction: **`C4Dynamic`** (or flowchart with `C4Dynamic unavailable`).
- Features: **`sequenceDiagram` only** (prefer `alt`/`opt` for errors).
- How-tos: no required Mermaid.
- HTML Mermaid figures are zoomable (wheel / drag / toolbar).
- GFM tables → `.wiki-table` on build. No escaped `\|` in table wikilinks.

### C4 layout and color (required for Architecture)

Mermaid C4 packs **4 shapes per row by default**, which overlaps labels on Interaction diagrams.

1. Interaction (`C4Dynamic`): `UpdateLayoutConfig($c4ShapeInRow="1")` — one box per row (top → bottom).
2. Building blocks: `UpdateLayoutConfig($c4ShapeInRow="2"|`"3")` so boxes are not cramped.
3. Short edge labels; use `UpdateRelStyle(..., $offsetX, $offsetY)` when labels sit on boxes.
4. Colors: standard C4-PlantUML palette (Person `#08427B`, Container `#438DD5`, DB `#2E6295`, External `#999999`, white text) — do not invent rainbow fills.
5. If C4Dynamic still overlaps: flowchart TB fallback + phrase `C4Dynamic unavailable`.

## Content anti-patterns

- Re-narrate diagrams in prose under Communication and data.
- Copy Architecture cross-cutting into every feature (use Cross-cutting deltas).
- Leave agent instructional essays on distilled pages (keep fill rules in AGENTS / this file).
- Force full API field tables when the feature only consumes an API (`Owns contract?` = `no`).
- Create Overview (`index.md`) or Quick start pages — remove them; they are obsolete.
- Put use-when rules only in Architecture ADR table (use `decisions.md`).
- Leave Topic index empty after features exist.
- Put multi-step ops only inside feature Testing and rollout when a reusable how-to would serve better.
- Silently edit past ADR Status/Date rows instead of superseding.
