# modules/leonai_bridge.py

"""
Modulo: leonai_bridge.py
Descrizione: Integrazione Leon AI per il controllo testuale/vocale del sistema operativo.
"""

import os

class LeonAI:
    def execute_command(self, command: str) -> str:
        try:
            result = os.popen(command).read()
            return f"✅ Comando eseguito:\n{result}"
        except Exception as e:
            return f"❌ Errore: {str(e)}"


# Test
if __name__ == "__main__":
    leon = LeonAI()
    print(leon.execute_command("echo 'Mercurius è operativo!'"))
