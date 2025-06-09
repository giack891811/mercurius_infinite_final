"""logical_state_tracker.py
Traccia lo stato logico e operativo di Mercurius∞.
"""

import json
import os
from datetime import datetime
from typing import Any, Dict

STATE_PATH = "data/memory/logical_state.json"


class LogicalStateTracker:
    def __init__(self):
        os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
        if os.path.exists(STATE_PATH):
            try:
                with open(STATE_PATH, "r", encoding="utf-8") as f:
                    self.state: Dict[str, Any] = json.load(f)
            except Exception:
                self.state = {}
        else:
            self.state = {}
            self._save()

    def _save(self):
        with open(STATE_PATH, "w", encoding="utf-8") as f:
            json.dump(self.state, f, ensure_ascii=False, indent=2)

    def update(self, key: str, value: Any) -> None:
        self.state[key] = {
            "value": value,
            "timestamp": datetime.now().isoformat()
        }
        self._save()

    def get(self, key: str) -> Any:
        return self.state.get(key, {}).get("value")

    def get_all(self) -> Dict[str, Any]:
        return self.state
