# modules/llm/gpt4o_validator.py
"""
Modulo: gpt4o_validator.py
Descrizione: Validazione e finalizzazione di risposte tramite modello GPT-4 ottimizzato.
"""
import os
import openai

class GPT4oAgent:
    def __init__(self, model_name: str = "gpt-4"):
        self.model = model_name
        self.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key

    def validate(self, prompt: str, context: dict = None) -> str:
        """
        Genera una risposta perfezionata/sintetizzata per il prompt fornito, utilizzando GPT-4.
        """
        try:
            messages = [
                {"role": "system", "content": "Sei un assistente esperto in sintesi e perfezionamento delle risposte."},
                {"role": "user", "content": prompt}
            ]
            response = openai.ChatCompletion.create(model=self.model, messages=messages, temperature=0.7, max_tokens=1024)
            result = response['choices'][0]['message']['content']
            return result
        except Exception as e:
            return f"Errore GPT4o: {e}"
