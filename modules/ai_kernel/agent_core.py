# modules/ai_kernel/agent_core.py
"""
Modulo: agent_core
Descrizione: Nucleo base per agenti AI operativi e autonomi Mercurius∞.
"""
import time
from modules.ai_kernel.lang_reasoner import LangReasoner

class AgentCore:
    def __init__(self, name="Agent_001"):
        self.name = name
        self.memory = []
        self.status = "idle"
        # Integrazione di un motore di ragionamento linguistico (LLM) per decisioni avanzate
        self.reasoner = LangReasoner()

    def perceive(self, input_data):
        """Analizza i dati in ingresso e li registra nella memoria dell'agente."""
        print(f"[{self.name}] Percezione: {input_data}")
        self.memory.append(input_data)

    def reason(self):
        """Elabora i dati memorizzati e decide un'azione utilizzando l'LLM (se disponibile)."""
        if not self.memory:
            return "Nessun dato per ragionare."
        last_input = self.memory[-1]
        try:
            # Utilizza il modello di linguaggio per decidere l'azione di alto livello
            prompt = f"L'input ricevuto è: {last_input}. Decidi l'azione appropriata."
            decision = self.reasoner.think(prompt)
            return decision
        except Exception as e:
            # In caso di errore del motore LLM, fallback a logica base
            return f"Azione basata su: {last_input}"

    def act(self, decision):
        """Esegue l'azione risultante dalla decisione elaborata."""
        print(f"[{self.name}] Azione: {decision}")
        self.status = "active"

    def boot(self):
        """Ciclo operativo di avvio dell'agente (demo operativo)."""
        print(f"[{self.name}] Booting...")
        for i in range(3):
            self.perceive(f"input_{i}")
            decision = self.reason()
            self.act(decision)
            time.sleep(1)
        self.status = "ready"
        print(f"[{self.name}] Pronto all'azione.")
