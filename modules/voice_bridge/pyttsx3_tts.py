# modules/voice_bridge/pyttsx3_tts.py
"""
Modulo: pyttsx3_tts.py
Descrizione: Sintesi vocale offline compatibile con qualsiasi Python (usando pyttsx3).
"""

import pyttsx3

class Pyttsx3TTS:
    def __init__(self, voice_id=None):
        self.engine = pyttsx3.init()
        if voice_id:
            self.engine.setProperty('voice', voice_id)

    def speak(self, text: str):
        self.engine.say(text)
        self.engine.runAndWait()
