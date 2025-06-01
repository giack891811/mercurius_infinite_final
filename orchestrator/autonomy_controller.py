"""
Modulo: autonomy_controller.py
Descrizione: Gestione autonoma delle esperienze e delle azioni eseguite da Mercurius∞.
Permette di registrare eventi, esiti e attivare modelli di adattamento comportamentale.
"""

from datetime import datetime

class AutonomyController:
    def __init__(self):
        self.experience_log = []

    def process_experience(self, action: str, outcome: str, success: bool, metadata: dict = None):
        """
        Registra un'esperienza eseguita da Mercurius, utile per addestramento successivo.
        """
        experience = {
            "timestamp": datetime.utcnow().isoformat(),
            "action": action,
            "outcome": outcome,
            "success": success,
            "metadata": metadata or {}
        }
        self.experience_log.append(experience)
        print(f"📒 Esperienza registrata → {action} | Successo: {success} | Extra: {metadata}")

    def get_history(self, limit=5):
        """
        Restituisce le ultime esperienze registrate.
        """
        return self.experience_log[-limit:]

    def reset_memory(self):
        """
        Pulisce la memoria esperienziale.
        """
        self.experience_log = []
        print("♻️ Memoria esperienziale resettata.")

    def summary(self):
        """
        Stampa un riassunto degli ultimi eventi appresi.
        """
        print("🧠 Riassunto Esperienze Recenti:")
        for exp in self.get_history(5):
            print(f"→ [{exp['timestamp']}] {exp['action']} => {exp['outcome']}")
