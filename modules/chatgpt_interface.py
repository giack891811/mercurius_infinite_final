"""
Modulo: chatgpt_interface.py
Descrizione: Interfaccia tra Mercurius∞ e ChatGPT-4 per ragionamento, validazione e supporto decisionale.
"""

import openai
import os


class ChatGPTInterface:
    def __init__(self, model="gpt-4", temperature=0.4):
        self.model = model
        self.temperature = temperature
        self.api_key = os.getenv("OPENAI_API_KEY", "")

        if not self.api_key:
            raise ValueError("❌ OPENAI_API_KEY non definita nell'ambiente.")

        openai.api_key = self.api_key

    def ask(self, prompt: str, system: str = "Agisci come supervisore AI avanzato.") -> str:
        """
        Invia un messaggio a ChatGPT e restituisce la risposta.
        """
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                temperature=self.temperature,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt}
                ]
            )
            reply = response.choices[0].message.content.strip()
            return reply
        except Exception as e:
            return f"⚠️ Errore nella richiesta a ChatGPT: {e}"

    def validate_code(self, code_snippet: str) -> str:
        """
        Chiede a ChatGPT di validare un frammento di codice.
        """
        prompt = f"Valuta se il seguente codice è valido e migliorabile:\n\n{code_snippet}"
        return self.ask(prompt, system="Sei un validatore di codice Python altamente esperto.")


# Uso diretto
if __name__ == "__main__":
    gpt = ChatGPTInterface()
    print(gpt.ask("Qual è il significato della vita secondo l'informatica?"))
