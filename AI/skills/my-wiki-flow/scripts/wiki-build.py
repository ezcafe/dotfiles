#!/usr/bin/env python3
"""Build ArchWiki-style static HTML from my-wiki-flow Markdown vault."""

from __future__ import annotations

import argparse
import html
import os
import re
import shutil
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path


FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n(.*)\Z", re.S)
HEADING_RE = re.compile(r"^(#{1,4})\s+(.+)$", re.M)
WIKI_LINK_RE = re.compile(r"\[\[([^\]|#]+)(?:\|([^\]]+))?\]\]")

# Matches Understand Anything parse-knowledge-base INFRA_FILES (vault root helpers).
INFRA_BASENAMES = {"index.md", "log.md", "agents.md", "claude.md", "soul.md", "context.md"}

# Canonical project nav order (project-structure.md).
PROJECT_PAGE_ORDER = (
    "architecture",
    "solution-design",
    "glossary",
)

TABLE_SEP_RE = re.compile(r"^\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)+\|?\s*$")
TABLE_ROW_RE = re.compile(r"^\|(.+)\|\s*$")


@dataclass
class Page:
    path: Path
    rel: Path
    title: str
    project: str
    tags: list[str] = field(default_factory=list)
    summary: str = ""
    source: str = ""
    updated: str = ""
    body_md: str = ""
    html_rel: Path = field(default_factory=Path)
    # Optional group label under Solution design (master feature name).
    nav_group: str = ""


def expand_root(raw: str) -> Path:
    return Path(raw).expanduser().resolve()


def load_config(root: Path) -> dict:
    cfg_path = root / "config.yaml"
    cfg = {
        "title": "My Wiki",
        "build": {"site_dir": "site"},
    }
    if not cfg_path.is_file():
        return cfg
    # Minimal YAML subset (key: value / nested 2-space)
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
    meta: dict[str, object] = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        k = k.strip()
        v = v.strip()
        if v.startswith("[") and v.endswith("]"):
            inner = v[1:-1].strip()
            meta[k] = [x.strip().strip('"').strip("'") for x in inner.split(",") if x.strip()]
        else:
            meta[k] = v.strip('"').strip("'")
    return meta, m.group(2)


def slugify(text: str) -> str:
    s = text.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[-\s]+", "-", s)
    return s.strip("-") or "section"


def build_link_map(pages: list[Page]) -> dict[str, Path]:
    """Map wikilink targets (several spellings) to generated HTML paths."""
    link_map: dict[str, Path] = {}
    for p in pages:
        stem = p.path.stem.lower()
        rel_no_ext = p.rel.with_suffix("").as_posix().lower()
        link_map[stem] = p.html_rel
        link_map[rel_no_ext] = p.html_rel
        if rel_no_ext.startswith("projects/"):
            short = rel_no_ext[len("projects/") :]
            link_map[short] = p.html_rel
        title_key = slugify(p.title)
        link_map.setdefault(title_key, p.html_rel)
    return link_map


def resolve_wikilink_href(target: str, from_html: Path, link_map: dict[str, Path]) -> str:
    raw = target.strip().strip("/")
    if raw.lower().endswith(".md"):
        raw = raw[:-3]
    keys = [raw.lower(), slugify(raw)]
    if "/" not in raw and raw.lower() not in link_map:
        keys.append(f"projects/{raw.lower()}")
    for key in keys:
        if key in link_map:
            return rel_href(from_html, link_map[key])
    return rel_href(from_html, Path(f"{slugify(raw.split('/')[-1])}.html"))


def split_table_cells(line: str) -> list[str]:
    raw = line.strip()
    if raw.startswith("|"):
        raw = raw[1:]
    if raw.endswith("|"):
        raw = raw[:-1]
    return [c.strip() for c in raw.split("|")]


def is_table_separator(line: str) -> bool:
    return bool(TABLE_SEP_RE.match(line.strip()))


def is_table_row(line: str) -> bool:
    s = line.strip()
    return s.startswith("|") and s.count("|") >= 2 and not is_table_separator(s)


