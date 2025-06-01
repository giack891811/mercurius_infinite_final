class HuggingFaceTools:
    def __init__(self):
        self.name = "HuggingFaceTools"

    def execute(self, tool_name: str, args: dict) -> str:
        return f"[{self.name}] Strumento '{tool_name}' eseguito con parametri {args}"
