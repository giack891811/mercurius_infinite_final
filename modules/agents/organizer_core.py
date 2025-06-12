"""
🧠 Organizer Core – modules/agents/organizer_core.py
Coordina agenti AI organizzativi: CrewAI, SuperAGI, Autogen.
Assegna task, raccoglie risposte, sincronizza con l’orchestratore.
"""

from modules.agent_router import send_to_agent


class AgentOrganizer:
    def __init__(self) -> None:
        self.agents = {
            "AZR": "analyze",
            "Reasoner": "decide",
            "GPT": "evolve",
        }

    def dispatch_task(self, task: str, meta_context: dict | None = None) -> dict:
        meta_context = meta_context or {}
        results: dict[str, str] = {}
        for name, command in self.agents.items():
            try:
                results[name] = send_to_agent(name, command, task, meta_context)
            except Exception as e:
                results[name] = f"❌ Errore: {e}"
        return results

    def evaluate_outcomes(self, results: dict) -> str:
        ranked = sorted(results.items(), key=lambda x: len(x[1]), reverse=True)
        return ranked[0][1] if ranked else ""

    def run_crewai(self, task: str, ctx: dict) -> str:
        return f"[CrewAI] Coordinamento squadra AI per: {task}"

# Test diretto
if __name__ == "__main__":
    core = AgentOrganizer()
    task = "Costruisci una roadmap AI per Mercurius∞"
    out = core.dispatch_task(task)
    final = core.evaluate_outcomes(out)
    print("🎯 Strategia selezionata:")
    print(final)
