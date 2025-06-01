# modules/localai_executor.py

"""
Modulo: localai_executor.py
Descrizione: Wrapper per gestire LocalAI in locale con modelli in formato GGUF.
Supporta: GPT, STT/TTS, SD.
"""

import subprocess

class LocalAIExecutor:
    def __init__(self, base_url="http://localhost:8080"):
        self.base_url = base_url

    def call_model(self, prompt: str, model="gpt4all"):
        try:
            # Simulazione chiamata locale (sostituibile con requests.post se installato)
            command = f'curl -X POST {self.base_url}/chat -d \'{{"prompt": "{prompt}", "model": "{model}"}}\''
            output = subprocess.getoutput(command)
            return output
        except Exception as e:
            return f"❌ Errore durante l'esecuzione: {str(e)}"
