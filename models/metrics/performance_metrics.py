"""
performance_metrics.py
=======================
Calcolo di metriche da esperienze Mercurius∞: accuracy, distribuzione profitti, ecc.
"""

from statistics import mean, stdev


class PerformanceMetrics:
    def __init__(self, experiences):
        self.experiences = experiences

    def profit_stats(self):
        profits = [e["result"].get("profit", 0) for e in self.experiences]
        return {
            "mean": mean(profits) if profits else 0,
            "stddev": stdev(profits) if len(profits) > 1 else 0,
            "count": len(profits)
        }

    def accuracy(self):
        correct = 0
        for e in self.experiences:
            profit = e["result"].get("profit", 0)
            action = e["trade"]["action"]
            if (profit > 0 and action == "BUY") or (profit < 0 and action == "SELL"):
                correct += 1
        return correct / len(self.experiences) if self.experiences else 0

    def summary(self):
        stats = self.profit_stats()
        return {
            **stats,
            "accuracy": self.accuracy()
        }
