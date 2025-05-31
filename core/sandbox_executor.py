# core/sandbox_executor.py

"""
Modulo: sandbox_executor.py
Descrizione: Esecuzione sicura, isolata e autoregolata di codice Python generato da Mercurius∞.
Include analisi statica, sandboxing con timeout, cattura stdout, e correzione automatica con AZR.
"""

import traceback
import contextlib
import io
import multiprocessing
from core.azr_reasoning import validate_with_azr


class SandboxExecutor:
    def __init__(self, timeout_seconds: int = 5):
        self.timeout = timeout_seconds
        self.last_output = ""
        self.last_error = ""

    def static_analysis(self, code: str) -> bool:
        """
        Verifica se il codice è sintatticamente valido.
        """
        try:
            compile(code, "<sandbox_analysis>", "exec")
            return True
        except SyntaxError:
            return False

    def _execute_code(self, code: str, return_dict):
        """
        Funzione interna per eseguire codice in un processo separato.
        """
        buffer = io.StringIO()
        local_vars = {}
        try:
            with contextlib.redirect_stdout(buffer):
                exec(code, {}, local_vars)
            return_dict["success"] = True
            return_dict["output"] = buffer.getvalue()
        except Exception as e:
            return_dict["success"] = False
            return_dict["output"] = traceback.format_exc()

    def run_sandboxed(self, code: str) -> dict:
        """
        Esegue codice in un ambiente isolato con timeout.
        """
        manager = multiprocessing.Manager()
        return_dict = manager.dict()

        process = multiprocessing.Process(target=self._execute_code, args=(code, return_dict))
        process.start()
        process.join(self.timeout)

        if process.is_alive():
            process.terminate()
            self.last_error = "❌ Timeout: codice troppo lento o bloccato."
            return {"success": False, "output": self.last_error}

        result = return_dict.copy()
        self.last_output = result.get("output", "")
        if not result.get("success"):
            self.last_error = self.last_output
            return {
                "success": False,
                "output": self.last_output,
                "suggested_fix": self.autofix_with_llm(code, self.last_output)
            }
        return result

    def autofix_with_llm(self, code: str, error_msg: str) -> str:
        """
        Richiede ad AZR una versione corretta del codice dato l'errore.
        """
        prompt = f"Codice:\n{code}\n\nErrore:\n{error_msg}\n\nSuggerisci una versione corretta:"
        return validate_with_azr(prompt)

    def report_stacktrace(self) -> str:
        return self.last_error or "Nessun errore registrato."

    def get_last_output(self) -> str:
        return self.last_output or "Nessun output disponibile."
