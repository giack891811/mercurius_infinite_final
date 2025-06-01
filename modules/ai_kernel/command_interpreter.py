"""
Modulo: command_interpreter.py
Descrizione: Interprete testuale dei comandi vocali o input testuali.
"""

class CommandInterpreter:
    def interpret(self, text: str) -> dict:
        command = text.strip().lower()
        if "apri" in command:
            return {"action": "apri_app", "context": {"app": command.replace("apri", "").strip()}}
        elif "saluta" in command:
            return {"action": "saluta"}
        elif "mostra" in command:
            return {"action": "mostra_dati"}
        else:
            return {"action": "ignora", "reason": "comando non riconosciuto"}
