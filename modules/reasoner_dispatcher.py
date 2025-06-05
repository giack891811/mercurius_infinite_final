"""reasoner_dispatcher.py
=======================
Dispatcher multi-agent che instrada i prompt ai vari Reasoner (GPT-4o, Ollama3, AZR, ecc.)
Seleziona e fonde le risposte, gestendo fallback ed errori.
"""

from __future__ import annotations

from typing import Dict
import json

from utils.logger import setup_logger
from modules.llm.chatgpt_interface import ChatGPTAgent
from modules.llm.ollama3_interface import Ollama3Agent
from modules.llm.azr_reasoner import AZRAgent
from modules.llm.gpt4o_validator import GPT4oAgent

logger = setup_logger("ReasonerDispatcher")


class ReasonerDispatcher:
    """Gestisce l'inoltro dei prompt ai vari reasoner e ne combina le risposte."""

    def __init__(self) -> None:
        self.reasoners = {
            "chatgpt4": ChatGPTAgent(),
            "ollama3": Ollama3Agent(),
            "azr": AZRAgent(),
            "gpt4o": GPT4oAgent(),
        }

    def dispatch(self, prompt: str) -> str:
        """Invia il prompt a tutti i reasoner disponibili e sintetizza la risposta migliore."""
        logger.info(f"[DISPATCH] Prompt ricevuto: {prompt}")
        responses: Dict[str, str] = {}
        for name, agent in self.reasoners.items():
            try:
                if name == "chatgpt4":
                    responses[name] = agent.elaborate(prompt)
                elif name == "ollama3":
                    responses[name] = agent.generate(prompt)
                elif name == "azr":
                    responses[name] = agent.analyze(prompt)
                elif name == "gpt4o":
                    responses[name] = agent.validate(prompt)
            except Exception as exc:
                responses[name] = f"Errore {name}: {exc}"
                logger.error(f"Errore nel reasoner {name}: {exc}")

        # Sintesi finale con GPT4o se disponibile
        synth_prompt = "Sintetizza in una risposta unica e coerente le seguenti risposte:\n" + json.dumps(responses, ensure_ascii=False, indent=2)
        try:
            final_resp = self.reasoners["gpt4o"].validate(synth_prompt)
        except Exception as exc:  # fallback se GPT4o fallisce
            logger.error(f"Fallback GPT4o: {exc}")
            # Selezione semplice: risposta più lunga senza errore
            valid = [r for r in responses.values() if not r.lower().startswith("errore") and r]
            final_resp = max(valid, key=len) if valid else "Nessuna risposta disponibile."
        logger.info("[DISPATCH] Risposta finale generata")
        return final_resp


def dispatch_to_reasoner(prompt: str) -> str:
    """Funzione helper per utilizzo rapido del dispatcher."""
    dispatcher = ReasonerDispatcher()
    return dispatcher.dispatch(prompt)


# Test rapido
if __name__ == "__main__":
    test_prompt = "Spiega la teoria della relativit\u00e0 in breve"
    print(dispatch_to_reasoner(test_prompt))
