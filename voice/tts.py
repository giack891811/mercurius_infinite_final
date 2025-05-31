# voice/tts.py (aggiornato)

"""
Modulo: tts.py
Descrizione: Sintesi vocale con fallback a gTTS se pyttsx3 non disponibile.
"""

try:
    import pyttsx3
    ENGINE = pyttsx3.init()
    USE_PYTTS = True
except ImportError:
    from gtts import gTTS
    import os
    USE_PYTTS = False


def speak(text: str):
    if USE_PYTTS:
        ENGINE.say(text)
        ENGINE.runAndWait()
    else:
        tts = gTTS(text=text, lang="it")
        file_path = "temp_audio.mp3"
        tts.save(file_path)
        os.system(f"start {file_path}" if os.name == "nt" else f"xdg-open {file_path}")
