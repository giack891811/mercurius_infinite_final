"""
strategic_coordinator.py

Modulo per la gestione del coordinamento strategico e della memoria sociale degli agenti AI.
Include:
- Mappatura degli obiettivi globali e locali
- Coordinamento delle missioni
- Memoria delle interazioni tra agenti
- Logica decisionale basata su priorità e storicità

Autore: Mercurius∞ System - Ciclo 020
"""

import json
import os
import random
from datetime import datetime
from pathlib import Path

MEMORY_PATH = Path("memory")
STRATEGIC_LOG = MEMORY_PATH / "strategy_log.json"
INTERACTION_LOG = MEMORY_PATH / "agent_interactions.json"
OBJECTIVES_FILE = MEMORY_PATH / "objectives_map.json"

class StrategicCoordinator:
    def __init__(self):
        self.memory_path = MEMORY_PATH
        self.memory_path.mkdir(parents=True, exist_ok=True)
        self.objectives = self._load_json(OBJECTIVES_FILE, default={})
        self.interactions = self._load_json(INTERACTION_LOG, default=[])
        self.strategy_log = self._load_json(STRATEGIC_LOG, default=[])

    def _load_json(self, path, default):
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return default

    def _save_json(self, path, data):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def map_objective(self, agent_name, objective, priority=1):
        if agent_name not in self.objectives:
            self.objectives[agent_name] = []
        self.objectives[agent_name].append({
            "objective": objective,
            "priority": priority,
            "timestamp": datetime.now().isoformat()
        })
        self._save_json(OBJECTIVES_FILE, self.objectives)

    def log_interaction(self, sender, receiver, topic):
        entry = {
            "from": sender,
            "to": receiver,
            "topic": topic,
            "time": datetime.now().isoformat()
        }
        self.interactions.append(entry)
        self._save_json(INTERACTION_LOG, self.interactions)

    def choose_agent_for_task(self, task_description):
        # Heuristic: agent with most recent matching objective
        best_agent = None
        best_score = -1
        for agent, objs in self.objectives.items():
            for obj in objs:
                if task_description.lower() in obj["objective"].lower():
                    score = obj["priority"] - (datetime.now().timestamp() - datetime.fromisoformat(obj["timestamp"]).timestamp()) / 3600
                    if score > best_score:
                        best_score = score
                        best_agent = agent
        return best_agent

    def log_strategy(self, strategy_description):
        entry = {
            "strategy": strategy_description,
            "timestamp": datetime.now().isoformat()
        }
        self.strategy_log.append(entry)
        self._save_json(STRATEGIC_LOG, self.strategy_log)

    def summarize_strategy_log(self):
        return self.strategy_log[-5:]

# ESEMPIO DI UTILIZZO
if __name__ == "__main__":
    sc = StrategicCoordinator()
    sc.map_objective("agent_brainstormer", "Ricercare nuovi modelli GPT per ragionamento strategico", priority=2)
    sc.log_interaction("agent_brainstormer", "agent_analyzer", "Richiesta analisi su nuovi modelli")
    print("Strategia recente:", sc.summarize_strategy_log())