def render_table(rows: list[list[str]], *, from_html: Path | None, link_map: dict[str, Path] | None) -> str:
    if not rows:
        return ""
    header, body = rows[0], rows[1:]
    thead = "".join(
        f"<th>{inline(c, from_html=from_html, link_map=link_map)}</th>" for c in header
    )
    trs = []
    for row in body:
        # Pad/truncate to header width
        cells = (row + [""] * len(header))[: len(header)]
        tds = "".join(
            f"<td>{inline(c, from_html=from_html, link_map=link_map)}</td>" for c in cells
        )
        trs.append(f"<tr>{tds}</tr>")
    return (
        '<div class="wiki-table-wrap"><table class="wiki-table">'
        f"<thead><tr>{thead}</tr></thead>"
        f"<tbody>{''.join(trs)}</tbody></table></div>"
    )


def md_to_html(
    md: str,
    *,
    from_html: Path | None = None,
    link_map: dict[str, Path] | None = None,
) -> tuple[str, list[tuple[int, str, str]]]:
    """Return (html_body, toc entries as level,id,title). Minimal Markdown + GFM tables + Mermaid."""
    lines = md.replace("\r\n", "\n").split("\n")
    out: list[str] = []
    toc: list[tuple[int, str, str]] = []
    i = 0
    in_code = False
    code_lang = ""
    code_buf: list[str] = []
    list_type: str | None = None

    def close_list() -> None:
        nonlocal list_type
        if list_type:
            out.append(f"</{list_type}>")
            list_type = None

    def flush_para(buf: list[str]) -> None:
        if not buf:
            return
        text = " ".join(buf).strip()
        if not text:
            buf.clear()
            return
        out.append(f"<p>{inline(text, from_html=from_html, link_map=link_map)}</p>")
        buf.clear()

    para: list[str] = []

    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            close_list()
            flush_para(para)
            if not in_code:
                in_code = True
                code_lang = line[3:].strip().split()[0] if line[3:].strip() else ""
                code_buf = []
            else:
                code = "\n".join(code_buf)
                lang = (code_lang or "").lower()
                if lang == "mermaid":
                    # Mermaid.js expects the diagram source inside .mermaid;
                    # toolbar + viewport enable pan/zoom after render.
                    out.append(
                        '<div class="wiki-mermaid" data-zoomable>'
                        '<div class="wiki-mermaid-toolbar" role="toolbar" aria-label="Diagram zoom">'
                        '<button type="button" data-zoom="in" title="Zoom in" aria-label="Zoom in">+</button>'
                        '<button type="button" data-zoom="out" title="Zoom out" aria-label="Zoom out">−</button>'
                        '<button type="button" data-zoom="reset" title="Reset zoom" aria-label="Reset zoom">Reset</button>'
                        "</div>"
                        f'<div class="wiki-mermaid-viewport"><pre class="mermaid">{html.escape(code)}</pre></div>'
                        "</div>"
                    )
                else:
                    lang_attr = f' class="language-{html.escape(code_lang)}"' if code_lang else ""
                    out.append(f"<pre><code{lang_attr}>{html.escape(code)}</code></pre>")
                in_code = False
            i += 1
            continue
        if in_code:
            code_buf.append(line)
            i += 1
            continue

        if not line.strip():
            close_list()
            flush_para(para)
            i += 1
            continue

        # GFM pipe table: header + separator + rows
        if is_table_row(line) and i + 1 < len(lines) and is_table_separator(lines[i + 1]):
            close_list()
            flush_para(para)
            table_rows: list[list[str]] = [split_table_cells(line)]
            i += 2  # skip header + separator
            while i < len(lines) and is_table_row(lines[i]):
                table_rows.append(split_table_cells(lines[i]))
                i += 1
            out.append(render_table(table_rows, from_html=from_html, link_map=link_map))
            continue

        hm = re.match(r"^(#{1,4})\s+(.+)$", line)
        if hm:
            close_list()
            flush_para(para)
            level = len(hm.group(1))
            title = hm.group(2).strip()
            hid = slugify(title)
            toc.append((level, hid, title))
            out.append(
                f'<h{level} id="{html.escape(hid)}">'
                f"{inline(title, from_html=from_html, link_map=link_map)}"
                f"</h{level}>"
            )
            i += 1
            continue

        if line.startswith("> "):
            close_list()
            flush_para(para)
            quote_lines = []
            while i < len(lines) and lines[i].startswith("> "):
                quote_lines.append(lines[i][2:])
                i += 1
            qtext = " ".join(quote_lines)
            kind = "note"
            label = "Note"
            for key, lab in (("Warning", "Warning"), ("Tip", "Tip"), ("Note", "Note")):
                if re.match(rf"^\*\*{key}\*\*", qtext, re.I) or qtext.lower().startswith(key.lower()):
                    kind = key.lower()
                    label = lab
                    qtext = re.sub(rf"^\*\*{key}\*\*\s*", "", qtext, flags=re.I)
                    qtext = re.sub(rf"^{key}\s*", "", qtext, flags=re.I)
                    break
            out.append(
                f'<div class="wiki-callout {kind}"><span class="label">{label}</span> '
                f"{inline(qtext, from_html=from_html, link_map=link_map)}</div>"
            )
            continue

        # Collapsible API example request/response: **Request** / **Response** + fence
        req_resp = re.match(
            r"^\*\*(Request|Response)\*\*(.*)$",
            line.strip(),
            re.I,
        )
        if req_resp:
            close_list()
            flush_para(para)
            label = req_resp.group(1).capitalize()
            suffix = req_resp.group(2).strip()
            summary = f"{label}{(' ' + suffix) if suffix else ''}"
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines) and lines[j].startswith("```"):
                code_lang = lines[j][3:].strip().split()[0] if lines[j][3:].strip() else ""
                j += 1
                code_buf = []
                while j < len(lines) and not lines[j].startswith("```"):
                    code_buf.append(lines[j])
                    j += 1
                if j < len(lines) and lines[j].startswith("```"):
                    j += 1  # closing fence
                code = "\n".join(code_buf)
                lang_attr = (
                    f' class="language-{html.escape(code_lang)}"' if code_lang else ""
                )
                out.append(
                    f'<details class="wiki-collapse">'
                    f"<summary>{html.escape(summary)}</summary>"
                    f"<pre><code{lang_attr}>{html.escape(code)}</code></pre>"
                    f"</details>"
                )
                i = j
                continue
            # No fence — fall through as normal paragraph

        ul = re.match(r"^[-*]\s+(.+)$", line)
        ol = re.match(r"^\d+\.\s+(.+)$", line)
        if ul or ol:
            flush_para(para)
            kind = "ul" if ul else "ol"
            if list_type != kind:
                close_list()
                list_type = kind
                out.append(f"<{kind}>")
            item = (ul or ol).group(1)
            out.append(f"<li>{inline(item, from_html=from_html, link_map=link_map)}</li>")
            i += 1
            continue

        close_list()
        para.append(line.strip())
        i += 1

    close_list()
    flush_para(para)
    # Drop first h1 from body if present — template already prints title
    body = "\n".join(out)
    body = re.sub(r"^<h1[^>]*>.*?</h1>\s*", "", body, count=1, flags=re.S)
    toc = [(lvl, hid, title) for (lvl, hid, title) in toc if lvl > 1]
    return body, toc


