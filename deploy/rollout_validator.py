# deploy/rollout_validator.py
"""
Modulo: rollout_validator.py
Descrizione: Confronta nuovo build vs precedente (test unit e health endpoint).
"""

import requests
import subprocess
from pathlib import Path
from typing import Dict

class RolloutValidator:
    def __init__(self, health_url="http://localhost:8081/health"):
        self.health_url = health_url

    def run_tests(self) -> bool:
        """Esegue pytest in modalità silenziosa."""
        res = subprocess.run(["pytest", "-q"], capture_output=True, text=True)
        Path("logs/ci_test.log").write_text(res.stdout + res.stderr, encoding="utf-8")
        return res.returncode == 0

    def check_health(self) -> Dict[str, bool]:
        try:
            r = requests.get(self.health_url, timeout=3)
            return {"status": r.ok, "detail": r.json()}
        except Exception as e:
            return {"status": False, "detail": str(e)}

