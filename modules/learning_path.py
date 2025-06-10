"""learning_path.py
Genera percorsi di apprendimento dinamici."""
from __future__ import annotations

from modules.llm.gpt4o_validator import GPT4oAgent
from modules.llm.azr_reasoner import validate_with_azr


class LearningPath:
    def __init__(self) -> None:
        self.llm = GPT4oAgent()

    def generate(self, topic: str) -> str:
        prompt = f"Crea una breve roadmap di studio per: {topic}"
        resp = self.llm.validate(prompt)
        return resp if validate_with_azr(resp) else ""
