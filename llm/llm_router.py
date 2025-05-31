# llm/llm_router.py

"""
Modulo: llm_router.py
Descrizione: Router centralizzato per la gestione dei Large Language Models (LLM) usati da Mercurius∞.
Supporta OpenAI, Ollama e GPT-4o. Seleziona il modello in base a disponibilità, compito o preferenza.
"""

import requests
import openai
import json
import os

CONFIG_PATH = "config/llm_config.json"


class LLMRouter:
    def __init__(self):
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "r") as f:
                self.config = json.load(f)
        else:
            self.config = {
                "default_model": "openai",
                "openai_key": "",
                "ollama_url": "http://localhost:11434",
                "gpt4o_token": ""
            }

    def query(self, prompt: str, model: str = None) -> str:
        engine = model or self.config["default_model"]
        if engine == "openai":
            return self._query_openai(prompt)
        elif engine == "ollama":
            return self._query_ollama(prompt)
        elif engine == "gpt4o":
            return self._query_gpt4o(prompt)
        else:
            return f"[ERRORE] Modello non riconosciuto: {engine}"

    def _query_openai(self, prompt: str) -> str:
        try:
            openai.api_key = self.config["openai_key"]
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"[OpenAI Errore]: {e}"

    def _query_ollama(self, prompt: str) -> str:
        try:
            response = requests.post(
                f"{self.config['ollama_url']}/api/generate",
                json={"model": "llama3", "prompt": prompt}
            )
            return response.json().get("response", "[nessuna risposta da Ollama]")
        except Exception as e:
            return f"[Ollama Errore]: {e}"

    def _query_gpt4o(self, prompt: str) -> str:
        try:
            headers = {"Authorization": f"Bearer {self.config['gpt4o_token']}"}
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json={
                    "model": "gpt-4o",
                    "messages": [{"role": "user", "content": prompt}]
                }
            )
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"[GPT-4o Errore]: {e}"
