"""
Modulo: genesis_orchestrator.py
Descrizione: Coordinamento neurale tra agenti cognitivi (ChatGPT-4, AZR, Ollama3, GPT-4o)
e moduli di supporto (AIScout, EyeAgent, SleepTimeCompute, TeacherMode).
"""

import subprocess
import threading
import time
from typing import Iterable

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


def auto_start_services(services: Iterable[str]) -> None:
    """Avvia in background servizi esterni richiesti."""
    for srv in services:
        try:
            subprocess.Popen([srv])
            logger.info(f"[BOOT] Avvio servizio: {srv}")
        except Exception as exc:  # pragma: no cover
            logger.error("Errore avvio %s: %s", srv, exc)


class GenesisOrchestrator:
    def __init__(self):
        # Agenti cognitivi
        self.agents = {
            "chatgpt4": ChatGPTAgent(),
            "ollama3": Ollama3Agent(),
            "azr": AZRAgent(),
            "gpt4o": GPT4oAgent()
        }

        # Moduli operativi
        self.modules = {
            "ai_scout": AIScout(),
            "sleep": SleepTimeCompute(),
            "eye_agent": EyeAgent(source=0, use_placeholder=True)
        }

        # Modalità insegnante
        self.teacher_mode = TeacherMode()

        # Avvio moduli in background
        threading.Thread(target=self.modules["sleep"].run, daemon=True).start()
        threading.Thread(target=self.modules["eye_agent"].start_stream, daemon=True).start()
        threading.Thread(target=self.teacher_mode.start, daemon=True).start()

        # Avvio ciclico Prompt di Dio
        threading.Thread(target=self.run_dioprompt_every_n, daemon=True).start()

    def route_task(self, task: str, context: dict = None) -> dict:
        """Instrada il task all'agente più adatto."""
        logger.info(f"[GENESIS] Routing del task: {task}")
        if "debug" in task or "logica" in task:
            return self.agents["azr"].analyze(task, context or {})
        elif "sintesi" in task or "finalizza" in task:
            return self.agents["gpt4o"].validate(task, context or {})
        elif "crea codice" in task or "script" in task:
            return self.agents["ollama3"].generate(task, context or {})
        else:
            return self.agents["chatgpt4"].elaborate(task, context or {})

    def coordinated_response(self, task: str) -> dict:
        """Tutti gli agenti contribuiscono; seleziona la risposta più coerente."""
        logger.info(f"[GENESIS] Task condiviso per risposta congiunta: {task}")
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
        if azr_retry and isinstance(azr_retry, dict):
            return {"source": "azr-fallback", "response": azr_retry}
        return {"source": "none", "response": "Nessuna risposta utile nemmeno da fallback AZR."}

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


if __name__ == "__main__":
    auto_start_services(["azr", "ollama", "n8n", "bridge_josch"])
    orchestrator = GenesisOrchestrator()
    sample_task = "crea codice per gestire input vocale e risposta testuale"
    result = orchestrator.coordinated_response(sample_task)
    print(f"🎯 Risposta selezionata ({result['source']}):\n{result['response']}")
else:
    auto_start_services(["azr", "ollama", "n8n", "bridge_josch"])
