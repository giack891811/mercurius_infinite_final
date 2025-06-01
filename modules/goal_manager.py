"""
Modulo: goal_manager.py
Descrizione: Gestione di obiettivi (Goal) con priorità, stato e contesto.
Autore: Mercurius∞ AI Engineer
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass(order=False)  # disattiva ordinamento automatico
class Goal:
    name: str
    priority: int = 1
    context: Dict[str, Any] = field(default_factory=dict)
    done: bool = False
    status: str = "pending"  # possible values: pending, active, completed

class GoalManager:
    def __init__(self):
        self._goals: List[Goal] = []

    # --- API principale ---
    def add_goal(self, name: str, priority: int = 1, context: Optional[Dict[str, Any]] = None):
        self._goals.append(Goal(name=name, priority=priority, context=context or {}))
        # ordina per PRIORITÀ decrescente (priorità alta prima)
        self._goals.sort(key=lambda g: g.priority, reverse=True)

    def get_next_goal(self) -> Optional[Goal]:
        for g in self._goals:
            if not g.done:
                g.status = "active"  # aggiorna lo stato a active
                return g
        return None

    def complete_goal(self, name: str):
        for g in self._goals:
            if g.name == name:
                g.done = True
                g.status = "completed"
                break

    def list_goals(self) -> List[Goal]:
        return self._goals

    def active_goals(self) -> List[Goal]:
        """Restituisce la lista di goal attivi (status active e non done)."""
        return [g for g in self._goals if g.status == "active" and not g.done]

# Esempio di utilizzo
if __name__ == "__main__":
    gm = GoalManager()
    gm.add_goal("Scrivere report", priority=5)
    gm.add_goal("Debug sistema", priority=10)
    next_goal = gm.get_next_goal()
    print("Goal attivo:", next_goal)
    gm.complete_goal(next_goal.name)
    print("Lista goal:", gm.list_goals())
