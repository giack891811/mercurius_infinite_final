"""voice_feedback.py
Sintesi vocale semplificata per fornire feedback all'utente."""
try:
    import pyttsx3
except Exception:  # pragma: no cover - optional
    pyttsx3 = None

from utils.logger import setup_logger

logger = setup_logger(__name__)

_engine = pyttsx3.init() if pyttsx3 else None


def speak_feedback(text: str) -> None:
    """Pronuncia o stampa il feedback."""
    if _engine:
        try:
            _engine.say(text)
            _engine.runAndWait()
        except Exception as exc:  # pragma: no cover
            logger.error("TTS error: %s", exc)
            print(text)
    else:
        print(text)
