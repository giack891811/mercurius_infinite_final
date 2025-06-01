# analytics/meta_learner.py
"""
Modulo: meta_learner.py
Descrizione: Analizza il Behavior Log e calcola KPI sulle performance
per suggerire miglioramenti a moduli/parametri.
"""

from collections import Counter
from typing import Dict, Any, List
import json

from analytics.behavior_logger import BehaviorLogger

class MetaLearner:
    def __init__(self):
        self.logger = BehaviorLogger()

    def _load_events(self) -> List[Dict[str, Any]]:
        raw = self.logger.tail(5000)
        return [json.loads(line) for line in raw]

    def kpi(self) -> Dict[str, Any]:
        data = self._load_events()
        total = len(data)
        errors = [e for e in data if e["event"] == "error"]
        successes = [e for e in data if e["event"] == "success"]
        modules = Counter(e["details"].get("module", "unknown") for e in errors)
        return {
            "total_events": total,
            "error_rate": len(errors) / total if total else 0,
            "success_rate": len(successes) / total if total else 0,
            "top_error_modules": modules.most_common(5),
        }

    def recommend(self) -> str:
        kpi = self.kpi()
        if kpi["error_rate"] > 0.2:
            worst = kpi["top_error_modules"][0][0] if kpi["top_error_modules"] else "unknown"
            return f"🤖 Consiglio: test approfonditi su modulo '{worst}' (errore>20%)."
        return "✅ Sistema stabile: nessuna azione critica."