def _inline_format(text: str) -> str:
    """Format Markdown inline markup; escape everything else. No raw HTML."""
    parts: list[str] = []
    for m in re.finditer(
        r"`([^`]+)`|\[([^\]]+)\]\(([^)]+)\)|\*\*([^*]+)\*\*|\*([^*]+)\*|([^*`\[]+)|.",
        text,
    ):
        if m.group(1) is not None:
            parts.append(f"<code>{html.escape(m.group(1))}</code>")
        elif m.group(2) is not None:
            parts.append(f'<a href="{html.escape(m.group(3))}">{html.escape(m.group(2))}</a>')
        elif m.group(4) is not None:
            parts.append(f"<strong>{html.escape(m.group(4))}</strong>")
        elif m.group(5) is not None:
            parts.append(f"<em>{html.escape(m.group(5))}</em>")
        elif m.group(6) is not None:
            parts.append(html.escape(m.group(6)))
        else:
            parts.append(html.escape(m.group(0)))
    return "".join(parts)


def inline(
    text: str,
    *,
    from_html: Path | None = None,
    link_map: dict[str, Path] | None = None,
) -> str:
    def wikilink_sub(m: re.Match[str]) -> str:
        label = m.group(2) or m.group(1)
        if from_html is not None and link_map is not None:
            href = resolve_wikilink_href(m.group(1), from_html, link_map)
        else:
            href = f"{slugify(m.group(1).split('/')[-1])}.html"
        return f'<a href="{html.escape(href)}">{html.escape(label)}</a>'

    # Convert wikilinks first, then format the rest without re-escaping those anchors.
    text = WIKI_LINK_RE.sub(wikilink_sub, text)
    chunks: list[str] = []
    for chunk in re.split(r'(<a\s[^>]*>.*?</a>)', text):
        if chunk.startswith("<a "):
            chunks.append(chunk)
        elif chunk:
            chunks.append(_inline_format(chunk))
    return "".join(chunks)


