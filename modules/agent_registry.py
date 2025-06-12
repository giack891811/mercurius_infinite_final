"""Registro dinamico degli agenti disponibili."""

_REGISTRY: dict[str, type] = {}


def register_agent(name: str, cls: type) -> None:
    _REGISTRY[name] = cls


def get_agent(name: str):
    return _REGISTRY.get(name)


# Registrazione di agenti principali se disponibili
try:
    from modules.llm.azr_reasoner import AZRAgent

    register_agent("AZR", AZRAgent)
except Exception:
    pass

try:
    from modules.llm.chatgpt_interface import ChatGPTAgent

    register_agent("GPT", ChatGPTAgent)
except Exception:
    pass

try:
    from modules.reasoner_dispatcher import ReasonerDispatcher

    register_agent("Reasoner", ReasonerDispatcher)
except Exception:
    pass
