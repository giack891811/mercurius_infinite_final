# agents/agent_generator.py

"""
Modulo: agent_generator.py
Descrizione: Generazione dinamica di nuovi agenti per Mercurius∞ con personalità e missione specifiche.
"""

from typing import Dict
import uuid


class Agent:
    def __init__(self, name: str, personality: str, mission: str):
        self.id = str(uuid.uuid4())
        self.name = name
        self.personality = personality
        self.mission = mission

    def describe(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "personality": self.personality,
            "mission": self.mission
        }


def generate_agent(personality: str, mission: str, name: str = "Unnamed Agent") -> Agent:
    """
    Crea un nuovo agente con parametri definiti.
    """
    return Agent(name, personality, mission)
