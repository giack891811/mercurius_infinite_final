"""
Modulo: nlp.py
Responsabilità: Interpretazione semantica dei comandi vocali/testuali
Autore: Mercurius∞ Engineer Mode
"""

from typing import Dict


class CommandInterpreter:
    """
    Interpreta frasi e comandi naturali in azioni simboliche.
    """

    def __init__(self):
        self.known_commands = {
            "analizza l'ambiente": {"action": "analizza_ambiente"},
            "vai alla base": {"action": "raggiungi_destinazione", "context": {"destinazione": "base"}},
            "parla con me": {"action": "interagisci_utente"},
        }

    def interpret(self, text: str) -> Dict:
        """
        Converte una frase in comando semantico.
        """
        text = text.lower().strip()
        if text in self.known_commands:
            return self.known_commands[text]
        elif "ambiente" in text:
            return {"action": "analizza_ambiente"}
        elif "base" in text:
            return {"action": "raggiungi_destinazione", "context": {"destinazione": "base"}}
        elif "parla" in text or "conversazione" in text:
            return {"action": "interagisci_utente"}
        else:
            return {"action": "ignora", "context": {"frase": text}}
