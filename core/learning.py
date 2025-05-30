"""
Modulo: learning.py
Responsabilità: Fornire capacità di apprendimento continuo al sistema Mercurius∞
Autore: Mercurius∞ Engineer Mode
"""

import os
import json
import datetime
from typing import List, Dict, Any


class KnowledgeBase:
    """
    Base di conoscenza incrementale dove il sistema salva ciò che apprende.
    """
    def __init__(self, path: str = "data/knowledge_base.json"):
        self.path = path
        if not os.path.exists(os.path.dirname(self.path)):
            os.makedirs(os.path.dirname(self.path))
        self._initialize()

    def _initialize(self):
        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                json.dump([], f)

    def add_entry(self, data: Dict[str, Any]):
        data["timestamp"] = datetime.datetime.now().isoformat()
        current = self.load()
        current.append(data)
        with open(self.path, "w") as f:
            json.dump(current, f, indent=4)

    def load(self) -> List[Dict[str, Any]]:
        with open(self.path, "r") as f:
            return json.load(f)

    def clear(self):
        with open(self.path, "w") as f:
            json.dump([], f)


class ContinuousLearner:
    """
    Sistema di apprendimento continuo per adattare le strategie in base all'esperienza.
    """
    def __init__(self, knowledge_path: str = "data/knowledge_base.json"):
        self.kb = KnowledgeBase(knowledge_path)

    def learn_from_experience(self, action: str, result: str, success: bool, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Registra un'esperienza e ne estrae apprendimento.
        """
        insight = self._analyze_experience(action, result, success, context)
        entry = {
            "action": action,
            "result": result,
            "success": success,
            "context": context,
            "insight": insight
        }
        self.kb.add_entry(entry)
        return entry

    def _analyze_experience(self, action: str, result: str, success: bool, context: Dict[str, Any]) -> str:
        """
        Elabora un'interpretazione strutturata di ciò che è stato appreso.
        """
        if success:
            return f"Esperienza positiva con '{action}'. Risultato ottenuto: {result}. Approccio efficace."
        else:
            return f"Errore riscontrato in '{action}': {context.get('error', 'non definito')}. Apprendimento da ottimizzare."

    def retrieve_insights(self) -> List[str]:
        """
        Estrae tutti gli insegnamenti appresi fino ad ora.
        """
        data = self.kb.load()
        return [d["insight"] for d in data]

    def stats(self) -> Dict[str, int]:
        """
        Statistiche sulle esperienze salvate.
        """
        data = self.kb.load()
        return {
            "total": len(data),
            "successes": sum(1 for d in data if d["success"]),
            "failures": sum(1 for d in data if not d["success"])
        }
