# memory/synaptic_log.py

"""
Modulo: synaptic_log.py
Descrizione: Registro cronologico delle interazioni e modifiche sinaptiche della memoria cognitiva.
Utile per analisi, debug e tracciamento evolutivo del comportamento AI.
"""

import os
from datetime import datetime
from typing import Optional

LOG_PATH = "data/memory/synaptic_log.txt"


class SynapticLog:
    def __init__(self):
        os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
        if not os.path.exists(LOG_PATH):
            with open(LOG_PATH, "w") as f:
                f.write("=== Synaptic Log Initialized ===\n")

    def log_event(self, module: str, action: str, detail: Optional[str] = ""):
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] [{module}] {action}"
        if detail:
            log_entry += f" - {detail}"
        with open(LOG_PATH, "a") as f:
            f.write(log_entry + "\n")

    def get_log_tail(self, lines: int = 20) -> str:
        with open(LOG_PATH, "r") as f:
            return "\n".join(f.readlines()[-lines:])
