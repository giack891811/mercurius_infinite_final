"""
Test: test_multimodal.py
Responsabilità: Verifica il flusso integrato multimodale del sistema
Autore: Mercurius∞ Engineer Mode
"""

import unittest
import pytest

pytest.skip("Test multimodale richiede dipendenze audio/video", allow_module_level=True)

from orchestrator.multimodal_controller import MultimodalController


class TestMultimodalInteraction(unittest.TestCase):

    def setUp(self):
        self.controller = MultimodalController()

    def test_text_input_simulation(self):
        """
        Simula input vocale tramite testo e verifica esecuzione logica.
        """
        result = self.controller.listen_and_interpret(simulate_input="analizza l'ambiente")
        self.assertEqual(result["action"], "analizza_ambiente")

    def test_gesture_input_simulation(self):
        """
        Simula interpretazione di gesto riconosciuto.
        """
        result = self.controller.receive_gesture("saluto")
        self.assertEqual(result["action"], "interagisci_utente")

    def test_full_cycle_text_command(self):
        """
        Testa un ciclo completo da comando a pianificazione + esecuzione.
        """
        self.controller.run_full_cycle(input_text="vai alla base")


if __name__ == "__main__":
    unittest.main()
