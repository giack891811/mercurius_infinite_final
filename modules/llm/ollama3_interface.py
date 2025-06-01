"""
Modulo: ollama3_interface
Descrizione: Interfaccia con Ollama3 per generazione di codice economica e brainstorming.
"""

import requests

class Ollama3Agent:
    def __init__(self, base_url="http://localhost:11434"):
        self.url = base_url

    def generate(self, prompt: str, context: dict = {}) -> str:
        try:
            response = requests.post(
                f"{self.url}/api/generate",
                json={"model": "llama3", "prompt": prompt}
            )
            return response.json().get("response", "Nessuna risposta.")
        except Exception as e:
            return f"Errore Ollama3: {e}"
