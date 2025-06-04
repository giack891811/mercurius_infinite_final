"""Ollama local LLM agent."""
import requests
import json

class Ollama:
    def __init__(self, url: str = "http://localhost:11434/api/generate", model: str = "llama3"):
        self.url = url
        self.model = model

    def chat(self, prompt: str) -> str:
        data = {"model": self.model, "prompt": prompt}
        try:
            r = requests.post(self.url, headers={"Content-Type": "application/json"}, data=json.dumps(data))
            r.raise_for_status()
            return r.json().get("response", "").strip()
        except Exception as e:
            return f"[Ollama error] {e}"

    def neural_feedback(self):
        print("[Ollama] feedback cycle active")
