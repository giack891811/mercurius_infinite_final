"""
Modulo: strategic_coordinator
Descrizione: Coordina le strategie dinamiche basate su obiettivi, contesto e feedback AI.
Autore: Mercurius∞ AI Engineer
"""

from modules.ai_kernel.goal_manager import GoalManager

class StrategicCoordinator:
    def __init__(self, goal_manager: GoalManager):
        self.goal_manager = goal_manager

    def assess_situation(self, signals: dict):
        """Analizza i segnali in ingresso e decide se generare nuovi obiettivi"""
        if "minaccia" in signals and signals["minaccia"] > 0.8:
            self.goal_manager.add_goal("Esegui protocolli difensivi", priority=1)
        if "opportunita" in signals and signals["opportunita"] > 0.6:
            self.goal_manager.add_goal("Massimizza opportunità identificata", priority=2)

    def execute_strategy(self):
        """Restituisce il prossimo obiettivo da eseguire"""
        goal = self.goal_manager.get_next_goal()
        return goal.description if goal else "Nessun obiettivo attivo"

# Test autonomo
if __name__ == "__main__":
    gm = GoalManager()
    sc = StrategicCoordinator(gm)

    sc.assess_situation({"opportunita": 0.7, "minaccia": 0.2})
    print(sc.execute_strategy())
