# core/dialogue_manager.py

"""
Modulo: dialogue_manager.py
Descrizione: Gestione del dialogo AI-utente per Mercurius∞.
Analizza il tono e l'emozione dell'utente, genera risposte adattive e contestuali.
"""

from core.emotion_analyzer import EmotionAnalyzer


class DialogueManager:
    def __init__(self):
        self.emotion = EmotionAnalyzer()

    def analyze_input(self, user_input: str) -> dict:
        """
        Analizza tono ed emozione dell'input utente.
        """
        tone = self.emotion.analyze_tone(user_input)
        mood = self.emotion.detect_emotion(user_input)
        return {"tone": tone, "emotion": mood}

    def generate_response(self, user_input: str) -> str:
        """
        Genera una risposta adattiva in base all'input e all'emozione rilevata.
        """
        analysis = self.analyze_input(user_input)
        tone = analysis["tone"]
        mood = analysis["emotion"]

        prefix = {
            "positivo": "😊 Mi fa piacere sentirlo!",
            "negativo": "😟 Capisco che non sia facile...",
            "neutro": "🤖 Ok, procediamo."
        }.get(tone, "")

        suffix = {
            "gioia": "Sono felice con te!",
            "tristezza": "Posso aiutarti a sentirti meglio?",
            "rabbia": "Vuoi parlarne o preferisci distrarti?",
            "sorpresa": "Davvero? Raccontami di più!",
            "paura": "Sono qui per rassicurarti.",
            "ansia": "Facciamo insieme un passo alla volta.",
            "neutro": ""
        }.get(mood, "")

        base = f"Hai detto: {user_input}"
        return f"{prefix} {base} {suffix}".strip()

    def quick_reply(self, message: str) -> str:
        """
        Risposta rapida senza elaborazione emozionale.
        """
        return f"📥 Ricevuto: {message}"
