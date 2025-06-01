"""
Script: start_voice_interface
Funzione: Comunicazione vocale Mercurius∞ da file audio nella root.
Autore: Mercurius∞ AI Engineer
"""

import os
from modules.voice_bridge.multimodal_controller import MultimodalController
from modules.ai_kernel.agent_core import AgentCore

AUDIO_FILE = "audio_input.wav"  # Assicurati che il file sia nella root!

def ensure_audio_exists(path):
    if not os.path.exists(path):
        print(f"[ERRORE] File audio non trovato: {path}")
        exit(1)

def avvia_interazione_vocale(audio_file):
    ensure_audio_exists(audio_file)

    agente = AgentCore()
    multimodale = MultimodalController()

    print("🎙️ Avvio comunicazione vocale...")
    multimodale.listen_and_respond(audio_file, agente.process_input)

if __name__ == "__main__":
    avvia_interazione_vocale(AUDIO_FILE)
