# safety/safety_guard.py
"""
Modulo: safety_guard
Descrizione: Punto di ingresso globale per controlli policy + human override + audit.
"""

from safety.policy_manager import PolicyManager
from safety.human_override import HumanOverride
from safety.audit_logger import audit


class SafetyGuard:
    def __init__(self, interactive=True):
        self.policy_mgr = PolicyManager()
        self.override = HumanOverride(interactive=interactive)

    def filter_text(self, text: str) -> str | None:
        """
        Applica policy. Se violazione -> chiede override umano.
        Ritorna testo se permesso, None se bloccato.
        """
        violation = self.policy_mgr.check(text)
        if violation:
            audit("policy_violation", {"rule": violation["name"], "text": text})
            allowed = self.override.confirm(
                f"Violazione '{violation['name']}'. Consentire comunque?"
            )
            if not allowed:
                print("⛔ Bloccato da SafetyGuard.")
                return None
        return text
