"""note_interface.py
Interfaccia HUD per Samsung Note10+ in stile Jarvis.
"""
from __future__ import annotations

import threading
import time

try:
    import requests
    import speech_recognition as sr
    import pyttsx3
    from kivy.app import App
    from kivy.uix.label import Label
    from kivy.uix.boxlayout import BoxLayout
    from kivy.core.window import Window
    from kivy.clock import Clock
except Exception:  # pragma: no cover - librerie opzionali
    requests = None
    sr = None
    pyttsx3 = None
    App = object  # type: ignore
    Label = object  # type: ignore
    BoxLayout = object  # type: ignore
    Window = object  # type: ignore
    Clock = object  # type: ignore

try:
    from voice.engine.elevenlabs_tts import ElevenLabsTTS
except Exception:  # pragma: no cover
    ElevenLabsTTS = None

HOTWORDS = ["aion", "signore", "analizza questo", "dimmi aion"]


class HUDApp(App):
    """Semplice interfaccia grafica translucida."""

    def build(self):
        if hasattr(Window, "clearcolor"):
            Window.clearcolor = (0, 0, 0, 0)
        self.label = Label(text="AION HUD", color=(0, 1, 1, 1), font_size="20sp")
        layout = BoxLayout(orientation="vertical")
        layout.add_widget(self.label)
        if hasattr(Clock, "schedule_interval"):
            Clock.schedule_interval(self._tick, 1)
        threading.Thread(target=self._listen_loop, daemon=True).start()
        return layout

    def _tick(self, _):  # pragma: no cover - placeholder animazione
        pass

    def _speak(self, text: str) -> None:
        if ElevenLabsTTS:
            try:
                ElevenLabsTTS().synthesize(text, voice="Jarvis")
                return
            except Exception:
                pass
        if pyttsx3:
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()

    def _listen_loop(self) -> None:
        if not sr:
            return
        recognizer = sr.Recognizer()
        mic = sr.Microphone()
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
        while True:
            with mic as source:
                audio = recognizer.listen(source, phrase_time_limit=4)
            try:
                text = recognizer.recognize_google(audio, language="it-IT").lower()
            except Exception:
                continue
            if any(hw in text for hw in HOTWORDS):
                response = self._ask_backend(text)
                self._speak(response)
                self.label.text = response

    def _ask_backend(self, prompt: str) -> str:
        if not requests:
            return "Elaboro, signore..."
        try:
            resp = requests.post("http://localhost:8000/ask", json={"prompt": prompt}, timeout=3)
            if resp.ok:
                return resp.json().get("response", "")
        except Exception:
            pass
        return "Elaboro, signore..."


def start_mobile_hud() -> None:
    """Avvia l'app mobile HUD."""
    HUDApp().run()


if __name__ == "__main__":  # pragma: no cover
    start_mobile_hud()

