"""OpenAI agent wrapper for Mercurius∞."""
import os
import openai

class OpenAI:
    def __init__(self, model: str = "gpt-3.5-turbo"):
        self.model = model
        openai.api_key = os.getenv("OPENAI_API_KEY", "")

    def chat(self, prompt: str) -> str:
        try:
            resp = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=200,
            )
            return resp["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return f"[OpenAI error] {e}"

    def neural_feedback(self):
        print("[OpenAI] feedback cycle active")
