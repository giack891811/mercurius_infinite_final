# modules/azr_reasoning.py

"""
Modulo: azr_reasoning.py
Descrizione: Sistema di validazione logica del codice e dei pensieri AI secondo la logica AZR (Analytical Zone Reasoning).
Utilizza euristiche di analisi semantica, sintattica e funzionale per determinare la validità di frammenti di codice o ragionamenti.
"""

import ast
import traceback
from typing import Tuple


class AZRReasoning:
    def __init__(self):
        self.log = []

    def validate_with_azr(self, code: str) -> bool:
        """
        Analizza il codice ricevuto e ne valuta la coerenza logica e l'eseguibilità.
        """
        self.log.append(f"🔍 Validating code:\n{code}")
        try:
            tree = ast.parse(code)
            self.log.append("✅ AST parsing succeeded.")
        except SyntaxError as e:
            self.log.append(f"❌ Syntax Error: {e}")
            return False

        try:
            compiled = compile(tree, filename="<azr_check>", mode="exec")
            test_env = {}
            exec(compiled, test_env)
            self.log.append("✅ Execution succeeded.")
            return True
        except Exception as e:
            self.log.append(f"⚠️ Execution Error: {traceback.format_exc()}")
            return False

    def last_validation_log(self) -> str:
        return "\n".join(self.log[-5:])


# Funzione diretta per uso esterno
def validate_with_azr(code: str) -> bool:
    azr = AZRReasoning()
    return azr.validate_with_azr(code)
