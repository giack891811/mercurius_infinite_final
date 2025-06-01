class QlibAdapter:
    def __init__(self):
        self.name = "Qlib"

    def execute_task(self, symbol: str, timeframe: str, mode: str = "forecast") -> str:
        return f"[{self.name}] {mode.upper()} per {symbol} su {timeframe} eseguita."
