# Canonical project structure

Every project under `projects/{slug}/` uses the pages below. Distill from **real
code** (sources, handlers, schemas, build/run config, tests) — **not** from
README/docs/ADRs. Repo Markdown is a pointer only; confirm every claim in code
at the validation SHA.

Aligned with [Diátaxis](https://diataxis.fr/),
[Google tech writing — large docs](https://developers.google.com/tech-writing/two/large-docs),
and [ADS](https://archstandard.org/v1/standard/overview/).

Frontmatter, lint rules, and Karpathy layers: [content-contract.md](content-contract.md).
Operations: [stages.md](stages.md).

```text
projects/{slug}/
  index.md                 # 1. Overview
  quick-start.md           # 2. Quick start (task-oriented)
  architecture.md          # 3. full profile
  solution-design.md       # 4. full — hub
  solution-design/         #    one page per feature
    {feature-slug}.md
  glossary.md              # 5. full profile
  references/              # overflow (article.template.md)
```

Scaffold: `wiki-scaffold-project.sh {slug} [workspace] [--lite|--full]`  
Feature page: `wiki-add-feature.sh {slug} {feature} [master-feature]`

## Profiles

| Profile | Pages | When |
|---------|-------|------|
| `full` (default) | All five + features | Multi-module apps, APIs, systems you maintain |
| `lite` | Overview + Quick start only | Small tools, scripts, early capture |

Store `profile` under `config.yaml` → `projects.{slug}.profile`. Expand lite → full
by re-running scaffold with `--full` (creates missing pages only).

## Page roles and required sections

Agents **must** use these H2 headings (exact titles). Do not invent alternate top-level names.

### 1. Overview — `index.md`

| Section | Content |
|---------|---------|
| Purpose | What the project does and who it serves |
| Scope | What is included and excluded |
| Key capabilities | Short list of major features |
| System context diagram | Users, this system, external systems (**Mermaid** `flowchart` or `C4Context`) |
| Technology summary | Only main technologies and platforms |
| Key links | Quick start, Architecture (if full), Solution design (if full), repository |

### 2. Quick start — `quick-start.md`

| Section | Content |
|---------|---------|
| Prerequisites | Tools, versions, accounts, permissions |
| Setup | Numbered install/configure steps |
| Run locally | Exact commands and expected result |
| Verify | Quick check that setup succeeded |
| Common setup issues | Symptom / fix table |
| Next steps | Links to Architecture / solution designs (if full) |

### 3. Architecture — `architecture.md` (full only)

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
| Key decisions and constraints | ADR-lite: Status, Date, Summary, Consequences |
| Related solution designs | Links to feature pages |

### 4. Solution design — hub + features (full only)

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

### 5. Glossary — `glossary.md` (full only)

| Term | Definition | Related link |
|------|------------|--------------|
| … | Project-specific meaning | `[[wikilink]]` |

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

After confirmation: `wiki-add-feature.sh` for each; fill from code; link from hub.

## Codebase validation (mandatory on distill / update)

1. Resolve workspace from `config.yaml` → `projects.{slug}.workspace`.
2. Inspect code: entrypoints, handlers, schemas-as-code, manifests/Makefile/CI, tests.
3. Do not treat README/`docs/**`/ADRs as source of truth.
4. Set `validated_against: workspace:{path}@{sha}` and `updated`.
5. Every Key claims bullet maps to a code path or runnable command.
6. If code and wiki disagree → update the wiki (or mark superseded).
7. Append `log.md`.

## Diagrams and tables

- Overview: `flowchart` or `C4Context` (system context).
- Architecture building blocks: **`C4Container`** or **`C4Component`**.
- Architecture interaction: **`C4Dynamic`** (or flowchart with `C4Dynamic unavailable`).
- Features: **`sequenceDiagram` only** (prefer `alt`/`opt` for errors).
- HTML Mermaid figures are zoomable (wheel / drag / toolbar).
- GFM tables → `.wiki-table` on build. No escaped `\|` in table wikilinks.

### C4 layout and color (required for Architecture)

Mermaid C4 packs **4 shapes per row by default**, which overlaps labels on Interaction diagrams.

1. Interaction: prefer **`flowchart TB`** + phrase `C4Dynamic unavailable` when there are return paths or >3 participants (Mermaid C4Dynamic often overlaps).
2. If using `C4Dynamic`: **required** `UpdateLayoutConfig($c4ShapeInRow="1")`; no reverse Rel on the same vertical stack; short labels + `UpdateRelStyle` offsets.
3. Building blocks: `UpdateLayoutConfig($c4ShapeInRow="2"|`"3")`; group many externals into one `System_Ext` when possible.
4. Colors: grayscale only — do not add `UpdateElementStyle` / `classDef` accent fills.

## Content anti-patterns

- Re-narrate diagrams in prose under Communication and data.
- Copy Architecture cross-cutting into every feature (use Cross-cutting deltas).
- Leave agent instructional essays on distilled pages (keep fill rules in AGENTS / this file).
- Force full API field tables when the feature only consumes an API (`Owns contract?` = `no`).
