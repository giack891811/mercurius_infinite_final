# culture/culture_manager.py

"""
Modulo: culture_manager.py
Descrizione: Gestione dell'evoluzione concettuale e culturale interna dell'intelligenza Mercurius∞.
Salva ed espande concetti astratti in learning_pulses.json.
"""

import json
import os
from datetime import datetime

PULSES_PATH = "data/learning_pulses.json"


class CultureManager:
    def __init__(self):
        os.makedirs(os.path.dirname(PULSES_PATH), exist_ok=True)
        if not os.path.exists(PULSES_PATH):
            with open(PULSES_PATH, "w") as f:
                json.dump([], f)
        with open(PULSES_PATH, "r") as f:
            self.pulses = json.load(f)

    def update_concepts_from_experience(self, entry: str, origin: str = "simulation", confidence: float = 0.85):
        """
        Aggiunge un concetto evolutivo al file pulses.
        """
        pulse = {
            "concept": entry,
            "origin": origin,
            "confidence": confidence,
            "timestamp": datetime.now().isoformat()
        }
        self.pulses.append(pulse)
        with open(PULSES_PATH, "w") as f:
            json.dump(self.pulses, f, indent=2)
