"""Genera nuovi agenti AI con configurazione autonoma."""

def generate_agent(name):
    with open(f"generated_agents/{name}.py", "w") as f:
        f.write(f"# Agente AI generato automaticamente: {name}\n")
from .adaptive_weights import update_weight