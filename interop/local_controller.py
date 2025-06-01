# interop/local_controller.py

"""
Modulo: local_controller.py
Descrizione: Controllo di comandi, cartelle e file del PC locale.
"""

import os
import subprocess

class LocalController:
    def list_dir(self, path="."):
        return os.listdir(path)

    def open_file(self, filepath):
        if os.path.exists(filepath):
            if os.name == "nt":  # Windows
                os.startfile(filepath)
            elif os.name == "posix":
                subprocess.call(["open" if "darwin" in os.sys.platform else "xdg-open", filepath])
            return True
        return False

    def run_script(self, script_path):
        try:
            subprocess.run(["python", script_path])
            return True
        except Exception as e:
            print(f"❌ Errore nell'esecuzione: {e}")
            return False