def collect_pages(root: Path) -> list[Page]:
    pages: list[Page] = []
    for base, project_default in ((root / "projects", None), (root / "inbox", "inbox")):
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*.md")):
            if path.name == ".gitkeep":
                continue
            # Vault helper docs — not wiki articles
            if path == root / "inbox" / "README.md":
                continue
            if path.name.lower() in INFRA_BASENAMES and path.parent == root:
                continue
            if path.parent.name == "references" and path.name.lower() == "readme.md":
                continue
            rel = path.relative_to(root)
            meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))
            project = str(meta.get("project") or project_default or "")
            if not project and rel.parts[0] == "projects" and len(rel.parts) > 1:
                project = rel.parts[1]
            if not project:
                project = "inbox"
            title = str(meta.get("title") or path.stem.replace("-", " ").title())
            tags = meta.get("tags") if isinstance(meta.get("tags"), list) else []
            nav_group = str(
                meta.get("nav_group") or meta.get("master_feature") or ""
            ).strip()
            page = Page(
                path=path,
                rel=rel,
                title=title,
                project=project,
                tags=[str(t) for t in tags],
                summary=str(meta.get("summary") or ""),
                source=str(meta.get("source") or ""),
                updated=str(meta.get("updated") or ""),
                body_md=body,
                nav_group=nav_group,
            )
            parts = list(path.relative_to(root).parts)
            if project == "inbox":
                page.html_rel = Path("inbox") / f"{path.stem}.html"
            elif rel.parts[0] == "projects" and len(rel.parts) >= 3:
                # Preserve nested paths: solution-design/, references/, …
                under = Path(*rel.parts[2:]).with_suffix(".html")
                page.html_rel = Path("projects") / project / under
            else:
                page.html_rel = Path("projects") / project / f"{path.stem}.html"
            pages.append(page)
    return pages


def rel_href(from_html: Path, to_html: Path) -> str:
    return Path(to_html.as_posix()).as_posix() if from_html.parent == Path(".") else (
        "/".join([".."] * len(from_html.parent.parts) + list(to_html.parts))
    )


def is_solution_design_hub(page: Page) -> bool:
    rel = page.rel.as_posix().lower()
    return page.path.stem.lower() == "solution-design" and "/solution-design/" not in rel


def is_solution_design_feature(page: Page) -> bool:
    return "/solution-design/" in page.rel.as_posix().lower()


def page_kind(page: Page) -> str:
    """CSS body kind for ArchWiki-style page accents."""
    stem = page.path.stem.lower()
    if is_solution_design_feature(page):
        return "solution-design-feature"
    if is_solution_design_hub(page):
        return "solution-design"
    if stem == "architecture":
        return "architecture"
    if stem == "glossary":
        return stem
    return "article"


