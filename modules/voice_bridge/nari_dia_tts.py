import soundfile as sf
from dia.model import Dia

class NariDiaTTS:
    def __init__(self, model_name="nari-labs/Dia-1.6B"):
        self.model = Dia.from_pretrained(model_name)

    def speak(self, text: str, output_path="output.wav"):
        """
        Genera audio da testo utilizzando Nari Dia.
        """
        output = self.model.generate(text)
        sf.write(output_path, output, 44100)
        # Riproduzione audio (opzionale)
        # playsound(output_path)
