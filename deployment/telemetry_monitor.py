# deployment/telemetry_monitor.py

"""
Modulo: telemetry_monitor.py
Descrizione: Telemetria di base per Mercurius∞. Traccia uptime, stato, log recenti.
"""

import os
import time
import platform
import psutil
from datetime import datetime


class TelemetryMonitor:
    def __init__(self):
        self.start_time = time.time()

    def get_uptime(self) -> str:
        uptime_sec = time.time() - self.start_time
        return str(datetime.timedelta(seconds=int(uptime_sec)))

    def get_system_status(self) -> dict:
        return {
            "platform": platform.platform(),
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory": psutil.virtual_memory()._asdict(),
            "disk": psutil.disk_usage("/")._asdict(),
        }

    def get_logs_tail(self, path: str, lines: int = 10) -> str:
        if not os.path.exists(path):
            return "[Nessun log trovato]"
        with open(path, "r") as f:
            return "\n".join(f.readlines()[-lines:])
