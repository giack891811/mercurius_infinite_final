"""Simple gTTS based TTS engine."""
from gtts import gTTS
import os
import tempfile

class TextToSpeech:
    def __init__(self, lang: str = "it"):
        self.lang = lang

    def speak(self, text: str):
        tts = gTTS(text=text, lang=self.lang)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            tts.save(f.name)
            os.system(f"mpg123 -q {f.name}" if os.name != "nt" else f"start {f.name}")
