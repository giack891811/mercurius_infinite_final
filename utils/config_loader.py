"""
config_loader.py
================
Carica la configurazione da file YAML (mock per ora).
"""

def load_config(path):
    """
    Mock del caricamento configurazione.
    In un sistema reale, caricherebbe da YAML/JSON.
    """
    return {
        "symbols": ["AAPL", "TSLA", "GOOG"],
        "base_trade_qty": 100,
        "min_confidence": 0.55,
        "retrain_threshold": 0.65
    }
