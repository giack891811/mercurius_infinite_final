import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
SOURCE_FILE = ROOT_DIR / 'project_tree'
PART_PREFIX = 'project_tree_part'
MAX_LINES = 17000


def split_file():
    if not SOURCE_FILE.exists():
        raise FileNotFoundError(f"{SOURCE_FILE} not found")
    content = SOURCE_FILE.read_text(encoding='utf-8').splitlines()
    total_lines = len(content)
    num_parts = (total_lines + MAX_LINES - 1) // MAX_LINES

    for i in range(1, num_parts + 1):
        start = (i - 1) * MAX_LINES
        end = i * MAX_LINES
        part_lines = content[start:end]
        part_path = ROOT_DIR / f"{PART_PREFIX}{i}.txt"
        part_path.write_text("\n".join(part_lines) + "\n", encoding='utf-8')

    # remove old part files if number decreased
    idx = num_parts + 1
    while True:
        extra_path = ROOT_DIR / f"{PART_PREFIX}{idx}.txt"
        if extra_path.exists():
            extra_path.unlink()
            idx += 1
        else:
            break


if __name__ == '__main__':
    split_file()
