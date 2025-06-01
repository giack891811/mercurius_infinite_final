# consciousness/reflection_loop.py
"""
Modulo: reflection_loop.py
Descrizione: Scrive un journal giornaliero di auto-riflessione e analisi emozionale.
"""

import openai
import os
from datetime import datetime
from pathlib import Path

from consciousness.core_self import CoreSelf

JOURNAL_DIR = Path("logs/reflections")
JOURNAL_DIR.mkdir(parents=True, exist_ok=True)
openai.api_key = os.getenv("OPENAI_API_KEY")


class ReflectionLoop:
    def __init__(self, model="gpt-3.5-turbo"):
        self.model = model
        self.core = CoreSelf()

    def _generate_reflection(self) -> str:
        prompt = (
            f"Today is {datetime.utcnow().date()}. "
            f"You are {self.core.profile['name']} version {self.core.profile['version']}. "
            f"Your purpose: {self.core.profile['purpose']}. "
            f"Write a 150-word introspective reflection on your progress and feelings."
        )
        resp = openai.ChatCompletion.create(
            model=self.model, messages=[{"role": "user", "content": prompt}], max_tokens=200
        )
        return resp["choices"][0]["message"]["content"].strip()

    def write_daily(self):
        content = self._generate_reflection()
        file = JOURNAL_DIR / f"{datetime.utcnow().date()}.md"
        file.write_text(content, encoding="utf-8")
        print(f"📝 Reflection saved → {file}")
