"""
Modulo: agent_core
Descrizione: Nucleo base per agenti AI operativi e autonomi Mercurius∞.
Autore: Mercurius∞ AI Engineer
"""

import time

class AgentCore:
    def __init__(self, name="Agent_001"):
        self.name = name
        self.memory = []
        self.status = "idle"

    def perceive(self, input_data):
        """Analizza dati in ingresso."""
        print(f"[{self.name}] Percezione: {input_data}")
        self.memory.append(input_data)

    def reason(self):
        """Elabora e decide un'azione."""
        if not self.memory:
            return "Nessun dato per ragionare."
        return f"Azione basata su: {self.memory[-1]}"

    def act(self, decision):
        """Esegue l'azione risultante dalla decisione."""
        print(f"[{self.name}] Azione: {decision}")
        self.status = "active"

    def boot(self):
        """Ciclo operativo di avvio dell'agente."""
        print(f"[{self.name}] Booting...")
        for i in range(3):
            self.perceive(f"input_{i}")
            decision = self.reason()
            self.act(decision)
            time.sleep(1)
        self.status = "ready"
        print(f"[{self.name}] Pronto all'azione.")

# Test diretto
if __name__ == "__main__":
    agent = AgentCore()
    agent.boot()
