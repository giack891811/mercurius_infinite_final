"""
Modulo: initializer
Descrizione: Avvio completo del sistema Mercurius∞ in modalità autonoma.
Autore: Mercurius∞ AI Engineer
"""

import os
import time
from modules.ai_kernel.agent_core import AgentCore
from modules.voice_bridge.audio_interface import AudioInterface
from modules.stream_vision.video_pipeline import VideoPipeline

class SystemInitializer:
    def __init__(self):
        self.agent = AgentCore()
        self.audio = AudioInterface()
        self.vision = VideoPipeline()

    def initialize_environment(self):
        """Setup iniziale del sistema."""
        print("[INIT] Configurazione ambiente...")
        os.environ['MERCURIUS_MODE'] = 'full'
        time.sleep(1)

    def start_components(self):
        """Avvia tutti i moduli principali."""
        print("[INIT] Avvio moduli principali...")
        self.vision.start()
        self.audio.initialize()
        self.agent.boot()

    def start_fullmode(self):
        """Avvia il sistema in modalità autonoma completa."""
        self.initialize_environment()
        self.start_components()
        print("[INIT] Mercurius∞ avviato in modalità FULLMODE.")

# Avvio diretto
if __name__ == "__main__":
    system = SystemInitializer()
    system.start_fullmode()
