"""
Modulo: chatgpt_interface
Descrizione: Interfaccia con ChatGPT-4 per ragionamento linguistico e conversazione.
"""

import openai
import os

class ChatGPTAgent:
    def __init__(self, model_name="gpt-4"):
        self.model = model_name
        self.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key

    def elaborate(self, prompt: str, context: dict = {}) -> str:
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Sei un assistente AI avanzato."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1024
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            return f"Errore ChatGPT: {e}"
