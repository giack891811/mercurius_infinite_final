"""
Test: test_orchestrator.py
Responsabilità: Validazione AutonomyController e processi decisionali
Autore: Mercurius∞ Engineer Mode
"""

import unittest
from orchestrator.autonomy_controller import AutonomyController


class TestAutonomyController(unittest.TestCase):

    def setUp(self):
        self.controller = AutonomyController()

    def test_process_experience(self):
        """
        Valida la riflessione e l'apprendimento su azione positiva.
        """
        feedback = self.controller.process_experience(
            action="test_comando",
            outcome="Eseguito correttamente",
            success=True,
            context={"livello": "base"}
        )
        self.assertIn("Apprendimento", feedback["learning"])
        self.assertIn("successo", feedback["reflection"])

    def test_summarize_autonomy(self):
        """
        Verifica il report cognitivo riepilogativo.
        """
        self.controller.process_experience("cmd", "done", True, {})
        summary = self.controller.summarize_autonomy()
        self.assertIn("successes", summary["reflection_summary"])


if __name__ == "__main__":
    unittest.main()
