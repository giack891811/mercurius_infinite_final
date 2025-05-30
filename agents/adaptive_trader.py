"""
adaptive_trader.py
==================
Agente autonomo per esecuzione dinamica di operazioni di trading sulla base
dei segnali ricevuti, stato di memoria, e ora anche adattamento esperienziale (AZR).
"""

from modules.experience.azr_analyzer import AZRAnalyzer
from modules.experience.experience_memory import ExperienceMemory

class AdaptiveTrader:
    def __init__(self, config, memory_manager, model_trainer, strategy_executor):
        self.config = config
        self.memory = memory_manager
        self.model_trainer = model_trainer
        self.strategy = strategy_executor
        self.trade_log = []
        self.experience_memory = ExperienceMemory(config)
        self.azr = AZRAnalyzer(self.experience_memory, config)

    def evaluate_signals(self, signals):
        """Valuta i segnali di trading ricevuti in base al contesto corrente."""
        evaluated = []
        for signal in signals:
            confidence = signal.get('confidence', 0.5)
            if confidence > self.config.get("min_confidence", 0.6):
                evaluated.append(signal)
        return evaluated

    def execute_trades(self, signals):
        """Esegue le operazioni basandosi sui segnali validati."""
        valid_signals = self.evaluate_signals(signals)
        for signal in valid_signals:
            trade = {
                "symbol": signal["symbol"],
                "action": signal["action"],
                "quantity": self._calculate_quantity(signal),
                "timestamp": signal.get("timestamp")
            }

            # Simula risultato
            result = self._simulate_trade_result(trade)
            feedback = self._generate_feedback(trade, result)

            self.experience_memory.record_experience(signal, trade, result, feedback)
            self.memory.record_trade(trade)
            self.trade_log.append(trade)

            print(f"Eseguito trade: {trade} → Profit: {result['profit']:.2f}")

        self._adaptive_adjustment()

    def _calculate_quantity(self, signal):
        """Calcola la quantità da tradare in base a rischio e asset allocation."""
        base_qty = self.config.get("base_trade_qty", 100)
        volatility_factor = signal.get("volatility", 1)
        return int(base_qty / volatility_factor)

    def _simulate_trade_result(self, trade):
        """Mock del risultato di un'operazione."""
        import random
        direction = 1 if trade["action"] == "BUY" else -1
        price_diff = random.uniform(-5, 10) * direction
        return {"profit": round(price_diff * trade["quantity"] * 0.01, 2)}

    def _generate_feedback(self, trade, result):
        """Mock di feedback evolutivo."""
        return {
            "profit_margin": result["profit"] / (trade["quantity"] + 1),
            "risk_level": trade["quantity"]
        }

    def _adaptive_adjustment(self):
        """Applica AZR per modificare i parametri in base all’esperienza recente."""
        new_config = self.azr.apply_adaptation(self.config)
        self.config.update(new_config)

    def get_trade_history(self):
        """Restituisce lo storico delle operazioni eseguite."""
        return self.trade_log
