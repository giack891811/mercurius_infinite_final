# orchestrator/genesis_orchestrator.py
"""
Modulo: genesis_orchestrator.py
Descrizione: Coordinamento neurale tra agenti cognitivi (ChatGPT-4, AZR, Ollama3, GPT-4o).
"""
import logging
from utils.logger import setup_logger
logger = setup_logger("MercuriusGenesis")

# Agenti cognitivi integrati
from modules.llm.chatgpt_interface import ChatGPTAgent
from modules.llm.ollama3_interface import Ollama3Agent
from modules.llm.azr_reasoner import AZRAgent
from modules.llm.gpt4o_validator import GPT4oAgent

class GenesisOrchestrator:
    def __init__(self):
        self.agents = {
            "chatgpt4": ChatGPTAgent(),
            "ollama3": Ollama3Agent(),
            "azr": AZRAgent(),
            "gpt4o": GPT4oAgent()
        }

    def route_task(self, task: str, context: dict = None) -> dict:
        """
        Analizza il task e lo instrada all'agente più adatto, restituendo il risultato.
        """
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
        """
        Ogni agente contribuisce con un parere per un task comune; 
        il sistema seleziona la risposta più coerente tra quelle fornite.
        """
        logger.info(f"[GENESIS] Task condiviso per risposta congiunta: {task}")
        responses = {
            "chatgpt4": self.agents["chatgpt4"].elaborate(task),
            "ollama3": self.agents["ollama3"].generate(task),
            "azr": self.agents["azr"].analyze(task),
            "gpt4o": self.agents["gpt4o"].validate(task)
        }
        # Valutazione semplice basata su priorità predefinita (in futuro: ponderazione dinamica)
        priority = ["azr", "gpt4o", "chatgpt4", "ollama3"]
        for agent_key in priority:
            resp = str(responses.get(agent_key, "")).lower()
            if responses[agent_key] and "error" not in resp and "errore" not in resp:
                return {"source": agent_key, "response": responses[agent_key]}
        return {"source": "none", "response": "Nessuna risposta valida disponibile."}

if __name__ == "__main__":
    orchestrator = GenesisOrchestrator()
    sample_task = "crea codice per gestire input vocale e risposta testuale"
    result = orchestrator.coordinated_response(sample_task)
    print(f"🎯 Risposta selezionata ({result['source']}):\n{result['response']}")
