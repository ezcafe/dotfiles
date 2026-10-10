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
    "index.md",
    "quick-start.md",
    "architecture.md",
    "solution-design.md",
    "glossary.md",
)
LITE_CANONICAL = ("index.md", "quick-start.md")
OBSOLETE = ("tips-and-tricks.md", "design-guide.md")

REQUIRED_H2 = {
    "index.md": [
        "Purpose",
        "Scope",
        "Key capabilities",
        "System context diagram",
        "Technology summary",
        "Key links",
    ],
    "quick-start.md": [
        "Prerequisites",
        "Setup",
        "Run locally",
        "Verify",
        "Common setup issues",
        "Next steps",
    ],
    "architecture.md": [
        "Purpose and scope",
        "Interaction diagram",
        "Component responsibilities",
        "Key interactions and data flows",
        "Cross-cutting concerns",
        "Deployment view",
        "Key decisions and constraints",
        "Related solution designs",
    ],
    "solution-design.md": [],  # hub — flexible index
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
    "Security and observability",
    "Testing and rollout",
    "Decisions and open questions",
]

DOCS_ONLY = re.compile(
    r"(?i)(README\.md|CONTRIBUTING\.md|docs/|/\.md\b|ADR|changelog)",
)


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
    for base in (root / "projects", root / "inbox"):
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
    return targets


def resolve_workspace(cfg: dict, slug: str, root: Path) -> Path | None:
    projects = cfg.get("projects") or {}
    entry = projects.get(slug) if isinstance(projects, dict) else None
    if isinstance(entry, dict):
        ws = entry.get("workspace") or entry.get("path")
        if ws:
            return expand_root(str(ws))
    if isinstance(entry, str) and entry:
        return expand_root(entry)
    # fallback: validated_against path from index.md
    index = root / "projects" / slug / "index.md"
    if index.is_file():
        text = index.read_text(encoding="utf-8")
        m = VALIDATED_RE.search(text)
        if m:
            return expand_root(m.group(1))
    return None


def project_profile(proj_dir: Path, cfg: dict, slug: str) -> str:
    projects = cfg.get("projects") or {}
    entry = projects.get(slug) if isinstance(projects, dict) else None
    if isinstance(entry, dict) and entry.get("profile") in ("lite", "full"):
        return str(entry["profile"])
    # Infer lite: missing architecture + solution-design + glossary
    has_arch = (proj_dir / "architecture.md").is_file()
    has_sd = (proj_dir / "solution-design.md").is_file()
    if not has_arch and not has_sd:
        return "lite"
    return "full"


def check_required_h2(body: str, required: list[str], path: str, result: LintResult) -> None:
    found = {h.strip() for h in H2_RE.findall(body)}
    for h in required:
        if h not in found:
            result.add("error", path, f"Missing required H2: ## {h}")


def check_mermaid_types(body: str, path: str, kind: str, result: LintResult) -> None:
    blocks = MERMAID_RE.findall(body)
    if not blocks:
        result.add("error", path, f"Missing Mermaid fence for {kind}")
        return
    for block in blocks:
        head = block.strip().splitlines()[0].strip().lower() if block.strip() else ""
        head_compact = head.replace(" ", "")
        if kind == "architecture":
            if "c4dynamic" in head_compact:
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
        elif kind == "sequence":
            if "sequencediagram" in head_compact:
                continue
            result.add(
                "error",
                path,
                "Feature Mermaid must be sequenceDiagram (not flowchart/C4)",
            )


def check_api_contracts(body: str, path: str, result: LintResult) -> None:
    if "## API contracts" not in body:
        return
    section = body.split("## API contracts", 1)[1]
    next_h2 = re.search(r"\n##\s+", section)
    if next_h2:
        section = section[: next_h2.start()]
    lower = section.lower()
    if "### api spec" not in lower and "api spec" not in lower:
        result.add("error", path, "API contracts must include an API spec subsection")
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
    # Example requests must be curl
    curl_count = len(re.findall(r"(?m)^\s*curl\b", section))
    if curl_count < 2:
        result.add(
            "error",
            path,
            "API contracts example requests must use curl "
            "(need curl for success and error)",
        )
    # Empty JSON arrays in response examples are not enough
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
    if "```" not in section:
        result.add(
            "error",
            path,
            "Complex logic must include a reference/example code fence",
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
    profile = project_profile(proj, cfg, slug)
    required_pages = LITE_CANONICAL if profile == "lite" else CANONICAL

    for name in OBSOLETE:
        if (proj / name).is_file():
            result.add("error", f"projects/{slug}/{name}", "Obsolete page — remove")

    for name in required_pages:
        p = proj / name
        rel = f"projects/{slug}/{name}"
        if not p.is_file():
            result.add("error", rel, f"Missing canonical page (profile={profile})")
            continue
        text = p.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(text)
        if not meta.get("validated_against") and profile == "full":
            result.add("warn", rel, "Missing validated_against frontmatter")
        if name in REQUIRED_H2 and REQUIRED_H2[name]:
            check_required_h2(body, REQUIRED_H2[name], rel, result)
        if name == "architecture.md":
            check_mermaid_types(body, rel, "architecture", result)
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
            check_required_h2(body, FEATURE_H2, rel, result)
            check_mermaid_types(body, rel, "sequence", result)
            check_complex_logic(body, rel, result)
            check_api_contracts(body, rel, result)
            check_key_claims(body, meta, rel, result)

    # SHA freshness
    ws = resolve_workspace(cfg, slug, root)
    if ws:
        head = git_short_sha(ws)
        index = proj / "index.md"
        if head and index.is_file():
            text = index.read_text(encoding="utf-8")
            m = VALIDATED_RE.search(text)
            if m:
                recorded = m.group(2)
                if recorded != "unknown" and recorded != head and not head.startswith(
                    recorded
                ) and not recorded.startswith(head):
                    result.add(
                        "warn",
                        f"projects/{slug}/index.md",
                        f"Stale validated_against SHA {recorded} vs HEAD {head}",
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
        if p.name == "index.md":
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
    ap.add_argument("--no-log", action="store_true", help="Do not append log.md")
    args = ap.parse_args()
    root = expand_root(args.root)
    if not root.is_dir():
        print(f"Wiki root missing: {root}", file=sys.stderr)
        return 2

    cfg = load_config(root)
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

    if not args.project:
        lint_orphans(root, pages, result)

    errors = result.errors
    warns = result.warns
    for i in result.issues:
        print(f"{i.severity.upper()}: {i.path}: {i.message}")

    summary = f"{len(errors)} error(s), {len(warns)} warning(s) across {len(slugs)} project(s)"
    print(summary)
    if not args.no_log:
        append_log(root, summary)

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
