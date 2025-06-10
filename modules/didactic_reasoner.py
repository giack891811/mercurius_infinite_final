"""didactic_reasoner.py
Genera spiegazioni e domande partendo dal testo estratto dalla visione.
"""
from __future__ import annotations

from modules.llm.gpt4o_validator import GPT4oAgent
from modules.llm.azr_reasoner import validate_with_azr
from utils.logger import setup_logger

logger = setup_logger(__name__)


class DidacticReasoner:
    """Reasoner educativo semplificato."""

    def __init__(self) -> None:
        self.llm = GPT4oAgent()

    def generate_feedback(self, text: str) -> str:
        """Restituisce una breve spiegazione o domanda."""
        prompt = (
            "Sei un tutor AI. Osserva il seguente contenuto e offri un breve suggerimento o una domanda costruttiva:\n"
            + text
        )
        try:
            resp = self.llm.validate(prompt)
        except Exception as exc:  # pragma: no cover
            logger.error("LLM error: %s", exc)
            resp = ""
        if validate_with_azr(resp):
            return resp
        logger.warning("Output non validato da AZR")
        return ""
