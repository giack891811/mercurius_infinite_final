"""
Modulo: autonomy_controller.py
Descrizione: Gestione autonoma delle esperienze e delle azioni eseguite da Mercurius∞.
Permette di registrare eventi, esiti e attivare modelli di adattamento comportamentale.
Autore: Mercurius∞ AI Engineer
"""

from datetime import datetime
from collections import Counter
from typing import List, Dict, Any


class AutonomyController:
    def __init__(self):
        # lista di dizionari esperienza
        self.experience_log: List[Dict[str, Any]] = []

    # ------------------------------------------------------------------ #
    #                       REGISTRAZIONE ESPERIENZA                     #
    # ------------------------------------------------------------------ #
    def process_experience(
        self,
        action: str,
        outcome: str,
        success: bool,
        context: dict | None = None,
    ) -> Dict[str, Any]:
        """
        Registra un’esperienza di Mercurius∞.

        Ritorna il dizionario esperienza, che ora include la chiave
        “learning” richiesta dai test.
        """
        experience = {
            "timestamp": datetime.utcnow().isoformat(),
            "action": action,
            "outcome": outcome,
            "success": success,
            "context": context or {},
            # feedback di apprendimento elementare
            "learning": (
                "Apprendimento registrato: rinforzo positivo."
                if success
                else "Apprendimento registrato: rinforzo negativo."
            ),
        }
        self.experience_log.append(experience)
        print(
            f"📒 Esperienza registrata → {action} | Successo: {success} | "
            f"Extra: {context or {}}"
        )
        return experience

    # ------------------------------------------------------------------ #
    #                              UTILITÀ                               #
    # ------------------------------------------------------------------ #
    def get_history(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Restituisce le ultime *limit* esperienze."""
        return self.experience_log[-limit:]

    def reset_memory(self) -> None:
        """Svuota la memoria esperienziale."""
        self.experience_log = []
        print("♻️ Memoria esperienziale resettata.")

    def summary(self) -> None:
        """Stampa a video un breve riassunto delle ultime esperienze."""
        print("🧠 Riassunto Esperienze Recenti:")
        for exp in self.get_history(5):
            print(f"→ [{exp['timestamp']}] {exp['action']} ⇒ {exp['outcome']}")

    # ------------------------------------------------------------------ #
    #                        RIEPILOGO STATISTICO                         #
    # ------------------------------------------------------------------ #
    def summarize_autonomy(self) -> dict:
        """
        Ritorna un riepilogo statistico con la chiave “reflection_summary”
        richiesta dai test end-to-end.
        """
        total = len(self.experience_log)
        successes = sum(e["success"] for e in self.experience_log)
        failures = total - successes
        most_common = Counter(e["action"] for e in self.experience_log).most_common(1)

        return {
            "total": total,
            "success_rate": successes / total if total else 0.0,
            "top_action": most_common[0][0] if most_common else None,
            "reflection_summary": {
                "successes": successes,
                "failures": failures,
            },
        }

    # ------------------------------------------------------------------ #
    #                        INSIGHT GLOBALI (NUOVO)                    #
    # ------------------------------------------------------------------ #
    def report_insights(self) -> dict:
        """
        Restituisce insight globali semplici sulla memoria autonoma:
         - Azioni più frequenti
         - Tassi di successo e fallimento
         - Ultime azioni eseguite
        """
        total = len(self.experience_log)
        if total == 0:
            return {"insight": "Nessuna esperienza registrata."}

        actions = [e["action"] for e in self.experience_log]
        outcomes = [e["outcome"] for e in self.experience_log]
        successes = [e for e in self.experience_log if e["success"]]
        failures = [e for e in self.experience_log if not e["success"]]

        most_common = Counter(actions).most_common(3)
        outcome_types = Counter(outcomes).most_common()

        return {
            "totale_esperienze": total,
            "azioni_frequenti": [a for a, _ in most_common],
            "tasso_successo": round(len(successes) / total, 2),
            "tasso_fallimento": round(len(failures) / total, 2),
            "ultime_azioni": actions[-5:],
            "outcome_summary": outcome_types,
        }


# -------------------------- TEST MANUALE RAPIDO -------------------------- #
if __name__ == "__main__":
    ac = AutonomyController()
    ac.process_experience("saluta", "ok", True, {"note": "inizio"})
    ac.process_experience("richiedi_input", "ok", True)
    ac.process_experience("rispondi", "errore", False)
    print(ac.summarize_autonomy())
    print(ac.report_insights())
    ac.summary()
