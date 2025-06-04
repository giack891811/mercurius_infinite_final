"""
Modulo: vosk_stt.py
Responsabilità: Speech-to-Text offline tramite Vosk.
Autore: Mercurius∞ AI Engineer
"""

class VoskSTT:
    def __init__(self, model_path="model"):
        try:
            import vosk
            self.vosk = vosk
            self.model = vosk.Model(model_path)
            self.ready = True
        except Exception:
            self.vosk = None
            self.model = None
            self.ready = False

    def is_available(self):
        return self.ready

    def transcribe(self, file_path: str) -> str:
        """
        Trascrive un file audio offline con Vosk (stub demo).
        """
        if not self.ready:
            return "[❌ Vosk non disponibile]"
        try:
            import wave
            wf = wave.open(file_path, "rb")
            rec = self.vosk.KaldiRecognizer(self.model, wf.getframerate())
            results = []
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if rec.AcceptWaveform(data):
                    results.append(rec.Result())
            results.append(rec.FinalResult())
            return "\n".join(results)
        except Exception as e:
            return f"[❌ Errore Vosk]: {e}"
