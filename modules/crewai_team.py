# modules/crewai_team.py

"""
Modulo: crewai_team.py
Descrizione: Simulazione di un team AI con ruoli definiti (coder, manager, validator) basato su CrewAI.
"""

class CrewAI:
    def __init__(self):
        self.members = {
            "Project Manager": [],
            "Senior Coder": [],
            "Validator": []
        }

    def assign_task(self, role: str, task: str):
        if role in self.members:
            self.members[role].append(task)
            return f"📌 Task assegnato a {role}: {task}"
        else:
            return f"❌ Ruolo non valido: {role}"

    def team_report(self):
        return "\n".join([f"{role}: {', '.join(tasks)}" if tasks else f"{role}: 🔕 Nessun task" for role, tasks in self.members.items()])


# Test
if __name__ == "__main__":
    crew = CrewAI()
    print(crew.assign_task("Senior Coder", "Sviluppare interfaccia OCR"))
    print(crew.assign_task("Validator", "Verifica modulo vocale"))
    print(crew.team_report())
