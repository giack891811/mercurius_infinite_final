"""Instrada i comandi verso l'agente registrato."""

from typing import Any

from .agent_registry import get_agent


_instances: dict[str, Any] = {}


def send_to_agent(name: str, command: str, message: str, context: dict | None = None) -> str:
    cls = get_agent(name)
    if cls is None:
        return f"Agente {name} non disponibile"
    if name not in _instances:
        _instances[name] = cls()
    agent = _instances[name]
    func = getattr(agent, command, None)
    if callable(func):
        return func(message) if context is None else func(message, context)
    elif hasattr(agent, "dispatch"):
        return agent.dispatch(message)
    return f"Comando {command} non supportato per {name}"
