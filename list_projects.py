#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path

HOME = Path.home()

SKIP = {
    "__pycache__", "node_modules", "dist", "build", "target",
    "venv", "env", ".venv", ".env", "vendor", "coverage",
    "tmp", "temp", "logs", "log",
    "src", "public", "app", "lib", "pkg", "cmd", "internal",
    "static", "templates", "assets", "migrations", "tests",
    "docs", "scripts", "config", "configs",
}


def get_root_dirs() -> list[str]:
    raw = os.getenv("project_dirs", "~/Projects")
    return [d.strip() for d in raw.split(",") if d.strip()]


def is_project_dir(path: Path) -> bool:
    return path.is_dir() and not path.name.startswith(".") and path.name not in SKIP


def collect_projects() -> list[dict]:
    items = []
    for raw_dir in get_root_dirs():
        root = Path(raw_dir).expanduser().resolve()
        if not root.is_dir():
            continue
        items.append(make_item(root))
        for child in sorted(root.iterdir()):
            if not is_project_dir(child):
                continue
            items.append(make_item(child))
            for grandchild in sorted(child.iterdir()):
                if not is_project_dir(grandchild):
                    continue
                items.append(make_item(grandchild))
    return items


def make_item(path: Path) -> dict:
    rel = f"~/{path.relative_to(HOME)}" if path.is_relative_to(HOME) else str(path)
    return {
        "title": path.name,
        "subtitle": rel,
        "arg": str(path),
        "autocomplete": f"{rel}/",
    }


def browse_path(query: str) -> list[dict]:
    path = Path(query.rstrip("/")).expanduser().resolve()
    items = []
    if path.is_dir():
        rel = f"~/{path.relative_to(HOME)}" if path.is_relative_to(HOME) else str(path)
        items.append({
            "title": f">> Open {path.name}",
            "subtitle": rel,
            "arg": str(path),
        })
        for child in sorted(path.iterdir()):
            if child.is_dir() and not child.name.startswith("."):
                items.append(make_item(child))
    elif path.parent.is_dir():
        prefix = path.name.lower()
        for child in sorted(path.parent.iterdir()):
            if child.is_dir() and not child.name.startswith(".") and child.name.lower().startswith(prefix):
                items.append(make_item(child))
    return items


def main():
    query = sys.argv[1].strip() if len(sys.argv) > 1 else ""
    if query.startswith(("~", "/")):
        items = browse_path(query)
    elif query:
        q = query.lower()
        items = [i for i in collect_projects() if q in i["subtitle"].lower()]
    else:
        items = collect_projects()
    print(json.dumps({"items": items or [{"title": "No matches", "valid": False}]}))


if __name__ == "__main__":
    main()
