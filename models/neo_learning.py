# modules/neo_learning.py

"""
Modulo: neo_learning.py
Descrizione: Sistema di apprendimento esperienziale per Mercurius∞.
Simula situazioni, osserva i risultati e aggiorna la memoria episodica in base all'esito.
"""

from typing import Dict
from memory.episodic_memory import EpisodicMemory
from memory.synaptic_log import SynapticLog


class NeoLearning:
    def __init__(self):
        self.memory = EpisodicMemory()
        self.logger = SynapticLog()

    def simulate_and_learn(self, experience: Dict) -> None:
        """
        Registra un'esperienza simulata nella memoria episodica e logga l'evento.
        """
        context = experience.get("context", "simulated")
        user_input = experience.get("scenario", "")
        ai_response = experience.get("outcome", "")
        self.memory.record_episode(context, user_input, ai_response)
        self.logger.log_event("NeoLearning", "Simulated Experience Learned", f"{context} -> {ai_response}")
