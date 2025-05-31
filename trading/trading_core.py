# trading/trading_core.py

"""
Modulo: trading_core.py
Descrizione: Integrazione centralizzata per operazioni di trading con TradingView, MetaTrader5 e Interactive Brokers.
Gestisce segnali, esecuzione ordini e monitoraggio stato.
Supporta import opzionali e fallback dinamici.
"""

import logging
from abc import ABC, abstractmethod

# ─── Import dinamici ─────────────────────────────────────────────────────────
try:
    import MetaTrader5 as mt5
except ImportError:
    mt5 = None

try:
    from ib_insync import IB, Stock, util
except ImportError:
    IB = None

# ─── Logging Base ────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO)

# ─── Interfaccia Trading Generale ─────────────────────────────────────────────
class TradingInterface(ABC):
    @abstractmethod
    def connect(self): pass

    @abstractmethod
    def execute_order(self, symbol: str, action: str, quantity: float): pass

    @abstractmethod
    def get_status(self) -> str: pass

# ─── TradingView ──────────────────────────────────────────────────────────────
class TradingViewInterface(TradingInterface):
    def connect(self):
        logging.info("✅ TradingView: Nessuna connessione richiesta (webhook o scraping).")

    def execute_order(self, symbol: str, action: str, quantity: float):
        logging.info(f"📡 Segnale da TradingView: {action.upper()} {quantity} {symbol}")

    def get_status(self) -> str:
        return "✔️ TradingView operativo (webhook)"

# ─── MetaTrader5 ──────────────────────────────────────────────────────────────
class MetaTraderInterface(TradingInterface):
    def connect(self):
        if mt5 and mt5.initialize():
            logging.info("✅ Connessione MT5 avviata.")
        else:
            logging.warning("⚠️ MT5 non disponibile o inizializzazione fallita.")

    def execute_order(self, symbol: str, action: str, quantity: float):
        if not mt5:
            return logging.error("❌ MT5 non disponibile.")
        try:
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
            logging.info(f"📈 Ordine MT5 eseguito: {result}")
        except Exception as e:
            logging.error(f"❌ Errore invio ordine MT5: {e}")

    def get_status(self) -> str:
        return "🔗 MT5: connesso" if mt5 and mt5.initialize() else "🚫 MT5: non connesso"

# ─── Interactive Brokers (IBKR) ───────────────────────────────────────────────
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
            logging.warning("⚠️ IB_insync non disponibile.")

    def execute_order(self, symbol: str, action: str, quantity: float):
        if not self.ib:
            return logging.error("❌ IB non inizializzato.")
        try:
            stock = Stock(symbol, "SMART", "USD")
            order_type = "BUY" if action.lower() == "buy" else "SELL"
            self.ib.qualifyContracts(stock)
            order = self.ib.marketOrder(order_type, quantity)
            trade = self.ib.placeOrder(stock, order)
            logging.info(f"📊 IBKR Ordine: {order_type} {quantity} {symbol}")
            return trade
        except Exception as e:
            logging.error(f"❌ Errore ordine IBKR: {e}")

    def get_status(self) -> str:
        return "🔗 IBKR: connesso" if self.ib and self.ib.isConnected() else "🚫 IBKR: disconnesso"
