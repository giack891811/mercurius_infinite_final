# memory/episodic_memory.py

"""
Modulo: episodic_memory.py
Descrizione: Gestione della memoria episodica per Mercurius∞. Salva e recupera eventi specifici
con dettagli temporali, contesto e risposta.
"""

import json
import os
from datetime import datetime
from typing import Dict, List

EPISODES_PATH = "data/memory/episodic_memory.json"


class EpisodicMemory:
    def __init__(self):
        os.makedirs(os.path.dirname(EPISODES_PATH), exist_ok=True)
        if not os.path.exists(EPISODES_PATH):
            with open(EPISODES_PATH, "w") as f:
                json.dump([], f)
        self._load_memory()

    def _load_memory(self):
        with open(EPISODES_PATH, "r") as f:
            self.episodes = json.load(f)

    def _save_memory(self):
        with open(EPISODES_PATH, "w") as f:
            json.dump(self.episodes, f, indent=2)

    def record_episode(self, context: str, user_input: str, ai_response: str):
        episode = {
            "timestamp": datetime.now().isoformat(),
            "context": context,
            "user_input": user_input,
            "ai_response": ai_response
        }
        self.episodes.append(episode)
        self._save_memory()

    def get_recent_episodes(self, limit: int = 10) -> List[Dict]:
        return self.episodes[-limit:]

    def search_episodes(self, keyword: str) -> List[Dict]:
        return [ep for ep in self.episodes if keyword.lower() in ep["user_input"].lower() or keyword.lower() in ep["ai_response"].lower()]
