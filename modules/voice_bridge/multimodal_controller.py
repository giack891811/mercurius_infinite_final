"""
Modulo: multimodal_controller
Descrizione: Gestione input/output multimodale vocale per Mercurius∞.
Autore: Mercurius∞ AI Engineer
"""

import time
from modules.voice_bridge.speech_to_text import WhisperSTT

# TTS avanzato (Nari Dia) + fallback
try:
    from modules.voice_bridge.nari_dia_tts import NariDiaTTS
    TTS_ENGINE = "nari"
except ImportError:
    from modules.voice_bridge.text_to_speech import TextToSpeech
    TTS_ENGINE = "pyttsx3"

class MultimodalController:
    def __init__(self):
        self.stt = WhisperSTT()
        if TTS_ENGINE == "nari":
            self.tts = NariDiaTTS()
        else:
            self.tts = TextToSpeech()

    def listen_and_respond(self, audio_file_path: str, ai_callback):
        """
        Ascolta un file audio, lo trascrive, passa il testo all'AI,
        e vocalizza la risposta.
        """
        print("🎧 Ricezione vocale in corso...")
        input_text = self.stt.transcribe(audio_file_path)
        print("🗣 Input:", input_text)

        response = ai_callback(input_text)
        print("🧠 Risposta AI:", response)

        time.sleep(0.5)  # Ottimizzazione dialogo
        self.tts.speak(response)
        return response

# Esecuzione di prova
if __name__ == "__main__":
    def mock_ai(text):
        return f"Hai detto: {text}"

    mmc = MultimodalController()
    mmc.listen_and_respond("sample_audio.wav", mock_ai)
