# voice/coqui_tts.py

"""
Modulo: coqui_tts.py
Descrizione: Sintesi vocale offline con Coqui TTS.
"""

from TTS.api import TTS

class CoquiTTS:
    def __init__(self, model_name="tts_models/en/ljspeech/tacotron2-DDC"):
        self.tts = TTS(model_name)

    def speak(self, text: str, output_path="coqui_output.wav"):
        self.tts.tts_to_file(text=text, file_path=output_path)
