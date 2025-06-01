"""
Modulo: command_interpreter.py
Descrizione: Interprete testuale dei comandi vocali o input testuali.
Autore: Mercurius∞ AI Engineer
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

        elif "analizza l'ambiente" in command:
            return {"action": "analizza_ambiente"}
        
        else:
            return {"action": "ignora", "reason": "comando non riconosciuto"}

# Esempio d’uso
if __name__ == "__main__":
    ci = CommandInterpreter()
    test_commands = [
        "Apri calendario",
        "Saluta",
        "Mostra report",
        "Analizza l'ambiente",
        "Qualcosa di strano"
    ]
    for cmd in test_commands:
        print(f"Input: {cmd} -> Output: {ci.interpret(cmd)}")
