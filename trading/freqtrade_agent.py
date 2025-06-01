class FreqtradeAgent:
    def __init__(self):
        self.name = "Freqtrade"

    def execute_task(self, strategy_name: str, action: str = "backtest") -> str:
        return f"[{self.name}] Strategia '{strategy_name}' eseguita in modalità {action}."