def page_kind_badge(kind: str) -> str:
    labels = {
        "architecture": "Architecture",
        "solution-design": "Solution design",
        "solution-design-feature": "Feature design",
    }
    label = labels.get(kind)
    if not label:
        return ""
    return (
        f'<p class="wiki-kind-badge" data-kind="{html.escape(kind)}">'
        f"{html.escape(label)}</p>"
    )


def page_sort_key(page: Page) -> tuple[int, str, str]:
    """Canonical pages first, then solution-design features, then the rest."""
    stem = page.path.stem.lower()
    rel = page.rel.as_posix().lower()
    if stem in PROJECT_PAGE_ORDER and "solution-design/" not in rel:
        return (0, f"{PROJECT_PAGE_ORDER.index(stem):02d}", page.title.lower())
    if "/solution-design/" in rel or rel.endswith("/solution-design.md"):
        if stem == "solution-design":
            return (0, f"{PROJECT_PAGE_ORDER.index('solution-design'):02d}", page.title.lower())
        return (1, page.nav_group.lower(), page.title.lower())
    return (2, stem, page.title.lower())


def _nav_link(page: Page, current: Page | None, from_html: Path) -> str:
    href = rel_href(from_html, page.html_rel)
    cls = ' class="current"' if current and page.path == current.path else ""
    return f'<a href="{html.escape(href)}"{cls}>{html.escape(page.title)}</a>'


def _nav_toggle(label: str = "Toggle section") -> str:
    return (
        f'<button type="button" class="nav-toggle" aria-expanded="true" '
        f'aria-label="{html.escape(label)}"></button>'
    )


def _feature_nav_tree(features: list[Page], current: Page | None, from_html: Path) -> str:
    """Nest features under Solution design; optional master-feature groups via nav_group."""
    if not features:
        return ""
    ungrouped: list[Page] = []
    groups: dict[str, list[Page]] = {}
    for f in sorted(features, key=lambda p: (p.nav_group.lower(), p.title.lower())):
        if f.nav_group:
            groups.setdefault(f.nav_group, []).append(f)
        else:
            ungrouped.append(f)
    parts: list[str] = ['<ul class="nav-children">']
    for f in ungrouped:
        parts.append(f"<li>{_nav_link(f, current, from_html)}</li>")
    for group_name in sorted(groups.keys(), key=str.lower):
        group_id = html.escape(slugify(group_name))
        group_pages = sorted(groups[group_name], key=lambda p: p.title.lower())
        group_cls = "nav-group nav-collapsible"
        if current and any(f.path == current.path for f in group_pages):
            group_cls += " has-current"
        parts.append(
            f'<li class="{group_cls}" data-nav-id="group:{group_id}">'
            f'<div class="nav-row">{_nav_toggle(f"Collapse {group_name}")}'
            f'<span class="nav-group-label">{html.escape(group_name)}</span></div>'
            f'<ul class="nav-children">'
        )
        for f in group_pages:
            parts.append(f"<li>{_nav_link(f, current, from_html)}</li>")
        parts.append("</ul></li>")
    parts.append("</ul>")
    return "".join(parts)


