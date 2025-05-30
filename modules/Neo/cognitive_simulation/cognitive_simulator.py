"""
cognitive_simulator.py

Simulatore di apprendimento esperienziale per agenti Mercurius.
Permette di far "vivere" esperienze sintetiche agli agenti per affinare le loro capacità decisionali e cognitive.

Include:
- Simulazione ambienti
- Cicli di esperienza-aggiustamento
- Valutazione e logging delle risposte
- Memoria di esperienze pregresse

Autore: Mercurius∞ – Ciclo 021
"""

import json
import os
from datetime import datetime
from pathlib import Path

EXPERIENCE_LOG = Path("memory") / "experiential_memory.json"
AGENT_PROFILE = Path("memory") / "agent_traits.json"


class CognitiveSimulator:
    def __init__(self):
        self.experience_log = self._load_json(EXPERIENCE_LOG, default=[])
        self.agent_traits = self._load_json(AGENT_PROFILE, default={})

    def _load_json(self, path, default):
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return default

    def _save_json(self, path, data):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def run_simulation(self, scenario_name, decisions, expected_outcomes):
        """
        scenario_name: str
        decisions: dict of {agent: decision}
        expected_outcomes: dict of {agent: expected_response}
        """
        report = []
        for agent, decision in decisions.items():
            expected = expected_outcomes.get(agent)
            feedback = "correct" if expected == decision else "incorrect"
            entry = {
                "agent": agent,
                "scenario": scenario_name,
                "decision": decision,
                "expected": expected,
                "feedback": feedback,
                "timestamp": datetime.now().isoformat()
            }
            self.experience_log.append(entry)
            self._adjust_trait(agent, feedback)
            report.append(entry)
        self._save_json(EXPERIENCE_LOG, self.experience_log)
        return report

    def _adjust_trait(self, agent, feedback):
        if agent not in self.agent_traits:
            self.agent_traits[agent] = {"accuracy": 0.5, "simulations": 0}
        data = self.agent_traits[agent]
        if feedback == "correct":
            data["accuracy"] += 0.01
        else:
            data["accuracy"] -= 0.01
        data["accuracy"] = max(0.0, min(1.0, data["accuracy"]))
        data["simulations"] += 1
        self._save_json(AGENT_PROFILE, self.agent_traits)

    def summary(self):
        return {
            "agents_trained": len(self.agent_traits),
            "total_experiences": len(self.experience_log)
        }


# USO ESEMPIO
if __name__ == "__main__":
    cs = CognitiveSimulator()
    simulation_result = cs.run_simulation(
        "decisione_critica_v1",
        decisions={"agent_risolve": "approccio_A", "agent_osserva": "approccio_B"},
        expected_outcomes={"agent_risolve": "approccio_A", "agent_osserva": "approccio_A"}
    )
    print("Risultato simulazione:", simulation_result)
    print("Riassunto:", cs.summary())