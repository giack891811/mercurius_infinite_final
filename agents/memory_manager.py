"""
memory_manager.py
=================
Gestione della memoria storica delle operazioni, segnali e parametri per l'adattività dell'agente.
"""

class MemoryManager:
    def __init__(self, config):
        self.config = config
        self.trade_memory = []
        self.signal_memory = []
        self.context = {}

    def record_trade(self, trade):
        """Registra un trade eseguito nella memoria storica."""
        self.trade_memory.append(trade)
        self._update_context(trade)

    def record_signal(self, signal):
        """Registra un segnale ricevuto."""
        self.signal_memory.append(signal)

    def _update_context(self, trade):
        """Aggiorna il contesto operativo in base ai trade recenti."""
        symbol = trade["symbol"]
        self.context[symbol] = self.context.get(symbol, 0) + 1

    def get_recent_trades(self, limit=10):
        """Restituisce gli ultimi trade effettuati."""
        return self.trade_memory[-limit:]

    def get_signal_history(self, symbol=None):
        """Restituisce la memoria dei segnali per uno specifico simbolo o tutti."""
        if symbol:
            return [s for s in self.signal_memory if s["symbol"] == symbol]
        return self.signal_memory

    def clear(self):
        """Resetta la memoria."""
        self.trade_memory.clear()
        self.signal_memory.clear()
        self.context.clear()

    def export_summary(self):
        """Ritorna una sintesi dello stato attuale della memoria."""
        return {
            "tot_trades": len(self.trade_memory),
            "tot_signals": len(self.signal_memory),
            "context_symbols": list(self.context.keys())
        }

    def analyze_bias(self):
        """Analizza possibili bias nel comportamento di trading."""
        counts = {}
        for trade in self.trade_memory:
            symbol = trade["symbol"]
            counts[symbol] = counts.get(symbol, 0) + 1
        return sorted(counts.items(), key=lambda x: -x[1])
