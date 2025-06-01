class ElevenLabsTTS:
    def __init__(self):
        self.name = "ElevenLabs"

    def synthesize(self, text: str, voice: str = "Jarvis") -> str:
        return f"[{self.name}] Sintesi vocale: '{text}' con voce {voice}"
