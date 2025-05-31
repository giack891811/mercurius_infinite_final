# voice/tts.py

"""
Modulo: tts.py
Descrizione: Sintesi vocale del testo tramite libreria pyttsx3 (offline, locale).
"""

import pyttsx3

engine = pyttsx3.init()

def speak(text: str):
    """
    Legge ad alta voce il testo fornito.
    """
    engine.say(text)
    engine.runAndWait()
