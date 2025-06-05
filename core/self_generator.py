"""
Modulo: self_generator.py
Responsabilità: Autogenerazione e autoadattamento del codice
Autore: Mercurius∞ Engineer Mode
"""


from typing import Optional
import openai

from utils.environment import Environment


class SelfGenerator:
    """
    Sistema in grado di proporre modifiche al codice o generarne di nuovo, in modo autonomo.
    """

    def __init__(self, model="gpt-4"):
        self.env = Environment()
        self.model = model or self.env.get("OPENAI_CHAT_MODEL")
        self.api_key = self.env.get("OPENAI_API_KEY")
        openai.api_key = self.api_key

    def generate_module(self, description: str, filename: str) -> Optional[str]:
        """
        Genera un nuovo modulo Python a partire da una descrizione testuale.
        """
        prompt = f"""Agisci come un ingegnere AI. Scrivi un modulo Python che rispetti questa descrizione:
'{description}'
Il codice deve essere pronto all'uso, ben documentato e senza dipendenze non standard."""

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=1200
            )

            content = response['choices'][0]['message']['content']
            self._save_to_disk(filename, content)
            return filename

        except Exception as e:
            print(f"[ERROR] Errore generazione modulo: {e}")
            return None

def propose_update(self, filepath: str, task: str) -> Optional[str]:
    """
    Propose a patch to an existing Python file given a task description.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        prompt = f"""Hai il seguente file Python:

{content}

🧠 Il tuo compito è: {task}

Scrivi solo il codice aggiornato, completamente riscritto.
Commenta dove hai apportato modifiche o miglioramenti.
⚠️ Non scrivere testo aggiuntivo. Solo Python puro."""

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=1500
        )

        new_code = response['choices'][0]['message']['content']
        self._save_to_disk(filepath, new_code)
        return filepath

    except Exception as e:
        print(f"[ERROR] Errore aggiornamento: {e}")
        return None
