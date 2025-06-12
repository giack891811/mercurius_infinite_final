"""Builder di pipeline SFT/DPO/RFT per AZR."""

import yaml
from pathlib import Path

from .fine_tuner import fine_tune_model
from .dataset_builder import md_to_jsonl


def train_from_config(config_path: str) -> str:
    cfg = yaml.safe_load(Path(config_path).read_text())
    md_path = cfg.get("dataset_md")
    jsonl_path = cfg.get("dataset_jsonl", "dataset.jsonl")
    if md_path:
        md_to_jsonl(md_path, jsonl_path)
    model = cfg.get("model", "gpt-3.5-turbo")
    return fine_tune_model(jsonl_path, model)


if __name__ == "__main__":
    import sys
    config_file = sys.argv[1] if len(sys.argv) > 1 else "config/finetune_config.yaml"
    job_id = train_from_config(config_file)
    print(f"Fine-tuning job: {job_id}")
