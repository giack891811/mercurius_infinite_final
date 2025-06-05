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
from core.thinking_loop import ThinkingLoop
from integrations.bridge_josch import send_command_to_pc
from sensors.sensor_hub import capture_screen_stream, listen_microphone

CONFIG_PATH = Path("config/genesis_config.yaml")

class Orchestrator:
    def __init__(self):
        self.config = self.load_config()
        self.agents = {}
        self.active = False
        self.sleep_monitor = SleepMonitor(idle_threshold=self.config.get("sleep_threshold", 300))
        self.thinking_loop: ThinkingLoop | None = None
        self.multisensorial_enabled = True

    def load_config(self):
        with open('config/config.yaml', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def activate_genesis(self):
        print("⚡ Attivazione modalità GENESIS...")
        self.active = True
        self.load_agents()
        self.start_feedback_loop()
        self.start_sleep_monitor()
        # Thinking loop opzionale
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                cfg = yaml.safe_load(f)
            if cfg.get("thinking_enabled", True):
                self.thinking_loop = ThinkingLoop(CONFIG_PATH)
                self.thinking_loop.start()
                print("🧠 Thinking loop attivo.")
        except Exception as e:
            print(f"⚠️ Errore avvio thinking loop: {e}")
        # 🔧 Patch: attiva anche il bridge Note10+ in parallelo
        try:
            from modules.vision_audio.note10_jarvis_bridge import start_jarvis_loop
            threading.Thread(target=start_jarvis_loop, daemon=True).start()
            print("📡 Note10+ Bridge attivo – In ascolto microfono e comandi vocali.")
        except Exception as e:
            print(f"⚠️ Errore avvio Note10+ Jarvis: {e}")
        # Avvia l'interfaccia mobile Flutter se disponibile
        try:
            from modules.mobile_flutter.flutter_bridge import start_mobile_ui
            threading.Thread(target=start_mobile_ui, daemon=True).start()
            print("📱 Mobile Jarvis UI attivo.")
        except Exception as e:
            print(f"⚠️ Errore avvio Mobile UI: {e}")
        #REMOTE_EXEC
        try:
            send_command_to_pc("start vscode")
        except Exception as e:
            print(f"⚠️ Errore invio comando PC: {e}")
        if self.multisensorial_enabled:
            try:
                capture_screen_stream()
                listen_microphone()
            except Exception as e:
                print(f"⚠️ Errore avvio sensori: {e}")
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

    def run_self_check(self, path: str = "."):
        """Esegue una scansione del progetto e produce un report."""
        print("🔍 Avvio self check dei moduli...")
        tuner = SelfTuner(project_root=path)
        tuner.run_autoanalysis()

    def execute_mission(self, mission_name: str):
        """Esegue una missione predefinita."""
        if mission_name == "#SELF_MISSION":
            try:
                from core.self_mission import genesis_directive
                genesis_directive()
            except Exception as exc:
                print(f"⚠️ Errore avvio SELF_MISSION: {exc}")
            self.activate_genesis()
        elif mission_name == "#ACTIVATE_NOTE_JARVIS":
            try:
                from modules.vision_audio.note10_jarvis_bridge import start_jarvis_loop
                start_jarvis_loop()
            except Exception as exc:
                print(f"⚠️ Errore attivazione Note10 Jarvis: {exc}")
        elif mission_name == "#ACTIVATE_MOBILE_UI":
            try:
                from modules.mobile_flutter.flutter_bridge import start_mobile_ui
                start_mobile_ui()
            except Exception as exc:
                print(f"⚠️ Errore attivazione Mobile UI: {exc}")
        else:
            print(f"⚠️ Missione sconosciuta: {mission_name}")


if __name__ == "__main__":
    orchestrator = Orchestrator()
    orchestrator.activate_genesis()
