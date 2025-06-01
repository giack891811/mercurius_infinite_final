class LocalAI:
    def __init__(self):
        self.name = "LocalAI"

    def execute_task(self, prompt: str) -> str:
        return f"[{self.name}] Esecuzione locale per prompt: {prompt}"
