import os
import pathspec
from utils import is_binary_file

# Hard exclusions (never shown)
ALWAYS_IGNORE_DIRS = {
    ".git", ".idea", ".venv", "__pycache__"
}

ALWAYS_IGNORE_FILES = {
    ".gitignore"
}


def load_gitignore(path):
    if not os.path.exists(path):
        return None

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.read().splitlines()

    return pathspec.PathSpec.from_lines("gitwildmatch", lines)


def scan_repository(repo_root):
    structure = []
    contents = []

    repo_root = os.path.abspath(repo_root)

    def walk(current_path, parent_spec, depth):
        rel_path = os.path.relpath(current_path, repo_root)
        rel_path = "" if rel_path == "." else rel_path

        folder_name = os.path.basename(current_path) or os.path.basename(repo_root)

        # 🔥 HARD IGNORE (folder-level)
        if folder_name in ALWAYS_IGNORE_DIRS:
            return

        # 🔥 GITIGNORE IGNORE (folder-level)
        if parent_spec and parent_spec.match_file(rel_path):
            return

        # Load local .gitignore AFTER folder is accepted
        local_gitignore = os.path.join(current_path, ".gitignore")
        local_spec = load_gitignore(local_gitignore)

        # Merge ignore rules
        if parent_spec and local_spec:
            spec = pathspec.PathSpec(parent_spec.patterns + local_spec.patterns)
        else:
            spec = local_spec or parent_spec

        indent = "│   " * depth
        structure.append(f"{indent}📁 {folder_name}/")

        try:
            entries = sorted(os.listdir(current_path))
        except PermissionError:
            return

        for entry in entries:
            full_entry = os.path.join(current_path, entry)
            rel_entry = os.path.relpath(full_entry, repo_root)
            entry_indent = "│   " * (depth + 1)

            # 🔥 HARD IGNORE (file/folder)
            if entry in ALWAYS_IGNORE_DIRS or entry in ALWAYS_IGNORE_FILES:
                continue

            # 🔥 GITIGNORE IGNORE
            if spec and spec.match_file(rel_entry):
                continue

            if os.path.isdir(full_entry):
                walk(full_entry, spec, depth + 1)

            elif os.path.isfile(full_entry):
                structure.append(f"{entry_indent}📄 {entry}")

                if is_binary_file(full_entry):
                    continue

                try:
                    with open(full_entry, "r", encoding="utf-8", errors="ignore") as f:
                        contents.append({
                            "path": rel_entry,
                            "content": f.read()
                        })
                except Exception:
                    contents.append({
                        "path": rel_entry,
                        "content": "[ERROR READING FILE]"
                    })

    walk(repo_root, None, 0)
    return structure, contents
