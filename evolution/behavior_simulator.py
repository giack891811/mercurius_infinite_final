# evolution/behavior_simulator.py

"""
Modulo: behavior_simulator.py
Descrizione: Simula scenari comportamentali per Mercurius∞ e valuta le risposte.
Utilizza la memoria episodica per registrare gli esiti.
"""

from typing import Dict
from memory.episodic_memory import EpisodicMemory
from memory.synaptic_log import SynapticLog


class BehaviorSimulator:
    def __init__(self):
        self.memory = EpisodicMemory()
        self.log = SynapticLog()

    def simulate_behavior_scenario(self, scenario: Dict) -> None:
        """
        Simula un comportamento e registra l'episodio risultante.
        """
        context = scenario.get("context", "default_behavior_test")
        user_input = scenario.get("stimulus", "Simulazione di risposta")
        ai_response = scenario.get("expected_response", "Risposta AI simulata")

        self.memory.record_episode(context, user_input, ai_response)
        self.log.log_event("BehaviorSimulator", "Simulated Scenario", f"{context} -> {ai_response}")
