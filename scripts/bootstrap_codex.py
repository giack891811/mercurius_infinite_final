"""
Script iniziale per ambiente Codex.
Attiva Mercurius, esegue check e lancia missione di completamento.
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from core.orchestrator import Orchestrator

def main():
    print("🚀 Avvio di Mercurius∞...")

    # Inizializza Orchestrator
    orchestrator = Orchestrator()

    # Esegue controllo e inizializzazione sistema
    print("🔍 Analisi interna...")
    orchestrator.run_self_check(path=".")

    # Attiva missione automatica di completamento
    print("🧠 Attivazione SELF_MISSION...")
    orchestrator.execute_mission("#SELF_MISSION")

if __name__ == "__main__":
    main()
