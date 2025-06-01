# orchestrator/patch_scheduler.py
"""
Modulo: patch_scheduler.py
Descrizione: Avvia periodicamente il SelfPatchEngine per evoluzione autonoma.
"""

import time
import threading
from analytics.self_patch_engine import SelfPatchEngine

class PatchScheduler:
    def __init__(self, interval_hours: int = 24):
        self.engine = SelfPatchEngine()
        self.interval = interval_hours * 3600
        threading.Thread(target=self._loop, daemon=True).start()

    def _loop(self):
        while True:
            try:
                self.engine.apply_patch()
            except Exception as e:
                print(f"⚠️ PatchScheduler error: {e}")
            time.sleep(self.interval)
