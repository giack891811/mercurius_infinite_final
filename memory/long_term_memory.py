\"\"\"Long-Term Memory – API semplificata per persistenza conoscenza.  
Attualmente salva/carica in JSON locale (placeholder).
\"\"\"

import json
from pathlib import Path
from utils.logger import setup_logger

logger = setup_logger(__name__)
MEM_PATH = Path("data") / "lt_memory.json"
MEM_PATH.parent.mkdir(exist_ok=True, parents=True)

def load_memory() -> dict:
    if not MEM_PATH.exists():
        return {}
    try:
        return json.loads(MEM_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        logger.warning("Corruzione memoria, reset.")
        return {}

def save_memory(data: dict):
    MEM_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def append(key: str, value):
    mem = load_memory()
    mem.setdefault(key, []).append(value)
    save_memory(mem)