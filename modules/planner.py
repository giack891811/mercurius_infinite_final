"""
Modulo: planner.py
Responsabilità: Pianificazione strategica delle azioni in base a obiettivi e contesto
Autore: Mercurius∞ Engineer Mode
"""

from typing import List, Dict, Any


class ActionPlanner:
    """
    Planner strategico per sequenziare azioni sulla base di obiettivi e contesto.
    """

    def __init__(self):
        self.last_plan: List[Dict[str, Any]] = []

    def generate_plan(self, goal: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Genera una sequenza di azioni per raggiungere un obiettivo dato il contesto.
        """
        # Placeholder semplice. In futuro: agenti LLM o regole fuzzy.
        plan = []

        if goal == "analizza_ambiente":
            plan.append({"action": "attiva_sensori", "params": {"tipo": "ambientali"}})
            plan.append({"action": "acquisisci_dati"})
            plan.append({"action": "valuta_rischi"})

        elif goal == "raggiungi_destinazione":
            plan.append({"action": "calcola_percorso", "params": {"destinazione": context.get("destinazione")}})
            plan.append({"action": "avvia_navigazione"})
            plan.append({"action": "monitoraggio_progresso"})

        elif goal == "interagisci_utente":
            plan.append({"action": "saluta"})
            plan.append({"action": "richiedi_input"})
            plan.append({"action": "rispondi"})

        else:
            plan.append({"action": "log", "params": {"messaggio": f"Nessun piano noto per '{goal}'"}})

        self.last_plan = plan
        return plan

    def describe_plan(self, plan: List[Dict[str, Any]]) -> str:
        """
        Descrive verbalmente un piano d'azione.
        """
        description = "Piano d'azione:\n"
        for step in plan:
            description += f" - {step['action']}"
            if "params" in step:
                description += f" con parametri {step['params']}"
            description += "\n"
        return description

    def validate_plan(self, plan: List[Dict[str, Any]]) -> bool:
        """
        Verifica che il piano contenga azioni ben definite.
        """
        for step in plan:
            if not isinstance(step.get("action"), str):
                return False
        return True

    def plan_summary(self) -> Dict[str, Any]:
        """
        Riepilogo dell'ultimo piano generato.
        """
        return {
            "step_count": len(self.last_plan),
            "actions": [step["action"] for step in self.last_plan]
        }
