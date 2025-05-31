# trading/trading_core.py

"""
Modulo: trading_core.py
Descrizione: Integrazione centralizzata per operazioni di trading con TradingView, MetaTrader5 e Interactive Brokers.
Gestisce segnali, esecuzione ordini e monitoraggio stato.
"""

import logging
from abc import ABC, abstractmethod

# Optional imports if available in environment
try:
    import MetaTrader5 as mt5
except ImportError:
    mt5 = None

try:
    from ib_insync import IB, Stock, util
except ImportError:
    IB = None

logging.basicConfig(level=logging.INFO)


class TradingInterface(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def execute_order(self, symbol: str, action: str, quantity: float):
        pass

    @abstractmethod
    def get_status(self) -> str:
        pass


class TradingViewInterface(TradingInterface):
    def connect(self):
        logging.info("✅ TradingView: Nessuna connessione diretta (webhook o scraping).")

    def execute_order(self, symbol: str, action: str, quantity: float):
        logging.info(f"📡 Segnale da TradingView: {action.upper()} {quantity} {symbol}")

    def get_status(self) -> str:
        return "🔁 Monitoraggio segnali via webhook (implementazione esterna richiesta)"


class MetaTraderInterface(TradingInterface):
    def connect(self):
        if mt5 and mt5.initialize():
            logging.info("✅ Connessione MT5 avviata.")
        else:
            logging.error("❌ MT5: Errore di inizializzazione.")

    def execute_order(self, symbol: str, action: str, quantity: float):
        if not mt5:
            logging.error("❌ MT5 non disponibile.")
            return
        type_order = mt5.ORDER_TYPE_BUY if action.lower() == "buy" else mt5.ORDER_TYPE_SELL
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": quantity,
            "type": type_order,
            "price": mt5.symbol_info_tick(symbol).ask,
            "deviation": 10,
            "magic": 234000,
            "comment": "Mercurius∞ Order",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        result = mt5.order_send(request)
        logging.info(f"📈 Ordine MT5: {result}")

    def get_status(self) -> str:
        return "🔗 MT5: connesso" if mt5 and mt5.initialize() else "🚫 MT5: non connesso"


class IBKRInterface(TradingInterface):
    def __init__(self):
        self.ib = IB() if IB else None

    def connect(self):
        if self.ib:
            try:
                self.ib.connect("127.0.0.1", 7497, clientId=1)
                logging.info("✅ Connessione IBKR attiva.")
            except Exception as e:
                logging.error(f"❌ Errore IBKR: {e}")
        else:
            logging.error("❌ IB_insync non disponibile.")

    def execute_order(self, symbol: str, action: str, quantity: float):
        if not self.ib:
            logging.error("❌ IB non inizializzato.")
            return
        stock = Stock(symbol, "SMART", "USD")
        order_type = "BUY" if action.lower() == "buy" else "SELL"
        self.ib.qualifyContracts(stock)
        order = self.ib.marketOrder(order_type, quantity)
        trade = self.ib.placeOrder(stock, order)
        logging.info(f"📊 IBKR Ordine: {order_type} {quantity} {symbol}")
        return trade

    def get_status(self) -> str:
        return "🔗 IBKR: connesso" if self.ib and self.ib.isConnected() else "🚫 IBKR: disconnesso"
