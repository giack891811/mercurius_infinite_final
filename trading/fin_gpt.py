class FinGPTAgent:
    def __init__(self):
        self.name = "FinGPT"

    def execute_task(self, market_context: str, parameters: dict = {}) -> str:
        return f"[{self.name}] Analisi sentiment su: {market_context}"
