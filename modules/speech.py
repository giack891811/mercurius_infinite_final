"""
Modulo: speech.py
Responsabilità: Gestione input vocale (ASR) e output vocale (TTS)
Autore: Mercurius∞ Engineer Mode
"""

try:
    import pyttsx3
except Exception:  # pragma: no cover - optional engine
    pyttsx3 = None
import speech_recognition as sr


class TextToSpeech:
    """
    Sintesi vocale basata su pyttsx3.
    """
    def __init__(self, voice_id=None):
        self.engine = None
        if pyttsx3 is not None:
            try:
                self.engine = pyttsx3.init()
                self.set_voice(voice_id)
            except Exception:
                self.engine = None

    def set_voice(self, voice_id):
        if not self.engine:
            return
        if voice_id is not None:
            self.engine.setProperty('voice', voice_id)
        else:
            voices = self.engine.getProperty('voices')
            if voices:
                self.engine.setProperty('voice', voices[0].id)

    def speak(self, text: str):
        if self.engine:
            self.engine.say(text)
            self.engine.runAndWait()
        else:
            print(f"[TTS] {text}")


class SpeechToText:
    """
    Riconoscimento vocale basato su speech_recognition.
    """
    def __init__(self, language: str = "it-IT"):
        self.recognizer = sr.Recognizer()
        self.language = language

    def listen(self, timeout: int = 5) -> str:
        with sr.Microphone() as source:
            print("🎙️ In ascolto...")
            audio = self.recognizer.listen(source, timeout=timeout)
            try:
                text = self.recognizer.recognize_google(audio, language=self.language)
                print("🗣️ Riconosciuto:", text)
                return text
            except sr.UnknownValueError:
                return "[ERROR] Non ho capito."
            except sr.RequestError as e:
                return f"[ERROR] Errore di connessione: {e}"
