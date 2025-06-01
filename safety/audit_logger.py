# safety/audit_logger.py
"""
Modulo: audit_logger
Descrizione: Log di audit immutabile per registrare azioni, decisioni e override.
"""

from pathlib import Path
from datetime import datetime
import json

AUDIT_FILE = Path("logs/audit_log.jsonl")
AUDIT_FILE.parent.mkdir(parents=True, exist_ok=True)


def audit(event_type: str, details: dict):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "type": event_type,
        "details": details,
    }
    with open(AUDIT_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
