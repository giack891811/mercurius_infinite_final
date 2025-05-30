"""
feature_engineering.py
======================
Trasformazione dei dati grezzi in feature ingegnerizzate per l’addestramento e la predizione.
"""

class FeatureEngineer:
    def __init__(self, config):
        self.config = config

    def transform(self, raw_data):
        """Crea feature a partire dai dati di mercato grezzi."""
        features = []
        for row in raw_data:
            features.append({
                "symbol": row["symbol"],
                "price_volatility_ratio": self._safe_div(row["price"], row["volatility"]),
                "momentum": self._mock_momentum(row["symbol"]),
                "volatility": row["volatility"]
            })
        return features

    def _safe_div(self, a, b):
        """Divisione sicura evitando zero division."""
        return a / b if b != 0 else 0.0

    def _mock_momentum(self, symbol):
        """Mock per il calcolo del momentum."""
        return hash(symbol) % 10

    def enrich_with_indicators(self, features):
        """Aggiunge indicatori tecnici simulati."""
        for f in features:
            f["rsi"] = self._simulate_rsi(f["momentum"])
            f["macd"] = self._simulate_macd(f["momentum"])
        return features

    def _simulate_rsi(self, momentum):
        """Simulazione semplice RSI."""
        return min(100, momentum * 7.5)

    def _simulate_macd(self, momentum):
        """Simulazione semplice MACD."""
        return momentum * 1.2 - 5
