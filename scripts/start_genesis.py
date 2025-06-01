"""
🚀 scripts/start_genesis.py
Script di avvio manuale per la modalità GENESIS – attiva il sistema AI Mercurius∞
"""

from core.orchestrator import Orchestrator
from core.self_mission import genesis_directive

def start():
    genesis_directive()
    orchestrator = Orchestrator()
    orchestrator.activate_genesis()

if __name__ == "__main__":
    start()
