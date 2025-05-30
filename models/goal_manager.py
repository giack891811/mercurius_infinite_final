"""
Modulo: goal_manager.py
Responsabilità: Gestione dinamica e gerarchica degli obiettivi del sistema
Autore: Mercurius∞ Engineer Mode
"""

from typing import List, Dict


class Goal:
    def __init__(self, name: str, priority: int = 1, context: Dict = None):
        self.name = name
        self.priority = priority
        self.context = context or {}
        self.status = "pending"  # può essere: pending, active, completed, failed

    def __repr__(self):
        return f"<Goal: {self.name}, priority={self.priority}, status={self.status}>"

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "priority": self.priority,
            "context": self.context,
            "status": self.status
        }


class GoalManager:
    """
    Gestore degli obiettivi a breve/lungo termine.
    """

    def __init__(self):
        self.goals: List[Goal] = []

    def add_goal(self, name: str, priority: int = 1, context: Dict = None):
        self.goals.append(Goal(name, priority, context))
        self.sort_goals()

    def sort_goals(self):
        self.goals.sort(key=lambda g: g.priority, reverse=True)

    def get_next_goal(self) -> Goal:
        for goal in self.goals:
            if goal.status == "pending":
                goal.status = "active"
                return goal
        return None

    def complete_goal(self, name: str):
        for goal in self.goals:
            if goal.name == name:
                goal.status = "completed"
                return True
        return False

    def fail_goal(self, name: str):
        for goal in self.goals:
            if goal.name == name:
                goal.status = "failed"
                return True
        return False

    def active_goals(self) -> List[Goal]:
        return [g for g in self.goals if g.status == "active"]

    def pending_goals(self) -> List[Goal]:
        return [g for g in self.goals if g.status == "pending"]

    def completed_goals(self) -> List[Goal]:
        return [g for g in self.goals if g.status == "completed"]

    def all_goals(self) -> List[Dict]:
        return [g.to_dict() for g in self.goals]
