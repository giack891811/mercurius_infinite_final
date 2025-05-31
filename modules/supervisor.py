"""
Modulo: supervisor.py
Responsabilità: Monitoraggio comportamentale e strategico del sistema
Autore: Mercurius∞ Engineer Mode
"""

import time
import datetime
from typing import Dict, List


class ActionLog:
    """
    Rappresenta un'azione osservata dal supervisore.
    """

    def __init__(self, action: str, outcome: str, success: bool, context: Dict):
        self.timestamp = datetime.datetime.now().isoformat()
        self.action = action
        self.outcome = outcome
        self.success = success
        self.context = context

    def to_dict(self) -> Dict:
        return {
            "timestamp": self.timestamp,
            "action": self.action,
            "outcome": self.outcome,
            "success": self.success,
            "context": self.context
        }


class Supervisor:
    """
    Sistema di supervisione del comportamento cognitivo e operativo.
    """

    def __init__(self):
        self.logs: List[Dict] = []
        self.total_actions = 0
        self.total_success = 0
        self.total_failures = 0
        self.start_time = time.time()

    def observe(self, action: str, outcome: str, success: bool, context: Dict):
        """
        Registra un evento/azione osservato.
        """
        self.total_actions += 1
        if success:
            self.total_success += 1
        else:
            self.total_failures += 1

        log_entry = ActionLog(action, outcome, success, context)
        self.logs.append(log_entry.to_dict())

    def performance_report(self) -> Dict:
        """
        Fornisce un report generale delle prestazioni osservate.
        """
        uptime = time.time() - self.start_time
        return {
            "uptime_sec": int(uptime),
            "actions_total": self.total_actions,
            "successes": self.total_success,
            "failures": self.total_failures,
            "success_rate": round((self.total_success / self.total_actions) * 100, 2) if self.total_actions else 0.0
        }

    def last_actions(self, count: int = 5) -> List[Dict]:
        return self.logs[-count:]
