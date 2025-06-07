import os
from pathlib import Path

# File extensions to include
EXTENSIONS = {'.py', '.json', '.yaml', '.yml', '.md', '.toml', '.txt'}

ROOT_DIR = Path(__file__).resolve().parent
OUTPUT_FILE = ROOT_DIR / 'project_tree'

def should_include(path: Path) -> bool:
    """Return True if file should be included in the project tree."""
    if '.git' in path.parts:
        return False
    return path.is_file() and path.suffix.lower() in EXTENSIONS

def collect_files(root: Path):
    return sorted(p for p in root.rglob('*') if should_include(p))

def build_tree(files):
    lines = []
    for file_path in files:
        rel = file_path.relative_to(ROOT_DIR)
        lines.append(f"### --- {rel.as_posix()} --- ###")
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
        lines.append(content.rstrip('\n'))
        lines.append('')
    return '\n'.join(lines) + '\n'

def main():
    files = collect_files(ROOT_DIR)
    tree_content = build_tree(files)
    OUTPUT_FILE.write_text(tree_content, encoding='utf-8')

if __name__ == '__main__':
    main()
