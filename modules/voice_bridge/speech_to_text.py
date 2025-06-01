"""
Modulo: speech_to_text
Descrizione: Interfaccia vocale STT usando Whisper per Mercurius∞.
Autore: Mercurius∞ AI Engineer
"""

import whisper

class WhisperSTT:
    def __init__(self, model_name="base"):
        self.model = whisper.load_model(model_name)

    def transcribe(self, audio_path: str) -> str:
        """Esegue la trascrizione da un file audio."""
        try:
            result = self.model.transcribe(audio_path, language='it')
            return result['text']
        except Exception as e:
            return f"[STT Error] {e}"

# Test
if __name__ == "__main__":
    stt = WhisperSTT()
    testo = stt.transcribe("sample_audio.wav")
    print("Trascrizione:", testo)
