# orchestrator/router_integration.py
"""
Modulo: router_integration.py
Descrizione: Integrazione del nuovo AgentRouter nel GenesisOrchestrator.
"""

from cognition.cognitive_map import CognitiveMap
from cognition.task_memory import TaskMemory
from cognition.agent_router import AgentRouter
from orchestrator.genesis_orchestrator import GenesisOrchestrator

# Crea mappa e memory globali
c_map = CognitiveMap()
t_memory = TaskMemory()

# Registra gli agenti cognitivi principali
for name, typ in [
    ("ChatGPTAgent", "cognitive"),
    ("Ollama3Agent", "cognitive"),
    ("AZRAgent", "cognitive"),
    ("GPT4oAgent", "cognitive"),
    ("AdaptiveTrader", "trading"),
]:
    c_map.add_agent(name, typ)

router = AgentRouter(c_map, t_memory)
core = GenesisOrchestrator()


def run_task(task: str):
    agent_name = router.choose_agent(task)
    print(f"🔀 Router seleziona: {agent_name} per → {task}")
    response = core.route_task(task)
    success = "errore" not in str(response).lower()
    router.record_result(agent_name, task, success)
    return response


if __name__ == "__main__":
    while True:
        txt = input("Task> ")
        print(run_task(txt))
