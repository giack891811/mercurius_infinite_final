# modules/experience/azr_analyzer.py
"""
Modulo: azr_analyzer.py
Descrizione: Analizzatore esperienziale per AZR – Adattamento Zero Retention.
Combina l’analisi statistica dei profitti con la capacità di AZRAgent di
suggerire adattamenti strategici basati su prompt di linguaggio naturale.
"""

import json
from statistics import mean, stdev
from typing import Any, Dict, List, Optional, Union

from modules.experience.experience_memory import ExperienceMemory
from modules.llm.azr_reasoner import AZRAgent


class AZRAnalyzer:
    """
    AZRAnalyzer unisce due livelli di analisi:
      1. Analisi statistica su profitti (mean, volatility, ed eventuale suggerimento di riduzione rischio).
      2. Creazione di un prompt testuale per AZRAgent, che analizza il batch recente e suggerisce adattamenti.
    """

    def __init__(self, exp_memory: ExperienceMemory, config: Dict[str, Any]):
        """
        - exp_memory: istanza di ExperienceMemory già inizializzata (backend JSON).
        - config: dizionario di configurazione, con possibili chiavi:
            - "azr_profit_floor": soglia minima media dei profitti (float), default 0.5
            - "base_trade_qty": quantità base del trade (int), default 100
            - "use_azr": booleano che abilita l’analisi LLM (default True)
        """
        self.exp_memory = exp_memory
        self.config = config
        self.azr = AZRAgent() if config.get("use_azr", True) else None

    def analyze_recent_performance(
        self, limit: int = 20
    ) -> Dict[str, Union[str, float, Dict[str, Any]]]:
        """
        Esegue un’analisi statistica sui profitti delle ultime `limit` esperienze.
        Restituisce un dizionario contenente:
          - "status": "no_data" o "ok"
          - "mean_profit": media dei profitti (float)
          - "volatility": deviazione standard (float)
          - "decision": suggerimento generico basato sul confronto con "azr_profit_floor"
        """
        recent = self.exp_memory.get_recent_experiences(limit)
        # Estrae la lista dei profitti, default a 0 se mancante
        profits: List[float] = [
            e.get("result", {}).get("profit", 0.0) for e in recent
        ]

        if not profits:
            return {"status": "no_data"}

        avg_profit = mean(profits)
        vol = stdev(profits) if len(profits) > 1 else 0.0
        decision = self._suggest_statistical(avg_profit)

        return {
            "status": "ok",
            "mean_profit": avg_profit,
            "volatility": vol,
            "decision": decision,
        }

    def _suggest_statistical(self, avg_profit: float) -> Dict[str, Any]:
        """
        Suggerisce un’azione di tuning se la media dei profitti è inferiore a "azr_profit_floor".
        Se avg_profit < soglia, restituisce:
          {
            "action": "decrease_risk",
            "new_qty": <metà di base_trade_qty o 10, se inferiore>
          }
        Altrimenti restituisce {"action": "maintain"}.
        """
        threshold = float(self.config.get("azr_profit_floor", 0.5))
        base_qty = int(self.config.get("base_trade_qty", 100))

        if avg_profit < threshold:
            new_qty = max(10, int(base_qty * 0.5))
            return {"action": "decrease_risk", "new_qty": new_qty}

        return {"action": "maintain"}

    def apply_statistical_adaptation(self, limit: int = 20) -> Dict[str, Any]:
        """
        Esegue l’analisi statistica e, se viene suggerita una riduzione del rischio,
        aggiorna `config["base_trade_qty"]`. Restituisce il risultato dell'analisi.
        """
        result = self.analyze_recent_performance(limit)
        decision = result.get("decision", {})
        if decision.get("action") == "decrease_risk":
            self.config["base_trade_qty"] = decision["new_qty"]
        return result

    def analyze_with_azr(self, limit: int = 10) -> Optional[Dict[str, Any]]:
        """
        Crea un prompt testuale basato sulle ultime `limit` esperienze e lo invia ad AZRAgent,
        che restituisce un’analisi in linguaggio naturale. Se AZRAgent suggerisce un cambiamento
        di rischio, viene applicato a config["base_trade_qty"] e viene restituito il dizionario
        {"action": ..., "new_qty": ...}. Altrimenti restituisce None.
        """
        if not self.azr:
            return None

        recent = self.exp_memory.get_recent_experiences(limit)
        if not recent:
            return None

        # Costruzione del prompt
        prompt_lines = ["Analizza queste esperienze di trading e suggerisci adattamento del rischio:"]
        for e in recent:
            profit = e.get("result", {}).get("profit", 0.0)
            qty = e.get("trade", {}).get("quantity", self.config.get("base_trade_qty", 100))
            prompt_lines.append(f"- Profit: {profit}, Quantity: {qty}")
        prompt = "\n".join(prompt_lines)

        # Chiamata ad AZRAgent
        analysis_text = self.azr.analyze(prompt)

        # Se AZRAgent parla di 'rischio' (o 'risk'), applichiamo la modifica
        if "rischio" in analysis_text.lower() or "risk" in analysis_text.lower():
            base_qty = int(self.config.get("base_trade_qty", 100))
            new_qty = max(1, int(base_qty * 0.5))
            self.config["base_trade_qty"] = new_qty
            return {"action": "decrease_risk", "new_qty": new_qty, "analysis": analysis_text}

        return None

    def apply_adaptation(self, use_azr: bool = True, limit: int = 20) -> Dict[str, Any]:
        """
        Combina le due modalità di adattamento:
          - Se use_azr=True e AZRAgent è disponibile, prova prima l’adattamento LLM:
            se AZR suggerisce un cambiamento, lo applica e lo restituisce.
          - Altrimenti, (o se AZR non suggerisce nulla) esegue l’adattamento statistico
            tramite `apply_statistical_adaptation(limit)`.
        Restituisce sempre un dizionario con la decisione effettiva.
        """
        # Tentativo con AZRAgent
        if use_azr and self.azr:
            azr_result = self.analyze_with_azr(limit // 2)
            if azr_result is not None:
                return {"method": "azr", "decision": azr_result}

        # Altrimenti, adattamento statistico
        stat_result = self.apply_statistical_adaptation(limit)
        return {"method": "statistical", "decision": stat_result.get("decision", {})}


# ========== ESEMPIO DI UTILIZZO ==========
if __name__ == "__main__":
    # Simulazione di integrazione con ExperienceMemory e config
    from modules.experience.experience_memory import ExperienceMemory

    config = {
        "azr_profit_floor": 0.5,
        "base_trade_qty": 100,
        "use_azr": True
    }

    # Inizializza la memoria esperienziale
    em = ExperienceMemory({"experience_file": "memory/experience_log.json", "max_recent": 50})

    # Registra alcune esperienze di test
    em.record_experience(
        signal={"symbol": "EURUSD", "type": "BUY", "price": 1.1000},
        trade={"quantity": 100, "entry": 1.1000, "exit": 1.1020},
        result={"profit": 20, "currency": "USD"},
        feedback="Esecuzione corretta"
    )
    em.record_experience(
        signal={"symbol": "EURUSD", "type": "SELL", "price": 1.1050},
        trade={"quantity": 100, "entry": 1.1050, "exit": 1.1030},
        result={"profit": -20, "currency": "USD"},
        feedback="Stop troppo stretto"
    )

    # Inizializza l’analizzatore
    analyzer = AZRAnalyzer(exp_memory=em, config=config)

    # Applichiamo l’adattamento (AZR o statistico)
    adaptation = analyzer.apply_adaptation(use_azr=True, limit=20)
    print("Adattamento applicato:", json.dumps(adaptation, indent=2))
