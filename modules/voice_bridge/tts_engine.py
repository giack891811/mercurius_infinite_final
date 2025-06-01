# modules/voice_bridge/tts_engine.py
"""
Modulo: tts_engine.py
Descrizione: Motore TTS basato su pyttsx3 per la sintesi vocale offline.
"""
from modules.speech import TextToSpeech

class Pyttsx3TTS(TextToSpeech):
    """
    Wrapper per il motore di sintesi vocale pyttsx3 (alias di TextToSpeech).
    """
    def __init__(self, voice_id=None):
        super().__init__(voice_id=voice_id)
