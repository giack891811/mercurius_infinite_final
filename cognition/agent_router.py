# cognition/agent_router.py
"""
Modulo: agent_router.py
Descrizione: Seleziona l'agente ottimale per un task usando CognitiveMap + TaskMemory.
"""

import re
from typing import Dict

from cognition.cognitive_map import CognitiveMap
from cognition.task_memory import TaskMemory


class AgentRouter:
    def __init__(self, c_map: CognitiveMap, memory: TaskMemory):
        self.map = c_map
        self.memory = memory
        # pattern → lista agent_type preferiti
        self.rules: Dict[str, list[str]] = {
            r"\b(trade|buy|sell)\b": ["trading"],
            r"\b(voice|speak|listen)\b": ["voice"],
            r"\b(debug|validate|logic)\b": ["cognitive"],
        }

    def _match_rule(self, task: str):
        for pattern, types in self.rules.items():
            if re.search(pattern, task, re.IGNORECASE):
                return types
        return ["cognitive"]

    def choose_agent(self, task: str) -> str:
        desired_types = self._match_rule(task)
        candidates = []
        for t in desired_types:
            candidates.extend(self.map.agents_by_type(t))
        # se più candidati, usa memoria di successo
        if candidates:
            return self.memory.suggest_best(candidates)
        # fallback: primo agente generico
        return next(iter(self.map.nodes))

    def record_result(self, agent: str, task: str, success: bool):
        self.memory.add_record(agent, task, success)
