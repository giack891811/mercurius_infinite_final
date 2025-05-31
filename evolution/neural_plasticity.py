# evolution/neural_plasticity.py

"""
Modulo: neural_plasticity.py
Descrizione: Simula la plasticità neurale rinforzando l'uso dei moduli più attivi nel sistema Mercurius∞.
Aggiorna il log sinaptico e crea una mappa di rafforzamento.
"""

from memory.synaptic_log import SynapticLog
from collections import defaultdict
import json
import os

PLASTICITY_TRACKER = "data/plasticity_weights.json"


class NeuralPlasticity:
    def __init__(self):
        self.log = SynapticLog()
        self.weights = defaultdict(int)
        self._load_weights()

    def _load_weights(self):
        if os.path.exists(PLASTICITY_TRACKER):
            with open(PLASTICITY_TRACKER, "r") as f:
                self.weights.update(json.load(f))

    def _save_weights(self):
        with open(PLASTICITY_TRACKER, "w") as f:
            json.dump(self.weights, f, indent=2)

    def reinforce_module_usage(self, module_name: str):
        self.weights[module_name] += 1
        self._save_weights()
        self.log.log_event("NeuralPlasticity", "Reinforced", f"{module_name}: {self.weights[module_name]}")
