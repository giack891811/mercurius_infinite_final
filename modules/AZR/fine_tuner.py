"""Wrapper per avviare un fine-tuning con OpenAI API."""

import os
import openai


def fine_tune_model(dataset_path: str, model: str = "gpt-3.5-turbo") -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY non impostata")
    openai.api_key = api_key
    try:
        job = openai.FineTuningJob.create(training_file=dataset_path, model=model)
        return job.id
    except Exception as exc:
        return f"Errore fine-tuning: {exc}"
