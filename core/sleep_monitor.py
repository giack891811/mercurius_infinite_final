# core/sleep_monitor.py

"""
Modulo: sleep_monitor.py
Descrizione: Monitoraggio inattività utente per attivare la modalità Self-Tuning.
"""

import time
import threading
from core.self_tuner import SelfTuner
from modules.scheduler.sleep_time_compute import SleepTimeCompute

class SleepMonitor:
    def __init__(self, idle_threshold=300):
        self.last_active = time.time()
        self.idle_threshold = idle_threshold
        self.tuner = SelfTuner()
        self.sleep_compute = SleepTimeCompute(interval=600)
        self._compute_thread: threading.Thread | None = None

    def notify_activity(self):
        self.last_active = time.time()

    def check_idle(self):
        if time.time() - self.last_active > self.idle_threshold:
            print("😴 Mercurius inattivo... attivazione Sleep Compute.")
            if not self._compute_thread or not self._compute_thread.is_alive():
                self._compute_thread = threading.Thread(target=self.sleep_compute.run, daemon=True)
                self._compute_thread.start()
            self.tuner.run_autoanalysis()
            self.last_active = time.time()

# Per essere integrato in `orchestrator.py` come thread parallelo
