"""
feedback_collector.py
=====================
Modulo per raccolta di feedback operativi su performance in tempo reale.
"""

class FeedbackCollector:
    def __init__(self):
        self.log = []

    def record(self, symbol, action, result, confidence, feedback):
        """Registra un feedback strutturato su ogni azione."""
        entry = {
            "symbol": symbol,
            "action": action,
            "profit": result.get("profit", 0),
            "confidence": confidence,
            "feedback": feedback
        }
        self.log.append(entry)

    def summary(self):
        """Statistiche rapide del feedback operativo."""
        if not self.log:
            return {}
        total = len(self.log)
        avg_profit = sum(f["profit"] for f in self.log) / total
        avg_conf = sum(f["confidence"] for f in self.log) / total
        return {
            "total": total,
            "avg_profit": avg_profit,
            "avg_confidence": avg_conf
        }

    def clear(self):
        self.log.clear()
