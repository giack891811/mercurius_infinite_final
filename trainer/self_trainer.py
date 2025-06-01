# trainer/self_trainer.py
"""
Modulo: self_trainer.py
Descrizione: Addestramento self-supervised a partire dalle esperienze accumulate.
"""

from memory.long_term_memory import LongTermMemory
import openai
import os
from pathlib import Path

class SelfTrainer:
    def __init__(self, model_name="gpt-3.5-turbo"):
        self.memory = LongTermMemory()
        self.model = model_name
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def build_prompt(self, experiences):
        prompt = "Sei un assistente AI che migliora le proprie strategie di trading.\n"
        prompt += "Ecco le ultime esperienze:\n"
        for exp in experiences[-10:]:
            prompt += f"- Profit: {exp['result']['profit']}, Qty: {exp['trade']['quantity']}\n"
        prompt += "\nSuggerisci tre modi per migliorare la strategia."
        return prompt

    def train_once(self, save_to: Path | None = None):
        data = self.memory.get_all()
        if not data:
            return "Nessuna esperienza."
        prompt = self.build_prompt(data)
        try:
            resp = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.3,
            )
            advice = resp["choices"][0]["message"]["content"]
            if save_to:
                save_to.write_text(advice, encoding="utf-8")
            return advice
        except Exception as e:
            return f"⚠️ Training error: {e}"
