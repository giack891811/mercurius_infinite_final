"""Costruzione prompt per Ollama."""

def build_prompt(task, context=""):
    return f"Ollama: {task}\nContesto: {context}"