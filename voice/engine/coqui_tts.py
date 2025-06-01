class CoquiTTS:
    def __init__(self):
        self.name = "CoquiTTS"

    def speak(self, phrase: str) -> str:
        return f"[{self.name}] Audio generato per: {phrase}"
