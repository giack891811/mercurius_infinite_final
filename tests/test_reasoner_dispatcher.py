from modules.reasoner_dispatcher import ReasonerDispatcher


class DummyAgent:
    def __init__(self, resp: str):
        self.resp = resp

    def elaborate(self, prompt):
        return self.resp

    def generate(self, prompt):
        return self.resp

    def analyze(self, prompt):
        return self.resp

    def validate(self, prompt):
        return self.resp


def test_dispatcher_combines_responses():
    dispatcher = ReasonerDispatcher()
    dispatcher.reasoners = {
        "chatgpt4": DummyAgent("a"),
        "ollama3": DummyAgent("b"),
        "azr": DummyAgent("c"),
        "gpt4o": DummyAgent("final"),
    }
    result = dispatcher.dispatch("ciao")
    assert result == "final"
