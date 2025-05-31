# voice/whisper_engine.py

"""
Modulo: whisper_engine.py
Descrizione: Sintesi vocale inversa (STT) ad alta precisione con Whisper v3.
Supporta più lingue e trascrizione offline tramite modelli locali o OpenAI API.
"""

import os
import tempfile
import torch
import whisper


class WhisperSTT:
    def __init__(self, model_name="large-v3"):
        self.model = whisper.load_model(model_name)

    def transcribe_audio_file(self, audio_path: str, language: str = "it") -> str:
        result = self.model.transcribe(audio_path, language=language)
        return result.get("text", "[Nessun testo estratto]")

    def transcribe_microphone(self, duration=5, tmp_format="micro_input.wav") -> str:
        import sounddevice as sd
        import scipy.io.wavfile

        samplerate = 16000
        recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1)
        sd.wait()

        tmp_path = os.path.join(tempfile.gettempdir(), tmp_format)
        scipy.io.wavfile.write(tmp_path, samplerate, recording)
        return self.transcribe_audio_file(tmp_path)
