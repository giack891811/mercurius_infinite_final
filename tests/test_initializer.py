import pytest
from modules.start_fullmode.initializer import SystemInitializer

def test_system_initializer():
    system = SystemInitializer()
    assert system.agent is not None
    assert system.audio is not None
    assert system.vision is not None

def test_environment_setup(monkeypatch):
    monkeypatch.setenv("MERCURIUS_MODE", "")
    system = SystemInitializer()
    system.initialize_environment()
    assert "MERCURIUS_MODE" in os.environ
    assert os.environ["MERCURIUS_MODE"] == "full"
