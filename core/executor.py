"""
Modulo: executor.py
Responsabilità: Esecuzione sicura e tracciata del codice generato o modificato
Autore: Mercurius∞ Engineer Mode
"""

import subprocess
import traceback
from typing import Tuple


class CodeExecutor:
    """
    Esegue file Python in modo isolato e ne cattura output ed errori.
    """

    def __init__(self, timeout: int = 10):
        self.timeout = timeout

    def run_python_file(self, filepath: str) -> Tuple[str, str]:
        """
        Esegue un file Python e ritorna stdout e stderr.
        """
        try:
            result = subprocess.run(
                ["python3", filepath],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=self.timeout,
                text=True
            )
            return result.stdout.strip(), result.stderr.strip()
        except subprocess.TimeoutExpired:
            return "", f"[ERROR] Timeout di {self.timeout}s superato."
        except Exception as e:
            return "", f"[EXCEPTION] {traceback.format_exc()}"

    def evaluate_output(self, output: str, expected_keywords: list) -> bool:
        """
        Valuta se l'output contiene i termini chiave attesi.
        """
        return all(keyword.lower() in output.lower() for keyword in expected_keywords)
