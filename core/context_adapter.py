# core/context_adapter.py

"""
Modulo: context_adapter.py
Descrizione: Adatta lo stile di risposta dell'AI in base al contesto emozionale, visivo e acustico.
Usato per generare empatia, urgenza, o tono assertivo secondo ambiente rilevato.
"""

class ContextAdapter:
    def __init__(self):
        self.last_emotion = "neutro"
        self.last_visual_alert = None
        self.last_audio_level = 0.0

    def update_context(self, emotion=None, vision=None, audio_level=None):
        if emotion:
            self.last_emotion = emotion
        if vision:
            self.last_visual_alert = vision
        if audio_level:
            self.last_audio_level = audio_level

    def generate_adaptive_response(self, message: str) -> str:
        if self.last_visual_alert in ["persona sconosciuta", "movimento sospetto"]:
            prefix = "🛑 Attenzione visiva!"
        elif self.last_emotion == "gioia":
            prefix = "😄 Felice per te!"
        elif self.last_emotion == "tristezza":
            prefix = "💬 Vuoi parlarne?"
        else:
            prefix = "🤖"

        return f"{prefix} {message}"
