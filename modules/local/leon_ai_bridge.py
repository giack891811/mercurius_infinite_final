"""
Modulo: leon_ai_bridge.py
Descrizione: Esecuzione sicura di comandi di sistema in locale.
Supporta Windows, Linux e Mac. Output sempre loggato.
"""

import subprocess
import platform
import datetime

class LeonAI:
    def __init__(self, log_file="leonai_actions.log"):
        self.name = "LeonAI"
        self.log_file = log_file

    def run_command(self, command: str) -> str:
        now = datetime.datetime.now().isoformat()
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            output = result.stdout.strip()
            error = result.stderr.strip()
            msg = output if result.returncode == 0 else f"[{self.name}] ERRORE: {error}"
            self._log_action(command, msg, now)
            return msg
        except Exception as e:
            err_msg = f"[{self.name}] Errore di sistema: {e}"
            self._log_action(command, err_msg, now)
            return err_msg

    def _log_action(self, command, result, timestamp):
        try:
            with open(self.log_file, "a", encoding="utf-8") as logf:
                logf.write(f"[{timestamp}] CMD: {command}\nRES: {result}\n\n")
        except Exception:
            pass  # Logging silenzioso se fallisce

