# consciousness/intention_manager.py
"""
Modulo: intention_manager.py
Descrizione: Gestisce i goal “intenzionali” di alto livello (desideri persistenti).
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any


class IntentionManager:
    def __init__(self):
        self.intentions: List[Dict[str, Any]] = []

    def add_intention(self, description: str, ttl_days: int = 30):
        expires = datetime.utcnow() + timedelta(days=ttl_days)
        self.intentions.append({"desc": description, "expires": expires})

    def active_intentions(self) -> List[str]:
        now = datetime.utcnow()
        self.intentions = [i for i in self.intentions if i["expires"] > now]
        return [i["desc"] for i in self.intentions]
