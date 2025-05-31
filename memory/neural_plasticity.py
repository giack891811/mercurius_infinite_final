# memory/neural_plasticity.py

"""
Estensione: Plasticità neurale dinamica di Mercurius∞
Descrizione: Mappa adattiva della frequenza di utilizzo dei moduli e suggerimenti di rinforzo o disattivazione.
"""

import json
import os
from datetime import datetime

class NeuralPlasticity:
    def __init__(self, map_path="memory/plasticity_map.json"):
        self.map_path = map_path
        self.map = self.load_map()

    def load_map(self):
        if os.path.exists(self.map_path):
            with open(self.map_path, "r") as f:
                return json.load(f)
        return {}

    def save_map(self):
        with open(self.map_path, "w") as f:
            json.dump(self.map, f, indent=2)

    def track_usage(self, module_name: str):
        if module_name not in self.map:
            self.map[module_name] = {"count": 0, "last_used": None}
        self.map[module_name]["count"] += 1
        self.map[module_name]["last_used"] = datetime.now().isoformat()
        self.save_map()

    def recommend_adaptation(self) -> list:
        sorted_usage = sorted(self.map.items(), key=lambda x: x[1]["count"], reverse=True)
        return [f"{mod[0]} → {mod[1]['count']} utilizzi" for mod in sorted_usage[:5]]

    def strengthen_pathways(self):
        adaptations = self.recommend_adaptation()
        print("🔧 Rinforzo neurale per i moduli più utilizzati:")
        for line in adaptations:
            print(f"  ⚡ {line}")
        return adaptations
