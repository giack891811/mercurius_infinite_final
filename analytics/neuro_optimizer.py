# analytics/neuro_optimizer.py
"""
Modulo: neuro_optimizer.py
Descrizione: Usa MetaLearner + LLM per proporre refactor automatici ai moduli peggiori.
"""

import os
import openai
from pathlib import Path

from analytics.meta_learner import MetaLearner

class NeuroOptimizer:
    def __init__(self, model="gpt-3.5-turbo"):
        self.meta = MetaLearner()
        self.model = model
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def _call_llm(self, prompt: str) -> str:
        resp = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=800,
        )
        return resp["choices"][0]["message"]["content"]

    def suggest_patch(self) -> dict | None:
        rec = self.meta.recommend()
        if "test approfonditi su modulo" not in rec:
            return None
        module_name = rec.split("'")[1]
        file_path = Path(f"{module_name.replace('.', '/')}.py")
        if not file_path.exists():
            return None
        original_code = file_path.read_text(encoding="utf-8")
        prompt = (
            "Migliora il codice seguente correggendo bug, aggiungendo docstring "
            "e typing. Restituisci il file completo.\n\n"
            f"FILE: {file_path}\n```python\n{original_code}\n```"
        )
        new_code = self._call_llm(prompt)
        return {"path": str(file_path), "code": new_code}
