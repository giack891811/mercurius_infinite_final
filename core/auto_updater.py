# core/auto_updater.py

"""
Modulo: auto_updater.py
Descrizione: Gestione aggiornamenti intelligenti per Mercurius∞. Scarica, valuta e integra nuove funzionalità.
"""

import os
import json
import difflib
from datetime import datetime
from core.azr_reasoning import validate_with_azr


class AutoUpdater:
    def __init__(self, log_path="logs/update_log.json"):
        self.log_path = log_path
        self.updates = []
        self.load_log()

    def load_log(self):
        if os.path.exists(self.log_path):
            with open(self.log_path, "r") as f:
                self.updates = json.load(f)

    def save_log(self):
        with open(self.log_path, "w") as f:
            json.dump(self.updates, f, indent=2)

    def check_improvements(self, old_code: str, new_code: str) -> bool:
        prompt = f"Confronta queste due versioni di codice Python:\n---\nVECCHIO:\n{old_code}\n---\nNUOVO:\n{new_code}\n\nIl nuovo è migliorativo? Rispondi SÌ o NO con spiegazione."
        evaluation = validate_with_azr(prompt)
        return "SÌ" in evaluation.upper()

    def apply_code_patch(self, path: str, patch_code: str) -> str:
        if not os.path.exists(path):
            return f"❌ File {path} non trovato."
        with open(path, "r") as f:
            original = f.read()
        if self.check_improvements(original, patch_code):
            with open(path, "w") as f:
                f.write(patch_code)
            diff = list(difflib.unified_diff(original.splitlines(), patch_code.splitlines()))
            self.log_update("✔️ Approvato", "\n".join(diff), path)
            return f"✅ Patch applicata a {path}."
        else:
            return "⚠️ Patch rifiutata: non migliorativa."

    def log_update(self, decision: str, diff: str, file_path: str):
        self.updates.append({
            "file": file_path,
            "decision": decision,
            "diff": diff,
            "timestamp": datetime.now().isoformat()
        })
        self.save_log()
