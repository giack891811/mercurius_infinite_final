"""
Test: test_end2end.py
Responsabilità: Simulazione di un flusso intero da input a pianificazione e log
Autore: Mercurius∞ Engineer Mode
"""

import unittest
import pytest

pytest.skip("Test End-to-End richiede dipendenze audio/video", allow_module_level=True)

from orchestrator.multimodal_controller import MultimodalController
from modules.supervisor import Supervisor


class TestEndToEnd(unittest.TestCase):

    def setUp(self):
        self.controller = MultimodalController()
        self.supervisor = Supervisor()

    def test_complete_workflow(self):
        """
        Simula ciclo completo da voce a comportamento e supervisione.
        """
        self.controller.run_full_cycle(input_text="parla con me")
        self.controller.run_full_cycle(input_text="analizza l'ambiente")
        self.controller.run_full_cycle(gesture="saluto")

        summary = self.controller.autonomy.summarize_autonomy()
        self.assertGreaterEqual(summary["reflection_summary"]["successes"], 2)

    def test_supervised_actions(self):
        """
        Simula log supervisionato indipendente.
        """
        self.supervisor.observe("auto-test", "OK", True, {"canale": "debug"})
        report = self.supervisor.performance_report()
        self.assertEqual(report["successes"], 1)


if __name__ == "__main__":
    unittest.main()
