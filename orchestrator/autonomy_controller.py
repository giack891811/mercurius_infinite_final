"""
Modulo: autonomy_controller.py
Responsabilità: Coordinare i moduli di riflessione e apprendimento continuo
Autore: Mercurius∞ Engineer Mode
"""

from core.self_reflection import SelfReflection
from core.learning import ContinuousLearner
from typing import Dict, Any


class AutonomyController:
    """
    Gestisce la riflessione cognitiva e l'apprendimento continuo del sistema.
    """

    def __init__(self):
        self.reflector = SelfReflection()
        self.learner = ContinuousLearner()

    def process_experience(self, action: str, outcome: str, success: bool, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Coordina riflessione e apprendimento dopo un'esperienza.
        """
        reflection = self.reflector.evaluate_action(action, outcome, success, context)
        learning = self.learner.learn_from_experience(action, outcome, success, context)

        return {
            "reflection": reflection["insight"],
            "learning": learning["insight"]
        }

    def summarize_autonomy(self) -> Dict[str, Any]:
        """
        Restituisce un riepilogo delle prestazioni cognitive.
        """
        reflection_stats = self.reflector.summarize_reflections()
        learning_stats = self.learner.stats()
        return {
            "reflection_summary": reflection_stats,
            "learning_summary": learning_stats
        }

    def report_insights(self) -> Dict[str, list]:
        """
        Riporta tutte le osservazioni generate finora.
        """
        return {
            "reflections": self.reflector.reflect_on_log(),
            "learnings": self.learner.retrieve_insights()
        }
