# genesis_orchestrator.py

"""
Modulo: genesis_orchestrator
Descrizione: Coordinamento neurale tra agenti cognitivi (ChatGPT-4, AZR, Ollama, GPT-4o)
Autore: Mercurius∞ Evolution Core
"""

import os
from typing import Dict, Any

# === AGENTI COGNITIVI INTEGRATI ===
from modules.llm.chatgpt_interface import ChatGPTAgent
from modules.llm.ollama3_interface import Ollama3Agent
from modules.llm.azr_reasoner import AZRAgent
from modules.llm.gpt4o_validator import GPT4oAgent

# === LOGGER BASE ===
from merc_io.logger import logger


class GenesisOrchestrator:
    def __init__(self):
        self.agents = {
            "chatgpt4": ChatGPTAgent(),
            "ollama3": Ollama3Agent(),
            "azr": AZRAgent(),
            "gpt4o": GPT4oAgent()
        }

    def route_task(self, task: str, context: Dict[str, Any] = {}) -> Dict[str, Any]:
        """
        Analizza il task e lo instrada all'agente più adatto.
        """
        logger.info(f"[GENESIS] Routing del task: {task}")

        if "debug" in task or "logica" in task:
            return self.agents["azr"].analyze(task, context)
        elif "sintesi" in task or "finalizza" in task:
            return self.agents["gpt4o"].validate(task, context)
        elif "crea codice" in task or "script" in task:
            return self.agents["ollama3"].generate(task, context)
        else:
            return self.agents["chatgpt4"].elaborate(task, context)

    def coordinated_response(self, task: str) -> Dict[str, Any]:
        """
        Ogni agente contribuisce con un parere per un task comune.
        Il sistema seleziona la risposta più coerente.
        """
        logger.info(f"[GENESIS] Task condiviso per risposta congiunta: {task}")
        responses = {
            "chatgpt4": self.agents["chatgpt4"].elaborate(task),
            "ollama3": self.agents["ollama3"].generate(task),
            "azr": self.agents["azr"].analyze(task),
            "gpt4o": self.agents["gpt4o"].validate(task)
        }

        # Valutazione con peso soggettivo (in futuro auto-adattivo)
        priority = ["azr", "gpt4o", "chatgpt4", "ollama3"]
        for agent in priority:
            if responses[agent] and "error" not in str(responses[agent]).lower():
                return {"source": agent, "response": responses[agent]}

        return {"source": "none", "response": "Nessuna risposta valida disponibile."}


if __name__ == "__main__":
    orchestrator = GenesisOrchestrator()
    task = "crea codice per gestire input vocale e risposta testuale"
    result = orchestrator.coordinated_response(task)
    print(f"🎯 Risposta selezionata ({result['source']}):\n{result['response']}")
