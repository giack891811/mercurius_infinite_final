"""
Modulo: secure_executor.py
Descrizione: Esecuzione sicura di codice Python in sandbox controllata con timeout.
Autore: Mercurius∞ AI Engineer
"""

import sys
import io
import multiprocessing
import traceback
import contextlib

class SecureExecutor:
    def __init__(self, timeout: int = 5):
        """
        timeout: tempo massimo di esecuzione in secondi
        """
        self.timeout = timeout

    def _run_code(self, code: str, return_dict):
        """Esegue codice Python in ambiente isolato e cattura output e errori."""
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
        """
        Esegue codice Python con timeout e isolamento tramite multiprocessing.
        Ritorna un dict con chiavi: output, stderr, error.
        """
        manager = multiprocessing.Manager()
        return_dict = manager.dict()

        proc = multiprocessing.Process(target=self._run_code, args=(code, return_dict))
        proc.start()
        proc.join(self.timeout)

        if proc.is_alive():
            proc.terminate()
            return {
                "output": "",
                "stderr": "",
                "error": "Execution timed out."
            }

        # Se l'errore non è stato catturato da exec, assegna stringa vuota
        if 'error' not in return_dict:
            return_dict['error'] = ""

        return dict(return_dict)

# Test esecuzione diretta
if __name__ == "__main__":
    executor = SecureExecutor(timeout=3)
    code_snippet = """
print('Hello from sandbox!')
for i in range(3):
    print(i)
"""
    result = executor.execute(code_snippet)
    print("Output:", result['output'])
    print("Error:", result['error'])
