# modules/autogen_chat.py

"""
Modulo: autogen_chat.py
Descrizione: Implementazione simulata di chat cooperativa multi-agente tramite Microsoft Autogen.
"""

class AutoGenChat:
    def __init__(self, agents=None):
        if agents is None:
            agents = ["Coder", "Planner", "Validator"]
        self.agents = agents

    def simulate_chat(self, topic: str):
        return "\n".join([f"{agent}: Partecipo alla discussione su '{topic}'." for agent in self.agents])


# Test
if __name__ == "__main__":
    chat = AutoGenChat()
    print(chat.simulate_chat("Sviluppo modulo di visione AI"))
