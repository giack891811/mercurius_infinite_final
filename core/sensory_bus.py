# core/sensory_bus.py

"""
Modulo: sensory_bus.py
Descrizione: Collettore centrale di segnali sensoriali audio-visivi per Mercurius∞.
Inoltra i dati ad altri moduli (es. ContextAdapter).
"""

from sensors.environment_analyzer import EnvironmentAnalyzer
from core.context_adapter import ContextAdapter
import threading
import time


class SensoryBus:
    def __init__(self):
        self.env = EnvironmentAnalyzer()
        self.ctx = ContextAdapter()
        self.running = False

    def start_stream(self, interval=5):
        self.running = True

        def loop():
            while self.running:
                noise = self.env.get_audio_level()
                vision = self.env.detect_motion()
                self.ctx.update_context(audio_level=noise, vision=vision)
                time.sleep(interval)

        threading.Thread(target=loop, daemon=True).start()

    def stop(self):
        self.running = False
