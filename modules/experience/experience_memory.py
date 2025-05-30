"""
experience_memory.py
====================
Memoria evolutiva esperienziale per il sistema Mercurius∞.
Registra trade, segnali e risultati. Alimenta i moduli AZR.
"""

import json
import os
from datetime import datetime


class ExperienceMemory:
    def __init__(self, config, storage_path="memory/experience_log.json"):
        self.config = config
        self.storage_path = storage_path
        self.history = []

        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        self._load()

    def _load(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r") as f:
                    self.history = json.load(f)
            except Exception:
                self.history = []

    def _save(self):
        with open(self.storage_path, "w") as f:
            json.dump(self.history, f, indent=2)

    def record_experience(self, signal, trade, result, feedback):
        self.history.append({
            "timestamp": datetime.utcnow().isoformat(),
            "signal": signal,
            "trade": trade,
            "result": result,
            "feedback": feedback
        })
        self._save()

    def get_recent_experiences(self, limit=10):
        return self.history[-limit:]

    def reset(self):
        self.history.clear()
        self._save()

    def summarize(self):
        return {
            "total": len(self.history),
            "last_timestamp": self.history[-1]["timestamp"] if self.history else None
        }
