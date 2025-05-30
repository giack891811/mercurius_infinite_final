"""
market_data_handler.py
======================
Modulo per l'acquisizione e il preprocessing iniziale dei dati di mercato.
"""

import random

class MarketDataHandler:
    def __init__(self, config):
        self.config = config

    def fetch_market_data(self):
        """Simula il recupero di dati di mercato."""
        symbols = self.config.get("symbols", ["AAPL", "GOOG", "TSLA"])
        data = []
        for sym in symbols:
            price = round(random.uniform(100, 300), 2)
            volatility = round(random.uniform(0.5, 2.0), 2)
            volume = random.randint(1000, 5000)
            data.append({
                "symbol": sym,
                "price": price,
                "volatility": volatility,
                "volume": volume,
                "timestamp": "2025-05-30T12:00:00"
            })
        return data

    def normalize_data(self, data):
        """Normalizza i dati su base 0-1 per feature quantitative."""
        max_price = max(d["price"] for d in data)
        max_volatility = max(d["volatility"] for d in data)
        for d in data:
            d["price_norm"] = d["price"] / max_price
            d["volatility_norm"] = d["volatility"] / max_volatility
        return data

    def filter_by_volume(self, data, min_volume=1000):
        """Filtra i dati rimuovendo elementi sotto una certa soglia di volume."""
        return [d for d in data if d["volume"] >= min_volume]