def build_nav(pages: list[Page], current: Page | None, from_html: Path) -> str:
    by_proj: dict[str, list[Page]] = {}
    for p in pages:
        by_proj.setdefault(p.project, []).append(p)
    chunks: list[str] = []
    for proj in sorted(by_proj.keys()):
        proj_pages = by_proj[proj]
        features = [p for p in proj_pages if is_solution_design_feature(p)]
        top = [p for p in proj_pages if not is_solution_design_feature(p)]
        current_here = bool(current and current.project == proj)
        proj_cls = "nav-project nav-collapsible"
        if current_here:
            proj_cls += " has-current"
        chunks.append(
            f'<div class="{proj_cls}" data-nav-id="project:{html.escape(proj)}">'
            f'<div class="nav-row project-row">'
            f"{_nav_toggle(f'Collapse project {proj}')}"
            f'<div class="project">{html.escape(proj)}</div>'
            f"</div>"
            f'<ul class="nav-root">'
        )
        for p in sorted(top, key=page_sort_key):
            if is_solution_design_hub(p):
                child_tree = _feature_nav_tree(features, current, from_html)
                parent_cls = "nav-parent nav-collapsible"
                if current and current.project == proj and (
                    is_solution_design_hub(current) or is_solution_design_feature(current)
                ):
                    parent_cls += " has-current"
                if child_tree:
                    # Hub link stays a peer of Architecture; toggle sits after the label.
                    chunks.append(
                        f'<li class="{parent_cls}" data-nav-id="hub:solution-design">'
                        f'<div class="nav-row nav-page-row">'
                        f"{_nav_link(p, current, from_html)}"
                        f'{_nav_toggle("Collapse Solution design")}</div>'
                        f"{child_tree}</li>"
                    )
                else:
                    chunks.append(f"<li>{_nav_link(p, current, from_html)}</li>")
            else:
                chunks.append(f"<li>{_nav_link(p, current, from_html)}</li>")
        # Orphan features if hub page is missing
        if features and not any(is_solution_design_hub(p) for p in top):
            chunks.append(
                f'<li class="nav-parent nav-collapsible" data-nav-id="hub:solution-design">'
                f'<div class="nav-row nav-page-row">'
                f'<span class="nav-page-label">Solution design</span>'
                f'{_nav_toggle("Collapse Solution design")}</div>'
                f"{_feature_nav_tree(features, current, from_html)}</li>"
            )
        chunks.append("</ul></div>")
    return "\n".join(chunks)


def build_toc(toc: list[tuple[int, str, str]]) -> str:
    if not toc:
        return ""
    items = []
    for level, hid, title in toc:
        pad = max(0, level - 2)
        style = f' style="margin-left:{pad}rem"' if pad else ""
        items.append(f'<li{style}><a href="#{html.escape(hid)}">{html.escape(title)}</a></li>')
    return (
        '<nav class="wiki-toc" aria-label="Contents">'
        '<div class="toc-title">Contents</div>'
        f'<ol>{"".join(items)}</ol></nav>'
    )


def render_page(
    template: str,
    site_title: str,
    page: Page,
    body_html: str,
    toc_html: str,
    nav_html: str,
    from_html: Path,
) -> str:
    depth = len(from_html.parent.parts)
    prefix = "/".join([".."] * depth) + "/" if depth else ""
    css = f"{prefix}assets/wiki.css"
    home = f"{prefix}index.html"
    project_href = f"{prefix}projects/{page.project}/architecture.html"
    if page.project == "inbox":
        project_href = f"{prefix}inbox/index.html"
    meta_bits = []
    if page.summary:
        meta_bits.append(f'<p class="wiki-lead">{html.escape(page.summary)}</p>')
    details = []
    if page.updated:
        details.append(f"Updated: {html.escape(page.updated)}")
    if page.source:
        details.append(f"Source: {html.escape(page.source)}")
    if page.tags:
        details.append("Tags: " + ", ".join(html.escape(t) for t in page.tags))
    meta = "".join(meta_bits)
    if details:
        meta += f'<p class="wiki-meta">{" · ".join(details)}</p>'

    kind = page_kind(page)
    body_class = f"wiki-kind-{kind}"
    return (
        template.replace("{{TITLE}}", html.escape(page.title))
        .replace("{{SITE_TITLE}}", html.escape(site_title))
        .replace("{{SUMMARY}}", html.escape(page.summary or page.title))
        .replace("{{BODY_CLASS}}", body_class)
        .replace("{{PAGE_KIND}}", page_kind_badge(kind))
        .replace("{{CSS_HREF}}", css)
        .replace("{{HOME_HREF}}", home)
        .replace("{{NAV}}", nav_html)
        .replace("{{TOC}}", toc_html)
        .replace("{{META}}", meta)
        .replace("{{BODY}}", body_html)
        .replace("{{PROJECT}}", html.escape(page.project))
        .replace("{{PROJECT_HREF}}", project_href)
        .replace("{{PAGEFIND_CSS}}", f"{prefix}pagefind/pagefind-component-ui.css")
        .replace("{{PAGEFIND_JS}}", f"{prefix}pagefind/pagefind-component-ui.js")
        .replace("{{PAGEFIND_BUNDLE}}", f"{prefix}pagefind/")
    )


