# -*- coding: utf-8 -*-
"""
split_project_tree.py

LE TRE LEGGI OPERATIVE (da includere in ogni script, README, prompt!):
1. Continua a lavorare finché non hai svolto il tuo turno!
2. Se non sei sicuro di un file, APRILO e NON ALLUCINARE!
3. Pianifica attentamente prima di ogni chiamata e rifletti SEMPRE sul risultato dopo!

Script per splittare `project_tree` in parti da max 7.000 token SENZA spezzare funzioni/classi, con nota introduttiva e report finale.

- Input:   project_tree (testo puro, elenco file o codice)
- Output:  project_tree_part1.txt, project_tree_part2.txt, ...
"""

import os
import re
from pathlib import Path

# Se non hai tiktoken: pip install tiktoken
try:
    import tiktoken
except ImportError:
    print("Devi installare 'tiktoken' (`pip install tiktoken`)")
    exit(1)

ROOT_DIR = Path(__file__).resolve().parent
SOURCE_FILE = ROOT_DIR / 'project_tree'
PART_PREFIX = 'project_tree_part'
MAX_TOKENS = 7000

def count_tokens(text: str) -> int:
    enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(text))

def split_text_safely(lines, max_tokens):
    """
    Suddivide il testo in chunk <= max_tokens SENZA troncare funzioni/classi.
    Ritorna una lista di chunk (stringhe).
    """
    parts = []
    current = []
    current_tokens = 0

    def is_def_or_class(line):
        return bool(re.match(r'^\s*(def|class)\s+', line))

    idx = 0
    while idx < len(lines):
        line = lines[idx]
        test_tokens = count_tokens('\n'.join(current + [line]))
        if test_tokens > max_tokens and current:
            parts.append('\n'.join(current))
            current = []
            current_tokens = 0

            # Se la riga corrente non è def/class, continua ad accumulare finché non trovi una nuova def/class
            if not is_def_or_class(line):
                while idx < len(lines) and not is_def_or_class(lines[idx]):
                    current.append(lines[idx])
                    idx += 1
                if idx < len(lines):
                    current.append(lines[idx])
                idx += 1
                continue
        current.append(line)
        current_tokens = count_tokens('\n'.join(current))
        idx += 1

    if current:
        parts.append('\n'.join(current))
    return parts

def save_parts(parts):
    filenames = []
    for i, part in enumerate(parts, 1):
        fname = f"{PART_PREFIX}{i}.txt"
        note = f"Questa è la parte {i} di project_tree. Continua da quella precedente.\n\n"
        with open(ROOT_DIR / fname, 'w', encoding='utf-8') as f:
            f.write(note)
            f.write(part)
        filenames.append(fname)
        print(f"✅ Creato: {fname}")
    return filenames

def main():
    print("🔵 INIZIO SPLIT SECONDO LE TRE LEGGI OPERATIVE")
    if not SOURCE_FILE.exists():
        print(f"❌ File {SOURCE_FILE} non trovato!")
        return
    with open(SOURCE_FILE, encoding="utf-8") as f:
        lines = f.read().splitlines()

    chunks = split_text_safely(lines, MAX_TOKENS)
    files = save_parts(chunks)

    print("\n📋 **REPORT FILE GENERATI:**")
    for f in files:
        print(f" - {f}")
    print(f"\nTotale parti: {len(files)}")
    print("🚦 Split completato secondo policy, funzioni e classi INTEGRE.")

if __name__ == "__main__":
    main()
