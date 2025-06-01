# modules/llm/azr_interface.py

"""
Modulo: azr_interface
Descrizione: Interfaccia per il modulo AZRReasoning.
"""

from modules.azr_reasoning import AZRReasoning

class AZRAgent:
    def __init__(self):
        self.reasoner = AZRReasoning()

    def analyze(self, code: str, context: dict = {}) -> str:
        is_valid = self.reasoner.validate_with_azr(code)
        log = self.reasoner.last_validation_log()
        return f"Validazione: {'Successo' if is_valid else 'Fallita'}\nLog:\n{log}"
