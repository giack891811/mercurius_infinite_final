#!/usr/bin/env python3
"""Generate project_tree.txt with the repository tree and file previews."""
import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
OUTPUT_FILE = ROOT_DIR / 'project_tree.txt'
MAX_LINES = 100
# File extensions considered text and included in preview
TEXT_EXTENSIONS = {
    '.py', '.json', '.md', '.txt', '.yml', '.yaml', '.ini', '.cfg', '.toml', '.js', '.ts'
}


def generate_tree():
    tree_lines = []
    text_files = []
    for root, dirs, files in os.walk(ROOT_DIR):
        if '.git' in dirs:
            dirs.remove('.git')
        dirs.sort()
        files.sort()
        level = Path(root).relative_to(ROOT_DIR).parts
        indent = '    ' * len(level)
        tree_lines.append(f"{indent}{Path(root).name}/")
        for name in files:
            tree_lines.append(f"{indent}    {name}")
            ext = Path(name).suffix.lower()
            if ext in TEXT_EXTENSIONS:
                text_files.append(Path(root) / name)
    return tree_lines, text_files


def read_snippet(file_path: Path):
    lines = []
    truncated = False
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for idx, line in enumerate(f):
                if idx >= MAX_LINES:
                    truncated = True
                    break
                lines.append(line.rstrip('\n'))
    except Exception as exc:
        lines.append(f"[Errore lettura: {exc}]")
    return lines, truncated


def main():
    tree_lines, text_files = generate_tree()
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out:
        out.write('PROJECT TREE\n')
        out.write('\n'.join(tree_lines))
        out.write('\n\nFILE PREVIEW\n')
        for file in text_files:
            rel = file.relative_to(ROOT_DIR)
            out.write(f"\n## {rel}\n")
            lines, truncated = read_snippet(file)
            for l in lines:
                out.write(l + '\n')
            if truncated:
                out.write('[TRONCATO]\n')


if __name__ == '__main__':
    main()
