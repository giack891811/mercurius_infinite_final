class LeonAI:
    def __init__(self):
        self.name = "LeonAI"

    def run_command(self, command: str) -> str:
        return f"[{self.name}] Comando locale eseguito: {command}"
