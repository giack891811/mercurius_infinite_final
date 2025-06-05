"""codex_cli.py
==============
Interfaccia CLI/funzionale per interagire con Codex/OpenAI.
Esegue un prompt e restituisce codice generato.
"""

from __future__ import annotations

import os
import openai
from utils.logger import setup_logger

logger = setup_logger("CodexCLI")
openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_code(prompt: str) -> str:
    """Invia il prompt a Codex (o modello GPT) e restituisce il codice risultante."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=1024,
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as exc:
        logger.error(f"Errore Codex: {exc}")
        return f"Errore Codex: {exc}"


def run_codex(prompt: str | None = None) -> str:
    """Esegui Codex da linea di comando o come funzione."""
    if prompt is None:
        prompt = input("Codex prompt> ")
    logger.info(f"[CODEX] Invio prompt: {prompt}")
    result = generate_code(prompt)
    print(result)
    return result


if __name__ == "__main__":
    run_codex()
