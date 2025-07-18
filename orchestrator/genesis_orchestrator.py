"""
Modulo: genesis_orchestrator.py
Descrizione: Coordinamento neurale tra agenti cognitivi (ChatGPT-4, AZR, Ollama3, GPT-4o)
e moduli di supporto (AIScout, EyeAgent, SleepTimeCompute, TeacherMode).
"""

import subprocess
import threading
import time
from typing import Iterable, Optional
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# ====================== BOOTSTRAP PATH E ENV ======================
load_dotenv()
sys.path.append(str(Path(__file__).resolve().parent.parent))

# ====================== IMPORT MERCURIUS ======================
from utils.logger import setup_logger
from modules.llm.chatgpt_interface import ChatGPTAgent
from modules.llm.ollama3_interface import Ollama3Agent
from modules.llm.azr_reasoner import AZRAgent
from modules.llm.gpt4o_validator import GPT4oAgent
from modules.scout.ai_scout import AIScout
from modules.teacher_mode import TeacherMode
from modules.scheduler.sleep_time_compute import SleepTimeCompute
from modules.vision.eye_agent import EyeAgent

logger = setup_logger("MercuriusGenesis")

# ====================== AVVIO SERVIZI ESTERNI ======================
def auto_start_services(services: Iterable[str]) -> None:
    """Avvia in background servizi esterni richiesti."""
    for srv in services:
        try:
            subprocess.Popen([srv])
            logger.info(f"[BOOT] Avvio servizio: {srv}")
        except Exception as exc:
            logger.error("Errore avvio %s: %s", srv, exc)

# ====================== ORCHESTRATORE ======================
class GenesisOrchestrator:
    def __init__(self):
        self.agents = {
            "chatgpt4": ChatGPTAgent(),
            "ollama3": Ollama3Agent(),
            "azr": AZRAgent(),
            "gpt4o": GPT4oAgent()
        }

        self.modules = {
            "ai_scout": AIScout(),
            "eye_agent": EyeAgent(source=0, use_placeholder=True),
            "sleep": SleepTimeCompute()
        }

        self.teacher_mode = TeacherMode()

        # Avvio moduli intelligenti in background
        threading.Thread(target=self.modules["sleep"].run, daemon=True).start()
        threading.Thread(target=self.modules["eye_agent"].start_stream, daemon=True).start()
        threading.Thread(target=self.teacher_mode.start, daemon=True).start()

        # Prompt di Dio (ciclo ogni N minuti)
        threading.Thread(target=self.run_dioprompt_every_n, daemon=True).start()

    def route_task(self, task: str, context: Optional[dict] = None) -> dict:
        """Smista un task all'agente più adatto."""
        logger.info(f"[GENESIS] Routing del task: {task}")
        context = context or {}
        if "debug" in task or "logica" in task:
            return self.agents["azr"].analyze(task, context)
        elif "sintesi" in task or "finalizza" in task:
            return self.agents["gpt4o"].validate(task, context)
        elif "crea codice" in task or "script" in task:
            return self.agents["ollama3"].generate(task, context)
        else:
            return self.agents["chatgpt4"].elaborate(task, context)

    def coordinated_response(self, task: str) -> dict:
        """Richiede risposta congiunta da tutti gli agenti."""
        logger.info(f"[GENESIS] Task congiunto: {task}")
        responses = {
            "chatgpt4": self.agents["chatgpt4"].elaborate(task),
            "ollama3": self.agents["ollama3"].generate(task),
            "azr": self.agents["azr"].analyze(task),
            "gpt4o": self.agents["gpt4o"].validate(task)
        }

        priority = ["azr", "gpt4o", "chatgpt4", "ollama3"]
        for agent_key in priority:
            resp = str(responses.get(agent_key, "")).lower()
            if responses[agent_key] and "error" not in resp and "errore" not in resp:
                return {"source": agent_key, "response": responses[agent_key]}

        logger.warning("⚠️ Nessuna risposta valida. Attivazione fallback AZR...")
        azr_retry = self.agents["azr"].solve(task)
        return {"source": "azr-fallback", "response": azr_retry or "Nessuna risposta utile."}

    def run_dioprompt_every_n(self, n: int = 3):
        """Esegue il Prompt di Dio ogni N minuti."""
        while True:
            time.sleep(n * 60)
            try:
                with open("config/prompt_di_dio.md", "r", encoding="utf-8") as f:
                    prompt = f.read()
                logger.info("📖 Prompt di Dio letto, invio agli agenti...")
                result = self.coordinated_response(prompt)
                logger.info(f"🧠 Risultato Prompt di Dio ({result['source']}):\n{result['response']}")
            except Exception as e:
                logger.error(f"[PromptDiDio] Errore esecuzione: {e}")

# ====================== ESECUZIONE LOCALE ======================
if __name__ == "__main__":
    auto_start_services(["azr", "ollama", "n8n", "bridge_josch"])
    orchestrator = GenesisOrchestrator()
    result = orchestrator.coordinated_response("analizza una strategia di breakout su BTC/USD")
    print(f"🎯 Risposta selezionata ({result['source']}):\n{result['response']}")
else:
    auto_start_services(["azr", "ollama", "n8n", "bridge_josch"])
