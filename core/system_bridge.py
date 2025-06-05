# core/system_bridge.py

"""
Modulo: system_bridge.py
Descrizione: Ponte operativo tra Mercurius∞ e il sistema operativo dell’utente.
Permette accesso a file, esecuzione comandi e manipolazione directory in modo sicuro e tracciabile.
"""

import os
import subprocess
import platform
import logging

LOG_PATH = "logs/system_operations.log"
os.makedirs("logs", exist_ok=True)
logging.basicConfig(filename=LOG_PATH, level=logging.INFO, format="%(asctime)s - %(message)s")


class SystemBridge:
    def __init__(self):
        self.os_name = platform.system()

    def execute_command(self, command: str) -> str:
        """
        Esegue un comando shell e restituisce l’output.
        """
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            output = result.stdout.strip() or result.stderr.strip()
            self._log_operation("CMD", command, output)
            return output
        except Exception as e:
            self._log_operation("CMD_ERROR", command, str(e))
            return f"[Errore comando]: {e}"

    def read_file(self, path: str) -> str:
        """
        Legge il contenuto di un file.
        """
        try:
            with open(path, "r") as f:
                content = f.read()
            self._log_operation("READ_FILE", path, f"{len(content)} chars")
            return content
        except Exception as e:
            self._log_operation("READ_FILE_ERROR", path, str(e))
            return f"[Errore lettura file]: {e}"

    def write_file(self, path: str, content: str, mode: str = "w") -> str:
        """
        Scrive contenuto in un file (sovrascrive o aggiunge).
        """
        try:
            with open(path, mode) as f:
                f.write(content)
            self._log_operation("WRITE_FILE", path, f"{len(content)} chars")
            return "✅ Scrittura completata"
        except Exception as e:
            self._log_operation("WRITE_FILE_ERROR", path, str(e))
            return f"[Errore scrittura file]: {e}"

    def list_directory(self, directory: str = ".") -> str:
        """
        Elenca i file e sottocartelle di una directory.
        """
        try:
            files = os.listdir(directory)
            self._log_operation("LIST_DIR", directory, f"{len(files)} elementi")
            return "\n".join(files)
        except Exception as e:
            self._log_operation("LIST_DIR_ERROR", directory, str(e))
            return f"[Errore listing dir]: {e}"

    def _log_operation(self, action: str, target: str, result: str):
        """
        Registra ogni operazione in un log dedicato.
        """
        logging.info(f"{action} on {target} ➜ {result}")
