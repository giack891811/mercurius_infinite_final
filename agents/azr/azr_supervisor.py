"""
azr_supervisor.py
=================
Controllore strategico per adattamento Mercurius∞ basato su esperienze.
"""

from modules.experience.azr_analyzer import AZRAnalyzer
from modules.metrics.performance_metrics import PerformanceMetrics


class AZRSupervisor:
    def __init__(self, agent, experience_memory, config):
        self.agent = agent
        self.memory = experience_memory
        self.config = config
        self.analyzer = AZRAnalyzer(self.memory, config)

    def supervise(self):
        analysis = self.analyzer.analyze_recent_performance()
        suggestion = analysis.get("decision", {})
        if suggestion.get("action") == "decrease_risk":
            new_qty = suggestion["new_qty"]
            self.agent.adjust_strategy({"base_trade_qty": new_qty})
        return analysis
