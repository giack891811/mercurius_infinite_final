class WhisperSTT:
    def __init__(self):
        self.name = "Whisper"

    def transcribe(self, audio_path: str) -> str:
        return f"[{self.name}] Trascrizione simulata del file: {audio_path}"
