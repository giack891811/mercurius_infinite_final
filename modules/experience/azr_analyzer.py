"""
azr_analyzer.py
===============
Analizzatore esperienziale per AZR – Adattamento Zero Retention.
Analizza profitti, confidenza e suggerisce cambiamenti strategici.
"""

from statistics import mean, stdev

class AZRAnalyzer:
    def __init__(self, experience_memory, config):
        self.memory = experience_memory
        self.config = config

    def analyze_recent_performance(self, limit=20):
        recent = self.memory.get_recent_experiences(limit)
        profits = [e["result"].get("profit", 0) for e in recent]

        if not profits:
            return {"status": "no_data"}

        return {
            "mean_profit": mean(profits),
            "volatility": stdev(profits) if len(profits) > 1 else 0,
            "decision": self._suggest(mean(profits))
        }

    def _suggest(self, avg_profit):
        threshold = self.config.get("azr_profit_floor", 0.5)
        if avg_profit < threshold:
            return {
                "action": "decrease_risk",
                "new_qty": max(10, int(self.config.get("base_trade_qty", 100) * 0.5))
            }
        return {"action": "maintain"}

    def apply_adaptation(self):
        result = self.analyze_recent_performance()
        if result["decision"]["action"] == "decrease_risk":
            self.config["base_trade_qty"] = result["decision"]["new_qty"]
        return result
