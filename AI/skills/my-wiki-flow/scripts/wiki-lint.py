#!/usr/bin/env python3
"""Lint my-wiki-flow vault: structure, diagrams, claims, links, SHA freshness."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n(.*)\Z", re.S)
WIKI_LINK_RE = re.compile(r"\[\[([^\]|#]+)(?:\|([^\]]+))?\]\]")
H2_RE = re.compile(r"^##\s+(.+)$", re.M)
MERMAID_RE = re.compile(r"```mermaid\s*\n(.*?)```", re.S | re.I)
WORKSPACE_RE = re.compile(r"workspace:([^\s\]`@]+)")
VALIDATED_RE = re.compile(
    r"validated_against:\s*workspace:([^\s@]+)@([A-Za-z0-9._-]+)", re.I
)
CLAIMS_FM_RE = re.compile(r"^claims:\s*\[(.*?)\]\s*$", re.M | re.S)

CANONICAL = (
    "architecture.md",
    "topic-index.md",
    "solution-design.md",
    "decisions.md",
    "glossary.md",
)
OBSOLETE = (
    "index.md",
    "quick-start.md",
    "tips-and-tricks.md",
    "design-guide.md",
)

REQUIRED_H2 = {
    "architecture.md": [
        "Purpose and quality goals",
        "Building block view",
        "Interaction diagram",
        "Communication and data",
        "Cross-cutting concerns",
        "Deployment view",
        "Risks and technical debt",
        "Key decisions and constraints",
        "Related solution designs",
    ],
    "topic-index.md": [
        "Topic map",
    ],
    "solution-design.md": [],  # hub — flexible index
    "decisions.md": [
        "Decision rules",
        "Anti-patterns",
        "Trade-offs",
        "Related architecture decisions",
    ],
    "glossary.md": [],  # table body
}

FEATURE_H2 = [
    "Summary",
    "Scope and requirements",
    "Design overview",
    "Sequence diagram",
    "API contracts",
    "Data and state changes",
    "Complex logic",
    "Failure and retry behavior",
    "Cross-cutting deltas",
    "Testing and rollout",
    "Decisions and open questions",
]

HOWTO_H2 = [
    "Prerequisites",
    "Steps",
    "Verify",
]

CONCEPT_H2 = [
    "Definition",
    "When to use",
    "Related projects",
]

VALID_ENTITY = {"tutorial", "how-to", "howto", "reference", "explanation", "concept"}
VALID_STATUS = {"proposed", "accepted", "superseded", "deprecated"}
VALID_CONFIDENCE = {"high", "medium", "low"}

DOCS_ONLY = re.compile(
    r"(?i)(README\.md|CONTRIBUTING\.md|docs/|/\.md\b|ADR|changelog)",
)
TABLE_SEP_RE = re.compile(r"^\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)+\|?\s*$")


@dataclass
class Issue:
    severity: str  # error | warn
    path: str
    message: str


@dataclass
class LintResult:
    issues: list[Issue] = field(default_factory=list)

    def add(self, severity: str, path: str, message: str) -> None:
        self.issues.append(Issue(severity, path, message))

    @property
    def errors(self) -> list[Issue]:
        return [i for i in self.issues if i.severity == "error"]

    @property
    def warns(self) -> list[Issue]:
        return [i for i in self.issues if i.severity == "warn"]


def expand_root(raw: str) -> Path:
    return Path(raw).expanduser().resolve()


def load_config(root: Path) -> dict:
    cfg_path = root / "config.yaml"
    cfg: dict = {"projects": {}, "build": {"site_dir": "site"}}
    if not cfg_path.is_file():
        return cfg
    stack: list[tuple[int, dict]] = [(0, cfg)]
    for line in cfg_path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        if ":" not in line:
            continue
        key, _, val = line.lstrip().partition(":")
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        while stack and indent < stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]
        if val == "":
            nested: dict = {}
            parent[key] = nested
            stack.append((indent + 2, nested))
        else:
            parent[key] = val
    return cfg


def parse_frontmatter(text: str) -> tuple[dict, str]:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    meta: dict = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        k = k.strip()
        v = v.strip()
        if v.startswith("[") and v.endswith("]"):
            inner = v[1:-1].strip()
            meta[k] = [
                x.strip().strip('"').strip("'")
                for x in inner.split(",")
                if x.strip()
            ]
        else:
            meta[k] = v.strip('"').strip("'")
    return meta, m.group(2)


def git_short_sha(workspace: Path) -> str | None:
    if not workspace.is_dir():
        return None
    try:
        out = subprocess.check_output(
            ["git", "-C", str(workspace), "rev-parse", "--short", "HEAD"],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        return out or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def collect_md_pages(root: Path) -> list[Path]:
    pages: list[Path] = []
    for base in (root / "projects", root / "inbox", root / "concepts"):
        if not base.is_dir():
            continue
        for p in base.rglob("*.md"):
            if p.name == "README.md":
                continue
            pages.append(p)
    return pages


def link_targets(root: Path, pages: list[Path]) -> set[str]:
    targets: set[str] = set()
    for p in pages:
        rel = p.relative_to(root).with_suffix("").as_posix().lower()
        targets.add(rel)
        targets.add(p.stem.lower())
        # projects/slug/index → projects/slug
        if p.name == "index.md":
            targets.add(p.parent.relative_to(root).as_posix().lower())
        text = p.read_text(encoding="utf-8")
        meta, _ = parse_frontmatter(text)
        aliases = meta.get("aliases")
        if isinstance(aliases, list):
            for a in aliases:
                key = str(a).strip().lower().removesuffix(".md").strip("/")
                if key:
                    targets.add(key)
                    targets.add(key.split("/")[-1])
    return targets


def maintain_ages(cfg: dict) -> tuple[int, int]:
    m = cfg.get("maintain") if isinstance(cfg.get("maintain"), dict) else {}
    inbox = int(str((m or {}).get("inbox_max_age_days") or 14))
    reviewed = int(str((m or {}).get("reviewed_max_age_days") or 90))
    return inbox, reviewed


def file_age_days(path: Path) -> int | None:
    try:
        mtime = path.stat().st_mtime
    except OSError:
        return None
    from datetime import datetime, timezone

    age = datetime.now(timezone.utc) - datetime.fromtimestamp(mtime, tz=timezone.utc)
    return max(0, age.days)


def resolve_workspace(cfg: dict, slug: str, root: Path) -> Path | None:
    projects = cfg.get("projects") or {}
    entry = projects.get(slug) if isinstance(projects, dict) else None
    if isinstance(entry, dict):
        ws = entry.get("workspace") or entry.get("path")
        if ws:
            return expand_root(str(ws))
    if isinstance(entry, str) and entry:
        return expand_root(entry)
    # fallback: validated_against path from architecture.md
    arch = root / "projects" / slug / "architecture.md"
    if arch.is_file():
        text = arch.read_text(encoding="utf-8")
        m = VALIDATED_RE.search(text)
        if m:
            return expand_root(m.group(1))
    return None


def check_required_h2(body: str, required: list[str], path: str, result: LintResult) -> None:
    found = {h.strip() for h in H2_RE.findall(body)}
    for h in required:
        if h not in found:
            result.add("error", path, f"Missing required H2: ## {h}")


def _section_body(body: str, heading: str) -> str:
    marker = f"## {heading}"
    if marker not in body:
        return ""
    section = body.split(marker, 1)[1]
    next_h2 = re.search(r"\n##\s+", section)
    if next_h2:
        section = section[: next_h2.start()]
    return section


def _mermaid_diagram_head(block: str) -> str:
    """First diagram keyword line, skipping %% comments and YAML frontmatter."""
    lines = block.strip().splitlines()
    i = 0
    if lines and lines[0].strip() == "---":
        i = 1
        while i < len(lines) and lines[i].strip() != "---":
            i += 1
        i += 1  # past closing ---
    while i < len(lines):
        line = lines[i].strip()
        if not line or line.startswith("%%"):
            i += 1
            continue
        return line.lower().replace(" ", "")
    return ""


def _mermaid_heads(section: str) -> list[tuple[str, str]]:
    """Return (head_compact, full_block) for each mermaid fence in section."""
    out: list[tuple[str, str]] = []
    for block in MERMAID_RE.findall(section):
        out.append((_mermaid_diagram_head(block), block))
    return out


def check_architecture_diagrams(body: str, path: str, result: LintResult) -> None:
    bb = _section_body(body, "Building block view")
    if not bb:
        result.add("error", path, "Missing ## Building block view section")
    else:
        heads = _mermaid_heads(bb)
        if not heads:
            result.add(
                "error",
                path,
                "Building block view must include Mermaid C4Container or C4Component",
            )
        else:
            ok = any(
                "c4container" in h or "c4component" in h for h, _ in heads
            )
            if not ok:
                result.add(
                    "error",
                    path,
                    "Building block view must use Mermaid C4Container or C4Component",
                )

    ix = _section_body(body, "Interaction diagram")
    if not ix:
        result.add("error", path, "Missing ## Interaction diagram section")
        return
    heads = _mermaid_heads(ix)
    if not heads:
        result.add(
            "error",
            path,
            "Interaction diagram must include Mermaid C4Dynamic "
            "(or flowchart with 'C4Dynamic unavailable')",
        )
        return
    for head_compact, block in heads:
        if "c4dynamic" in head_compact:
            # Horizontal C4Dynamic packs ~4/row and overlaps return labels — require 1/row.
            if not re.search(
                r"updatelayoutconfig\s*\([^)]*c4shapeinrow\s*=\s*[\"']1[\"']",
                block,
                re.I,
            ):
                result.add(
                    "error",
                    path,
                    "C4Dynamic Interaction diagram must include "
                    "UpdateLayoutConfig($c4ShapeInRow=\"1\") "
                    "(or use flowchart TB with 'C4Dynamic unavailable')",
                )
            continue
        if "c4dynamic unavailable" in block.lower() and (
            head_compact.startswith("flowchart") or head_compact.startswith("graph")
        ):
            result.add(
                "warn",
                path,
                "Architecture uses flowchart fallback (C4Dynamic unavailable)",
            )
            continue
        result.add(
            "error",
            path,
            "Architecture Interaction diagram must use Mermaid C4Dynamic "
            "(or flowchart with 'C4Dynamic unavailable' note)",
        )


def check_mermaid_types(body: str, path: str, kind: str, result: LintResult) -> None:
    blocks = MERMAID_RE.findall(body)
    if not blocks:
        result.add("error", path, f"Missing Mermaid fence for {kind}")
        return
    if kind == "architecture":
        check_architecture_diagrams(body, path, result)
        return
    if kind == "sequence":
        has_seq = False
        has_alt_opt = False
        for block in blocks:
            head = block.strip().splitlines()[0].strip().lower() if block.strip() else ""
            head_compact = head.replace(" ", "")
            if "sequencediagram" in head_compact:
                has_seq = True
                if re.search(r"(?m)^\s*(alt|opt)\b", block):
                    has_alt_opt = True
            else:
                result.add(
                    "error",
                    path,
                    "Feature Mermaid must be sequenceDiagram (not flowchart/C4)",
                )
        if not has_seq:
            result.add(
                "error",
                path,
                "Feature Mermaid must be sequenceDiagram (not flowchart/C4)",
            )
        elif not has_alt_opt:
            result.add(
                "warn",
                path,
                "Sequence diagram should include alt or opt for a failure/edge path",
            )


def check_scope_and_requirements(body: str, path: str, result: LintResult) -> None:
    if "## Scope and requirements" not in body:
        return
    section = body.split("## Scope and requirements", 1)[1]
    next_h2 = re.search(r"\n##\s+", section)
    if next_h2:
        section = section[: next_h2.start()]
    if "business requirement" not in section.lower():
        result.add(
            "error",
            path,
            "Scope and requirements must include Business requirements "
            "(### Business requirements or a Business requirement column)",
        )


def _owns_api_contract(section: str) -> bool:
    """True when Spec summary marks any row as owning the contract."""
    lower = section.lower()
    if "owns contract" not in lower:
        # Legacy / incomplete: treat as owning so full checks still apply
        return True
    # Table cells: | yes | or | shared | near Owns column — look for yes/shared values
    # Prefer explicit owns markers in the section body.
    for line in section.splitlines():
        if "owns contract" in line.lower():
            continue  # header row
        cells = [c.strip().lower() for c in line.split("|") if c.strip()]
        if not cells:
            continue
        if any(c in ("yes", "shared") for c in cells):
            return True
    return False


def check_api_contracts(body: str, path: str, result: LintResult) -> None:
    if "## API contracts" not in body:
        return
    section = body.split("## API contracts", 1)[1]
    next_h2 = re.search(r"\n##\s+", section)
    if next_h2:
        section = section[: next_h2.start()]
    lower = section.lower()
    if "spec summary" not in lower:
        result.add("error", path, "API contracts must include a Spec summary")
    if "workspace:" not in section:
        result.add(
            "error",
            path,
            "API contracts must cite at least one workspace: canonical source",
        )

    owns = _owns_api_contract(section)
    if not owns:
        # Progressive: link-only consumer feature
        return

    if "### api spec" not in lower and re.search(r"(?m)^###\s+api spec\b", section) is None:
        if "api spec" not in lower:
            result.add("error", path, "API contracts must include an API spec subsection")
    if "request fields" not in lower:
        result.add(
            "error",
            path,
            "API spec must list Request fields (table with type + example value)",
        )
    if "response fields" not in lower:
        result.add(
            "error",
            path,
            "API spec must list Response fields (success and/or error) with example values",
        )
    if "example value" not in lower and "example values" not in lower:
        result.add(
            "error",
            path,
            "API spec field tables must include an Example value column",
        )
    if "example — success" not in lower and "### example — success" not in lower:
        if "success" not in lower or "request" not in lower:
            result.add(
                "error",
                path,
                "API contracts must include example request/response for success",
            )
    if "example — error" not in lower and "### example — error" not in lower:
        if "error" not in lower or ("response" not in lower):
            result.add(
                "error",
                path,
                "API contracts must include example request/response for error",
            )
    curl_count = len(re.findall(r"(?m)^\s*curl\b", section))
    if curl_count < 2:
        result.add(
            "error",
            path,
            "API contracts example requests must use curl "
            "(need curl for success and error)",
        )
    if re.search(r":\s*\[\s*\]", section):
        result.add(
            "warn",
            path,
            "API contracts response should not use empty arrays []; "
            "show at least the first item when the field is an array",
        )
    fence_count = section.count("```")
    if fence_count < 4:
        result.add(
            "warn",
            path,
            "API contracts should include separate request/response examples "
            "(success and error)",
        )


def check_complex_logic(body: str, path: str, result: LintResult) -> None:
    if "## Complex logic" not in body:
        return
    section = body.split("## Complex logic", 1)[1]
    next_h2 = re.search(r"\n##\s+", section)
    if next_h2:
        section = section[: next_h2.start()]
    if "workspace:" not in section:
        result.add(
            "error",
            path,
            "Complex logic must cite workspace: reference path(s)",
        )
    na = bool(re.search(r"\bn/?a\b", section, re.I))
    if not na and "```" not in section:
        result.add(
            "error",
            path,
            "Complex logic must include a reference/example code fence "
            "(or N/A with a workspace: cite)",
        )


def check_topic_index(body: str, path: str, result: LintResult) -> None:
    """Topic index must route with a table and at least one project wikilink."""
    section = _section_body(body, "Topic map")
    if not section:
        return
    if "|" not in section:
        result.add("error", path, "Topic map must be a GFM table (Topic | Page | Notes)")
        return
    links = WIKI_LINK_RE.findall(section)
    if not links:
        result.add(
            "error",
            path,
            "Topic map must include at least one [[wikilink]] to a project page",
        )


def check_decisions(body: str, path: str, result: LintResult) -> None:
    """Decision layer tables should cite workspace evidence."""
    for heading in ("Decision rules", "Anti-patterns", "Trade-offs"):
        section = _section_body(body, heading)
        if not section:
            continue
        # Placeholder-only stubs are OK at scaffold time; warn if filled rows lack cites
        rows = [
            ln
            for ln in section.splitlines()
            if ln.strip().startswith("|")
            and not TABLE_SEP_RE.match(ln.strip())
            and "---" not in ln
            and not re.search(r"\|\s*Rule\s*\|", ln, re.I)
            and not re.search(r"\|\s*Anti-pattern\s*\|", ln, re.I)
            and not re.search(r"\|\s*Choice A\s*\|", ln, re.I)
            and "…" not in ln
            and "..." not in ln
        ]
        for ln in rows:
            if "workspace:" not in ln:
                result.add(
                    "warn",
                    path,
                    f"{heading} row lacks workspace: cite: {ln.strip()[:80]}",
                )


def check_adr_status(body: str, path: str, result: LintResult) -> None:
    section = _section_body(body, "Key decisions and constraints")
    if not section:
        return
    for ln in section.splitlines():
        if not ln.strip().startswith("|") or TABLE_SEP_RE.match(ln.strip()):
            continue
        if re.search(r"\|\s*Decision\s*\|", ln, re.I):
            continue
        if "…" in ln or "..." in ln:
            continue
        cells = [c.strip().lower() for c in ln.split("|") if c.strip()]
        if len(cells) < 2:
            continue
        status = cells[1]
        if status and status not in VALID_STATUS and status not in (
            "accepted / superseded / proposed",
            "proposed / accepted / superseded / deprecated",
        ):
            # Allow multi-word placeholders in scaffold templates
            if "/" in status and all(
                part.strip() in VALID_STATUS or part.strip() in ("accepted",)
                for part in status.replace("deprecated", "deprecated").split("/")
            ):
                continue
            if status not in VALID_STATUS:
                result.add(
                    "warn",
                    path,
                    f"ADR Status should be one of {sorted(VALID_STATUS)}: {cells[1][:40]}",
                )


def check_howto(body: str, path: str, result: LintResult) -> None:
    check_required_h2(body, HOWTO_H2, path, result)
    steps = _section_body(body, "Steps")
    if steps and not re.search(r"(?m)^\s*\d+\.\s+", steps):
        result.add("warn", path, "How-to Steps should use a numbered list")


def check_concept(body: str, path: str, result: LintResult) -> None:
    check_required_h2(body, CONCEPT_H2, path, result)


def check_frontmatter_meta(meta: dict, path: str, result: LintResult) -> None:
    et = str(meta.get("entity_type") or "").strip().lower()
    if et and et not in VALID_ENTITY:
        result.add(
            "warn",
            path,
            f"entity_type should be tutorial|how-to|reference|explanation (got {et})",
        )
    conf = str(meta.get("confidence") or "").strip().lower()
    if conf and conf not in VALID_CONFIDENCE:
        result.add(
            "warn",
            path,
            f"confidence should be high|medium|low (got {conf})",
        )


def check_key_claims(body: str, meta: dict, path: str, result: LintResult) -> None:
    if "## Key claims" not in body:
        result.add("warn", path, "Missing ## Key claims section")
        return
    section = body.split("## Key claims", 1)[1]
    next_h2 = re.search(r"\n##\s+", section)
    if next_h2:
        section = section[: next_h2.start()]
    bullets = [
        ln.strip()
        for ln in section.splitlines()
        if ln.strip().startswith("-") and ln.strip() not in ("-", "- …", "- ...")
    ]
    for b in bullets:
        if "workspace:" not in b and "`" not in b:
            result.add(
                "warn",
                path,
                f"Key claim may lack code path: {b[:80]}",
            )
        if DOCS_ONLY.search(b) and "workspace:" not in b:
            result.add(
                "error",
                path,
                f"Key claim cites docs only (no workspace: code path): {b[:80]}",
            )
    fm_claims = meta.get("claims")
    if isinstance(fm_claims, list) and fm_claims:
        body_lower = section.lower()
        for c in fm_claims:
            if str(c).lower() not in body_lower and str(c) not in section:
                result.add(
                    "warn",
                    path,
                    f"Frontmatter claim not reflected in Key claims: {c}",
                )


def lint_project(
    root: Path, slug: str, cfg: dict, result: LintResult, all_targets: set[str]
) -> None:
    proj = root / "projects" / slug
    if not proj.is_dir():
        return
    for name in OBSOLETE:
        if (proj / name).is_file():
            result.add("error", f"projects/{slug}/{name}", "Obsolete page — remove")

    for name in CANONICAL:
        p = proj / name
        rel = f"projects/{slug}/{name}"
        if not p.is_file():
            result.add("error", rel, "Missing canonical page")
            continue
        text = p.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(text)
        check_frontmatter_meta(meta, rel, result)
        if not meta.get("validated_against"):
            result.add("warn", rel, "Missing validated_against frontmatter")
        if name in REQUIRED_H2 and REQUIRED_H2[name]:
            check_required_h2(body, REQUIRED_H2[name], rel, result)
        if name == "architecture.md":
            check_architecture_diagrams(body, rel, result)
            check_adr_status(body, rel, result)
        if name == "topic-index.md":
            check_topic_index(body, rel, result)
        if name == "decisions.md":
            check_decisions(body, rel, result)
        check_key_claims(body, meta, rel, result)
        # wikilinks
        for m in WIKI_LINK_RE.finditer(body):
            target = m.group(1).strip().lower().replace("\\", "/")
            target = target.removesuffix(".md")
            if target not in all_targets and not target.startswith("http"):
                # allow relative project-local short forms
                alt = f"projects/{slug}/{target}".lower()
                if alt not in all_targets and target.split("/")[-1] not in all_targets:
                    result.add("warn", rel, f"Possibly broken wikilink: [[{m.group(1)}]]")

    # Feature pages
    sd_dir = proj / "solution-design"
    if sd_dir.is_dir():
        for fp in sorted(sd_dir.glob("*.md")):
            rel = f"projects/{slug}/solution-design/{fp.name}"
            text = fp.read_text(encoding="utf-8")
            meta, body = parse_frontmatter(text)
            check_frontmatter_meta(meta, rel, result)
            check_required_h2(body, FEATURE_H2, rel, result)
            check_mermaid_types(body, rel, "sequence", result)
            check_complex_logic(body, rel, result)
            check_scope_and_requirements(body, rel, result)
            check_api_contracts(body, rel, result)
            check_key_claims(body, meta, rel, result)

    # How-to pages
    ht_dir = proj / "how-to"
    if ht_dir.is_dir():
        for fp in sorted(ht_dir.glob("*.md")):
            if fp.name.lower() == "readme.md":
                continue
            rel = f"projects/{slug}/how-to/{fp.name}"
            text = fp.read_text(encoding="utf-8")
            meta, body = parse_frontmatter(text)
            check_frontmatter_meta(meta, rel, result)
            check_howto(body, rel, result)
            check_key_claims(body, meta, rel, result)

    # SHA freshness
    ws = resolve_workspace(cfg, slug, root)
    if ws:
        head = git_short_sha(ws)
        arch = proj / "architecture.md"
        if head and arch.is_file():
            text = arch.read_text(encoding="utf-8")
            m = VALIDATED_RE.search(text)
            if m:
                recorded = m.group(2)
                if recorded != "unknown" and recorded != head and not head.startswith(
                    recorded
                ) and not recorded.startswith(head):
                    result.add(
                        "warn",
                        f"projects/{slug}/architecture.md",
                        f"Stale validated_against SHA {recorded} vs HEAD {head}",
                    )


def lint_concepts(
    root: Path, result: LintResult, all_targets: set[str], *, maintain: bool, reviewed_max: int
) -> None:
    concepts = root / "concepts"
    if not concepts.is_dir():
        return
    topic = concepts / "topic-index.md"
    if topic.is_file():
        text = topic.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(text)
        check_frontmatter_meta(meta, "concepts/topic-index.md", result)
        check_topic_index(body, "concepts/topic-index.md", result)
    for fp in sorted(concepts.glob("*.md")):
        if fp.name.lower() in ("readme.md", "topic-index.md"):
            continue
        rel = f"concepts/{fp.name}"
        text = fp.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(text)
        check_frontmatter_meta(meta, rel, result)
        check_concept(body, rel, result)
        check_key_claims(body, meta, rel, result)
        if maintain:
            reviewed = str(meta.get("reviewed") or "").strip()
            if not reviewed:
                result.add("warn", rel, "Missing reviewed: frontmatter (concepts)")
            else:
                try:
                    from datetime import datetime

                    d = datetime.strptime(reviewed, "%Y-%m-%d").date()
                    age = (date.today() - d).days
                    if age > reviewed_max:
                        result.add(
                            "warn",
                            rel,
                            f"reviewed: {reviewed} is {age} days old (max {reviewed_max})",
                        )
                except ValueError:
                    result.add("warn", rel, f"Invalid reviewed: date {reviewed}")
        for m in WIKI_LINK_RE.finditer(body):
            target = m.group(1).strip().lower().replace("\\", "/").removesuffix(".md")
            if target not in all_targets and not target.startswith("http"):
                if target.split("/")[-1] not in all_targets:
                    result.add("warn", rel, f"Possibly broken wikilink: [[{m.group(1)}]]")


def lint_inbox_maintain(root: Path, result: LintResult, inbox_max: int) -> None:
    inbox = root / "inbox"
    if not inbox.is_dir():
        return
    for fp in sorted(inbox.glob("*.md")):
        if fp.name.lower() == "readme.md":
            continue
        age = file_age_days(fp)
        rel = f"inbox/{fp.name}"
        if age is not None and age > inbox_max:
            result.add(
                "warn",
                rel,
                f"Inbox item age {age} days (max {inbox_max}) — promote, file, or delete",
            )


def lint_references_reviewed(
    root: Path, slug: str, result: LintResult, reviewed_max: int
) -> None:
    ref = root / "projects" / slug / "references"
    if not ref.is_dir():
        return
    for fp in sorted(ref.glob("*.md")):
        if fp.name.lower() == "readme.md":
            continue
        rel = f"projects/{slug}/references/{fp.name}"
        text = fp.read_text(encoding="utf-8")
        meta, _ = parse_frontmatter(text)
        reviewed = str(meta.get("reviewed") or "").strip()
        if not reviewed:
            result.add("warn", rel, "Missing reviewed: frontmatter (references)")
            continue
        try:
            from datetime import datetime

            d = datetime.strptime(reviewed, "%Y-%m-%d").date()
            age = (date.today() - d).days
            if age > reviewed_max:
                result.add(
                    "warn",
                    rel,
                    f"reviewed: {reviewed} is {age} days old (max {reviewed_max})",
                )
        except ValueError:
            result.add("warn", rel, f"Invalid reviewed: date {reviewed}")


def coverage_summary(root: Path, cfg: dict, slugs: list[str]) -> str:
    pages = collect_md_pages(root)
    inbox_n = sum(
        1
        for p in pages
        if "inbox" in p.parts and p.name.lower() != "readme.md"
    )
    concepts_n = sum(
        1
        for p in pages
        if "concepts" in p.parts
        and p.name.lower() not in ("readme.md", "topic-index.md")
    )
    features = 0
    howtos = 0
    fresh = 0
    stale = 0
    for slug in slugs:
        sd = root / "projects" / slug / "solution-design"
        if sd.is_dir():
            features += len(list(sd.glob("*.md")))
        ht = root / "projects" / slug / "how-to"
        if ht.is_dir():
            howtos += len([p for p in ht.glob("*.md") if p.name.lower() != "readme.md"])
        ws = resolve_workspace(cfg, slug, root)
        arch = root / "projects" / slug / "architecture.md"
        if ws and arch.is_file():
            head = git_short_sha(ws)
            m = VALIDATED_RE.search(arch.read_text(encoding="utf-8"))
            if head and m:
                recorded = m.group(2)
                if recorded == "unknown" or recorded == head or head.startswith(
                    recorded
                ) or recorded.startswith(head):
                    fresh += 1
                else:
                    stale += 1
    return (
        f"coverage: projects={len(slugs)} features={features} howtos={howtos} "
        f"concepts={concepts_n} inbox={inbox_n} sha_fresh={fresh} sha_stale={stale}"
    )


def lint_orphans(root: Path, pages: list[Path], result: LintResult) -> None:
    """Pages under projects/ with no inbound wikilink from any page or index."""
    inbound: set[str] = set()
    corpus = list(pages)
    for extra in (root / "index.md", root / "ai" / "INDEX.md"):
        if extra.is_file():
            corpus.append(extra)
    for p in corpus:
        text = p.read_text(encoding="utf-8")
        for m in WIKI_LINK_RE.finditer(text):
            inbound.add(m.group(1).strip().lower().removesuffix(".md"))
    for p in pages:
        if "projects" not in p.parts:
            continue
        # Canonical top pages are linked from root index on build; skip orphan noise
        if p.name in CANONICAL:
            continue
        rel = p.relative_to(root).with_suffix("").as_posix().lower()
        stem = p.stem.lower()
        if rel not in inbound and stem not in inbound:
            # solution-design hub should link features; still warn
            result.add(
                "warn",
                str(p.relative_to(root)),
                "Orphan page (no inbound wikilink found)",
            )


def append_log(root: Path, summary: str) -> None:
    log = root / "log.md"
    if not log.is_file():
        return
    line = f"\n## [{date.today().isoformat()}] lint | {summary}\n"
    with log.open("a", encoding="utf-8") as f:
        f.write(line)


def main() -> int:
    ap = argparse.ArgumentParser(description="Lint my-wiki-flow vault")
    ap.add_argument(
        "--root",
        default=os.environ.get("WIKI_ROOT", str(Path.home() / "Documents/my-wiki")),
    )
    ap.add_argument("--project", default="", help="Lint one project slug only")
    ap.add_argument(
        "--maintain",
        action="store_true",
        help="Vault hygiene: inbox age, reviewed age, coverage summary",
    )
    ap.add_argument("--no-log", action="store_true", help="Do not append log.md")
    args = ap.parse_args()
    root = expand_root(args.root)
    if not root.is_dir():
        print(f"Wiki root missing: {root}", file=sys.stderr)
        return 2

    cfg = load_config(root)
    inbox_max, reviewed_max = maintain_ages(cfg)
    result = LintResult()
    pages = collect_md_pages(root)
    targets = link_targets(root, pages)

    projects_dir = root / "projects"
    slugs: list[str] = []
    if projects_dir.is_dir():
        slugs = sorted(
            d.name
            for d in projects_dir.iterdir()
            if d.is_dir() and not d.name.startswith(".")
        )
    if args.project:
        slugs = [args.project]

    for slug in slugs:
        lint_project(root, slug, cfg, result, targets)
        if args.maintain:
            lint_references_reviewed(root, slug, result, reviewed_max)

    if not args.project:
        lint_concepts(
            root, result, targets, maintain=args.maintain, reviewed_max=reviewed_max
        )
        lint_orphans(root, pages, result)
        if args.maintain:
            lint_inbox_maintain(root, result, inbox_max)

    errors = result.errors
    warns = result.warns
    for i in result.issues:
        print(f"{i.severity.upper()}: {i.path}: {i.message}")

    summary = f"{len(errors)} error(s), {len(warns)} warning(s) across {len(slugs)} project(s)"
    if args.maintain:
        cov = coverage_summary(root, cfg, slugs)
        print(cov)
        summary = f"maintain | {summary} | {cov}"
    print(summary)
    if not args.no_log:
        if args.maintain:
            log = root / "log.md"
            if log.is_file():
                line = f"\n## [{date.today().isoformat()}] maintain | {summary}\n"
                with log.open("a", encoding="utf-8") as f:
                    f.write(line)
        else:
            append_log(root, summary)

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
