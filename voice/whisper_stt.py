# voice/whisper_stt.py

"""
Modulo: whisper_stt.py
Descrizione: Trascrizione vocale avanzata multilingua tramite Whisper Large-V3.
"""

import whisper
import sounddevice as sd
import numpy as np
import tempfile
import os
import wave


class WhisperSTT:
    def __init__(self, model_name="large-v3"):
        self.model = whisper.load_model(model_name)

    def record_audio(self, duration=5, fs=16000, device_index=None) -> str:
        print(f"🎙️ Registrazione audio... ({duration}s)")
        audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, device=device_index)
        sd.wait()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            wav_file = f.name
            with wave.open(wav_file, "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(fs)
                wf.writeframes((audio * 32767).astype(np.int16).tobytes())
        return wav_file

    def transcribe_live_audio(self, duration=5, device_index=None) -> str:
        file_path = self.record_audio(duration, device_index=device_index)
        return self.transcribe_file(file_path)

    def transcribe_file(self, file_path: str) -> str:
        result = self.model.transcribe(file_path)
        return result["text"]

    def detect_language(self, file_path: str) -> str:
        audio = whisper.load_audio(file_path)
        audio = whisper.pad_or_trim(audio)
        mel = whisper.log_mel_spectrogram(audio).to(self.model.device)
        _, probs = self.model.detect_language(mel)
        return max(probs, key=probs.get)
