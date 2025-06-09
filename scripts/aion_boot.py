import os
import sys
import time
import threading

# Aggiunge la root del progetto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.orchestrator import Orchestrator
from utils.environment import Environment
from ai_launcher import ensure_ai_online


def main():
    print("🧬 Avvio AION – Modalità: dialogic-autonomous")

    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass


    env = Environment()
    os.environ["RUN_MODE"] = "dialogic-autonomous"
    print(f"🌐 AION_RUN_MODE = {env.get('RUN_MODE')}")

    print("🔧 Verifica servizi critici...")
    ensure_ai_online()

    orchestrator = Orchestrator()

    print("🚀 Avvio sistema GENESIS...")
    orchestrator.activate_genesis()

    print("🔍 Eseguo self-check...")
    orchestrator.run_self_check(path=".")

    try:
        from deployment.aion_api import start_api
        threading.Thread(target=start_api, daemon=True).start()
        print("🌐 Aion API server avviato sulla porta 8000")
    except Exception as exc:
        print(f"⚠️ Avvio Aion API fallito: {exc}")

    try:
        from modules.voice_bridge.voice_loop import start_listening
        print("🎙️ Voice recognition attiva...")
        threading.Thread(target=start_listening, daemon=True).start()
    except Exception as exc:
        print(f"⚠️ Voice module non disponibile: {exc}")

    try:
        headless = env.get("HEADLESS", "0") == "1"
        if not headless:
            from modules.dashboard import launch_dashboard
            print("🖥️ Avvio dashboard...")
            threading.Thread(target=launch_dashboard, daemon=True).start()
        else:
            print("🖥️ Modalità headless attiva - dashboard disabilitata")
    except Exception as exc:
        print(f"⚠️ Dashboard non trovata: {exc}")

    print("✅ AION operativo. In ascolto comandi.")

    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
