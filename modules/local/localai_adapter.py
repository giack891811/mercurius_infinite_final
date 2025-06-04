"""
Modulo: localai_adapter.py
Descrizione: Integrazione LLM locale (es. GPT-2 HuggingFace).
Risponde ai prompt senza cloud. Funziona offline!
"""

import os

class LocalAI:
    def __init__(self, model_name="gpt2"):
        self.name = "LocalAI"
        try:
            from transformers import pipeline
            self.generator = pipeline("text-generation", model=model_name)
            self.online = True
        except Exception as e:
            self.generator = None
            self.online = False
            print(f"[LocalAI] Errore nel caricamento modello locale: {e}")

    def execute_task(self, prompt: str) -> str:
        if self.generator:
            try:
                output = self.generator(prompt, max_length=200, do_sample=True)
                return output[0]["generated_text"]
            except Exception as e:
                return f"[{self.name}] Errore modello locale: {e}"
        else:
            return f"[{self.name}] Offline: modello non disponibile. Prompt ricevuto: '{prompt}'."
