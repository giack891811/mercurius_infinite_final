# voice/voice_identity.py

"""
Modulo: voice_identity.py
Descrizione: Riconoscimento vocale degli speaker e saluti personalizzati.
"""

import os
import speech_recognition as sr
import json
from datetime import datetime
import hashlib


class VoiceIdentityManager:
    def __init__(self, db_path="logs/voice_profiles.json"):
        self.db_path = db_path
        if not os.path.exists(self.db_path):
            with open(self.db_path, "w") as f:
                json.dump({}, f)
        self.db = self._load_db()

    def _load_db(self):
        with open(self.db_path, "r") as f:
            return json.load(f)

    def identify_speaker(self, audio: sr.AudioData, recognizer: sr.Recognizer) -> str:
        try:
            text = recognizer.recognize_google(audio, language="it-IT")
            voice_id = self._voice_hash(audio)
            if voice_id in self.db:
                return f"🎙️ Bentornato {self.db[voice_id]['titolo']} {self.db[voice_id]['nome']}!"
            else:
                print("Voce non riconosciuta. Chi sei?")
                return self.register_new_voice(voice_id, text)
        except Exception:
            return "❌ Voce non comprensibile."

    def register_new_voice(self, voice_id: str, input_text: str) -> str:
        name = input_text.strip().split()[-1].capitalize()
        titolo = "Signor" if name[-1] not in "aeiou" else "Signora"
        self.db[voice_id] = {"nome": name, "titolo": titolo, "registrato": datetime.now().isoformat()}
        with open(self.db_path, "w") as f:
            json.dump(self.db, f, indent=2)
        return f"🎙️ Piacere {titolo} {name}, registrazione completata."

    def _voice_hash(self, audio: sr.AudioData) -> str:
        return hashlib.sha256(audio.get_raw_data()).hexdigest()[:16]
