# voice/vosk_stt.py

"""
Modulo: vosk_stt.py
Descrizione: Riconoscimento vocale locale con Vosk.
"""

import sounddevice as sd
import queue
import vosk
import json

class VoskSTT:
    def __init__(self, model_path="model"):
        self.model = vosk.Model(model_path)
        self.q = queue.Queue()

    def listen(self, duration=5, fs=16000):
        def callback(indata, frames, time, status):
            self.q.put(bytes(indata))
        with sd.RawInputStream(samplerate=fs, blocksize=8000, dtype="int16", channels=1, callback=callback):
            rec = vosk.KaldiRecognizer(self.model, fs)
            for _ in range(int(duration * fs / 8000)):
                data = self.q.get()
                if rec.AcceptWaveform(data):
                    res = json.loads(rec.Result())
                    return res.get("text", "")
            return ""
