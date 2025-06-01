# safety/human_override.py
"""
Modulo: human_override
Descrizione: Consente all'operatore umano di confermare/bloccare azioni critiche.
"""

from typing import Callable, Any

class HumanOverride:
    def __init__(self, interactive: bool = True):
        self.interactive = interactive

    def confirm(self, message: str) -> bool:
        """
        Chiede conferma all'utente per procedere con un'azione sensibile.
        In modalità non interattiva ritorna sempre False (azione bloccata).
        """
        if not self.interactive:
            print(f"⛔ Override: azione '{message}' bloccata (non-interactive).")
            return False
        reply = input(f"⚠️ Confermi azione critica? '{message}' (y/n): ").strip().lower()
        return reply in {"y", "yes"}

    def guard(self, message: str) -> Callable:
        """
        Decoratore per funzioni che necessitano approvazione umana.
        """

        def decorator(func: Callable) -> Callable:
            def wrapper(*args, **kwargs) -> Any:
                if self.confirm(message):
                    return func(*args, **kwargs)
                else:
                    print("🚫 Azione annullata dall'operatore.")
                    return None

            return wrapper

        return decorator
