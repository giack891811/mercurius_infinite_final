"""voice_bridge.py
Output vocale tramite engine TTS locale.
"""

from __future__ import annotations

import pyttsx3

_engine = pyttsx3.init()


def speak(text: str) -> None:
    """Riproduce testo tramite sintesi vocale."""
    _engine.say(text)
    _engine.runAndWait()
