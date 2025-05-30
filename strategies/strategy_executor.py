"""
strategy_executor.py
====================
Genera segnali operativi basati su output del modello predittivo.
"""

class StrategyExecutor:
    def __init__(self, config):
        self.config = config

    def generate_signals(self, model, features):
        """Genera segnali di trading basandosi sull'output del modello."""
        signals = []
        for f in features:
            pred = model.forward([
                f["price_volatility_ratio"],
                f["momentum"],
                f["volatility"]
            ])[0]
            action = "BUY" if pred > 0.5 else "SELL"
            signals.append({
                "symbol": f["symbol"],
                "action": action,
                "confidence": pred,
                "volatility": f["volatility"],
                "timestamp": "2025-05-30T12:00:00"
            })
        return signals

    def filter_signals(self, signals, min_confidence=0.6):
        """Filtra i segnali con bassa confidenza."""
        return [s for s in signals if s["confidence"] >= min_confidence]

    def summary_stats(self, signals):
        """Statistiche dei segnali generati."""
        summary = {"BUY": 0, "SELL": 0}
        for s in signals:
            summary[s["action"]] += 1
        return summary
