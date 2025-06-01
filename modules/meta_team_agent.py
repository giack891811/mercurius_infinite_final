# modules/meta_team_agent.py

"""
Modulo: meta_team_agent.py
Descrizione: Simula un team AI composto da PM, Developer e QA utilizzando MetaGPT o logica equivalente. Coordina task evolutivi.
"""

class MetaTeamAgent:
    def __init__(self):
        self.roles = {
            "PM": self.project_manager,
            "DEV": self.developer,
            "QA": self.quality_assurance
        }

    def assign_task(self, task: str) -> str:
        pm_result = self.roles["PM"](task)
        dev_result = self.roles["DEV"](pm_result)
        return self.roles["QA"](dev_result)

    def project_manager(self, task: str) -> str:
        return f"[PM] Definizione requisiti per: {task}"

    def developer(self, spec: str) -> str:
        return f"[DEV] Implementazione codice basata su: {spec}"

    def quality_assurance(self, code: str) -> str:
        return f"[QA] Validazione e test eseguiti su: {code}"


# Test locale
if __name__ == "__main__":
    meta = MetaTeamAgent()
    print(meta.assign_task("Crea un modulo per la gestione vocale"))
