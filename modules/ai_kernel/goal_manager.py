"""
Modulo: goal_manager
Descrizione: Gestione degli obiettivi e sotto-obiettivi dell'agente Mercurius∞.
Autore: Mercurius∞ AI Engineer
"""

from datetime import datetime
import uuid

class Goal:
    def __init__(self, description: str, priority: int = 5):
        self.id = str(uuid.uuid4())
        self.description = description
        self.priority = priority
        self.created_at = datetime.now()
        self.completed = False

    def mark_completed(self):
        self.completed = True

class GoalManager:
    def __init__(self):
        self.goals = []

    def add_goal(self, description: str, priority: int = 5):
        goal = Goal(description, priority)
        self.goals.append(goal)
        return goal

    def list_active_goals(self):
        return [g for g in self.goals if not g.completed]

    def get_next_goal(self):
        active = self.list_active_goals()
        return sorted(active, key=lambda g: g.priority)[0] if active else None

    def complete_goal(self, goal_id: str):
        for g in self.goals:
            if g.id == goal_id:
                g.mark_completed()
                return g
        return None

# Test interattivo
if __name__ == "__main__":
    gm = GoalManager()
    gm.add_goal("Analizza segnali economici", 1)
    gm.add_goal("Controlla parametri ambientali", 3)
    gm.add_goal("Salva log missione", 7)

    print("Prossimo obiettivo:", gm.get_next_goal().description)
