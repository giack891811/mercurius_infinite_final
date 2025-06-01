# genesis_launcher.py

"""
Modulo: genesis_launcher.py
Descrizione:
Unisce il componente GenesisActivator per l’attivazione di GENESIS_MODE
con il ciclo di input interattivo che utilizza SafetyGuard per filtrare i comandi.
Log degli eventi e audit di ogni comando/processamento inclusi.
"""

from interface.genesis_bridge import GenesisBridge
from modules.ai_kernel.cognitive_integration import CognitiveCore
from dashboard.genesis_monitor import GenesisMonitor
from logs.genesis_logger import GenesisLogger
from memory.genesis_memory import GenesisMemory

from safety.safety_guard import SafetyGuard
from safety.audit_logger import audit


class GenesisActivator:
    def __init__(self):
        self.bridge = GenesisBridge()
        self.core = CognitiveCore()
        self.monitor = GenesisMonitor()
        self.logger = GenesisLogger()
        self.memory = GenesisMemory()

    def activate(self, method: str = "manual", command: str = "#genesis_mode"):
        """
        Se il comando corrisponde al trigger di GenesisBridge,
        abilita la modalità Genesis: log, monitoraggio, loop cognitivo e salvataggio del contesto.
        """
        if self.bridge.activate_from_command(command):
            self.logger.log_event("⚡ GENESIS_MODE trigger ricevuto")
            self.monitor.update_status("🟢 ATTIVO")
            self.core.start_thought_loop("INIZIO GENESIS")
            self.memory.save_context("last_trigger", method)
            self.monitor.show()
            return "✅ GENESIS attivato"
        return "⛔ Trigger ignorato"


if __name__ == "__main__":
    """
    Ciclo principale: legge l'input dell'utente, lo filtra con SafetyGuard e,
    se approvato, prova ad attivare GENESIS_MODE tramite GenesisActivator.
    Ogni comando e risposta viene infine registrato tramite l'audit logger.
    """
    guard = SafetyGuard(interactive=True)
    activator = GenesisActivator()

    while True:
        try:
            user_input = input("💬> ")
        except (EOFError, KeyboardInterrupt):
            print("\n✋ Uscita dal programma.")
            break

        # Filtra il testo con SafetyGuard
        safe_text = guard.filter_text(user_input)
        if not safe_text:
            # Messaggio omesso o rimosso da SafetyGuard
            continue

        # Prova ad attivare GENESIS_MODE
        response = activator.activate(method="interactive", command=safe_text)
        print(f"🤖 {response}")

        # Registra audit: comando utente e risposta data
        audit("user_command", {"input": user_input, "response": response})
