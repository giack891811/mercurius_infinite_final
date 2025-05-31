# core/dialog_manager.py

"""
Modulo: Dialog Manager Unificato
Autore: Mercurius∞
Descrizione: Gestione del dialogo AI-utente con memoria, emozioni e contesto.
"""

import json
from datetime import datetime
from memory.synaptic_memory import SynapticMemory
from core.azr_reasoning import validate_with_azr
from core.emotion_analyzer import EmotionAnalyzer


class DialogManager:
    def __init__(self, memory_path="logs/dialog_history.json"):
        self.memory = SynapticMemory()
        self.emotion = EmotionAnalyzer()
        self.context_log = []
        self.memory_path = memory_path
        self.load_history()

    def load_history(self):
        try:
            with open(self.memory_path, "r") as f:
                self.context_log = json.load(f)
        except FileNotFoundError:
            self.context_log = []

    def save_history(self):
        with open(self.memory_path, "w") as f:
            json.dump(self.context_log, f, indent=2)

    def track_dialog_context(self, user_input: str, ai_response: str) -> None:
        entry = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "ai_response": ai_response
        }
        self.context_log.append(entry)
        self.save_history()
        self.memorize_interaction(entry)

    def memorize_interaction(self, dialog_entry: dict):
        self.memory.store_fact(f"[DIALOG] {dialog_entry['user_input']} → {dialog_entry['ai_response']}")

    def recall_last_state(self) -> str:
        if not self.context_log:
            return "Nessun dialogo precedente registrato."
        last = self.context_log[-1]
        return f"L'ultima interazione era:\n🧠 {last['user_input']}\n🤖 {last['ai_response']}"

    def analyze_input(self, user_input: str) -> dict:
        tone = self.emotion.analyze_tone(user_input)
        mood = self.emotion.detect_emotion(user_input)
        return {"tone": tone, "emotion": mood}

    def generate_response(self, user_input: str) -> str:
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
        response = f"{prefix} {base} {suffix}".strip()

        self.track_dialog_context(user_input, response)
        return response

    def adapt_response(self, prompt: str) -> str:
        recent_context = [x["user_input"] for x in self.context_log[-5:]]
        context = "\n".join(recent_context)
        evaluated = validate_with_azr(f"Contesto: {context}\nInput: {prompt}")
        self.track_dialog_context(prompt, evaluated)
        return evaluated

    def quick_reply(self, message: str) -> str:
        reply = f"📥 Ricevuto: {message}"
        self.track_dialog_context(message, reply)
        return reply
