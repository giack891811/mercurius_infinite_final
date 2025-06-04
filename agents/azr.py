"""AZR reasoning agent."""
from modules.llm.azr_reasoner import AZRAgent

class AZR:
    def __init__(self):
        self.agent = AZRAgent()

    def analyze(self, text: str) -> str:
        return self.agent.analyze(text)

    def neural_feedback(self):
        print("[AZR] feedback cycle active")
