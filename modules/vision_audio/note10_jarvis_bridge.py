"""note10_jarvis_bridge.py
Modulo: note10_jarvis_bridge
Descrizione: trasforma un Note10+ in assistente vocale continuo in stile Jarvis.
"""

from __future__ import annotations

import logging
import queue
import threading
import time
from typing import Callable, List, Optional

try:
    import sounddevice as sd
except Exception:  # pragma: no cover - sounddevice may not be available
    sd = None

try:
    import whisper
except Exception:  # pragma: no cover - whisper may not be installed
    whisper = None

try:
    import vosk
except Exception:  # pragma: no cover - vosk may not be installed
    vosk = None

try:
    import requests
except Exception:  # pragma: no cover
    requests = None

HOTWORDS = [
    "tu che ne pensi aion",
    "analizzami questo aion",
    "tu che dici aion",
    "vero aion",
    "giusto aion?",
]

logger = logging.getLogger(__name__)


class VoiceListener:
    """Microfono sempre attivo con hotword detection."""

    def __init__(self, hotwords: Optional[List[str]] = None, model: str = "base"):
        self.hotwords = [h.lower() for h in (hotwords or HOTWORDS)]
        self.model_name = model
        self._queue: queue.Queue[bytes] = queue.Queue()
        self._stop = threading.Event()
        self._callback: Optional[Callable[[str], None]] = None
        self.use_whisper = False
        self.use_vosk = False
        self._init_models()

    def _init_models(self) -> None:
        if whisper:
            try:
                self.whisper_model = whisper.load_model(self.model_name)
                self.use_whisper = True
                logger.info("Whisper model ready")
            except Exception as exc:  # pragma: no cover
                logger.warning("Whisper load failed: %s", exc)
        if not self.use_whisper and vosk:
            try:
                self.vosk_model = vosk.Model("model")
                self.use_vosk = True
                logger.info("Vosk model ready")
            except Exception as exc:  # pragma: no cover
                logger.warning("Vosk load failed: %s", exc)

    def start(self, on_trigger: Callable[[str], None]) -> None:
        self._callback = on_trigger
        threading.Thread(target=self._listen_loop, daemon=True).start()

    def stop(self) -> None:
        self._stop.set()

    def _audio_cb(self, indata, frames, time_info, status) -> None:
        self._queue.put(bytes(indata))

    def _listen_loop(self) -> None:
        if not sd:
            logger.error("sounddevice non disponibile")
            return
        with sd.InputStream(channels=1, samplerate=16000, callback=self._audio_cb):
            while not self._stop.is_set():
                time.sleep(0.1)
                if not self._queue.empty():
                    data = b"".join([self._queue.get() for _ in range(self._queue.qsize())])
                    text = self._transcribe(data)
                    if text:
                        lowered = text.lower().strip()
                        if any(h in lowered for h in self.hotwords):
                            logger.info("Hotword detected: %s", lowered)
                            if self._callback:
                                self._callback(lowered)

    def _transcribe(self, audio: bytes) -> str:
        if self.use_whisper:
            try:
                import numpy as np
                result = self.whisper_model.transcribe(np.frombuffer(audio, dtype="int16"), language="it")
                return result.get("text", "")
            except Exception as exc:  # pragma: no cover
                logger.error("Whisper error: %s", exc)
        if self.use_vosk:
            try:
                rec = vosk.KaldiRecognizer(self.vosk_model, 16000)
                if rec.AcceptWaveform(audio):
                    import json
                    return json.loads(rec.Result()).get("text", "")
            except Exception as exc:  # pragma: no cover
                logger.error("Vosk error: %s", exc)
        return ""


class PermissionHandler:
    """Gestisce l'autorizzazione dell'assistente."""

    def __init__(self) -> None:
        self.authorized = True

    def can_respond(self, speaker: Optional[str] = None) -> bool:
        return self.authorized

    def request(self) -> str:
        return "Signore, posso rispondere?"


class MercuriusConnector:
    """Invia e riceve messaggi da Mercurius∞."""

    def __init__(self, url: str = "http://localhost:8000/ask") -> None:
        self.url = url

    def ask(self, prompt: str) -> str:
        if not requests:
            logger.error("requests non disponibile")
            return ""
        try:
            resp = requests.post(self.url, json={"prompt": prompt}, timeout=10)
            if resp.ok:
                return resp.json().get("response", "")
            return ""
        except Exception as exc:  # pragma: no cover
            logger.error("HTTP error: %s", exc)
            return ""


class JarvisResponder:
    """Risposte vocali eleganti con TTS."""

    def __init__(self) -> None:
        self.voice = None
        self._init_tts()

    def _init_tts(self) -> None:
        try:
            from voice.engine.elevenlabs_tts import ElevenLabsTTS
            self.voice = ElevenLabsTTS()
        except Exception:  # pragma: no cover
            try:
                from voice.engine.coqui_tts import CoquiTTS  # type: ignore
                self.voice = CoquiTTS()
            except Exception:
                logger.warning("Nessun motore TTS disponibile")

    def speak(self, text: str) -> None:
        if not self.voice:
            print(f"[JARVIS]: {text}")
        else:
            try:
                self.voice.synthesize(text, voice="Jarvis")  # type: ignore[attr-defined]
            except Exception as exc:  # pragma: no cover
                logger.error("TTS error: %s", exc)
                print(f"[JARVIS]: {text}")


class Note10JarvisBridge:
    """Orchestratore del bridge vocale."""

    def __init__(self) -> None:
        self.listener = VoiceListener()
        self.responder = JarvisResponder()
        self.connector = MercuriusConnector()
        self.permissions = PermissionHandler()

    def _handle_phrase(self, phrase: str) -> None:
        if not self.permissions.can_respond():
            self.responder.speak("Con tutto il rispetto, io rispondo solo al mio creatore.")
            return
        response = self.connector.ask(phrase)
        if not response:
            self.responder.speak("Attenda un istante, Signore. Sto raccogliendo i dati")
        else:
            self.responder.speak(response.strip()[:250])

    def start(self) -> None:
        self.listener.start(self._handle_phrase)
        print("🤖 Note10 Jarvis Bridge attivo. Microfono in ascolto...")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.listener.stop()


def start_jarvis_loop() -> None:
    """Funzione helper per avviare il loop."""
    bridge = Note10JarvisBridge()
    bridge.start()
