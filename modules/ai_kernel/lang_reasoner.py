# modules/ai_kernel/lang_reasoner.py
"""
Modulo: lang_reasoner
Descrizione: Wrapper base per ragionamento LLM-driven (integrazione modelli di linguaggio).
"""
import os
import openai

class LangReasoner:
    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        # Inizializza il modello di linguaggio (es. OpenAI GPT) e chiave API
        self.model = model_name
        self.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key

    def think(self, query: str) -> str:
        """
        Genera una risposta ragionata alla query fornita utilizzando un LLM.
        """
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": query}],
                temperature=0.7,
                max_tokens=150
            )
            answer = response['choices'][0]['message']['content'].strip()
            return answer
        except Exception as e:
            return f"[LangReasoner Error] {e}"
