"""
Modulo: ollama3_interface.py
Descrizione: Interfaccia per comunicare con il server locale di Ollama 3 e ottenere risposte da modelli LLM open source.
"""

import requests
import json


class Ollama3Interface:
    def __init__(self, base_url="http://localhost:11434/api/generate", model="llama3"):
        self.base_url = base_url
        self.model = model

    def ask(self, prompt: str, stream: bool = False) -> str:
        """
        Invia un prompt al modello Ollama 3 e restituisce la risposta.
        """
        headers = {"Content-Type": "application/json"}
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": stream
        }

        try:
            response = requests.post(self.base_url, headers=headers, data=json.dumps(data))
            response.raise_for_status()

            if stream:
                return self._handle_stream_response(response)
            else:
                output = response.json().get("response", "").strip()
                return output
        except Exception as e:
            return f"⚠️ Errore comunicazione con Ollama: {e}"

    def _handle_stream_response(self, response) -> str:
        output = ""
        for line in response.iter_lines():
            if line:
                try:
                    decoded = json.loads(line.decode("utf-8"))
                    chunk = decoded.get("response", "")
                    output += chunk
                except json.JSONDecodeError:
                    continue
        return output


# Test del modulo
if __name__ == "__main__":
    ollama = Ollama3Interface()
    reply = ollama.ask("Scrivi una funzione Python che calcola il fattoriale.")
    print(reply)
