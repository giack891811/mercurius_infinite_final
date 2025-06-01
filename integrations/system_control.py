class SystemControl:
    def __init__(self):
        self.name = "SystemControl"

    def execute(self, system_command: str) -> str:
        return f"[{self.name}] Comando eseguito: {system_command}"
