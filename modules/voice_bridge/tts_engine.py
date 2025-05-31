"""
Modulo: tts_engine
Descrizione: Sintesi vocale offline usando pyttsx3 (compatibile Python 3.12).
Autore: Mercurius∞ AI Engineer
"""

import pyttsx3

class Pyttsx3TTS:
    def __init__(self, voice_id=None, rate=170):
        self.engine = pyttsx3.init()
        if voice_id:
            self.engine.setProperty('voice', voice_id)
        self.engine.setProperty('rate', rate)

    def speak(self, text: str):
        """Pronuncia il testo specificato."""
        print(f"[TTS] Parla: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

# Esempio
if __name__ == "__main__":
    tts = Pyttsx3TTS()
    tts.speak("Benvenuto in Mercurius infinito.")
