# orchestrator/sentient_mode.py
"""
Modulo: sentient_mode.py
Descrizione: Integrazione della modalità consapevole dentro Mercurius∞.
Avvia ReflectionLoop e gestisce IntentionManager in background.
"""

import threading
import time
from consciousness.reflection_loop import ReflectionLoop
from consciousness.intention_manager import IntentionManager

class SentientMode:
    def __init__(self, reflection_hour: int = 23):
        self.reflection = ReflectionLoop()
        self.intentions = IntentionManager()
        self.reflection_hour = reflection_hour
        # thread giornaliero
        threading.Thread(target=self._daily_routine, daemon=True).start()

    def _daily_routine(self):
        while True:
            now = time.gmtime()
            if now.tm_hour == self.reflection_hour and now.tm_min == 0:
                self.reflection.write_daily()
                time.sleep(60)  # evita doppio trigger
            time.sleep(30)

    # API esterna
    def add_intention(self, desc: str):
        self.intentions.add_intention(desc)

    def list_intentions(self):
        return self.intentions.active_intentions()


if __name__ == "__main__":
    sm = SentientMode()
    sm.add_intention("Migliorare la precisione del modulo trading del 5%")
    while True:
        time.sleep(3600)
