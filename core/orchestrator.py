"""
🧠 core/orchestrator.py
Modulo centrale di orchestrazione – Mercurius∞ Neural AI System
Gestisce la rete multi-agente in modalità GENESIS con auto-adattamento.
"""

import importlib
import yaml
import time
import threading
from pathlib import Path
from core.self_tuner import SelfTuner
from core.sleep_monitor import SleepMonitor

CONFIG_PATH = Path("config/genesis_config.yaml")

class Orchestrator:
    def __init__(self):
        self.config = self.load_config()
        self.agents = {}
        self.active = False
        self.sleep_monitor = SleepMonitor(idle_threshold=self.config.get("sleep_threshold", 300))

    def load_config(self):
        with open(CONFIG_PATH, "r") as f:
            return yaml.safe_load(f)

    def activate_genesis(self):
        print("⚡ Attivazione modalità GENESIS...")
        self.active = True
        self.load_agents()
        self.start_feedback_loop()
        self.start_sleep_monitor()
        print("✅ GENESIS attiva – Rete neurale in esecuzione.")

    def load_agents(self):
        print("🔌 Caricamento agenti dalla configurazione...")
        agent_groups = self.config.get("agents", {})
        for group, agent_list in agent_groups.items():
            self.agents[group] = []
            for agent_name in agent_list:
                try:
                    module_path = f"agents.{agent_name.lower()}"
                    agent_module = importlib.import_module(module_path)
                    agent = getattr(agent_module, agent_name)()
                    self.agents[group].append(agent)
                    print(f"🧠 Caricato agente: {agent_name} in {group}")
                except Exception as e:
                    print(f"⚠️ Errore caricamento {agent_name}: {e}")

    def start_feedback_loop(self):
        if self.config["communication"]["feedback_loop"]:
            print("🔁 Avvio feedback loop neurale...")
            threading.Thread(target=self.feedback_cycle, daemon=True).start()

    def feedback_cycle(self):
        cycle_time = self.config["communication"]["update_cycle_seconds"]
        while self.active:
            for group, agents in self.agents.items():
                for agent in agents:
                    if hasattr(agent, "neural_feedback"):
                        try:
                            agent.neural_feedback()
                        except Exception as e:
                            print(f"⚠️ Errore feedback {agent.__class__.__name__}: {e}")
            time.sleep(cycle_time)

    def start_sleep_monitor(self):
        print("😴 Monitoraggio inattività attivo...")
        threading.Thread(target=self._sleep_check_loop, daemon=True).start()

    def _sleep_check_loop(self):
        while self.active:
            self.sleep_monitor.check_idle()
            time.sleep(5)

    def notify_activity(self):
        self.sleep_monitor.notify_activity()


if __name__ == "__main__":
    orchestrator = Orchestrator()
    orchestrator.activate_genesis()
