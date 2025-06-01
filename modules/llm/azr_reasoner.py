# modules/llm/azr_reasoner.py
"""
Modulo: azr_reasoner.py
Descrizione: Sistema di validazione logica del codice e dei pensieri AI secondo la logica AZR.
Utilizza analisi sintattica ed esecuzione controllata per determinare la validità di frammenti di codice.
"""
import ast
import traceback
from typing import Any

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
            test_env: dict[str, Any] = {}
            exec(compiled, test_env)
            self.log.append("✅ Execution succeeded.")
            return True
        except Exception as e:
            self.log.append(f"⚠️ Execution Error: {traceback.format_exc()}")
            return False

    def last_validation_log(self) -> str:
        """Restituisce le ultime voci di log della validazione."""
        return "\n".join(self.log[-5:])

# Funzione diretta per uso esterno
def validate_with_azr(code: str) -> bool:
    azr = AZRReasoning()
    return azr.validate_with_azr(code)

# Agente AZR: utilizza AZRReasoning per analizzare task di debug/logica
class AZRAgent:
    def __init__(self):
        self.azr = AZRReasoning()

    def analyze(self, text: str, context: dict = None) -> str:
        """
        Analizza il testo (es. codice) con la logica AZR e restituisce un responso.
        """
        code_to_check = text if context is None else context.get("code", text)
        success = self.azr.validate_with_azr(code_to_check)
        if success:
            return "✅ AZR: codice valido e logica consistente."
        else:
            # Include dettagli di errore nel risultato
            error_log = self.azr.last_validation_log()
            return f"❌ AZR: rilevate criticità logiche.\nLog: {error_log}"
