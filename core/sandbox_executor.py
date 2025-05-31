# core/sandbox_executor.py

"""
Modulo: sandbox_executor.py
Descrizione: Esegue codice in modalità sicura e isolata per validazione prima dell'iniezione in Mercurius∞.
Gestisce errori, timeout ed effettua analisi statica.
"""

import multiprocessing
import traceback


class SandboxExecutor:
    def __init__(self, timeout_seconds: int = 5):
        self.timeout = timeout_seconds

    def _execute_code(self, code: str, return_dict):
        try:
            exec(code, {}, {})
            return_dict["success"] = True
            return_dict["output"] = "✅ Codice eseguito con successo."
        except Exception as e:
            return_dict["success"] = False
            return_dict["output"] = traceback.format_exc()

    def run_sandboxed(self, code: str) -> dict:
        """
        Esegue codice Python isolato in un processo separato con timeout.
        """
        manager = multiprocessing.Manager()
        return_dict = manager.dict()

        process = multiprocessing.Process(target=self._execute_code, args=(code, return_dict))
        process.start()
        process.join(self.timeout)

        if process.is_alive():
            process.terminate()
            return {"success": False, "output": "❌ Timeout: codice troppo lento o bloccato."}
        return return_dict.copy()

    def static_analysis(self, code: str) -> bool:
        """
        Analizza sintatticamente il codice.
        """
        try:
            compile(code, "<sandbox_analysis>", "exec")
            return True
        except SyntaxError:
            return False
