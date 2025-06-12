"""FinRLAgent - Analisi e generazione di segnali di trading."""

class FinRLAgent:
    def analyze_market(self, market_data: list[dict]) -> list[dict]:
        """Elabora i dati di mercato e restituisce analisi semplificate."""
        analyses = []
        for row in market_data:
            signal = {
                "symbol": row.get("symbol"),
                "score": row.get("volatility", 1) * 0.5,
            }
            analyses.append(signal)
        return analyses

    def generate_trade_signals(self, analyses: list[dict]) -> list[dict]:
        """Converte le analisi in semplici segnali buy/sell."""
        signals = []
        for a in analyses:
            action = "BUY" if a.get("score", 0) > 0.5 else "SELL"
            signals.append({"symbol": a["symbol"], "action": action, "confidence": a["score"]})
        return signals
