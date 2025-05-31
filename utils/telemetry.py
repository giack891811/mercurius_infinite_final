"""
Modulo: telemetry.py
Responsabilità: Raccolta telemetria interna (risorse, moduli, stato sistema)
Autore: Mercurius∞ Engineer Mode
"""

import psutil
import platform
import os
import time
from typing import Dict


class Telemetry:
    """
    Fornisce dati interni sullo stato del sistema e delle risorse.
    """

    @staticmethod
    def system_info() -> Dict:
        return {
            "platform": platform.system(),
            "platform_version": platform.version(),
            "architecture": platform.machine(),
            "cpu_count": psutil.cpu_count(),
            "memory_total_MB": round(psutil.virtual_memory().total / (1024 ** 2), 2),
        }

    @staticmethod
    def current_usage() -> Dict:
        mem = psutil.virtual_memory()
        return {
            "cpu_percent": psutil.cpu_percent(interval=0.5),
            "memory_used_MB": round(mem.used / (1024 ** 2), 2),
            "memory_percent": mem.percent,
            "active_processes": len(psutil.pids()),
            "uptime_sec": int(time.time() - psutil.boot_time())
        }

    @staticmethod
    def process_info(pid: int = os.getpid()) -> Dict:
        p = psutil.Process(pid)
        return {
            "pid": pid,
            "name": p.name(),
            "status": p.status(),
            "cpu_percent": p.cpu_percent(interval=0.5),
            "memory_MB": round(p.memory_info().rss / (1024 ** 2), 2),
            "threads": p.num_threads()
        }
