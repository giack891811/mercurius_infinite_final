#!/usr/bin/env python3
"""Create prompt.txt combining project tree and user commands."""
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
OUTPUT_FILE = ROOT_DIR / 'prompt.txt'
TREE_FILE = ROOT_DIR / 'project_tree.txt'
COMMANDS_FILE = ROOT_DIR / 'prompt_commands.txt'


def read_file(path: Path) -> str:
    return path.read_text(encoding='utf-8') if path.exists() else ''


def main():
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out:
        out.write('**STRUTTURA E FILE DEL PROGETTO:**\n')
        out.write(read_file(TREE_FILE))
        out.write('\n**ISTRUZIONI OPERATIVE:**\n')
        out.write(read_file(COMMANDS_FILE))


if __name__ == '__main__':
    main()
