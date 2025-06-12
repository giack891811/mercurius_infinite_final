import importlib
import yaml
import sys

sys.modules["yaml"] = yaml
orch_module = importlib.import_module("orchestrator.orchestrator")
importlib.reload(orch_module)
orch_module.yaml = yaml
orch_module.yaml.safe_load = lambda f: {
    "agents": {"enabled": []},
    "communication": {"feedback_loop": True, "max_retries": 1, "retry_delay": 1, "update_cycle_seconds": 1},
    "mission_defaults": {"run_mode": "test", "tasks": []},
    "paths": {"transcripts": "t", "logs": "l"},
}
Orchestrator = orch_module.Orchestrator


def test_load_config():
    orch = Orchestrator()
    assert isinstance(orch.config, dict)
