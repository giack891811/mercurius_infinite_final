from modules.ai_kernel.agent_core import AgentCore


class DummyReasoner:
    def think(self, query: str) -> str:
        return "dummy decision"


def test_agent_boot(monkeypatch):
    monkeypatch.setattr(
        "modules.ai_kernel.agent_core.LangReasoner", lambda: DummyReasoner()
    )
    agent = AgentCore("TestAgent")
    agent.boot()
    assert agent.status == "ready"
