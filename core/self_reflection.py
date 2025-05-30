"""
Modulo: self_reflection.py
Responsabilità: Fornire capacità di auto-riflessione al sistema Mercurius∞
Autore: Mercurius∞ Engineer Mode
"""

import json
import datetime
import os
from typing import List, Dict, Any


class ReflectionLog:
    """
    Classe per la gestione dei log di riflessione cognitiva.
    """
    def __init__(self, path: str = "data/reflection_log.json"):
        self.path = path
        if not os.path.exists(os.path.dirname(self.path)):
            os.makedirs(os.path.dirname(self.path))
        self._initialize_log()

    def _initialize_log(self):
        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                json.dump([], f)

    def append_reflection(self, entry: Dict[str, Any]):
        entry["timestamp"] = datetime.datetime.now().isoformat()
        log = self.load_log()
        log.append(entry)
        with open(self.path, "w") as f:
            json.dump(log, f, indent=4)

    def load_log(self) -> List[Dict[str, Any]]:
        with open(self.path, "r") as f:
            return json.load(f)

    def clear_log(self):
        with open(self.path, "w") as f:
            json.dump([], f)


class SelfReflection:
    """
    Classe che rappresenta la capacità del sistema di riflettere sulle proprie azioni e decisioni.
    """
    def __init__(self, log_path: str = "data/reflection_log.json"):
        self.logger = ReflectionLog(log_path)

    def evaluate_action(self, action_description: str, outcome: str, success: bool, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valuta un'azione eseguita e ne registra il risultato.
        """
        reflection = {
            "action": action_description,
            "outcome": outcome,
            "success": success,
            "context": context,
            "insight": self._generate_insight(action_description, outcome, success, context)
        }
        self.logger.append_reflection(reflection)
        return reflection

    def _generate_insight(self, action: str, outcome: str, success: bool, context: Dict[str, Any]) -> str:
        """
        Genera un'osservazione basata sui risultati dell'azione.
        """
        if success:
            return f"Azione '{action}' eseguita con successo. Approccio da riutilizzare in contesti simili."
        else:
            return f"Fallimento in '{action}'. Potenziale causa: {context.get('error', 'non specificata')}. Suggerita strategia alternativa."

    def reflect_on_log(self) -> List[str]:
        """
        Analizza il log delle riflessioni per identificare pattern.
        """
        log = self.logger.load_log()
        insights = [entry["insight"] for entry in log]
        return insights

    def summarize_reflections(self) -> Dict[str, int]:
        """
        Ritorna un riassunto statistico delle riflessioni registrate.
        """
        log = self.logger.load_log()
        success_count = sum(1 for e in log if e["success"])
        fail_count = sum(1 for e in log if not e["success"])
        return {"total": len(log), "successes": success_count, "failures": fail_count}
