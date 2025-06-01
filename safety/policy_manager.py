# safety/policy_manager.py
"""
Modulo: policy_manager
Descrizione: Gestisce le policy etiche, di sicurezza e privacy per Mercurius∞.
Le policy sono definite in YAML ed estendibili in runtime.
"""

import yaml
from pathlib import Path
from typing import Dict, Any, List

POLICY_FILE = Path("safety/policies.yaml")


class PolicyManager:
    def __init__(self):
        self.policies: List[Dict[str, Any]] = []
        self.load_policies()

    # ---------- Public API ----------
    def load_policies(self) -> None:
        if POLICY_FILE.exists():
            self.policies = yaml.safe_load(POLICY_FILE.read_text(encoding="utf-8")) or []
        else:
            self.policies = []

    def add_policy(self, name: str, rule: str, action: str = "block") -> None:
        self.policies.append({"name": name, "rule": rule, "action": action})
        self._save()

    def check(self, text: str) -> Dict[str, Any] | None:
        """
        Ritorna la policy violata se text ne infrange una.
        """
        for pol in self.policies:
            if pol["rule"].lower() in text.lower():
                return pol
        return None

    # ---------- Private ----------
    def _save(self):
        POLICY_FILE.parent.mkdir(exist_ok=True, parents=True)
        yaml.safe_dump(self.policies, POLICY_FILE.open("w", encoding="utf-8"))