def write_home(
    site: Path,
    template: str,
    site_title: str,
    pages: list[Page],
) -> None:
    by_proj: dict[str, list[Page]] = {}
    for p in pages:
        by_proj.setdefault(p.project, []).append(p)
    sections = ["<p class=\"wiki-lead\">Knowledge base grouped by project. Use search or the navigation menu.</p>"]
    for proj in sorted(by_proj.keys()):
        proj_pages = by_proj[proj]
        features = [p for p in proj_pages if is_solution_design_feature(p)]
        top = [p for p in proj_pages if not is_solution_design_feature(p)]
        sections.append(f"<h2 id=\"{html.escape(slugify(proj))}\">{html.escape(proj)}</h2><ul>")
        for p in sorted(top, key=page_sort_key):
            item = (
                f'<li><a href="{html.escape(p.html_rel.as_posix())}">{html.escape(p.title)}</a>'
                + (f" — {html.escape(p.summary)}" if p.summary else "")
            )
            if is_solution_design_hub(p) and features:
                item += "<ul>"
                for f in sorted(features, key=lambda x: (x.nav_group.lower(), x.title.lower())):
                    label = f"{f.nav_group}: {f.title}" if f.nav_group else f.title
                    item += (
                        f'<li><a href="{html.escape(f.html_rel.as_posix())}">{html.escape(label)}</a>'
                        + (f" — {html.escape(f.summary)}" if f.summary else "")
                        + "</li>"
                    )
                item += "</ul>"
            item += "</li>"
            sections.append(item)
        sections.append("</ul>")
    home = Page(
        path=Path("."),
        rel=Path("index.md"),
        title="Home",
        project="home",
        summary="Wiki home",
        body_md="",
        html_rel=Path("index.html"),
    )
    # Fake body page for template
    body = "\n".join(sections)
    toc = build_toc([(2, slugify(p), p) for p in sorted(by_proj.keys())])
    nav = build_nav(pages, None, Path("index.html"))
    # Manual fill without double h1 body conflict
    html_out = render_page(template, site_title, home, body, toc, nav, Path("index.html"))
    # Fix project footer for home
    html_out = html_out.replace(
        f'Project: <a href="projects/home/architecture.html">home</a>',
        "Home",
    )
    (site / "index.html").write_text(html_out, encoding="utf-8")


def update_root_index(root: Path, pages: list[Page], site_title: str) -> None:
    """Karpathy index.md — ## categories with [[wikilinks]] for Understand Anything."""
    by_proj: dict[str, list[Page]] = {}
    for p in pages:
        by_proj.setdefault(p.project, []).append(p)
    lines = [
        "# Wiki index",
        "",
        f"{site_title} — catalog for humans, agents, and Understand Anything.",
        "",
    ]
    for proj in sorted(by_proj.keys()):
        display = proj.replace("-", " ").title()
        lines.append(f"## {display}")
        lines.append("")
        proj_pages = by_proj[proj]
        features = [p for p in proj_pages if is_solution_design_feature(p)]
        top = [p for p in proj_pages if not is_solution_design_feature(p)]
        for p in sorted(top, key=page_sort_key):
            rel = p.rel.with_suffix("").as_posix()
            summary = f" — {p.summary}" if p.summary else ""
            lines.append(f"- [[{rel}|{p.title}]]{summary}")
            if is_solution_design_hub(p):
                # Nested under hub for Understand Anything edge parsing + human catalog
                by_group: dict[str, list[Page]] = {}
                for f in features:
                    by_group.setdefault(f.nav_group or "", []).append(f)
                for group_name in sorted(by_group.keys(), key=lambda g: (g == "", g.lower())):
                    group_pages = sorted(by_group[group_name], key=lambda x: x.title.lower())
                    if group_name:
                        lines.append(f"  - {group_name}")
                        indent = "    "
                    else:
                        indent = "  "
                    for f in group_pages:
                        frel = f.rel.with_suffix("").as_posix()
                        fsum = f" — {f.summary}" if f.summary else ""
                        lines.append(f"{indent}- [[{frel}|{f.title}]]{fsum}")
        lines.append("")
    raw = root / "raw"
    if raw.is_dir() and any(raw.iterdir()):
        lines.append("## Sources")
        lines.append("")
        for f in sorted(raw.rglob("*")):
            if f.is_file() and not f.name.startswith("."):
                lines.append(f"- `raw/{f.relative_to(raw).as_posix()}`")
        lines.append("")
    (root / "index.md").write_text("\n".join(lines), encoding="utf-8")


