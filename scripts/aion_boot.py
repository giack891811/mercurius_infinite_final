import os
import sys

# Aggiunge la root del progetto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.orchestrator import Orchestrator
from utils.environment import Environment


def main():
    print("🧬 Avvio AION – Modalità: dialogic-autonomous")

    env = Environment()
    os.environ["RUN_MODE"] = "dialogic-autonomous"
    print(f"🌐 AION_RUN_MODE = {env.get('RUN_MODE')}")

    orchestrator = Orchestrator()

    print("🚀 Avvio sistema GENESIS...")
    orchestrator.activate_genesis()

    print("🔍 Eseguo self-check...")
    orchestrator.run_self_check(path=".")

    try:
        from deployment.aion_api import start_api
        import threading
        threading.Thread(target=start_api, daemon=True).start()
        print("🌐 Aion API server avviato sulla porta 8000")
    except Exception as exc:
        print(f"⚠️ Avvio Aion API fallito: {exc}")

    try:
        from modules.voice_bridge.voice_loop import start_listening
        print("🎙️ Voice recognition attiva...")
        start_listening()
    except ImportError:
        print("⚠️ Voice module non disponibile")

    try:
        from modules.dashboard import launch_dashboard
        print("🖥️ Avvio dashboard...")
        launch_dashboard()
    except ImportError:
        print("⚠️ Dashboard non trovata")

    print("✅ AION operativo. In ascolto comandi.")

if __name__ == "__main__":
    main()
