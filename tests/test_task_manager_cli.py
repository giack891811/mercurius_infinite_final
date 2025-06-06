import sys
import types

# crea moduli Localai.local_ai e Leonai.leon_ai fittizi prima dell'import
localai_stub = types.SimpleNamespace(LocalAI=lambda: None)
leonai_stub = types.SimpleNamespace(LeonAI=lambda: None)
sys.modules.setdefault('modules.Localai.local_ai', localai_stub)
sys.modules.setdefault('modules.Leonai.leon_ai', leonai_stub)

import importlib
modules_cli = importlib.import_module('modules.task_manager_cli')


def test_create_agent(monkeypatch):
    called = {}

    def fake_bootstrap():
        called['ok'] = True

    monkeypatch.setattr(modules_cli, 'bootstrap_agents', fake_bootstrap)
    modules_cli.create_agent('AgentX')
    assert called.get('ok')
