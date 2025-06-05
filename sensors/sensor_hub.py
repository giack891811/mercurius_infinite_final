"""sensor_hub.py
Cattura schermo e microfono con semplice hotword detection.
Espone stream FastAPI per integrazione multisensoriale.
"""

from __future__ import annotations

import io
from typing import Generator
from fastapi import FastAPI, Response
import uvicorn
from mss import mss
from PIL import Image
import speech_recognition as sr

app = FastAPI(title="Sensor Hub")


def _grab_screen() -> bytes:
    with mss() as sct:
        shot = sct.grab(sct.monitors[0])
        img = Image.frombytes("RGB", shot.size, shot.rgb)
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        return buf.getvalue()


def capture_screen_stream() -> bytes:
    """Restituisce un frame dello schermo in JPEG."""
    return _grab_screen()


@app.get("/vision")
def vision() -> Response:
    frame = _grab_screen()
    return Response(content=frame, media_type="image/jpeg")


def _recognize_speech(duration: int = 3) -> str:
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.record(source, duration=duration)
    try:
        return recognizer.recognize_google(audio, language="it-IT")
    except Exception:
        return ""


def listen_microphone(duration: int = 3) -> str:
    """Ritorna testo dal microfono."""
    return _recognize_speech(duration)


@app.get("/audio")
def audio() -> dict:
    text = _recognize_speech()
    return {"text": text}


def detect_hotword(hotword: str = "hey mercurius", duration: int = 3) -> bool:
    text = _recognize_speech(duration).lower()
    return hotword.lower() in text


@app.get("/hotword")
def hotword() -> dict:
    return {"detected": detect_hotword()}


def start_sensor_server(host: str = "0.0.0.0", port: int = 5124) -> None:
    """Avvia il server dei sensori."""
    uvicorn.run(app, host=host, port=port)
