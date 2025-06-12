"""Modulo per l'esecuzione di trading semi-automatico."""

from modules.FinRLAgent import FinRLAgent
from trading.trading_core import TradingViewInterface


n_default_qty = 1.0


class AutoTraderAI:
    """Implementazione semplice di un trader automatico."""

    def __init__(self, quantity: float = n_default_qty):
        self.finrl = FinRLAgent()
        self.tv = TradingViewInterface()
        self.quantity = quantity
        self.tv.connect()

    def run(self, market_data: list[dict]) -> list[dict]:
        """Analizza dati e invia ordini simulati."""
        analyses = self.finrl.analyze_market(market_data)
        signals = self.finrl.generate_trade_signals(analyses)
        for s in signals:
            self.tv.execute_order(s["symbol"], s["action"], self.quantity)
        return signals
