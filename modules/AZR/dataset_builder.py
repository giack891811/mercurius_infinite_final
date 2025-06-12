"""Costruisce dataset JSONL a partire da file markdown."""

import json
from pathlib import Path


def md_to_jsonl(md_path: str, jsonl_path: str) -> None:
    md_file = Path(md_path)
    lines = md_file.read_text(encoding="utf-8").splitlines()
    entries = [
        {"prompt": line, "completion": ""} for line in lines if line.strip()
    ]
    with open(jsonl_path, "w", encoding="utf-8") as f:
        for e in entries:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")
