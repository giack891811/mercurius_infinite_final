# cognition/cognitive_map.py
"""
Modulo: cognitive_map.py
Descrizione: Rappresentazione dinamica della mappa mentale di Mercurius∞.
Ogni nodo è un agente, ogni arco è una dipendenza o canale di comunicazione.
"""

from collections import defaultdict
from typing import Dict, List


class CognitiveMap:
    def __init__(self):
        # {agent: {"type": "cognitive|trading|voice", "edges": [to_agent, ...]}}
        self.nodes: Dict[str, Dict] = defaultdict(lambda: {"type": "generic", "edges": []})

    # ---------- Gestione nodi ----------
    def add_agent(self, name: str, agent_type: str = "generic"):
        self.nodes[name]["type"] = agent_type

    def link(self, src: str, dest: str):
        if dest not in self.nodes[src]["edges"]:
            self.nodes[src]["edges"].append(dest)

    def remove_agent(self, name: str):
        self.nodes.pop(name, None)
        for n in self.nodes.values():
            if name in n["edges"]:
                n["edges"].remove(name)

    # ---------- Query ----------
    def agents_by_type(self, agent_type: str) -> List[str]:
        return [a for a, meta in self.nodes.items() if meta["type"] == agent_type]

    def connections_of(self, name: str) -> List[str]:
        return self.nodes[name]["edges"]

    def to_dict(self):
        return self.nodes
