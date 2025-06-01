from interface.genesis_bridge import GenesisBridge
from modules.ai_kernel.cognitive_integration import CognitiveCore
from dashboard.genesis_monitor import GenesisMonitor
from logs.genesis_logger import GenesisLogger
from memory.genesis_memory import GenesisMemory

class GenesisActivator:
    def __init__(self):
        self.bridge = GenesisBridge()
        self.core = CognitiveCore()
        self.monitor = GenesisMonitor()
        self.logger = GenesisLogger()
        self.memory = GenesisMemory()

    def activate(self, method: str = "manual", command: str = "#genesis_mode"):
        if self.bridge.activate_from_command(command):
            self.logger.log_event("⚡ GENESIS_MODE trigger ricevuto")
            self.monitor.update_status("🟢 ATTIVO")
            self.core.start_thought_loop("INIZIO GENESIS")
            self.memory.save_context("last_trigger", method)
            self.monitor.show()
            return "✅ GENESIS attivato"
        return "⛔ Trigger ignorato"

if __name__ == "__main__":
    trigger = GenesisActivator()
    print(trigger.activate())
