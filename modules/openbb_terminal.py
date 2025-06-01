# modules/openbb_terminal.py

"""
Modulo: openbb_terminal.py
Descrizione: Wrapper per OpenBB Terminal. Supporta richieste CLI per dati e strategie via comando.
"""

import subprocess

class OpenBBWrapper:
    def run_command(self, command: str) -> str:
        try:
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True
            )
            return result.stdout or "✅ Comando eseguito"
        except Exception as e:
            return f"❌ Errore: {e}"


# Test
if __name__ == "__main__":
    obb = OpenBBWrapper()
    print(obb.run_command("echo 'Simulazione OpenBB'"))
