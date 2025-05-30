"""Esegue una richiesta GPT su prompt costruiti."""

from .prompt_builder import build_gpt_prompt

def run_gpt(intent):
    prompt = build_gpt_prompt(intent)
    return f"GPT> {prompt}"