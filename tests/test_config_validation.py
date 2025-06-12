import yaml
from cerberus import Validator
from config.config_schema import CONFIG_SCHEMA


def test_config_validates(monkeypatch):
    def fake_load(_):
        return {
            "agents": {"enabled": ["A"]},
            "communication": {
                "feedback_loop": True,
                "max_retries": 1,
                "retry_delay": 1,
                "update_cycle_seconds": 1,
            },
            "mission_defaults": {"run_mode": "test", "tasks": []},
            "paths": {"transcripts": "t", "logs": "l"},
        }

    monkeypatch.setattr(yaml, "safe_load", fake_load, raising=False)
    with open("config/config.yaml", "r") as f:
        cfg = yaml.safe_load(f)
    v = Validator(CONFIG_SCHEMA)
    assert v.validate(cfg)
