import os
import pathspec
from utils.file_utils import (
    is_binary_file,
    is_large_file,
    looks_binary_by_content
)

ALWAYS_IGNORE_DIRS = {".git", ".idea", ".venv", "__pycache__"}
ALWAYS_IGNORE_FILES = {".gitignore"}


def load_gitignore(path):
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8", errors="ignore") as f:
        return pathspec.PathSpec.from_lines("gitwildmatch", f.read().splitlines())


def scan_repository(repo_root):
    repo_root = os.path.abspath(repo_root)

    structure = []
    contents = []
    stats = dict(
        files_total=0,
        files_dumped=0,
        files_skipped=0,
        folders_total=0
    )

    def walk(path, parent_spec, depth):
        name = os.path.basename(path)
        rel = os.path.relpath(path, repo_root)
        rel = "" if rel == "." else rel

        if name in ALWAYS_IGNORE_DIRS:
            return

        if parent_spec and parent_spec.match_file(rel):
            return

        local_spec = load_gitignore(os.path.join(path, ".gitignore"))
        spec = (
            pathspec.PathSpec(parent_spec.patterns + local_spec.patterns)
            if parent_spec and local_spec
            else local_spec or parent_spec
        )

        indent = "│   " * depth
        structure.append(f"{indent}📁 {name}/")
        stats["folders_total"] += 1

        for entry in sorted(os.listdir(path)):
            full = os.path.join(path, entry)
            rel_entry = os.path.relpath(full, repo_root)

            if entry in ALWAYS_IGNORE_DIRS or entry in ALWAYS_IGNORE_FILES:
                continue
            if spec and spec.match_file(rel_entry):
                continue

            entry_indent = "│   " * (depth + 1)

            if os.path.isdir(full):
                walk(full, spec, depth + 1)

            elif os.path.isfile(full):
                stats["files_total"] += 1
                structure.append(f"{entry_indent}📄 {entry}")

                if (
                    is_binary_file(full)
                    or looks_binary_by_content(full)
                    or is_large_file(full)
                ):
                    stats["files_skipped"] += 1
                    contents.append({
                        "path": rel_entry,
                        "content": "[BINARY / MEDIA FILE SKIPPED]"
                    })
                    continue

                with open(full, encoding="utf-8", errors="ignore") as f:
                    contents.append({
                        "path": rel_entry,
                        "content": f.read()
                    })
                    stats["files_dumped"] += 1

    walk(repo_root, None, 0)
    return structure, contents, stats
