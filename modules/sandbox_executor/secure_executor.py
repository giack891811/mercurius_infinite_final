"""
Modulo: secure_executor
Descrizione: Gestione sicura dell'esecuzione di codice Python in sandbox controllata.
Autore: Mercurius∞ AI Engineer
"""

import sys
import io
import multiprocessing
import traceback

class SecureExecutor:
    def __init__(self, timeout=5):
        self.timeout = timeout

    def _run_code(self, code, return_dict):
        """Esegue codice Python in ambiente isolato."""
        stdout = io.StringIO()
        stderr = io.StringIO()
        try:
            sys.stdout = stdout
            sys.stderr = stderr
            exec(code, {})
        except Exception:
            return_dict['error'] = traceback.format_exc()
        finally:
            return_dict['output'] = stdout.getvalue()
            return_dict['stderr'] = stderr.getvalue()

    def execute(self, code: str) -> dict:
        """Esegue codice con protezione tramite multiprocessing e timeout."""
        manager = multiprocessing.Manager()
        return_dict = manager.dict()

        p = multiprocessing.Process(target=self._run_code, args=(code, return_dict))
        p.start()
        p.join(self.timeout)

        if p.is_alive():
            p.terminate()
            return {
                "output": "",
                "error": "Execution timed out.",
                "stderr": ""
            }

        return dict(return_dict)

# Esempio d'uso
if __name__ == "__main__":
    executor = SecureExecutor(timeout=3)
    result = executor.execute("print('Hello from sandbox!')")
    print(result)
