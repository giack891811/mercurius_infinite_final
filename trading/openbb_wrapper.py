class OpenBBWrapper:
    def __init__(self):
        self.name = "OpenBB"

    def execute_task(self, command: str, options: dict = {}) -> str:
        return f"[{self.name}] Comando OpenBB eseguito: {command}"