def update_ai_index(root: Path, pages: list[Page]) -> None:
    by_proj: dict[str, list[Page]] = {}
    for p in pages:
        by_proj.setdefault(p.project, []).append(p)
    lines = ["# Wiki index", "", f"_Generated {date.today().isoformat()}_", ""]
    for proj in sorted(by_proj.keys()):
        lines.append(f"## {proj}")
        lines.append("")
        proj_pages = by_proj[proj]
        features = [p for p in proj_pages if is_solution_design_feature(p)]
        top = [p for p in proj_pages if not is_solution_design_feature(p)]
        for p in sorted(top, key=page_sort_key):
            rel = p.rel.as_posix()
            summary = f" — {p.summary}" if p.summary else ""
            lines.append(f"- [{p.title}](../{rel}){summary}")
            if is_solution_design_hub(p):
                for f in sorted(features, key=lambda x: (x.nav_group.lower(), x.title.lower())):
                    label = f"{f.nav_group}: {f.title}" if f.nav_group else f.title
                    fsum = f" — {f.summary}" if f.summary else ""
                    lines.append(f"  - [{label}](../{f.rel.as_posix()}){fsum}")
        lines.append("")
    (root / "ai" / "INDEX.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Build my-wiki-flow static site")
    ap.add_argument("--root", default="", help="Vault root (default WIKI_ROOT or ~/Documents/my-wiki)")
    args = ap.parse_args()
    root = expand_root(args.root or __import__("os").environ.get("WIKI_ROOT", "~/Documents/my-wiki"))
    if not root.is_dir():
        raise SystemExit(f"Wiki root not found: {root}. Run wiki-init.sh first.")

    cfg = load_config(root)
    site_title = str(cfg.get("title") or "My Wiki")
    site_dir = str((cfg.get("build") or {}).get("site_dir") or "site")
    site = root / site_dir

    skill_assets = Path(__file__).resolve().parent.parent / "assets"
    template_path = skill_assets / "page.template.html"
    template = template_path.read_text(encoding="utf-8")

    if site.exists():
        for child in site.iterdir():
            if child.name == "pagefind":
                continue
            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()
    site.mkdir(parents=True, exist_ok=True)

    # Site CSS: skill bundle on each build (ArchWiki theme updates).
    # Set WIKI_USE_VAULT_CSS=1 to copy ~/Documents/my-wiki/assets/wiki.css instead.
    (site / "assets").mkdir(exist_ok=True)
    vault_css = root / "assets" / "wiki.css"
    skill_css = skill_assets / "wiki.css"

    if os.environ.get("WIKI_USE_VAULT_CSS") == "1" and vault_css.is_file():
        shutil.copy2(vault_css, site / "assets" / "wiki.css")
    else:
        shutil.copy2(skill_css, site / "assets" / "wiki.css")

    pages = collect_pages(root)
    link_map = build_link_map(pages)
    if not pages:
        # Still write a minimal home
        write_home(site, template, site_title, [])
        update_root_index(root, [], site_title)
        print(f"Built 0 pages → {site}")
        return 0

    for page in pages:
        body_html, toc = md_to_html(page.body_md, from_html=page.html_rel, link_map=link_map)
        toc_html = build_toc(toc)
        nav = build_nav(pages, page, page.html_rel)
        out = render_page(template, site_title, page, body_html, toc_html, nav, page.html_rel)
        dest = site / page.html_rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(out, encoding="utf-8")

    write_home(site, template, site_title, pages)
    update_root_index(root, pages, site_title)
    update_ai_index(root, pages)
    print(f"Built {len(pages)} pages → {site}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
