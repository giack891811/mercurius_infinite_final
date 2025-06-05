# core/sleep_monitor.py

"""
Modulo: sleep_monitor.py
Descrizione: Monitoraggio inattività utente per attivare la modalità Self-Tuning.
"""

import time
from core.self_tuner import SelfTuner

class SleepMonitor:
    def __init__(self, idle_threshold=300):
        self.last_active = time.time()
        self.idle_threshold = idle_threshold
        self.tuner = SelfTuner()

    def notify_activity(self):
        self.last_active = time.time()

    def check_idle(self):
        if time.time() - self.last_active > self.idle_threshold:
            print("😴 Mercurius inattivo... attivazione Self-Tuning.")
            self.tuner.run_autoanalysis()
            self.last_active = time.time()

# Per essere integrato in `orchestrator.py` come thread parallelo
