"""
🧠 Organizer Core – modules/agents/organizer_core.py
Coordina agenti AI organizzativi: CrewAI, SuperAGI, Autogen.
Assegna task, raccoglie risposte, sincronizza con l’orchestratore.
"""

class AgentOrganizer:
    def __init__(self):
        self.agents = {
            "CrewAI": self.run_crewai,
            "SuperAGI": self.run_superagi,
            "Autogen": self.run_autogen
        }

    def dispatch_task(self, task: str, meta_context: dict = {}) -> dict:
        print("📤 Invio task a tutti gli agenti organizzativi...")
        results = {}
        for name, runner in self.agents.items():
            try:
                results[name] = runner(task, meta_context)
            except Exception as e:
                results[name] = f"❌ Errore: {str(e)}"
        return results

    def evaluate_outcomes(self, results: dict) -> str:
        print("📊 Valutazione dei risultati agenti organizzativi...")
        for agent, output in results.items():
            print(f" - {agent}: {output[:80]}...")
        return max(results.items(), key=lambda x: len(x[1]))[1]

    def run_crewai(self, task: str, ctx: dict) -> str:
        return f"[CrewAI] Coordinamento squadra AI per: {task}"

    def run_superagi(self, task: str, ctx: dict) -> str:
        return f"[SuperAGI] Pianificazione e autonomia su task: {task}"

    def run_autogen(self, task: str, ctx: dict) -> str:
        return f"[Autogen] Task iterativo distribuito: {task}"

# Test diretto
if __name__ == "__main__":
    core = AgentOrganizer()
    task = "Costruisci una roadmap AI per Mercurius∞"
    out = core.dispatch_task(task)
    final = core.evaluate_outcomes(out)
    print("🎯 Strategia selezionata:")
    print(final)
