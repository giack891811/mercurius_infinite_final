# voice/nari_tts.py

"""
Modulo: nari_tts.py
Descrizione: Sintesi vocale con il modello Nari Dia TTS.
"""

import soundfile as sf
from dia.model import Dia

class NariDiaTTS:
    def __init__(self, model_name="nari-labs/Dia-1.6B"):
        self.model = Dia.from_pretrained(model_name)

    def speak(self, text: str, output_path="output.wav"):
        output = self.model.generate(text)
        sf.write(output_path, output, 44100)
