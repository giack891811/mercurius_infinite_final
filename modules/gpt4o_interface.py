"""
Modulo: gpt4o_interface.py
Descrizione: Comunicazione diretta con GPT-4o per validazione, riflessione e finalizzazione dei task AI.
"""

import openai
import os

class GPT4oInterface:
    def __init__(self, api_key: str = None, model: str = "gpt-4o"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        openai.api_key = self.api_key

    def ask(self, prompt: str, temperature: float = 0.7, max_tokens: int = 1024) -> str:
        """
        Invia un prompt a GPT-4o e restituisce la risposta testuale.
        """
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return f"❌ Errore GPT-4o: {str(e)}"


# Test locale
if __name__ == "__main__":
    gpt = GPT4oInterface()
    reply = gpt.ask("Validami questa funzione Python: def somma(a, b): return a + b")
    print(reply)
