# analytics/behavior_logger.py
"""
Modulo: behavior_logger.py
Descrizione: Log comportamentale centralizzato per Mercurius∞.
Registra errori, fallback, performance-hit e successi in un file JSONL con TTL.
"""

from pathlib import Path
from datetime import datetime
import json
import hashlib

LOG_FILE = Path("logs/behavior_log.jsonl")
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)


class BehaviorLogger:
    def __init__(self):
        self.file = LOG_FILE

    def log(self, event: str, details: dict):
        entry = {
            "ts": datetime.utcnow().isoformat(),
            "event": event,
            "hash": hashlib.md5(event.encode()).hexdigest()[:6],
            "details": details,
        }
        with self.file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    def tail(self, n: int = 100):
        if not self.file.exists():
            return []
        return self.file.read_text(encoding="utf-8").splitlines()[-n:]
