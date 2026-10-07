#!/usr/bin/env python3
"""Ensure GitHub Project GTD fields + views (idempotent). Uses gh + GraphQL."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from typing import Any

TITLE = os.environ.get("GTD_PROJECT_TITLE", "GTD")
OWNER = os.environ.get("GTD_GITHUB_OWNER", "@me")

# Required GTD Status options (board columns / filters)
STATUS_OPTIONS = [
    ("Inbox", "GRAY", "Unprocessed captures"),
    ("Today", "ORANGE", "Committed for today"),
    ("Next", "BLUE", "Clarified next actions"),
    ("Waiting", "YELLOW", "Blocked on someone else"),
    ("Someday", "PURPLE", "Maybe later"),
    ("Done", "GREEN", "Completed"),
]

DURATION_OPTIONS = [
    ("5m", "GRAY", ""),
    ("30m", "BLUE", "Default"),
    ("1h", "GREEN", ""),
    ("2h", "ORANGE", "Deep work / multiday default chunk"),
    ("4h", "RED", "Half-day"),
]

CONTEXT_OPTIONS = [
    ("computer", "BLUE", ""),
    ("phone", "GREEN", ""),
    ("errands", "ORANGE", ""),
]

CHUNK_OPTIONS = [
    ("1h", "GREEN", "Multiday block"),
    ("2h", "ORANGE", "Multiday block"),
    ("4h", "RED", "Multiday block"),
]

# name, layout, filter (None = no filter)
VIEWS = [
    ("Board", "BOARD_LAYOUT", None),
    ("Inbox", "TABLE_LAYOUT", "status:Inbox"),
    ("Today", "TABLE_LAYOUT", "status:Today"),
    ("Next", "TABLE_LAYOUT", "status:Next"),
    ("Waiting", "TABLE_LAYOUT", "status:Waiting"),
    ("Someday", "TABLE_LAYOUT", "status:Someday"),
]


def gh_json(args: list[str]) -> Any:
    out = subprocess.check_output(["gh", *args], text=True)
    return json.loads(out) if out.strip() else {}


def gql(query: str, variables: dict | None = None) -> dict:
    payload: dict[str, Any] = {"query": query}
    if variables is not None:
        payload["variables"] = variables
    out = subprocess.check_output(
        ["gh", "api", "graphql", "--input", "-"],
        input=json.dumps(payload),
        text=True,
    )
    data = json.loads(out)
    if data.get("errors"):
        raise RuntimeError(json.dumps(data["errors"], indent=2))
    return data["data"]


def resolve_login() -> str:
    return subprocess.check_output(["gh", "api", "user", "-q", ".login"], text=True).strip()


def find_or_create_project() -> tuple[str, int, str]:
    """Return (node_id, number, url)."""
    raw = gh_json(
        ["project", "list", "--owner", OWNER, "--limit", "100", "--format", "json"]
    )
    projects = raw.get("projects") or []
    for p in projects:
        if (p.get("title") or "").strip() == TITLE:
            return p["id"], int(p["number"]), p.get("url") or ""
    created = gh_json(
        ["project", "create", "--owner", OWNER, "--title", TITLE, "--format", "json"]
    )
    return created["id"], int(created["number"]), created.get("url") or ""


def load_project(node_id: str) -> dict:
    data = gql(
        """
        query($id: ID!) {
          node(id: $id) {
            ... on ProjectV2 {
              id
              number
              title
              fields(first: 50) {
                nodes {
                  __typename
                  ... on ProjectV2FieldCommon { id name dataType }
                  ... on ProjectV2SingleSelectField {
                    id name dataType
                    options { id name }
                  }
                }
              }
              views(first: 30) {
                nodes { id name layout filter }
              }
            }
          }
        }
        """,
        {"id": node_id},
    )
    return data["node"]


def ensure_single_select(
    project_id: str,
    fields: list[dict],
    name: str,
    options: list[tuple[str, str, str]],
) -> str:
    """Create or update SINGLE_SELECT field; return field id."""
    existing = next(
        (
            f
            for f in fields
            if (f.get("name") or "").lower() == name.lower()
            and f.get("__typename") == "ProjectV2SingleSelectField"
        ),
        None,
    )
    wanted_names = [o[0] for o in options]
    color_by = {o[0]: o[1] for o in options}
    desc_by = {o[0]: o[2] for o in options}

    if existing:
        by_name = {o["name"]: o["id"] for o in (existing.get("options") or [])}
        # Map default GitHub Status labels → GTD names (keep option ids)
        rename_map = {
            "Todo": "Inbox",
            "In Progress": "Today",
            "In progress": "Today",
        }
        id_for_wanted: dict[str, str] = {}
        for old_name, oid in by_name.items():
            target = rename_map.get(old_name, old_name)
            if target in wanted_names and target not in id_for_wanted:
                id_for_wanted[target] = oid
        for wname in wanted_names:
            if wname not in id_for_wanted and wname in by_name:
                id_for_wanted[wname] = by_name[wname]

        option_inputs = []
        for wname in wanted_names:
            entry: dict[str, str] = {
                "name": wname,
                "color": color_by[wname],
                "description": desc_by[wname],
            }
            if wname in id_for_wanted:
                entry["id"] = id_for_wanted[wname]
            option_inputs.append(entry)

        current = [o["name"] for o in (existing.get("options") or [])]
        desired = wanted_names
        if current == desired:
            print(f"  Field '{name}' options already match.")
            return existing["id"]
        print(f"  Updating field '{name}' options → {desired}")
        gql(
            """
            mutation($input: UpdateProjectV2FieldInput!) {
              updateProjectV2Field(input: $input) {
                projectV2Field {
                  ... on ProjectV2SingleSelectField { id name }
                }
              }
            }
            """,
            {"input": {"fieldId": existing["id"], "singleSelectOptions": option_inputs}},
        )
        return existing["id"]

    print(f"  Creating field '{name}'…")
    data = gql(
        """
        mutation($input: CreateProjectV2FieldInput!) {
          createProjectV2Field(input: $input) {
            projectV2Field {
              ... on ProjectV2SingleSelectField { id name }
            }
          }
        }
        """,
        {
            "input": {
                "projectId": project_id,
                "dataType": "SINGLE_SELECT",
                "name": name,
                "singleSelectOptions": [
                    {"name": n, "color": c, "description": d} for n, c, d in options
                ],
            }
        },
    )
    return data["createProjectV2Field"]["projectV2Field"]["id"]


def ensure_date_field(project_id: str, fields: list[dict], name: str = "Due") -> str | None:
    existing = next(
        (f for f in fields if (f.get("name") or "").lower() == name.lower()),
        None,
    )
    if existing:
        print(f"  Field '{name}' already present.")
        return existing.get("id")
    # DATE custom fields
    print(f"  Creating DATE field '{name}'…")
    try:
        data = gql(
            """
            mutation($input: CreateProjectV2FieldInput!) {
              createProjectV2Field(input: $input) {
                projectV2Field { ... on ProjectV2Field { id name } }
              }
            }
            """,
            {
                "input": {
                    "projectId": project_id,
                    "dataType": "DATE",
                    "name": name,
                }
            },
        )
        return data["createProjectV2Field"]["projectV2Field"]["id"]
    except RuntimeError as e:
        print(f"  warn: could not create DATE field '{name}': {e}", file=sys.stderr)
        return None


def ensure_views(project_id: str, views: list[dict]) -> None:
    by_name = {(v.get("name") or ""): v for v in views}
    # Rename default View 1 → Board if Board missing
    if "Board" not in by_name and "View 1" in by_name:
        v = by_name["View 1"]
        print("  Renaming 'View 1' → 'Board' (board layout)…")
        gql(
            """
            mutation($input: UpdateProjectV2ViewInput!) {
              updateProjectV2View(input: $input) { projectV2View { id name } }
            }
            """,
            {
                "input": {
                    "viewId": v["id"],
                    "name": "Board",
                    "layout": "BOARD_LAYOUT",
                    "filter": None,
                }
            },
        )
        by_name["Board"] = {**v, "name": "Board", "layout": "BOARD_LAYOUT"}
        del by_name["View 1"]

    for name, layout, filt in VIEWS:
        if name in by_name:
            cur = by_name[name]
            need_update = (cur.get("layout") != layout) or (
                (cur.get("filter") or None) != filt
            )
            if need_update:
                print(f"  Updating view '{name}' (layout={layout}, filter={filt})…")
                inp: dict[str, Any] = {
                    "viewId": cur["id"],
                    "name": name,
                    "layout": layout,
                }
                if filt is not None:
                    inp["filter"] = filt
                else:
                    inp["filter"] = ""
                gql(
                    """
                    mutation($input: UpdateProjectV2ViewInput!) {
                      updateProjectV2View(input: $input) { projectV2View { id name } }
                    }
                    """,
                    {"input": inp},
                )
            else:
                print(f"  View '{name}' already ok.")
            continue
        print(f"  Creating view '{name}' ({layout})…")
        data = gql(
            """
            mutation($input: CreateProjectV2ViewInput!) {
              createProjectV2View(input: $input) {
                projectV2View { id name }
              }
            }
            """,
            {
                "input": {
                    "projectId": project_id,
                    "name": name,
                    "layout": layout,
                }
            },
        )
        view_id = data["createProjectV2View"]["projectV2View"]["id"]
        if filt:
            gql(
                """
                mutation($input: UpdateProjectV2ViewInput!) {
                  updateProjectV2View(input: $input) { projectV2View { id } }
                }
                """,
                {"input": {"viewId": view_id, "filter": filt}},
            )


def main() -> None:
    # Progress → stderr; machine JSON → stdout (for gtd-setup-github.sh)
    import builtins

    real_print = builtins.print

    def print_stderr(*args, **kwargs):
        kwargs.setdefault("file", sys.stderr)
        real_print(*args, **kwargs)

    builtins.print = print_stderr  # type: ignore

    print(f"GitHub GTD setup (owner={OWNER}, title={TITLE})…")
    node_id, number, url = find_or_create_project()
    print(f"  Project #{number} id={node_id}")
    proj = load_project(node_id)
    fields = proj.get("fields", {}).get("nodes") or []

    print("Fields:")
    ensure_single_select(node_id, fields, "Status", STATUS_OPTIONS)
    proj = load_project(node_id)
    fields = proj.get("fields", {}).get("nodes") or []
    ensure_single_select(node_id, fields, "Duration", DURATION_OPTIONS)
    proj = load_project(node_id)
    fields = proj.get("fields", {}).get("nodes") or []
    ensure_single_select(node_id, fields, "Context", CONTEXT_OPTIONS)
    proj = load_project(node_id)
    fields = proj.get("fields", {}).get("nodes") or []
    ensure_single_select(node_id, fields, "Chunk", CHUNK_OPTIONS)
    proj = load_project(node_id)
    fields = proj.get("fields", {}).get("nodes") or []
    ensure_date_field(node_id, fields, "Due")

    proj = load_project(node_id)
    views = proj.get("views", {}).get("nodes") or []
    print("Views:")
    ensure_views(node_id, views)

    login = resolve_login()
    builtins.print = real_print  # type: ignore
    real_print(
        json.dumps(
            {
                "owner": login,
                "project_number": number,
                "project_id": node_id,
                "url": url,
                "status_field": "Status",
                "inbox_status": "Inbox",
                "status_options": [n for n, _, _ in STATUS_OPTIONS],
                "views": [n for n, _, _ in VIEWS],
            }
        )
    )


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        print(e.stderr or e, file=sys.stderr)
        raise SystemExit(1)
    except RuntimeError as e:
        print(e, file=sys.stderr)
        raise SystemExit(1)
