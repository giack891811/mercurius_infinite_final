# cognition/task_memory.py
"""
Modulo: task_memory.py
Descrizione: Salvataggio outcome dei task per apprendere preferenze di routing.
"""

from collections import deque
from typing import Dict, Any, Deque, List


class TaskMemory:
    def __init__(self, maxlen: int = 2000):
        self.records: Deque[Dict[str, Any]] = deque(maxlen=maxlen)

    def add_record(self, agent: str, task: str, success: bool):
        self.records.append({"agent": agent, "task": task, "success": success})

    def agent_score(self, agent: str) -> float:
        """Percentuale di successi dell’agente."""
        entries = [r for r in self.records if r["agent"] == agent]
        if not entries:
            return 0.5
        ok = sum(1 for e in entries if e["success"])
        return ok / len(entries)

    def suggest_best(self, candidates: List[str]) -> str:
        """Ritorna l’agente col punteggio più alto tra i candidati."""
        return max(candidates, key=self.agent_score)
