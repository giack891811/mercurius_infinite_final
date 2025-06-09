"""
Verifica completa della struttura e dei moduli di Mercurius∞.
"""

import os
import importlib
from pathlib import Path

LOG_PATH = Path("logs/self_tuning_report.md")
MODULES = [
    "orchestrator.orchestrator",
    "orchestrator.genesis_orchestrator",
    "orchestrator.mission_controller",
    "modules.llm.chatgpt_interface",
    "modules.llm.ollama3_interface",
    "modules.llm.azr_reasoner",
    "modules.llm.gpt4o_validator",
    "integrations.bridge_josch",
    "utils.logger"
]


def check_module(name):
    try:
        importlib.import_module(name)
        return f"✅ {name} importato correttamente."
    except Exception as e:
        return f"❌ Errore nel modulo {name}: {e}"


def run_check():
    results = ["# 🔍 SELF CHECK – Mercurius∞", ""]
    results.append("**Moduli da verificare:**")
    for module in MODULES:
        results.append(check_module(module))
    
    results.append("\n**Controllo cartelle essenziali:**")
    folders = ["logs", "missions", "modules", "orchestrator"]
    for folder in folders:
        if os.path.exists(folder):
            results.append(f"✅ {folder}/ esiste")
        else:
            results.append(f"❌ {folder}/ mancante!")

    results.append("\n**Controllo completato.**")

    LOG_PATH.parent.mkdir(exist_ok=True)
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(results))
    
    print("\n".join(results))


if __name__ == "__main__":
    run_check()
